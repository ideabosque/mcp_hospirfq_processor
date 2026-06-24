#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
End-to-end integration tests for MCP HospiRFQ Processor via MCPHttpClient.

This script exercises the same 38 processor tools as ``run_integration.py``
but instead of calling ``MCPHospiRFQProcessor`` methods directly in-process,
it drives every call through the **gateway REST/JSON-RPC MCP endpoint**
using ``mcp_http_client.MCPHttpClient``.

Flow:
    test script → MCPHttpClient → HTTP JSON-RPC → gateway /{endpoint_id}/mcp
        → dispatch_mcp → MCPHospiRFQProcessor.<tool>()

The gateway handles all backend dispatch internally. The test script only
talks to the gateway's MCP REST endpoint — no GraphQL access is needed.

This validates the full agent-to-gateway MCP transport layer (JSON-RPC
``initialize``, ``tools/list``, ``tools/call``).

Prerequisites:
  1. silvaengine_gateway is running:
       python -m silvaengine_gateway.tests.run_daemon
  2. Test data has been seeded (prepare_test_data scripts in the backend).
  3. mcp_hospirfq_processor is loaded into the gateway's MCP daemon engine
     (loadMcpConfiguration / processMcpPackage).
  4. tests/.env is configured with correct endpoint_id, part_id, and credentials.

Usage:
  # Run all tool groups end-to-end via MCPHttpClient:
  python -m mcp_hospirfq_processor.tests.run_http_integration

  # Run only specific tool groups:
  python -m mcp_hospirfq_processor.tests.run_http_integration --only items,requests

  # Run a single tool:
  python -m mcp_hospirfq_processor.tests.run_http_integration --only search_items

  # List available groups:
  python -m mcp_hospirfq_processor.tests.run_http_integration --list

  # Export a Markdown report:
  python -m mcp_hospirfq_processor.tests.run_http_integration --export docs/http_integration_results.md

Tool groups (mirror run_integration.py):
  items        — search_items, get_item, get_provider_items
  requests     — submit, get, search, update, add/remove item, assign/remove provider item
  quotes       — confirm_request_and_create_quotes, get_quote, search_quotes, update_quote, update_quote_item
  pricing      — get_item_price_tiers, get_discount_prompts, calculate_quote_pricing
  installments — confirm_quote_and_create_installments, create_installment, update_installment, create_installments, get_installments
  files        — upload_rfq_file, get_rfq_files
  segments     — get_segment_contacts
  availability — check, acquire, confirm, release, expire
  bundles      — search_bundles, get_bundle, search_bundle_components
  cancellation — get_cancellation_policy, search_cancellation_policies
  catalog      — inquire_catalog
"""

from __future__ import annotations, print_function

__author__ = "Idea Bosque"

import argparse
import asyncio
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv

# ── Load .env from tests/ directory ──────────────────────────────────────────
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    load_dotenv(_env_path, override=True)
    print(f"Loaded .env from: {_env_path}")
else:
    print(f"WARNING: .env not found at {_env_path} - using defaults / env vars")

# ── sys.path setup ───────────────────────────────────────────────────────────
base_dir = os.getenv("base_dir", "")
if not base_dir:
    base_dir = str(Path(__file__).resolve().parent.parent.parent.parent)
print(f"base_dir: {base_dir}")
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, "silvaengine_utility"))
sys.path.insert(0, os.path.join(base_dir, "silvaengine_constants"))
sys.path.insert(0, os.path.join(base_dir, "silvaengine_dynamodb_base"))
sys.path.insert(0, os.path.join(base_dir, "mcp_hospirfq_processor"))
sys.path.insert(0, os.path.join(base_dir, "mcp_http_client"))

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("integration_hospirfq_http")

# ── Imports (after sys.path) ─────────────────────────────────────────────────
from mcp_http_client import MCPHttpClient


# =============================================================================
# Configuration
# =============================================================================

GATEWAY_BASE_URL = os.getenv("GATEWAY_BASE_URL", "http://localhost:8765")
ENDPOINT_ID = os.getenv("endpoint_id", "gpt")
PART_ID = os.getenv("part_id", "nestaging")
# Gateway login credentials (fall back to the legacy ADMIN_* names).
TOKEN_USERNAME = os.getenv("TOKEN_USERNAME", os.getenv("ADMIN_USERNAME", "admin"))
TOKEN_PASSWORD = os.getenv("TOKEN_PASSWORD", os.getenv("ADMIN_PASSWORD", "admin123"))
GATEWAY_TOKEN = os.getenv("GATEWAY_TOKEN", os.getenv("ADMIN_STATIC_TOKEN", ""))

# The gateway's REST/JSON-RPC MCP endpoint. MCPHttpClient POSTs JSON-RPC
# messages (initialize, tools/list, tools/call) to this URL.
MCP_REST_URL = os.getenv(
    "MCP_REST_URL",
    f"{GATEWAY_BASE_URL}/{ENDPOINT_ID}/mcp",
)

PARTITION_KEY = f"{ENDPOINT_ID}#{PART_ID}"

# =============================================================================
# Sample data (hardcoded UUIDs from prepared flight test fixtures)
# =============================================================================

SAMPLE: Dict[str, Any] = {
    # Items (flight_products.json)
    "item_uuid": "06041993713794695296",        # Flight ATL->ORD Premium Economy
    "item_uuid_2": "52065619693805781120",       # Flight ATL->ORD Economy
    "item_uuid_in_request": "06041993713794695296",
    "item_name": "Flight ATL->ORD Premium Economy",
    "item_type": "flight",
    # Provider items
    "provider_item_uuid": "39876487618607726720",
    "provider_item_uuid_2": "39876487618607726720",
    "provider_item_uuid_in_request": "39876487618607726720",
    "provider_corp_external_id": "AIRLINE-AF",
    "provider_corp_external_id_2": "AIRLINE-QF",
    # Batches
    "batch_no": "AF5319-20260907",
    "service_start_at": "2026-09-07T12:00:00Z",
    "service_end_at": "2026-09-07T14:37:07.381744Z",
    # Requests
    "request_uuid": "96306650268729098368",
    "email": "jessicacooper@example.com",
    # Quotes
    "quote_uuid": "83893620897501692032",
    "quote_uuid_with_items": "51485446173562519680",
    "request_uuid_for_quote_with_items": "87119168162060320896",
    "quote_item_uuid": "73631515167125684352",
    # Segments
    "segment_uuid": "61268299727527493760",
    # Bundles
    "bundle_uuid": "80092055917037633664",
    "bundle_uuid_2": "49956565412585947264",
    # Cancellation policies
    "policy_uuid": "70591963290008567936",
    # Catalog
    "catalog_query": "Air France ATL ORD Premium Economy flight with meal included",
    "catalog_namespace": "FLIGHTS",
}

# PostgreSQL-backend sample data. Active when SAMPLE_BACKEND=postgresql.
# These IDs come from the PostgreSQL flight_products.json fixtures (UUID-style),
# not the DynamoDB load_sample_data.py numeric keys.
SAMPLE_POSTGRESQL: Dict[str, Any] = {
    "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",       # Flight NRT->CDG First
    "item_uuid_2": "d6dd8e87-34f1-4741-b293-dc41992089b1",      # Flight CDG->ORD Economy
    "item_uuid_in_request": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
    "item_name": "Flight NRT->CDG First",
    "item_type": "flight",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",  # DL-NRT-CDG-FIR
    "provider_item_uuid_2": "bad12922-6da1-4117-95ec-5ee0284a5d95",  # SQ-CDG-ORD-ECO
    "provider_item_uuid_in_request": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "provider_corp_external_id": "AIRLINE-DL",
    "provider_corp_external_id_2": "AIRLINE-SQ",
    "batch_no": "DL4822-20260918",
    "service_start_at": "2026-09-18T14:45:00Z",
    "service_end_at": "2026-09-18T23:28:08.831283Z",
    "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
    "email": "zbrown@example.org",
    "quote_uuid": "9e8378fa-f6b3-4353-bf9a-af2ff6036ff8",
    "quote_uuid_with_items": "9e8378fa-f6b3-4353-bf9a-af2ff6036ff8",
    "request_uuid_for_quote_with_items": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
    "quote_item_uuid": "84336230-ce18-4a57-bf2b-4b8759255781",
    "segment_uuid": "323dec2b-1f03-4d42-a5ef-73ef9e17c4e6",
    "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",     # FLT-ITIN-001
    "bundle_uuid_2": "78af79fc-f9bc-4661-b968-72ab4233df5b",   # FLT-ITIN-002
    "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",     # First Fare Cancellation
    "catalog_query": "Delta Air Lines NRT CDG First class flight with meal included",
    "catalog_namespace": "FLIGHTS",
}

# Active backend selector for sample data. "postgresql" switches to the
# PostgreSQL-seeded fixtures; anything else (default) uses the DynamoDB
# numeric-key fixtures. Driven by the SAMPLE_BACKEND env var.
_SAMPLE_BACKEND = (os.getenv("SAMPLE_BACKEND") or "").strip().lower()
if _SAMPLE_BACKEND == "postgresql":
    SAMPLE = dict(SAMPLE_POSTGRESQL)

RUN_STATE: Dict[str, Any] = {}


def _parse_mcp_content(content_list: List[Dict]) -> Any:
    """Extract the text payload from MCP ``tools/call`` content items.

    MCP returns a list of content dicts, each with ``type`` and ``text``.
    The text is a JSON string that we decode to a Python object. If the
    text isn't JSON, return the raw string.
    """
    if not content_list:
        return None
    for item in content_list:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if text is None:
            continue
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return text
    return content_list


# =============================================================================
# Gateway auth token (for MCPHttpClient bearer_token)
# =============================================================================

def _get_gateway_token() -> str:
    """Obtain a JWT Bearer token from the gateway's /auth/token endpoint."""
    import requests as _requests

    if GATEWAY_TOKEN:
        print("Using static gateway token from .env")
        return GATEWAY_TOKEN

    print(f"Authenticating as {TOKEN_USERNAME} at {GATEWAY_BASE_URL}/auth/token ...")
    resp = _requests.post(
        f"{GATEWAY_BASE_URL}/auth/token",
        data={"username": TOKEN_USERNAME, "password": TOKEN_PASSWORD},
        timeout=10,
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    print(f"Auth OK - token received (len={len(token)})")
    return token


# =============================================================================
# Result printing & tracking
# =============================================================================

_passed = 0
_failed = 0
_skipped = 0
_results: List[Dict[str, Any]] = []


def _safe_json(value: Any, max_chars: int = 12000) -> str:
    text = json.dumps(value, default=str, indent=2, ensure_ascii=False)
    if len(text) > max_chars:
        return text[:max_chars] + "\n... (truncated)"
    return text


def _result_has_error_payload(value: Any) -> bool:
    """Detect both MCP error dicts and in-band error envelopes."""
    if isinstance(value, dict):
        if "error" in value:
            return True
        if value.get("error_code") or value.get("errorCode"):
            return True
        return any(_result_has_error_payload(v) for v in value.values())
    if isinstance(value, list):
        return any(_result_has_error_payload(item) for item in value)
    return False


def _is_expected_live_noop(tool_name: str, result: Any) -> bool:
    if tool_name != "expire_availability_hold" or not isinstance(result, dict):
        return False
    text = json.dumps(result, default=str)
    return "Availability hold has not expired" in text


async def call_tool(
    client: MCPHttpClient,
    tool_name: str,
    arguments: Dict[str, Any],
    group: str,
    label: Optional[str] = None,
) -> Tuple[Optional[Any], Optional[str]]:
    """
    Call a processor tool via MCPHttpClient (JSON-RPC tools/call), print the
    result, and track pass/fail.

    Returns (result, error_str).
    """
    global _passed, _failed, _skipped
    display = label or tool_name
    cid = uuid.uuid4().hex[:8]
    print(f"\n{'-' * 80}")
    print(f"  [{group}] {display}")
    print(f"  cid={cid}  args={json.dumps(arguments, default=str, ensure_ascii=False)[:300]}")
    print(f"{'-' * 80}")

    t0 = time.perf_counter()

    try:
        raw_content = await client.call_tool(tool_name, arguments)
        elapsed = round((time.perf_counter() - t0) * 1000, 2)

        # MCPHttpClient.call_tool returns the "content" list from the JSON-RPC
        # result. Each item is {type: "text", text: "<json>"}. Decode the text
        # payload so downstream logic works on the actual business object.
        result = _parse_mcp_content(raw_content)

        # Check if result is an error response
        is_error = _result_has_error_payload(result) and not _is_expected_live_noop(tool_name, result)

        if is_error:
            if isinstance(result, dict):
                error_val = (
                    result.get("error")
                    or result.get("error_message")
                    or result.get("errorMessage")
                    or result.get("error_code")
                    or result.get("errorCode")
                )
            else:
                error_val = result
            if isinstance(error_val, dict):
                error_msg = error_val.get("message", str(error_val))
            else:
                error_msg = str(error_val)
            print(f"  ERROR RESPONSE  ({elapsed}ms)")
            print(f"  {json.dumps(result, default=str, indent=2, ensure_ascii=False)[:1000]}")
            _results.append({
                "tool": display,
                "method": tool_name,
                "group": group,
                "arguments": arguments,
                "status": "error",
                "error": error_msg,
                "result": result,
                "elapsed_ms": elapsed,
            })
            _skipped += 1
            return result, error_msg

        # Success
        result_str = json.dumps(result, default=str, indent=2, ensure_ascii=False)
        if len(result_str) > 2000:
            result_str = result_str[:2000] + "\n  ... (truncated)"
        print(f"  PASS  ({elapsed}ms)")
        print(f"  {result_str}")
        _passed += 1
        _results.append({
            "tool": display,
            "method": tool_name,
            "group": group,
            "arguments": arguments,
            "status": "pass",
            "elapsed_ms": elapsed,
            "result": result,
        })
        return result, None

    except Exception as exc:
        elapsed = round((time.perf_counter() - t0) * 1000, 2)
        print(f"  FAIL EXCEPTION  ({elapsed}ms)")
        print(f"  {type(exc).__name__}: {exc}")
        _failed += 1
        _results.append({
            "tool": display,
            "method": tool_name,
            "group": group,
            "arguments": arguments,
            "status": "fail",
            "error": str(exc),
            "elapsed_ms": elapsed,
        })
        return None, str(exc)


def print_summary() -> None:
    print(f"\n{'=' * 80}")
    print(f"  HTTP INTEGRATION TEST SUMMARY (via MCPHttpClient)")
    print(f"{'=' * 80}")
    print(f"  Passed:      {_passed}")
    print(f"  Error resp:  {_skipped}")
    print(f"  Failed:      {_failed}")
    print(f"  Total:       {_passed + _skipped + _failed}")
    print()

    if _results:
        print(f"{'Group':<16} {'Tool':<45} {'Status':<8} {'Time'}")
        print(f"{'-' * 80}")
        for r in _results:
            status_icon = {"pass": "PASS", "error": "ERROR", "fail": "FAIL"}.get(r["status"], "?")
            print(f"{r['group']:<16} {r['tool']:<45} {status_icon} {r['status']:<5} {r.get('elapsed_ms', '?')}ms")

    print(f"{'=' * 80}\n")


def export_results(path: str, run_groups: List[str]) -> None:
    """Write a Markdown integration report."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now(timezone.utc).isoformat()

    lines = [
        "# MCP HospiRFQ Processor HTTP Integration Results (MCPHttpClient)",
        "",
        f"- Generated at: `{started_at}`",
        f"- Gateway: `{GATEWAY_BASE_URL}`",
        f"- MCP REST URL: `{MCP_REST_URL}`",
        f"- Endpoint: `{ENDPOINT_ID}`",
        f"- Partition: `{PART_ID}`",
        f"- Transport: MCPHttpClient → JSON-RPC → gateway `/mcp`",
        f"- Dependency order: `{', '.join(run_groups)}`",
        f"- Passed: `{_passed}`",
        f"- Error responses: `{_skipped}`",
        f"- Failed: `{_failed}`",
        f"- Total calls: `{_passed + _skipped + _failed}`",
        "",
        "## Executive Summary",
        "",
        "End-to-end HTTP integration testing was executed through the "
        "`mcp_http_client.MCPHttpClient` against the `silvaengine_gateway` "
        "REST/JSON-RPC MCP endpoint (`/{endpoint_id}/mcp`, with `Part-Id` "
        "sent as a request header). Each "
        "tool was invoked via JSON-RPC `tools/call`, exercising the full "
        "agent → gateway → `MCPHospiRFQProcessor` stack. The gateway handles "
        "all backend dispatch internally. "
        f"The run completed with {_passed} passing function calls, "
        f"{_skipped} error responses, and {_failed} failures.",
        "",
        "## Scope",
        "",
        "- In scope: MCP JSON-RPC transport (initialize, tools/list, "
        "tools/call), gateway MCP dispatch, MCPHospiRFQProcessor tool "
        "execution. The gateway handles backend dispatch internally.",
        "- Out of scope: production validation, destructive cleanup, "
        "load testing, UI testing.",
        "",
        "## Function Results",
        "",
    ]

    for idx, result in enumerate(_results, start=1):
        lines.extend([
            f"### {idx}. {result['group']} / {result['tool']}",
            "",
            f"- Method: `{result.get('method', '')}`",
            f"- Status: `{result['status']}`",
            f"- Elapsed: `{result.get('elapsed_ms', '?')} ms`",
            "",
            "Arguments:",
            "",
            "```json",
            _safe_json(result.get("arguments", {}), max_chars=6000),
            "```",
            "",
        ])

        if "error" in result:
            lines.extend([
                "Error:",
                "",
                "```text",
                str(result["error"]),
                "```",
                "",
            ])

        if "result" in result:
            lines.extend([
                "Output:",
                "",
                "```json",
                _safe_json(result["result"]),
                "```",
                "",
            ])

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Results exported to: {output_path}")


# =============================================================================
# Tool group definitions (mirror run_integration.py group structure)
# =============================================================================

GROUP_ORDER = [
    "items",
    "requests",
    "quotes",
    "pricing",
    "installments",
    "files",
    "segments",
    "availability",
    "bundles",
    "cancellation",
    "catalog",
]
GROUPS = set(GROUP_ORDER)


async def run_items(client: MCPHttpClient) -> None:
    """Item management tools (3)."""
    await call_tool(client, "search_items", {
        "item_type": SAMPLE["item_type"],
        "limit": 10,
        "page_number": 1,
    }, "items", "search_items (flight type)")

    await call_tool(client, "get_item", {
        "item_uuid": SAMPLE["item_uuid"],
    }, "items", f"get_item ({SAMPLE['item_name']})")

    await call_tool(client, "get_provider_items", {
        "item_uuid": SAMPLE["item_uuid"],
    }, "items", "get_provider_items (with batches)")


async def run_requests(client: MCPHttpClient) -> None:
    """Request management tools (8)."""
    # Submit a new RFQ request
    result, _ = await call_tool(client, "submit_rfq_request", {
        "email": SAMPLE["email"],
        "request_title": f"HTTP integration test: {SAMPLE['item_name']}",
        "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
        "items": [
            {
                "item_uuid": SAMPLE["item_uuid"],
                "item_name": SAMPLE["item_name"],
                "qty": 2,
                "pax_breakdown": {"adult": 2},
            }
        ],
        "notes": "Created by run_http_integration.py",
        "expired_at": "2026-12-31T23:59:59Z",
    }, "requests", "submit_rfq_request")

    target_request_uuid = SAMPLE["request_uuid"]
    if result and isinstance(result, dict) and result.get("request_uuid"):
        target_request_uuid = result["request_uuid"]
        RUN_STATE["request_uuid"] = target_request_uuid

    await call_tool(client, "get_rfq_request", {
        "request_uuid": SAMPLE["request_uuid"],
    }, "requests", "get_rfq_request (seeded)")

    await call_tool(client, "search_rfq_requests", {
        "limit": 5,
        "page_number": 1,
    }, "requests", "search_rfq_requests")

    await call_tool(client, "update_rfq_request", {
        "request_uuid": target_request_uuid,
        "request_title": f"HTTP integration test: {SAMPLE['item_name']} (updated)",
        "notes": "Updated via run_http_integration.py",
    }, "requests", "update_rfq_request")

    await call_tool(client, "add_item_to_rfq_request", {
        "request_uuid": target_request_uuid,
        "item": {
            "item_uuid": SAMPLE["item_uuid_2"],
            "item_name": "Flight ATL->ORD Economy",
            "qty": 1,
        },
    }, "requests", "add_item_to_rfq_request")

    await call_tool(client, "remove_item_from_rfq_request", {
        "request_uuid": target_request_uuid,
        "item_uuid": SAMPLE["item_uuid_2"],
    }, "requests", "remove_item_from_rfq_request")

    await call_tool(client, "assign_provider_item_to_request_item", {
        "request_uuid": target_request_uuid,
        "item_uuid": SAMPLE["item_uuid"],
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
        "provider_corp_external_id": SAMPLE["provider_corp_external_id"],
        "qty": 2,
        "batch_no": SAMPLE["batch_no"],
    }, "requests", "assign_provider_item_to_request_item")

    await call_tool(client, "remove_provider_item_from_request_item", {
        "request_uuid": target_request_uuid,
        "item_uuid": SAMPLE["item_uuid"],
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
    }, "requests", "remove_provider_item_from_request_item")

    await call_tool(client, "assign_provider_item_to_request_item", {
        "request_uuid": target_request_uuid,
        "item_uuid": SAMPLE["item_uuid"],
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
        "provider_corp_external_id": SAMPLE["provider_corp_external_id"],
        "qty": 2,
        "batch_no": SAMPLE["batch_no"],
    }, "requests", "assign_provider_item_to_request_item (for quote workflow)")


async def run_quotes(client: MCPHttpClient) -> None:
    """Quote management tools (5)."""
    request_uuid = RUN_STATE.get("request_uuid", SAMPLE["request_uuid"])

    confirm_result, _ = await call_tool(client, "confirm_request_and_create_quotes", {
        "request_uuid": request_uuid,
        "provider_corp_external_ids": [SAMPLE["provider_corp_external_id"]],
        "segment_uuid": SAMPLE["segment_uuid"],
        "batch_no": SAMPLE["batch_no"],
        "service_start_at": SAMPLE["service_start_at"],
        "service_end_at": SAMPLE["service_end_at"],
    }, "quotes", "confirm_request_and_create_quotes")

    quote_uuid = SAMPLE["quote_uuid"]
    quote_item_uuid = None
    if isinstance(confirm_result, dict):
        created_quotes = confirm_result.get("created_quotes", [])
        if created_quotes:
            quote = created_quotes[0]
            quote_uuid = quote.get("quote_uuid", quote_uuid)
            RUN_STATE["quote_uuid"] = quote_uuid
            RUN_STATE["request_uuid"] = request_uuid
            quote_items = quote.get("quote_items") or []
            if quote_items:
                quote_item_uuid = quote_items[0].get("quote_item_uuid")
                if quote_item_uuid:
                    RUN_STATE["quote_item_uuid"] = quote_item_uuid

    await call_tool(client, "get_quote", {
        "quote_uuid": quote_uuid,
        "request_uuid": request_uuid,
    }, "quotes", "get_quote")

    await call_tool(client, "search_quotes", {
        "request_uuid": request_uuid,
        "limit": 10,
        "page_number": 1,
    }, "quotes", "search_quotes")

    await call_tool(client, "update_quote", {
        "request_uuid": request_uuid,
        "quote_uuid": quote_uuid,
        "notes": "Updated via HTTP integration test",
        "shipping_method": "ticket_delivery",
        "shipping_amount": 25.0,
    }, "quotes", "update_quote")

    quote_item_uuid = RUN_STATE.get("quote_item_uuid", SAMPLE["quote_item_uuid"])

    await call_tool(client, "update_quote_item", {
        "quote_uuid": quote_uuid,
        "quote_item_uuid": quote_item_uuid,
        "request_uuid": request_uuid,
        "discount_amount": 50.0,
        "notes": "HTTP integration test discount",
    }, "quotes", "update_quote_item")


async def run_pricing(client: MCPHttpClient) -> None:
    """Pricing tools (3)."""
    await call_tool(client, "get_item_price_tiers", {
        "email": SAMPLE["email"],
        "quote_items": [
            {
                "item_uuid": SAMPLE["item_uuid"],
                "provider_item_uuid": SAMPLE["provider_item_uuid"],
                "qty": 2,
            }
        ],
    }, "pricing", "get_item_price_tiers")

    await call_tool(client, "get_discount_prompts", {
        "email": SAMPLE["email"],
        "quote_items": [
            {
                "item_uuid": SAMPLE["item_uuid"],
                "provider_item_uuid": SAMPLE["provider_item_uuid"],
            }
        ],
    }, "pricing", "get_discount_prompts")

    await call_tool(client, "calculate_quote_pricing", {
        "request_uuid": SAMPLE["request_uuid"],
        "email": SAMPLE["email"],
    }, "pricing", "calculate_quote_pricing")


async def create_confirmed_quote_setup(
    client: MCPHttpClient,
    label: str,
) -> Tuple[Optional[str], Optional[str]]:
    """Create a fresh confirmed quote for standalone installment scenarios."""
    request_result, request_error = await call_tool(client, "submit_rfq_request", {
        "email": SAMPLE["email"],
        "request_title": f"HTTP installment setup ({label}): {SAMPLE['item_name']}",
        "request_description": "Setup request for standalone installment tool validation",
        "items": [
            {
                "item_uuid": SAMPLE["item_uuid"],
                "item_name": SAMPLE["item_name"],
                "qty": 1,
                "pax_breakdown": {"adult": 1},
            }
        ],
        "notes": f"Created by run_http_integration.py for {label}",
        "expired_at": "2026-12-31T23:59:59Z",
    }, "installments", f"setup submit_rfq_request ({label})")
    if request_error or not isinstance(request_result, dict):
        return None, None

    request_uuid = request_result.get("request_uuid")
    if not request_uuid:
        return None, None

    _, assign_error = await call_tool(client, "assign_provider_item_to_request_item", {
        "request_uuid": request_uuid,
        "item_uuid": SAMPLE["item_uuid"],
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
        "provider_corp_external_id": SAMPLE["provider_corp_external_id"],
        "qty": 1,
        "batch_no": SAMPLE["batch_no"],
    }, "installments", f"setup assign_provider_item_to_request_item ({label})")
    if assign_error:
        return request_uuid, None

    confirm_result, confirm_error = await call_tool(client, "confirm_request_and_create_quotes", {
        "request_uuid": request_uuid,
        "provider_corp_external_ids": [SAMPLE["provider_corp_external_id"]],
        "segment_uuid": SAMPLE["segment_uuid"],
        "batch_no": SAMPLE["batch_no"],
        "service_start_at": SAMPLE["service_start_at"],
        "service_end_at": SAMPLE["service_end_at"],
    }, "installments", f"setup confirm_request_and_create_quotes ({label})")
    if confirm_error or not isinstance(confirm_result, dict):
        return request_uuid, None

    created_quotes = confirm_result.get("created_quotes") or []
    if not created_quotes:
        return request_uuid, None

    quote_uuid = created_quotes[0].get("quote_uuid")
    if not quote_uuid:
        return request_uuid, None

    _, update_error = await call_tool(client, "update_quote", {
        "request_uuid": request_uuid,
        "quote_uuid": quote_uuid,
        "status": "confirmed",
        "notes": f"Confirmed setup quote for {label}",
    }, "installments", f"setup update_quote confirmed ({label})")
    if update_error:
        return request_uuid, None

    return request_uuid, quote_uuid


async def run_installments(client: MCPHttpClient) -> None:
    """Installment tools (5)."""
    request_uuid = RUN_STATE.get("request_uuid", SAMPLE["request_uuid"])
    quote_uuid = RUN_STATE.get("quote_uuid", SAMPLE["quote_uuid"])

    await call_tool(client, "confirm_quote_and_create_installments", {
        "request_uuid": request_uuid,
        "quote_uuid": quote_uuid,
        "create_single_installment": True,
        "payment_method": "bank_transfer",
    }, "installments", "confirm_quote_and_create_installments")

    # Get installments — extract a real installment_uuid for subsequent calls
    inst_result, _ = await call_tool(client, "get_installments", {
        "quote_uuid": quote_uuid,
        "limit": 10,
        "page_number": 1,
    }, "installments", "get_installments")

    real_installment_uuid = None
    if inst_result and isinstance(inst_result, dict):
        inst_list = inst_result.get("installment_list", [])
        if inst_list:
            real_installment_uuid = inst_list[0].get("installment_uuid")

    single_request_uuid, single_quote_uuid = await create_confirmed_quote_setup(
        client, "create_installment"
    )
    await call_tool(client, "create_installment", {
        "quote_uuid": single_quote_uuid or quote_uuid,
        "request_uuid": single_request_uuid or request_uuid,
        "installment_amount": 100.0,
        "payment_method": "credit_card",
    }, "installments", "create_installment")

    multi_request_uuid, multi_quote_uuid = await create_confirmed_quote_setup(
        client, "create_installments"
    )
    await call_tool(client, "create_installments", {
        "quote_uuid": multi_quote_uuid or quote_uuid,
        "request_uuid": multi_request_uuid or request_uuid,
        "interval_num": 3,
        "total_pay_period": 6,
        "payment_method": "bank_transfer",
    }, "installments", "create_installments")

    # Update an installment — use the real UUID if we got one
    update_uuid = real_installment_uuid or "00000000000000000000"
    await call_tool(client, "update_installment", {
        "quote_uuid": quote_uuid,
        "installment_uuid": update_uuid,
        "status": "paid",
    }, "installments", f"update_installment (uuid={update_uuid[:12]}...)")


async def run_files(client: MCPHttpClient) -> None:
    """File tools (2)."""
    await call_tool(client, "upload_rfq_file", {
        "request_uuid": SAMPLE["request_uuid"],
        "file_name": "http_integration_test_spec.pdf",
        "email": SAMPLE["email"],
    }, "files", "upload_rfq_file")

    await call_tool(client, "get_rfq_files", {
        "request_uuid": SAMPLE["request_uuid"],
        "limit": 10,
        "page_number": 1,
    }, "files", "get_rfq_files")


async def run_segments(client: MCPHttpClient) -> None:
    """Segment tools (1)."""
    await call_tool(client, "get_segment_contacts", {
        "email": SAMPLE["email"],
        "limit": 10,
        "page_number": 1,
    }, "segments", "get_segment_contacts")


async def run_availability(client: MCPHttpClient) -> None:
    """Availability hold tools (5)."""
    await call_tool(client, "check_availability", {
        "partition_key": PARTITION_KEY,
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
        "service_start_at": SAMPLE["service_start_at"],
        "service_end_at": SAMPLE["service_end_at"],
        "batch_no": SAMPLE["batch_no"],
        "qty": 2,
    }, "availability", "check_availability")

    result, _ = await call_tool(client, "acquire_availability_hold", {
        "partition_key": PARTITION_KEY,
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
        "service_start_at": SAMPLE["service_start_at"],
        "service_end_at": SAMPLE["service_end_at"],
        "qty": 2,
        "batch_no": SAMPLE["batch_no"],
        "pax_breakdown": {"adult": 2},
    }, "availability", "acquire_availability_hold")

    hold_token = None
    if result and isinstance(result, dict):
        avail = result.get("availability", result)
        hold_token = avail.get("hold_token") or avail.get("holdToken")

    if hold_token:
        await call_tool(client, "confirm_availability_hold", {
            "partition_key": PARTITION_KEY,
            "hold_token": hold_token,
            "provider_item_uuid": SAMPLE["provider_item_uuid"],
            "batch_no": SAMPLE["batch_no"],
        }, "availability", "confirm_availability_hold")

        result2, _ = await call_tool(client, "acquire_availability_hold", {
            "partition_key": PARTITION_KEY,
            "provider_item_uuid": SAMPLE["provider_item_uuid"],
            "service_start_at": SAMPLE["service_start_at"],
            "service_end_at": SAMPLE["service_end_at"],
            "qty": 1,
            "batch_no": SAMPLE["batch_no"],
        }, "availability", "acquire_availability_hold (for release test)")

        hold_token2 = None
        if result2 and isinstance(result2, dict):
            avail2 = result2.get("availability", result2)
            hold_token2 = avail2.get("hold_token") or avail2.get("holdToken")

        if hold_token2:
            await call_tool(client, "release_availability_hold", {
                "partition_key": PARTITION_KEY,
                "hold_token": hold_token2,
                "provider_item_uuid": SAMPLE["provider_item_uuid"],
                "batch_no": SAMPLE["batch_no"],
            }, "availability", "release_availability_hold")

        result3, _ = await call_tool(client, "acquire_availability_hold", {
            "partition_key": PARTITION_KEY,
            "provider_item_uuid": SAMPLE["provider_item_uuid"],
            "service_start_at": SAMPLE["service_start_at"],
            "service_end_at": SAMPLE["service_end_at"],
            "qty": 1,
            "batch_no": SAMPLE["batch_no"],
        }, "availability", "acquire_availability_hold (for expire test)")

        hold_token3 = None
        if result3 and isinstance(result3, dict):
            avail3 = result3.get("availability", result3)
            hold_token3 = avail3.get("hold_token") or avail3.get("holdToken")

        if hold_token3:
            await call_tool(client, "expire_availability_hold", {
                "partition_key": PARTITION_KEY,
                "hold_token": hold_token3,
                "provider_item_uuid": SAMPLE["provider_item_uuid"],
                "batch_no": SAMPLE["batch_no"],
            }, "availability", "expire_availability_hold")
    else:
        print("  WARNING: No hold_token in acquire result - skipping lifecycle calls")


async def run_bundles(client: MCPHttpClient) -> None:
    """Bundle tools (3)."""
    await call_tool(client, "search_bundles", {
        "partition_key": PARTITION_KEY,
        "bundle_type": "itinerary",
    }, "bundles", "search_bundles (itinerary type)")

    await call_tool(client, "get_bundle", {
        "partition_key": PARTITION_KEY,
        "bundle_uuid": SAMPLE["bundle_uuid"],
    }, "bundles", "get_bundle (FLT-ITIN-001)")

    await call_tool(client, "search_bundle_components", {
        "partition_key": PARTITION_KEY,
        "bundle_uuid": SAMPLE["bundle_uuid"],
    }, "bundles", "search_bundle_components")


async def run_cancellation(client: MCPHttpClient) -> None:
    """Cancellation policy tools (2)."""
    await call_tool(client, "get_cancellation_policy", {
        "partition_key": PARTITION_KEY,
        "policy_uuid": SAMPLE["policy_uuid"],
    }, "cancellation", "get_cancellation_policy (Business Fare)")

    await call_tool(client, "search_cancellation_policies", {
        "partition_key": PARTITION_KEY,
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
    }, "cancellation", "search_cancellation_policies")


async def run_catalog(client: MCPHttpClient) -> None:
    """Catalog inquiry tool (1)."""
    await call_tool(client, "inquire_catalog", {
        "partition_key": PARTITION_KEY,
        "query_text": SAMPLE["catalog_query"],
        "namespace": SAMPLE["catalog_namespace"],
        "limit": 5,
    }, "catalog", "inquire_catalog")


# Group → runner mapping (preserves logical execution order)
GROUP_RUNNERS = {
    "items": run_items,
    "requests": run_requests,
    "quotes": run_quotes,
    "pricing": run_pricing,
    "installments": run_installments,
    "files": run_files,
    "segments": run_segments,
    "availability": run_availability,
    "bundles": run_bundles,
    "cancellation": run_cancellation,
    "catalog": run_catalog,
}


# =============================================================================
# Main
# =============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="E2E integration tests for MCP HospiRFQ Processor via MCPHttpClient through silvaengine_gateway"
    )
    parser.add_argument(
        "--only", type=str, default=None,
        help="Comma-separated tool groups to run (e.g. 'items,requests'). Default: all.",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List available tool groups and exit.",
    )
    parser.add_argument(
        "--export", type=str, default="docs/http_integration_results.md",
        help="Markdown path for per-function output. Default: docs/http_integration_results.md",
    )
    parser.add_argument(
        "--list-tools", action="store_true",
        help="Call tools/list via MCPHttpClient and print available tools, then exit.",
    )
    return parser.parse_args()


async def _run_groups(client: MCPHttpClient, run_groups: List[str]) -> Optional[Exception]:
    """Execute the selected tool groups sequentially."""
    group_error: Optional[Exception] = None
    for group in run_groups:
        runner = GROUP_RUNNERS.get(group)
        if not runner:
            print(f"WARNING: No runner for group '{group}' - skipping")
            continue

        print(f"\n{'=' * 80}")
        print(f"  GROUP: {group.upper()}")
        print(f"{'=' * 80}")

        try:
            await runner(client)
        except Exception as exc:
            print(f"  FAIL GROUP ERROR: {exc}")
            import traceback
            traceback.print_exc()
            group_error = exc
            break
    return group_error


async def _async_main() -> None:
    args = parse_args()

    if args.list:
        print("Available tool groups:")
        for g in GROUP_ORDER:
            runner = GROUP_RUNNERS.get(g)
            print(f"  {g:<16} - {runner.__doc__.strip().split(chr(10))[0] if runner else '(no runner)'}")
        return

    # Determine which groups to run
    if args.only:
        requested = set(g.strip() for g in args.only.split(","))
        unknown = requested - GROUPS
        if unknown:
            print(f"ERROR: Unknown group(s): {unknown}")
            print(f"Available: {sorted(GROUPS)}")
            sys.exit(1)
        run_groups = [g for g in GROUP_ORDER if g in requested]
    else:
        run_groups = list(GROUP_ORDER)

    print(f"\n{'=' * 80}")
    print(f"  MCP HospiRFQ Processor - HTTP Integration Tests (MCPHttpClient)")
    print(f"{'=' * 80}")
    print(f"  Gateway:       {GATEWAY_BASE_URL}")
    print(f"  MCP REST URL:   {MCP_REST_URL}")
    print(f"  Endpoint:      {ENDPOINT_ID}")
    print(f"  Partition:     {PART_ID}")
    print(f"  Groups:         {', '.join(run_groups)}")
    print(f"{'=' * 80}\n")

    # ── Obtain gateway JWT ──────────────────────────────────────────────────
    try:
        bearer_token = _get_gateway_token()
        print(f"MCPHttpClient will use Bearer auth\n")
    except Exception as exc:
        print(f"FATAL: Cannot authenticate with gateway: {exc}")
        print(f"Is the gateway running at {GATEWAY_BASE_URL}?")
        sys.exit(1)

    # ── Create MCPHttpClient (async context manager) ──────────────────────
    client_setting: Dict[str, Any] = {
        "base_url": MCP_REST_URL,
        "bearer_token": bearer_token,
        "headers": {
            "Part-Id": PART_ID,
        },
    }

    async with MCPHttpClient(logger, **client_setting) as client:
        # ── Optional: list tools first ─────────────────────────────────────
        if args.list_tools:
            print(f"\n{'=' * 80}")
            print(f"  tools/list via MCPHttpClient")
            print(f"{'=' * 80}")
            tools = await client.list_tools()
            print(f"  {len(tools)} tools available:")
            for tool in tools:
                print(f"    - {tool.name}: {tool.description[:80]}")
            print()
            if not args.only and not run_groups:
                return

        # ── Run tool groups ────────────────────────────────────────────────
        group_error = await _run_groups(client, run_groups)

    # ── Summary ──────────────────────────────────────────────────────────────
    print_summary()
    if args.export:
        export_results(args.export, run_groups)
    if group_error is not None or _failed or _skipped:
        sys.exit(1)


def main() -> None:
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
