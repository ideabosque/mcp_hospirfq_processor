#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
__author__ = "Idea Bosque"
from typing import Any, Dict
import humps
from silvaengine_utility import convert_decimal_to_number
from .error_handler import (ErrorCode, ValidationError, build_error_response, handle_errors, propagate_error_if_present, validate_not_empty)
from .graphql_backed_processor import GraphQLBackedProcessor


class CatalogMixin(GraphQLBackedProcessor):

    @handle_errors(operation_name="inquire_catalog")
    def inquire_catalog(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        partition_key = arguments.get("partition_key")
        validate_not_empty(partition_key, "partition_key")
        query_text = arguments.get("query_text")
        validate_not_empty(query_text, "query_text")

        variables = {
            "partitionKey": partition_key,
            "query": {
                "queryText": query_text,
                "searchMode": arguments.get("search_mode", "vector"),
                "topK": arguments.get("top_k", arguments.get("limit", 10)),
                "page": arguments.get("page", 1),
                "limit": arguments.get("limit", 10),
            },
            "namespace": arguments.get("namespace"),
        }
        query = variables["query"]
        if arguments.get("index_name"):
            query["indexName"] = arguments["index_name"]
        if arguments.get("retrieval_query"):
            query["retrievalQuery"] = arguments["retrieval_query"]
        if arguments.get("filters"):
            query["filters"] = arguments["filters"]
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        operation_name = "inquireCatalog"
        result = self._execute_graphql_query("rfq_graphql", operation_name, "Query", variables)
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(convert_decimal_to_number(result))
