#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
__author__ = "Idea Bosque"
from typing import Any, Dict
import humps
from silvaengine_utility import convert_decimal_to_number
from .error_handler import (ErrorCode, ValidationError, build_error_response, handle_errors, propagate_error_if_present, validate_not_empty)
from .graphql_backed_processor import GraphQLBackedProcessor


class FileMixin(GraphQLBackedProcessor):

    @handle_errors(operation_name="upload_rfq_file")
    def upload_rfq_file(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        request_uuid = arguments.get("request_uuid")
        validate_not_empty(request_uuid, "request_uuid")
        file_name = arguments.get("file_name")
        validate_not_empty(file_name, "file_name")

        variables = {
            "requestUuid": request_uuid,
            "fileName": file_name,
            "email": arguments.get("email"),
            "updatedBy": "MCP",
        }
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        operation_name = "insertUpdateFile"
        result = self._execute_graphql_query("rfq_graphql", operation_name, "Mutation", variables)
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(convert_decimal_to_number(result))

    @handle_errors(operation_name="get_rfq_files")
    def get_rfq_files(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        variables = {
            "pageNumber": arguments.get("page_number"),
            "limit": arguments.get("limit"),
            "requestUuid": arguments.get("request_uuid"),
            "fileType": arguments.get("file_type"),
        }
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        operation_name = "fileList"
        result = self._execute_graphql_query("rfq_graphql", operation_name, "Query", variables)
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(convert_decimal_to_number(result))
