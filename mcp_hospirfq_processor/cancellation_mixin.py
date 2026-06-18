#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
__author__ = "Idea Bosque"
from typing import Any, Dict
import humps
from silvaengine_utility import convert_decimal_to_number
from .error_handler import (ErrorCode, ValidationError, build_error_response, handle_errors, propagate_error_if_present, validate_not_empty)
from .graphql_backed_processor import GraphQLBackedProcessor


class CancellationMixin(GraphQLBackedProcessor):

    @handle_errors(operation_name="get_cancellation_policy")
    def get_cancellation_policy(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        partition_key = arguments.get("partition_key")
        validate_not_empty(partition_key, "partition_key")
        policy_uuid = arguments.get("policy_uuid")
        validate_not_empty(policy_uuid, "policy_uuid")

        variables = {
            "partitionKey": partition_key,
            "policyUuid": policy_uuid,
        }
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        operation_name = "cancellationPolicy"
        result = self._execute_graphql_query("ai_rfq_graphql", operation_name, "Query", variables)
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(convert_decimal_to_number(result))

    @handle_errors(operation_name="search_cancellation_policies")
    def search_cancellation_policies(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        partition_key = arguments.get("partition_key")
        validate_not_empty(partition_key, "partition_key")

        variables = {
            "partitionKey": partition_key,
            "providerItemUuid": arguments.get("provider_item_uuid"),
            "status": arguments.get("status"),
        }
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        operation_name = "cancellationPolicyList"
        result = self._execute_graphql_query("ai_rfq_graphql", operation_name, "Query", variables)
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(convert_decimal_to_number(result))