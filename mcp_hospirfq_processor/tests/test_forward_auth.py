"""``auth: "forward"``: rfq_engine calls use the caller's per-call bearer token."""

import logging
from unittest.mock import MagicMock, patch

from mcp_hospirfq_processor.graphql_backed_processor import GraphQLBackedProcessor
from mcp_hospirfq_processor.graphql_client import GraphQLClient, GraphQLModule

FORWARD = {"graphql_modules": {"rfq_engine": {
    "endpoint": "http://gw/{endpoint_id}/rfq_graphql", "auth": "forward",
    # stored credentials must be ignored in forward mode
    "token_username": "u", "token_password": "p", "gateway_base_url": "http://gw",
}}}


def _client(setting, caller=None):
    client = GraphQLClient(logging.getLogger("t"), **setting)
    client.endpoint_id = "banyan"
    client.part_id = "tenant-1"
    client.caller_authorization = caller
    return client


def _post_capture(status=200):
    http = MagicMock()
    http.__enter__.return_value = http
    http.post.return_value.status_code = status
    http.post.return_value.json.return_value = {"data": {"op": {"ok": True}}}
    return http


def test_auth_mode_forward():
    assert GraphQLModule("banyan", auth="forward").auth_mode == "forward"
    assert GraphQLModule("banyan", auth="FORWARD ").auth_mode == "forward"
    assert GraphQLModule("banyan", gateway_token="t").auth_mode == "jwt"


def test_forward_sends_caller_token_and_tenant_part_id():
    http = _post_capture()
    client = _client(FORWARD, caller="caller-token")
    with patch("mcp_hospirfq_processor.graphql_client.httpx.Client", return_value=http), \
            patch("mcp_hospirfq_processor.graphql_client.httpx.post") as login:
        assert client.execute_query("f", "op", "Query", {}, query="query{op}") == {"ok": True}
    headers = http.post.call_args.kwargs["headers"]
    assert headers["Authorization"] == "Bearer caller-token"
    assert headers["Part-Id"] == "tenant-1"
    login.assert_not_called()  # never logs in with stored credentials


def test_forward_without_caller_token_fails_closed():
    http = _post_capture()
    client = _client(FORWARD, caller=None)
    with patch("mcp_hospirfq_processor.graphql_client.httpx.Client", return_value=http), \
            patch("mcp_hospirfq_processor.graphql_client.httpx.post") as login:
        result = client.execute_query("f", "op", "Query", {}, query="query{op}")
    # execute_query reports failures as a structured error response
    assert "forward auth requires" in str(result)
    http.post.assert_not_called()
    login.assert_not_called()


def test_forward_does_not_retry_401_with_stored_credentials():
    http = _post_capture(status=401)
    http.post.return_value.json.return_value = {"errors": [{"message": "denied"}]}
    client = _client(FORWARD, caller="caller-token")
    with patch("mcp_hospirfq_processor.graphql_client.httpx.Client", return_value=http), \
            patch("mcp_hospirfq_processor.graphql_client.httpx.post") as login:
        result = client.execute_query("f", "op", "Query", {}, query="query{op}")
    assert "denied" in str(result)
    assert http.post.call_count == 1
    login.assert_not_called()


def test_processor_exposes_caller_authorization_for_the_host():
    processor = GraphQLBackedProcessor(logging.getLogger("t"), **FORWARD)
    assert hasattr(processor, "caller_authorization")
    processor.caller_authorization = "tok"
    assert processor.graphql_client.caller_authorization == "tok"
