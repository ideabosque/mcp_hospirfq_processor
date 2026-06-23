#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pytest configuration and fixtures for MCP HospiRFQ Processor tests."""
from __future__ import annotations

__author__ = "Idea Bosque"

import logging
import os
import sys
from unittest.mock import MagicMock

import pytest

# Setup logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("test_mcp_hospirfq_processor")

# Make package importable — project root (parent of the mcp_hospirfq_processor package dir)
base_dir = os.getenv("base_dir", os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, base_dir)

from mcp_hospirfq_processor.mcp_hospirfq_processor import MCPHospiRFQProcessor


# Minimal setting dict — graphql_modules are required by GraphQLClient
# but for unit tests we mock _execute_graphql_query so they're not called.
SETTING = {
    "graphql_modules": {
        "rfq_engine": {
            "class_name": "RFQEngine",
            "endpoint": "https://mock.example.com/graphql/{endpoint_id}",
            "x_api_key": "mock-api-key",
        }
    },
    "sales_rep_emails": {
        "PROVIDER-001": "sales1@provider.com",
        "PROVIDER-002": "sales2@provider.com",
    },
}


@pytest.fixture
def processor():
    """Provide an MCPHospiRFQProcessor instance with mocked GraphQL execution.

    The _execute_graphql_query method is replaced with a MagicMock so
    each test can configure its return value independently.
    """
    proc = MCPHospiRFQProcessor(logger, **SETTING)
    proc.endpoint_id = "test-endpoint-id"
    proc.part_id = "test-part-id"
    proc._execute_graphql_query = MagicMock()
    return proc


@pytest.fixture
def gql_result_factory():
    """Factory fixture to build clean GraphQL result dicts.

    Usage::

        result = gql_result_factory({"requestUuid": "123", "status": "initial"})
        processor._execute_graphql_query.return_value = result
    """

    def _make(data: dict):
        return data

    return _make