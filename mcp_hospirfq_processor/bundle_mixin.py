#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
__author__ = "Idea Bosque"
from typing import Any, Dict
import humps
from silvaengine_utility import convert_decimal_to_number
from .error_handler import (ErrorCode, ValidationError, build_error_response, handle_errors, propagate_error_if_present, validate_not_empty)
from .graphql_backed_processor import GraphQLBackedProcessor


class BundleMixin(GraphQLBackedProcessor):

    @handle_errors(operation_name="search_bundles")
    def search_bundles(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        partition_key = arguments.get("partition_key")
        validate_not_empty(partition_key, "partition_key")

        variables = {
            "partitionKey": partition_key,
            "bundleCode": arguments.get("bundle_code"),
            "bundleType": arguments.get("bundle_type"),
            "status": arguments.get("status"),
        }
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        operation_name = "bundleList"
        result = self._execute_graphql_query("rfq_graphql", operation_name, "Query", variables)
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(convert_decimal_to_number(result))

    @handle_errors(operation_name="get_bundle")
    def get_bundle(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        partition_key = arguments.get("partition_key")
        validate_not_empty(partition_key, "partition_key")
        bundle_uuid = arguments.get("bundle_uuid")
        validate_not_empty(bundle_uuid, "bundle_uuid")

        variables = {
            "partitionKey": partition_key,
            "bundleUuid": bundle_uuid,
        }
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        operation_name = "bundle"
        result = self._execute_graphql_query("rfq_graphql", operation_name, "Query", variables)
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(convert_decimal_to_number(result))

    @handle_errors(operation_name="search_bundle_components")
    def search_bundle_components(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        partition_key = arguments.get("partition_key")
        validate_not_empty(partition_key, "partition_key")
        bundle_uuid = arguments.get("bundle_uuid")
        validate_not_empty(bundle_uuid, "bundle_uuid")

        variables = {
            "partitionKey": partition_key,
            "bundleUuid": bundle_uuid,
        }
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        operation_name = "bundleComponentList"
        result = self._execute_graphql_query("rfq_graphql", operation_name, "Query", variables)
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(convert_decimal_to_number(result))
