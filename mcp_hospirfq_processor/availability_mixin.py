#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Idea Bosque"

from typing import Any, Dict

import humps
from silvaengine_utility import convert_decimal_to_number

from .error_handler import (
    ErrorCode,
    ValidationError,
    build_error_response,
    handle_errors,
    propagate_error_if_present,
    validate_not_empty,
)
from .graphql_backed_processor import GraphQLBackedProcessor


class AvailabilityMixin(GraphQLBackedProcessor):
    """MCP tools for availability checking and hold lifecycle management.

    These are NEW hospitality-specific tools that manage capacity
    reservations for service-dated inventory (hotel rooms, restaurant
    covers, event seats, transfers, activities, delegate fees, flights).
    """

    # ==================== Availability Hold Tools ====================

    # * MCP Function.
    @handle_errors(operation_name="check availability")
    def check_availability(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if a provider item has available capacity for a service window.
        Maps to GraphQL: checkAvailability query

        Returns availability status with matched batches and available quantity.

        Required:
            partition_key: Tenant partition key
            provider_item_uuid: The provider item to check
            service_start_at: Service window start (ISO 8601)
            service_end_at: Service window end (ISO 8601)

        Optional:
            batch_no: Optional specific batch number
            qty: Number of units requested
        """
        self.logger.info(f"Checking availability: {arguments}")

        variables = {
            "partitionKey": arguments["partition_key"],
            "providerItemUuid": arguments["provider_item_uuid"],
            "serviceStartAt": arguments["service_start_at"],
            "serviceEndAt": arguments["service_end_at"],
            "batchNo": arguments.get("batch_no"),
            "qty": arguments.get("qty"),
        }

        # Remove None values
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        result = self._execute_graphql_query(
            "ai_rfq_graphql",
            "checkAvailability",
            "Query",
            variables,
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(result)

    # * MCP Function.
    @handle_errors(operation_name="acquire availability hold")
    def acquire_availability_hold(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atomically reserve capacity and create a hold with 15-min TTL.
        Maps to GraphQL: acquireAvailabilityHold mutation

        Returns {hold_token, expires_at, status: "held"}.

        Required:
            partition_key: Tenant partition key
            provider_item_uuid: The provider item to hold
            service_start_at: Service window start (ISO 8601)
            service_end_at: Service window end (ISO 8601)
            qty: Number of units to hold

        Optional:
            batch_no: Optional specific batch number
            pax_breakdown: Optional PAX type counts, e.g. {"adult": 2, "child": 1}
            quote_uuid: Associated quote
            quote_item_uuid: Associated quote item
        """
        self.logger.info(f"Acquiring availability hold: {arguments}")

        variables = {
            "partitionKey": arguments["partition_key"],
            "providerItemUuid": arguments["provider_item_uuid"],
            "serviceStartAt": arguments["service_start_at"],
            "serviceEndAt": arguments["service_end_at"],
            "qty": arguments["qty"],
            "batchNo": arguments.get("batch_no"),
            "paxBreakdown": arguments.get("pax_breakdown"),
            "quoteUuid": arguments.get("quote_uuid"),
            "quoteItemUuid": arguments.get("quote_item_uuid"),
            "updatedBy": "MCP",
        }

        # Remove None values
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        result = self._execute_graphql_query(
            "ai_rfq_graphql",
            "acquireAvailabilityHold",
            "Mutation",
            variables,
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(result)

    # * MCP Function.
    @handle_errors(operation_name="release availability hold")
    def release_availability_hold(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Release a held reservation and restore capacity.
        Maps to GraphQL: releaseAvailabilityHold mutation

        Idempotent — repeat calls return the same result.

        Required:
            partition_key: Tenant partition key
            hold_token: The hold token to release
            provider_item_uuid: The provider item the hold was for
        Optional:
            batch_no: Optional batch number to scope the release
        """
        self.logger.info(f"Releasing availability hold: {arguments}")

        variables = {
            "partitionKey": arguments["partition_key"],
            "holdToken": arguments["hold_token"],
            "providerItemUuid": arguments.get("provider_item_uuid"),
            "batchNo": arguments.get("batch_no"),
            "updatedBy": "MCP",
        }

        # Remove None values
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        result = self._execute_graphql_query(
            "ai_rfq_graphql",
            "releaseAvailabilityHold",
            "Mutation",
            variables,
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(result)

    # * MCP Function.
    @handle_errors(operation_name="confirm availability hold")
    def confirm_availability_hold(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Confirm a held reservation (transition to confirmed, no second capacity decrement).
        Maps to GraphQL: confirmAvailabilityHold mutation

        No second capacity decrement — the hold's capacity is already reserved.

        Required:
            partition_key: Tenant partition key
            hold_token: The hold token to confirm
            provider_item_uuid: The provider item the hold was for
        Optional:
            batch_no: Optional batch number to scope the confirmation
        """
        self.logger.info(f"Confirming availability hold: {arguments}")

        variables = {
            "partitionKey": arguments["partition_key"],
            "holdToken": arguments["hold_token"],
            "providerItemUuid": arguments.get("provider_item_uuid"),
            "batchNo": arguments.get("batch_no"),
            "updatedBy": "MCP",
        }

        # Remove None values
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        result = self._execute_graphql_query(
            "ai_rfq_graphql",
            "confirmAvailabilityHold",
            "Mutation",
            variables,
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(result)

    # * MCP Function.
    @handle_errors(operation_name="expire availability hold")
    def expire_availability_hold(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expire a stale hold and restore capacity (idempotent).
        Maps to GraphQL: expireAvailabilityHold mutation

        Restores capacity. Idempotent — repeat calls return the same result.

        Required:
            partition_key: Tenant partition key
            hold_token: The hold token to expire
            provider_item_uuid: The provider item the hold was for
        Optional:
            batch_no: Optional batch number to scope the expiry
        """
        self.logger.info(f"Expiring availability hold: {arguments}")

        variables = {
            "partitionKey": arguments["partition_key"],
            "holdToken": arguments["hold_token"],
            "providerItemUuid": arguments.get("provider_item_uuid"),
            "batchNo": arguments.get("batch_no"),
            "updatedBy": "MCP",
        }

        # Remove None values
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        result = self._execute_graphql_query(
            "ai_rfq_graphql",
            "expireAvailabilityHold",
            "Mutation",
            variables,
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(result)