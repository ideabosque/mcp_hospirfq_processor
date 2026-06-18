#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
__author__ = "Idea Bosque"
from typing import Any, Dict
import humps
from silvaengine_utility import convert_decimal_to_number
from .error_handler import (ErrorCode, ValidationError, build_error_response, handle_errors, propagate_error_if_present, validate_not_empty)
from .graphql_backed_processor import GraphQLBackedProcessor


class SegmentMixin(GraphQLBackedProcessor):

    @handle_errors(operation_name="get_segment_contacts")
    def get_segment_contacts(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        email = arguments.get("email")
        validate_not_empty(email, "email")

        variables = {
            "email": email,
            "pageNumber": arguments.get("page_number"),
            "limit": arguments.get("limit"),
            "consumerCorpExternalId": arguments.get("consumer_corp_external_id"),
        }
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        operation_name = "segmentContactList"
        result = self._execute_graphql_query("ai_rfq_graphql", operation_name, "Query", variables)
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(convert_decimal_to_number(result))
