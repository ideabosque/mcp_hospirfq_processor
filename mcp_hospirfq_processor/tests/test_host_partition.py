"""Hosted calls derive the data partition from the request, not the arguments.

The MCP host sets ``endpoint_id`` / ``part_id`` per call from the gateway
route and the Part-Id header; tools must use ``<endpoint_id>#<part_id>`` and
ignore any other ``partition_key`` a caller supplies.
"""

import logging
from unittest.mock import patch

from mcp_hospirfq_processor.graphql_backed_processor import GraphQLBackedProcessor
from mcp_hospirfq_processor.mcp_configuration import MCP_CONFIGURATION
from mcp_hospirfq_processor.mcp_hospirfq_processor import MCPHospiRFQProcessor

HOST = "banyan#7d9a2146-f34b-40d8-a695-7c6c22076d04"


def _processor(endpoint_id="banyan", part_id="7d9a2146-f34b-40d8-a695-7c6c22076d04"):
    p = MCPHospiRFQProcessor(logging.getLogger("t"))
    p.endpoint_id = endpoint_id
    p.part_id = part_id
    return p


def test_host_partition_wins_over_supplied_value():
    p = _processor()
    assert p.host_partition_key == HOST
    assert p._partition_key({"partition_key": "banyan#nestaging"}) == HOST
    assert p._partition_key({}) == HOST


def test_argument_is_only_a_fallback_without_host():
    p = GraphQLBackedProcessor(logging.getLogger("t"))
    assert p.host_partition_key is None
    assert p._partition_key({"partition_key": "banyan#x"}) == "banyan#x"


def test_graphql_variables_are_forced_to_host_partition():
    p = _processor()
    with patch.object(p.graphql_client, "execute_query", return_value={}) as run:
        p._execute_graphql_query("f", "op", "Query", {"partitionKey": "banyan#nestaging", "a": 1})
    assert run.call_args.args[3] == {"partitionKey": HOST, "a": 1}


def test_variables_without_partition_untouched():
    p = _processor()
    with patch.object(p.graphql_client, "execute_query", return_value={}) as run:
        p._execute_graphql_query("f", "op", "Query", {"a": 1})
    assert run.call_args.args[3] == {"a": 1}


def test_inquire_catalog_uses_host_partition_and_needs_no_argument():
    p = _processor()
    with patch.object(p.graphql_client, "execute_query", return_value={"ok": 1}) as run:
        p.inquire_catalog(namespace="FLIGHTS", query_text="NRT to SFO",
                          partition_key="banyan#nestaging")
        p.inquire_catalog(namespace="FLIGHTS", query_text="NRT to SFO")
    for call in run.call_args_list:
        assert call.args[3]["partitionKey"] == HOST


def test_schemas_no_longer_require_partition_key():
    for tool in MCP_CONFIGURATION["tools"]:
        assert "partition_key" not in tool["inputSchema"].get("required", []), tool["name"]
