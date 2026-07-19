#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GraphQL Client for MCP HospiRFQ Processor

Handles GraphQL query execution via HTTP/2 against the rfq_engine backend.
"""

__author__ = "Idea Bosque"

import base64
import json
import logging
import time
import traceback
from typing import Any, Dict

import httpx

from silvaengine_utility.graphql import Graphql
from silvaengine_utility.serializer import Serializer

from .error_handler import (
    ErrorCode,
    GraphQLError,
    build_error_response,
    extract_error_message,
)

# Seconds of safety margin before a JWT's ``exp`` at which the client proactively
# re-authenticates, so a token never expires mid-request.
_TOKEN_EXPIRY_SKEW_SECONDS = 60


def _jwt_expiry(token: str | None) -> float | None:
    """Best-effort parse of a JWT's ``exp`` claim (epoch seconds).

    Reads the payload segment only (no signature verification — the client is
    the token bearer, not the validator). Returns ``None`` when the token is
    absent, not a JWT, or has no ``exp`` claim, in which case the caller falls
    back to reactive 401 re-authentication.
    """
    if not token:
        return None
    try:
        payload_b64 = token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)  # restore base64 padding
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        exp = payload.get("exp")
        return float(exp) if exp is not None else None
    except Exception:
        return None


class GraphQLModule:
    """Encapsulates GraphQL module configuration and schema management."""

    def __init__(
        self,
        endpoint_id: str,
        module_name: str | None = None,
        class_name: str | None = None,
        endpoint: str | None = None,
        x_api_key: str | None = None,
    ):
        self.endpoint_id = endpoint_id
        self._module_name = module_name
        self._class_name = class_name
        # The endpoint template references only ``{endpoint_id}``. part_id is
        # never part of the URL path — it is carried in the ``Part-Id`` request
        # header (see GraphQLClient.execute_query).
        self._endpoint = endpoint.format(endpoint_id=endpoint_id) if endpoint else None
        self._x_api_key = x_api_key
        self._schema = None

    @property
    def module_name(self) -> str | None:
        return self._module_name

    @property
    def class_name(self) -> str | None:
        return self._class_name

    @property
    def endpoint(self) -> str | None:
        return self._endpoint

    @property
    def x_api_key(self) -> str | None:
        return self._x_api_key

    @property
    def schema(self):
        """Get the cached GraphQL schema, loading it if necessary."""
        if self._schema is None and self._module_name and self._class_name:
            self.refresh_schema()
        return self._schema

    def refresh_schema(self):
        """Load or reload the GraphQL schema from the configured module and class."""
        if self._module_name and self._class_name:
            self._schema = Graphql.get_graphql_schema(
                module_name=self._module_name,
                class_name=self._class_name,
            )


class GraphQLClient:
    """Client for executing GraphQL operations via HTTP/2."""

    def __init__(self, logger: logging.Logger, **setting: Dict[str, Any]):
        self.logger = logger
        self.setting = setting
        self._endpoint_id = None
        self._part_id = None
        self._graphql_modules = {}
        # Gateway (silvaengine_gateway) JWT Bearer auth configuration. When a
        # ``gateway_base_url`` is configured the client logs in to the gateway
        # to obtain a JWT and sends ``Authorization: Bearer <token>`` instead of
        # the AWS API Gateway ``x-api-key`` header.
        self._gateway_base_url = setting.get("gateway_base_url")
        self._token_username = setting.get("token_username")
        self._token_password = setting.get("token_password")
        # Optional pre-issued token (skips the /auth/token login round-trip).
        self._gateway_token = setting.get("gateway_token")
        # Cached JWT expiry (epoch seconds) for proactive refresh; parsed from
        # the token itself. ``None`` means unknown -> rely on reactive 401 retry.
        self._gateway_token_exp = _jwt_expiry(self._gateway_token)

    @property
    def endpoint_id(self) -> str | None:
        return self._endpoint_id

    @endpoint_id.setter
    def endpoint_id(self, value: str):
        self._endpoint_id = value

    @property
    def part_id(self) -> str | None:
        return self._part_id

    @part_id.setter
    def part_id(self, value: str):
        self._part_id = value

    @property
    def graphql_modules(self) -> Dict[str, GraphQLModule]:
        return self._graphql_modules

    def get_graphql_module(self, module_name: str) -> GraphQLModule | None:
        """Get a GraphQL module by name, lazy-creating it on first access."""
        if not self._graphql_modules.get(module_name):
            self._graphql_modules[module_name] = GraphQLModule(
                endpoint_id=self.endpoint_id,
                module_name=module_name,
                class_name=self.setting.get("graphql_modules", {})
                .get(module_name, {})
                .get("class_name"),
                endpoint=self.setting.get("graphql_modules", {})
                .get(module_name, {})
                .get("endpoint"),
                x_api_key=self.setting.get("graphql_modules", {})
                .get(module_name, {})
                .get("x_api_key"),
            )
        return self._graphql_modules.get(module_name)

    def _token_expired(self) -> bool:
        """True when the cached JWT is at/near its ``exp`` (within the skew).

        Unknown expiry (unparseable token) returns ``False`` so the token is
        still used and the reactive 401 retry remains the safety net.
        """
        if self._gateway_token_exp is None:
            return False
        return time.time() >= (self._gateway_token_exp - _TOKEN_EXPIRY_SKEW_SECONDS)

    def get_gateway_token(self) -> str | None:
        """Obtain a JWT Bearer token for the silvaengine_gateway.

        Returns ``None`` when no gateway auth is configured (in which case the
        client falls back to AWS API Gateway ``x-api-key`` auth). A successfully
        issued token is cached on the instance and reused until it nears its
        ``exp`` claim, at which point it is proactively re-issued so a token
        never expires mid-request (long-lived processes such as the MCP daemon).
        """
        if not self._gateway_base_url:
            return None
        # Reuse the cached token while it is still valid.
        if self._gateway_token and not self._token_expired():
            return self._gateway_token
        if not (self._token_username and self._token_password):
            # No credentials to (re)authenticate with — return whatever we have
            # (possibly a pre-issued token) rather than nothing.
            return self._gateway_token

        resp = httpx.post(
            f"{self._gateway_base_url.rstrip('/')}/auth/token",
            data={
                "username": self._token_username,
                "password": self._token_password,
            },
            timeout=15,
        )
        resp.raise_for_status()
        self._gateway_token = resp.json()["access_token"]
        self._gateway_token_exp = _jwt_expiry(self._gateway_token)
        return self._gateway_token

    def execute_query(
        self,
        function_name: str,
        operation_name: str,
        operation_type: str,
        variables: Dict[str, Any],
        query: str = None,
        module_name: str = "rfq_engine",
    ) -> Dict[str, Any]:
        """Execute a GraphQL query or mutation."""
        try:
            graphql_module = self.get_graphql_module(module_name)
            if query is None:
                query = Graphql.generate_graphql_operation(
                    operation_name, operation_type, graphql_module.schema
                )

            payload = Serializer.json_dumps({"query": query, "variables": variables})

            # Prefer gateway JWT Bearer auth when configured; otherwise fall
            # back to AWS API Gateway x-api-key auth.
            def _build_headers(token: str | None) -> Dict[str, str]:
                if token:
                    hdrs = {
                        "Authorization": f"Bearer {token}",
                        "Part-Id": self.part_id,
                        "Content-Type": "application/json",
                    }
                else:
                    hdrs = {
                        "x-api-key": graphql_module.x_api_key,
                        "Part-Id": self.part_id,
                        "Content-Type": "application/json",
                    }
                # httpx rejects None-valued headers with a TypeError. Drop any
                # that came out None so the request goes through cleanly. The
                # common case is Part-Id when the tool is invoked via
                # /{endpoint_id}/mcp instead of /{endpoint_id}/{part_id}/mcp;
                # x-api-key can also be None when neither Bearer nor API-key
                # auth is configured for the module.
                return {k: v for k, v in hdrs.items() if v is not None}

            token = self.get_gateway_token()

            timeout = httpx.Timeout(60.0, connect=15.0)
            with httpx.Client(http2=True, timeout=timeout) as client:
                response = client.post(
                    graphql_module.endpoint,
                    headers=_build_headers(token),
                    content=payload,
                )

                # The gateway JWT is cached on the instance and can expire in a
                # long-lived process (e.g. the MCP daemon), causing a 401 even
                # though the credentials are still valid. Re-authenticate once
                # with a fresh token and retry before surfacing the failure.
                if response.status_code in (401, 403) and (
                    self._token_username and self._token_password
                ):
                    self._gateway_token = None
                    token = self.get_gateway_token()
                    response = client.post(
                        graphql_module.endpoint,
                        headers=_build_headers(token),
                        content=payload,
                    )

            result = response.json()

            if "errors" in result:
                error_message = result["errors"][0].get("message", "GraphQL error")
                raise Exception(f"GraphQL error: {error_message}")

            return result.get("data", {}).get(operation_name)

        except GraphQLError as e:
            log = traceback.format_exc()
            self.logger.error(log)
            return build_error_response(e.message, e.error_code, e.details)
        except Exception as e:
            log = traceback.format_exc()
            self.logger.error(log)
            return build_error_response(
                extract_error_message(str(e)),
                ErrorCode.GRAPHQL_QUERY_FAILED,
                {"function_name": function_name, "operation": operation_name},
            )
