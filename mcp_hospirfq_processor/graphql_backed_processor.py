#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Base processor providing GraphQL execution for all mixins."""

from __future__ import annotations

__author__ = "Idea Bosque"

import logging
from typing import Any, Dict

from .graphql_client import GraphQLClient


class GraphQLBackedProcessor:
    """Root base class for all MCP HospiRFQ mixins.

    Provides ``self.logger``, ``self.setting``, ``self.graphql_client``,
    and the ``_execute_graphql_query`` method that every mixin uses to
    communicate with the rfq_engine backend.
    """

    def __init__(self, logger: logging.Logger, **setting: Dict[str, Any]):
        self.logger = logger
        self.setting = setting
        self.graphql_client = GraphQLClient(logger, **setting)

    @property
    def endpoint_id(self) -> str | None:
        return self.graphql_client.endpoint_id

    @endpoint_id.setter
    def endpoint_id(self, value: str):
        self.graphql_client.endpoint_id = value

    @property
    def part_id(self) -> str | None:
        return self.graphql_client.part_id

    @part_id.setter
    def part_id(self, value: str):
        self.graphql_client.part_id = value

    @property
    def caller_authorization(self) -> str | None:
        """Caller's bearer token for ``auth: "forward"`` modules (set per call
        by the MCP host; never persisted)."""
        return self.graphql_client.caller_authorization

    @caller_authorization.setter
    def caller_authorization(self, value: str | None):
        self.graphql_client.caller_authorization = value

    @property
    def host_partition_key(self) -> str | None:
        """``<endpoint_id>#<part_id>`` set per call by the MCP host, if known."""
        if self.endpoint_id and self.part_id:
            return f"{self.endpoint_id}#{self.part_id}"
        return None

    def _partition_key(self, arguments: Dict[str, Any]) -> Any:
        """Data partition for a tool call.

        Hosted calls always use the request's partition (``endpoint_id`` /
        ``part_id`` set by the MCP host from the gateway route and Part-Id);
        a ``partition_key`` argument naming another partition is ignored so a
        caller can never reach another tenant's data. The argument is only a
        fallback when the processor runs without a host partition.
        """
        host = self.host_partition_key
        supplied = arguments.get("partition_key")
        if host:
            if supplied and supplied != host:
                self.logger.warning(
                    "partition_key %r ignored; using host partition %r",
                    supplied,
                    host,
                )
            return host
        return supplied

    def _execute_graphql_query(
        self,
        function_name: str,
        operation_name: str,
        operation_type: str,
        variables: Dict[str, Any],
        query: str = None,
    ) -> Dict[str, Any]:
        # Defense in depth: a hosted call never sends another partition.
        host = self.host_partition_key
        if host and "partitionKey" in variables:
            variables = {**variables, "partitionKey": host}
        return self.graphql_client.execute_query(
            function_name, operation_name, operation_type, variables, query=query
        )