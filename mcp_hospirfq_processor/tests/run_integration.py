#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
End-to-end integration tests for MCP HospiRFQ Processor through silvaengine_gateway.

This script exercises all 38 processor tools against a live gateway instance.
It authenticates with the gateway, patches the GraphQLClient to use Bearer JWT
auth (the gateway's auth model) instead of x-api-key, and calls each tool with
sample data from ai_rfq_engine's prepare_test_data fixtures.

Prerequisites:
  1. silvaengine_gateway is running:
       python -m silvaengine_gateway.tests.run_daemon
  2. ai_rfq_engine test data has been seeded (prepare_test_data scripts).
  3. tests/.env is configured with correct endpoint_id, part_id, and credentials.

Usage:
  # Run all 38 tools end-to-end:
  python -m mcp_hospirfq_processor.tests.run_integration

  # Run only specific tool groups:
  python -m mcp_hospirfq_processor.tests.run_integration --only items,requests

  # Run a single tool:
  python -m mcp_hospirfq_processor.tests.run_integration --only search_items

  # List available groups:
  python -m mcp_hospirfq_processor.tests.run_integration --list

Tool groups:
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
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
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
sys.path.insert(0, os.path.join(base_dir, "ai_rfq_engine"))
sys.path.insert(0, os.path.join(base_dir, "mcp_hospirfq_processor"))

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("integration_hospirfq")

# ── Imports (after sys.path) ─────────────────────────────────────────────────
from silvaengine_utility.graphql import Graphql
from silvaengine_utility.serializer import Serializer

from mcp_hospirfq_processor.mcp_hospirfq_processor import MCPHospiRFQProcessor


# =============================================================================
# Configuration
# =============================================================================

GATEWAY_BASE_URL = os.getenv("GATEWAY_BASE_URL", "http://localhost:8765")
ENDPOINT_ID = os.getenv("endpoint_id", "gpt")
PART_ID = os.getenv("part_id", "nestaging")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
ADMIN_STATIC_TOKEN = os.getenv("ADMIN_STATIC_TOKEN", "")

# GraphQL endpoint on the gateway
GRAPHQL_PATH = f"/{ENDPOINT_ID}/{PART_ID}/ai_rfq_graphql"
GRAPHQL_URL = f"{GATEWAY_BASE_URL}{GRAPHQL_PATH}"

# Partition key (gateway constructs this from path params, but some tools pass it directly)
PARTITION_KEY = f"{ENDPOINT_ID}#{PART_ID}"

# Processor setting — endpoint is the gateway route; x_api_key is a placeholder
# because the gateway uses Bearer JWT, not x-api-key.
SETTING = {
    "graphql_modules": {
        "ai_rfq_engine": {
            "class_name": os.getenv("AI_RFQ_ENGINE_CLASS_NAME", "AIRFQEngine"),
            "endpoint": GRAPHQL_URL,
            "x_api_key": os.getenv("AI_RFQ_ENGINE_X_API_KEY", "placeholder"),
        }
    },
    "sales_rep_emails": json.loads(
        os.getenv(
            "SALES_REP_EMAILS",
            '{"PROVIDER-001":"sales1@provider.com","PROVIDER-002":"sales2@provider.com"}',
        )
    ),
}

# =============================================================================
# Sample data (from ai_rfq_engine/tests/prepare_test_data/)
# =============================================================================

SAMPLE = {
    # Items (flight_products.json)
    "item_uuid": "17735923656909930624",        # Flight CDG->JFK Business
    "item_uuid_2": "52065619693805781120",       # Flight ATL->ORD Economy
    # Item that exists in the seeded request 96306650268729098368
    "item_uuid_in_request": "06041993713794695296",  # Flight ATL->ORD Premium Economy
    "item_name": "Flight CDG->JFK Business",
    "item_type": "flight",
    # Provider items
    "provider_item_uuid": "55349863084404523136",  # AF-CDG-JFK-BUS
    "provider_item_uuid_2": "39876487618607726720",  # AF-ATL-ORD-PRE
    # Provider item for the item in the seeded request
    "provider_item_uuid_in_request": "39876487618607726720",  # AF-ATL-ORD-PRE (matches item 06041993713794695296)
    "provider_corp_external_id": "AIRLINE-AF",
    "provider_corp_external_id_2": "AIRLINE-QF",
    # Batches (provider_item_batches in flight_products.json)
    "batch_no": "AF8751-20260811",
    "service_start_at": "2026-08-11T08:30:00Z",
    "service_end_at": "2026-08-11T20:57:51.046308Z",
    # Requests (requests.json)
    "request_uuid": "96306650268729098368",
    "email": "jessicacooper@example.com",
    # Quotes (quotes.json) — quote 83893620897501692032 is empty (no quote items)
    # Use quote 51485446173562519680 which has quote items (quote_items.json)
    "quote_uuid": "83893620897501692032",
    "quote_uuid_with_items": "51485446173562519680",
    "request_uuid_for_quote_with_items": "87119168162060320896",
    # Quote items (quote_items.json)
    "quote_item_uuid": "73631515167125684352",
    # Segments
    "segment_uuid": "61268299727527493760",
    # Bundles (flight_products.json)
    "bundle_uuid": "80092055917037633664",       # FLT-ITIN-001
    "bundle_uuid_2": "49956565412585947264",      # FLT-ITIN-002
    # Cancellation policies (flight_products.json)
    "policy_uuid": "70591963290008567936",       # Business Fare Cancellation
    # Catalog
    "catalog_query": "Air France ATL ORD Premium Economy flight with meal included",
    "catalog_namespace": "FLIGHTS",
}


RUN_STATE: Dict[str, Any] = {}


def _load_flight_catalog_refs() -> Dict[str, Any]:
    refs_path = (
        Path(base_dir)
        / "ai_rfq_engine"
        / "ai_rfq_engine"
        / "tests"
        / "prepare_test_data"
        / "flight_catalog_refs.json"
    )
    if not refs_path.exists():
        return {}
    return json.loads(refs_path.read_text(encoding="utf-8"))


def _load_flight_products() -> Dict[str, Any]:
    products_path = (
        Path(base_dir)
        / "ai_rfq_engine"
        / "ai_rfq_engine"
        / "tests"
        / "prepare_test_data"
        / "flight_products.json"
    )
    if not products_path.exists():
        return {}
    return json.loads(products_path.read_text(encoding="utf-8"))


def _item_name_from_catalog_ref(ref: Dict[str, Any]) -> Optional[str]:
    extra = ref.get("extra") or {}
    route = extra.get("route")
    cabin_class = extra.get("cabinClass")
    if not route or not cabin_class:
        return None
    return f"Flight {route.replace('-', '->')} {cabin_class}"


def _provider_corp_from_catalog_ref(ref: Dict[str, Any]) -> str:
    extra = ref.get("extra") or {}
    airline_code = extra.get("airlineCode")
    if airline_code:
        return f"AIRLINE-{airline_code}"
    provider_external_id = extra.get("providerItemExternalId", "")
    if "-" in provider_external_id:
        return f"AIRLINE-{provider_external_id.split('-', 1)[0]}"
    return SAMPLE["provider_corp_external_id"]


def _batch_from_selected_ref(ref: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    products = _load_flight_products()
    batches = products.get("provider_item_batches") or []
    for batch in batches:
        if (
            batch.get("itemUuid") == ref.get("itemUuid")
            and batch.get("providerItemUuid") == ref.get("providerItemUuid")
        ):
            return batch
    return None


def _apply_catalog_discovery(result: Any) -> bool:
    """Use the first matching catalog search hit to choose the primary test item."""
    refs = _load_flight_catalog_refs()
    matched_refs = refs.get("matched") or []
    if not matched_refs or not isinstance(result, dict):
        return False

    results = ((result.get("payload") or {}).get("results") or [])
    result_blob = json.dumps(result, ensure_ascii=False)

    selected_ref = None
    for hit in results:
        if not isinstance(hit, dict):
            continue
        hit_text = str(((hit.get("metadata") or {}).get("node") or {}).get("text") or "")
        for ref in matched_refs:
            item_name = _item_name_from_catalog_ref(ref)
            node_id = ref.get("nodeId")
            if (
                (item_name and item_name in hit_text)
                or (node_id and node_id in hit_text)
            ):
                selected_ref = ref
                break
        if selected_ref:
            break

    if selected_ref is None:
        for ref in matched_refs:
            item_name = _item_name_from_catalog_ref(ref)
            node_id = ref.get("nodeId")
            if (
                (item_name and item_name in result_blob)
                or (node_id and node_id in result_blob)
            ):
                selected_ref = ref
                break

    if selected_ref is None:
        return False

    item_name = _item_name_from_catalog_ref(selected_ref)
    batch = _batch_from_selected_ref(selected_ref)
    SAMPLE["item_uuid"] = selected_ref.get("itemUuid", SAMPLE["item_uuid"])
    SAMPLE["provider_item_uuid"] = selected_ref.get(
        "providerItemUuid", SAMPLE["provider_item_uuid"]
    )
    SAMPLE["provider_corp_external_id"] = _provider_corp_from_catalog_ref(selected_ref)
    if batch:
        SAMPLE["batch_no"] = batch.get("batchNo", SAMPLE["batch_no"])
        SAMPLE["service_start_at"] = batch.get("serviceStartAt", SAMPLE["service_start_at"])
        SAMPLE["service_end_at"] = batch.get("serviceEndAt", SAMPLE["service_end_at"])
        SAMPLE["policy_uuid"] = batch.get("cancellationPolicyUuid", SAMPLE["policy_uuid"])
    if item_name:
        SAMPLE["item_name"] = item_name
    RUN_STATE["catalog_selected_item"] = {
        "item_uuid": SAMPLE["item_uuid"],
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
        "provider_corp_external_id": SAMPLE["provider_corp_external_id"],
        "item_name": SAMPLE["item_name"],
        "batch_no": SAMPLE["batch_no"],
        "service_start_at": SAMPLE["service_start_at"],
        "service_end_at": SAMPLE["service_end_at"],
        "node_id": selected_ref.get("nodeId"),
        "catalog_ref_uuid": selected_ref.get("catalogRefUuid"),
    }
    return True


# =============================================================================
# Auth & Gateway Client
# =============================================================================

def get_gateway_token() -> str:
    """Authenticate with the gateway and return a JWT access token."""
    if ADMIN_STATIC_TOKEN:
        print(f"Using static token from .env")
        return ADMIN_STATIC_TOKEN

    print(f"Authenticating as {ADMIN_USERNAME} at {GATEWAY_BASE_URL}/auth/token ...")
    resp = httpx.post(
        f"{GATEWAY_BASE_URL}/auth/token",
        data={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
        timeout=15,
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    print(f"Auth OK - token received (len={len(token)})")
    return token


def patch_graphql_client(processor: MCPHospiRFQProcessor, token: str) -> None:
    """
    Replace GraphQLClient.execute_query with a version that:
    1. Formats the endpoint URL with both endpoint_id AND part_id
    2. Sends Authorization: Bearer <token> instead of x-api-key
    3. Otherwise behaves identically (schema fetch, query generation, etc.)
    """
    original_client = processor.graphql_client
    original_execute = original_client.execute_query

    def patched_execute(
        function_name: str,
        operation_name: str,
        operation_type: str,
        variables: Dict[str, Any],
        query: str = None,
        module_name: str = "ai_rfq_engine",
    ) -> Dict[str, Any]:
        try:
            graphql_module = original_client.get_graphql_module(module_name)
            if query is None:
                query = Graphql.generate_graphql_operation(
                    operation_name, operation_type, graphql_module.schema
                )

            payload = Serializer.json_dumps({"query": query, "variables": variables})

            # Use Bearer auth + Part-Id (gateway model)
            headers = {
                "Authorization": f"Bearer {token}",
                "Part-Id": original_client.part_id or PART_ID,
                "Content-Type": "application/json",
            }

            url = GRAPHQL_URL  # already formatted with endpoint_id + part_id

            with httpx.Client(http2=True, timeout=60) as client:
                response = client.post(url, headers=headers, content=payload)

            result = response.json()

            if "errors" in result:
                error_message = result["errors"][0].get("message", "GraphQL error")
                raise Exception(f"GraphQL error: {error_message}")

            return result.get("data", {}).get(operation_name)

        except Exception as e:
            import traceback
            log = traceback.format_exc()
            logger.error(log)
            from mcp_hospirfq_processor.error_handler import (
                ErrorCode,
                build_error_response,
                extract_error_message,
            )
            err_msg = str(e)
            if isinstance(e, dict):
                err_msg = extract_error_message(e)
            return build_error_response(
                err_msg,
                ErrorCode.GRAPHQL_QUERY_FAILED,
                {"function_name": function_name, "operation": operation_name},
            )

    original_client.execute_query = patched_execute


# =============================================================================
# Result printing
# =============================================================================

_passed = 0
_failed = 0
_skipped = 0
_results: List[Dict[str, Any]] = []


def _safe_json(value: Any, max_chars: int = 12000) -> str:
    """Serialize result data for logs and docs without overwhelming the report."""
    text = json.dumps(value, default=str, indent=2, ensure_ascii=False)
    if len(text) > max_chars:
        return text[:max_chars] + "\n... (truncated)"
    return text


def _result_has_error_payload(value: Any) -> bool:
    """Detect both MCP error dicts and in-band GraphQL error envelopes."""
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
    """Some live-only lifecycle calls validly return an in-band no-op envelope."""
    if tool_name != "expire_availability_hold" or not isinstance(result, dict):
        return False
    text = json.dumps(result, default=str)
    return "Availability hold has not expired" in text


def call_tool(
    processor: MCPHospiRFQProcessor,
    tool_name: str,
    arguments: Dict[str, Any],
    group: str,
    label: Optional[str] = None,
    skip_on_error: bool = False,
) -> Tuple[Optional[Any], Optional[str]]:
    """
    Call a processor tool, print the result, and track pass/fail.

    Returns (result, error_str).
    """
    display = label or tool_name
    cid = uuid.uuid4().hex[:8]
    print(f"\n{'-' * 80}")
    print(f"  [{group}] {display}")
    print(f"  cid={cid}  args={json.dumps(arguments, default=str, ensure_ascii=False)[:300]}")
    print(f"{'-' * 80}")

    t0 = time.perf_counter()

    try:
        method = getattr(processor, tool_name)
    except AttributeError as exc:
        elapsed = round((time.perf_counter() - t0) * 1000, 2)
        print(f"  FAIL METHOD NOT FOUND: {exc}  ({elapsed}ms)")
        global _failed
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

    try:
        result = method(**arguments)
        elapsed = round((time.perf_counter() - t0) * 1000, 2)

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
            global _skipped
            _skipped += 1
            return result, error_msg
        else:
            # Success
            result_str = json.dumps(result, default=str, indent=2, ensure_ascii=False)
            # Truncate very long results for display
            if len(result_str) > 2000:
                result_str = result_str[:2000] + "\n  ... (truncated)"
            print(f"  PASS  ({elapsed}ms)")
            print(f"  {result_str}")
            global _passed
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
    """Print final summary of all tool calls."""
    print(f"\n{'=' * 80}")
    print(f"  INTEGRATION TEST SUMMARY")
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
    """Write a Markdown integration report under docs/."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now(timezone.utc).isoformat()

    lines = [
        "# MCP HospiRFQ Processor Live Integration Results",
        "",
        f"- Generated at: `{started_at}`",
        f"- Gateway: `{GATEWAY_BASE_URL}`",
        f"- Endpoint: `{ENDPOINT_ID}`",
        f"- Partition: `{PART_ID}`",
        f"- GraphQL URL: `{GRAPHQL_URL}`",
        f"- Dependency order: `{', '.join(run_groups)}`",
        f"- Passed: `{_passed}`",
        f"- Error responses: `{_skipped}`",
        f"- Failed: `{_failed}`",
        f"- Total calls: `{_passed + _skipped + _failed}`",
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
# Tool group definitions
# =============================================================================

GROUP_ORDER = [
    "catalog_discovery",
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


def run_catalog_discovery(processor: MCPHospiRFQProcessor) -> None:
    """Catalog-first item discovery gate (1)."""
    result, _ = call_tool(processor, "inquire_catalog", {
        "partition_key": PARTITION_KEY,
        "query_text": SAMPLE["catalog_query"],
        "namespace": SAMPLE["catalog_namespace"],
        "limit": 5,
    }, "catalog_discovery", "inquire_catalog (select primary item)")
    if not _apply_catalog_discovery(result):
        raise RuntimeError(
            "Catalog discovery did not return a result that maps to flight_catalog_refs.json"
        )
    if RUN_STATE.get("catalog_selected_item"):
        print(
            "  Catalog-selected item: "
            f"{json.dumps(RUN_STATE['catalog_selected_item'], ensure_ascii=False)}"
        )


def run_items(processor: MCPHospiRFQProcessor) -> None:
    """Item management tools (3)."""
    call_tool(processor, "search_items", {
        "item_type": SAMPLE["item_type"],
        "limit": 10,
        "page_number": 1,
    }, "items", "search_items (flight type)")

    call_tool(processor, "get_item", {
        "item_uuid": SAMPLE["item_uuid"],
    }, "items", f"get_item ({SAMPLE['item_name']})")

    call_tool(processor, "get_provider_items", {
        "item_uuid": SAMPLE["item_uuid"],
    }, "items", "get_provider_items (with batches)")


def run_requests(processor: MCPHospiRFQProcessor) -> None:
    """Request management tools (8)."""
    # Submit a new RFQ request
    result, err = call_tool(processor, "submit_rfq_request", {
        "email": SAMPLE["email"],
        "request_title": f"Integration test: {SAMPLE['item_name']}",
        "request_description": "E2E test request via silvaengine_gateway",
        "items": [
            {
                "item_uuid": SAMPLE["item_uuid"],
                "item_name": SAMPLE["item_name"],
                "qty": 2,
                "pax_breakdown": {"adult": 2},
            }
        ],
        "notes": "Created by run_integration.py",
        "expired_at": "2026-12-31T23:59:59Z",
    }, "requests", "submit_rfq_request")

    # Use the newly created request for mutating lifecycle operations.
    target_request_uuid = SAMPLE["request_uuid"]
    if result and isinstance(result, dict) and result.get("request_uuid"):
        target_request_uuid = result["request_uuid"]
        RUN_STATE["request_uuid"] = target_request_uuid

    call_tool(processor, "get_rfq_request", {
        "request_uuid": SAMPLE["request_uuid"],
    }, "requests", "get_rfq_request (seeded)")

    call_tool(processor, "search_rfq_requests", {
        "limit": 5,
        "page_number": 1,
    }, "requests", "search_rfq_requests")

    # Update the fresh request
    call_tool(processor, "update_rfq_request", {
        "request_uuid": target_request_uuid,
        "request_title": f"Integration test: {SAMPLE['item_name']} (updated)",
        "notes": "Updated via run_integration.py",
    }, "requests", "update_rfq_request")

    # Add item to request
    call_tool(processor, "add_item_to_rfq_request", {
        "request_uuid": target_request_uuid,
        "item": {
            "item_uuid": SAMPLE["item_uuid_2"],
            "item_name": "Flight ATL->ORD Economy",
            "qty": 1,
        },
    }, "requests", "add_item_to_rfq_request")

    # Remove the item we just added
    call_tool(processor, "remove_item_from_rfq_request", {
        "request_uuid": target_request_uuid,
        "item_uuid": SAMPLE["item_uuid_2"],
    }, "requests", "remove_item_from_rfq_request")

    # Assign/remove/reassign a provider item so the later quote workflow has quote items.
    call_tool(processor, "assign_provider_item_to_request_item", {
        "request_uuid": target_request_uuid,
        "item_uuid": SAMPLE["item_uuid"],
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
        "provider_corp_external_id": SAMPLE["provider_corp_external_id"],
        "qty": 2,
        "batch_no": SAMPLE["batch_no"],
    }, "requests", "assign_provider_item_to_request_item")

    # Remove provider item
    call_tool(processor, "remove_provider_item_from_request_item", {
        "request_uuid": target_request_uuid,
        "item_uuid": SAMPLE["item_uuid"],
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
    }, "requests", "remove_provider_item_from_request_item")

    call_tool(processor, "assign_provider_item_to_request_item", {
        "request_uuid": target_request_uuid,
        "item_uuid": SAMPLE["item_uuid"],
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
        "provider_corp_external_id": SAMPLE["provider_corp_external_id"],
        "qty": 2,
        "batch_no": SAMPLE["batch_no"],
    }, "requests", "assign_provider_item_to_request_item (for quote workflow)")


def run_quotes(processor: MCPHospiRFQProcessor) -> None:
    """Quote management tools (5)."""
    request_uuid = RUN_STATE.get("request_uuid", SAMPLE["request_uuid"])

    # Convenience: confirm request and create quotes
    confirm_result, _ = call_tool(processor, "confirm_request_and_create_quotes", {
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

    call_tool(processor, "get_quote", {
        "quote_uuid": quote_uuid,
        "request_uuid": request_uuid,
    }, "quotes", "get_quote")

    call_tool(processor, "search_quotes", {
        "request_uuid": request_uuid,
        "limit": 10,
        "page_number": 1,
    }, "quotes", "search_quotes")

    call_tool(processor, "update_quote", {
        "request_uuid": request_uuid,
        "quote_uuid": quote_uuid,
        "notes": "Updated via integration test",
        "shipping_method": "ticket_delivery",
        "shipping_amount": 25.0,
    }, "quotes", "update_quote")

    if "quote_item_uuid" not in RUN_STATE:
        quote_item = processor._add_quote_item(
            quote_uuid=quote_uuid,
            request_uuid=request_uuid,
            provider_item_uuid=SAMPLE["provider_item_uuid"],
            item_uuid=SAMPLE["item_uuid"],
            qty=2,
            pax_breakdown={"adult": 2},
            segment_uuid=SAMPLE["segment_uuid"],
            batch_no=SAMPLE["batch_no"],
        )
        if isinstance(quote_item, dict):
            quote_item_uuid = (
                quote_item.get("quote_item_uuid")
                or quote_item.get("quoteItemUuid")
                or (quote_item.get("quote_item") or {}).get("quote_item_uuid")
                or (quote_item.get("quoteItem") or {}).get("quoteItemUuid")
            )
        if quote_item_uuid:
            RUN_STATE["quote_item_uuid"] = quote_item_uuid

    call_tool(processor, "update_quote_item", {
        "quote_uuid": quote_uuid,
        "quote_item_uuid": quote_item_uuid,
        "request_uuid": request_uuid,
        "discount_amount": 50.0,
        "notes": "Integration test discount",
    }, "quotes", "update_quote_item")


def run_pricing(processor: MCPHospiRFQProcessor) -> None:
    """Pricing tools (3)."""
    call_tool(processor, "get_item_price_tiers", {
        "email": SAMPLE["email"],
        "quote_items": [
            {
                "item_uuid": SAMPLE["item_uuid"],
                "provider_item_uuid": SAMPLE["provider_item_uuid"],
                "qty": 2,
            }
        ],
    }, "pricing", "get_item_price_tiers")

    call_tool(processor, "get_discount_prompts", {
        "email": SAMPLE["email"],
        "quote_items": [
            {
                "item_uuid": SAMPLE["item_uuid"],
                "provider_item_uuid": SAMPLE["provider_item_uuid"],
            }
        ],
    }, "pricing", "get_discount_prompts")

    call_tool(processor, "calculate_quote_pricing", {
        "request_uuid": SAMPLE["request_uuid"],
        "email": SAMPLE["email"],
    }, "pricing", "calculate_quote_pricing")


def _create_confirmed_quote_for_installments(
    processor: MCPHospiRFQProcessor,
    label: str,
) -> Optional[str]:
    """Create and confirm a fresh quote used only as installment test setup."""
    request_uuid = RUN_STATE.get("request_uuid")
    if not request_uuid:
        return None

    quote = processor._create_quote(
        request_uuid=request_uuid,
        provider_corp_external_id=SAMPLE["provider_corp_external_id"],
        sales_rep_email=SETTING["sales_rep_emails"].get(SAMPLE["provider_corp_external_id"]),
        segment_uuid=SAMPLE["segment_uuid"],
        batch_no=SAMPLE["batch_no"],
        service_start_at=SAMPLE["service_start_at"],
        service_end_at=SAMPLE["service_end_at"],
        notes=f"Setup quote for {label}",
    )
    if not isinstance(quote, dict) or quote.get("error"):
        RUN_STATE[f"{label}_setup_error"] = quote
        return None

    quote_uuid = quote.get("quote_uuid")
    priced = processor.update_quote(
        request_uuid=request_uuid,
        quote_uuid=quote_uuid,
        shipping_method="ticket_delivery",
        shipping_amount=300.0,
        notes=f"Priced setup quote for {label}",
    )
    if not isinstance(priced, dict) or priced.get("error"):
        RUN_STATE[f"{label}_setup_error"] = priced
        return None

    confirmed = processor.update_quote(
        request_uuid=request_uuid,
        quote_uuid=quote_uuid,
        status="confirmed",
        notes=f"Confirmed setup quote for {label}",
    )
    if not isinstance(confirmed, dict) or confirmed.get("error"):
        RUN_STATE[f"{label}_setup_error"] = confirmed
        return None

    return quote_uuid


def run_installments(processor: MCPHospiRFQProcessor) -> None:
    """Installment tools (5)."""
    request_uuid = RUN_STATE.get("request_uuid", SAMPLE["request_uuid"])
    quote_uuid = RUN_STATE.get("quote_uuid", SAMPLE["quote_uuid"])

    # Convenience: confirm quote and create installments
    call_tool(processor, "confirm_quote_and_create_installments", {
        "request_uuid": request_uuid,
        "quote_uuid": quote_uuid,
        "create_single_installment": True,
        "payment_method": "bank_transfer",
    }, "installments", "confirm_quote_and_create_installments")

    # Get installments — extract a real installment_uuid for subsequent calls
    inst_result, _ = call_tool(processor, "get_installments", {
        "quote_uuid": quote_uuid,
        "limit": 10,
        "page_number": 1,
    }, "installments", "get_installments")

    real_installment_uuid = None
    if inst_result and isinstance(inst_result, dict):
        inst_list = inst_result.get("installment_list", [])
        if inst_list:
            real_installment_uuid = inst_list[0].get("installment_uuid")

    # Create a single installment (note: MCP tool name → private method _create_installment)
    single_quote_uuid = _create_confirmed_quote_for_installments(
        processor, "create_installment"
    )
    multi_quote_uuid = _create_confirmed_quote_for_installments(
        processor, "create_installments"
    )

    call_tool(processor, "_create_installment", {
        "quote_uuid": single_quote_uuid or quote_uuid,
        "request_uuid": request_uuid,
        "installment_amount": 100.0,
        "payment_method": "credit_card",
    }, "installments", "create_installment")

    # Create multiple installments (note: MCP tool name → private method _create_installments)
    call_tool(processor, "_create_installments", {
        "quote_uuid": multi_quote_uuid or quote_uuid,
        "request_uuid": request_uuid,
        "interval_num": 3,
        "total_pay_period": 6,
        "payment_method": "bank_transfer",
    }, "installments", "create_installments")

    # Update an installment — use the real UUID if we got one
    update_uuid = real_installment_uuid or "00000000000000000000"
    call_tool(processor, "update_installment", {
        "quote_uuid": quote_uuid,
        "installment_uuid": update_uuid,
        "status": "paid",
    }, "installments", f"update_installment (uuid={update_uuid[:12]}...)")


def run_files(processor: MCPHospiRFQProcessor) -> None:
    """File tools (2)."""
    call_tool(processor, "upload_rfq_file", {
        "request_uuid": SAMPLE["request_uuid"],
        "file_name": "integration_test_spec.pdf",
        "email": SAMPLE["email"],
    }, "files", "upload_rfq_file")

    call_tool(processor, "get_rfq_files", {
        "request_uuid": SAMPLE["request_uuid"],
        "limit": 10,
        "page_number": 1,
    }, "files", "get_rfq_files")


def run_segments(processor: MCPHospiRFQProcessor) -> None:
    """Segment tools (1)."""
    call_tool(processor, "get_segment_contacts", {
        "email": SAMPLE["email"],
        "limit": 10,
        "page_number": 1,
    }, "segments", "get_segment_contacts")


def run_availability(processor: MCPHospiRFQProcessor) -> None:
    """Availability hold tools (5)."""
    # Check availability
    call_tool(processor, "check_availability", {
        "partition_key": PARTITION_KEY,
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
        "service_start_at": SAMPLE["service_start_at"],
        "service_end_at": SAMPLE["service_end_at"],
        "batch_no": SAMPLE["batch_no"],
        "qty": 2,
    }, "availability", "check_availability")

    # Acquire hold
    result, err = call_tool(processor, "acquire_availability_hold", {
        "partition_key": PARTITION_KEY,
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
        "service_start_at": SAMPLE["service_start_at"],
        "service_end_at": SAMPLE["service_end_at"],
        "qty": 2,
        "batch_no": SAMPLE["batch_no"],
        "pax_breakdown": {"adult": 2},
    }, "availability", "acquire_availability_hold")

    # Extract hold token — humps.decamelize wraps result under "availability" key
    hold_token = None
    if result and isinstance(result, dict):
        avail = result.get("availability", result)
        hold_token = avail.get("hold_token") or avail.get("holdToken")

    if hold_token:
        # Confirm the hold
        call_tool(processor, "confirm_availability_hold", {
            "partition_key": PARTITION_KEY,
            "hold_token": hold_token,
            "provider_item_uuid": SAMPLE["provider_item_uuid"],
            "batch_no": SAMPLE["batch_no"],
        }, "availability", "confirm_availability_hold")

        # Acquire another hold to test release
        result2, _ = call_tool(processor, "acquire_availability_hold", {
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
            call_tool(processor, "release_availability_hold", {
                "partition_key": PARTITION_KEY,
                "hold_token": hold_token2,
                "provider_item_uuid": SAMPLE["provider_item_uuid"],
                "batch_no": SAMPLE["batch_no"],
            }, "availability", "release_availability_hold")

        # Expire the confirmed hold (idempotent — may no-op)
        result3, _ = call_tool(processor, "acquire_availability_hold", {
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
            call_tool(processor, "expire_availability_hold", {
                "partition_key": PARTITION_KEY,
                "hold_token": hold_token3,
                "provider_item_uuid": SAMPLE["provider_item_uuid"],
                "batch_no": SAMPLE["batch_no"],
            }, "availability", "expire_availability_hold")
    else:
        print("  WARNING: No hold_token in acquire result - skipping lifecycle calls")


def run_bundles(processor: MCPHospiRFQProcessor) -> None:
    """Bundle tools (3)."""
    call_tool(processor, "search_bundles", {
        "partition_key": PARTITION_KEY,
        "bundle_type": "itinerary",
    }, "bundles", "search_bundles (itinerary type)")

    call_tool(processor, "get_bundle", {
        "partition_key": PARTITION_KEY,
        "bundle_uuid": SAMPLE["bundle_uuid"],
    }, "bundles", "get_bundle (FLT-ITIN-001)")

    call_tool(processor, "search_bundle_components", {
        "partition_key": PARTITION_KEY,
        "bundle_uuid": SAMPLE["bundle_uuid"],
    }, "bundles", "search_bundle_components")


def run_cancellation(processor: MCPHospiRFQProcessor) -> None:
    """Cancellation policy tools (2)."""
    call_tool(processor, "get_cancellation_policy", {
        "partition_key": PARTITION_KEY,
        "policy_uuid": SAMPLE["policy_uuid"],
    }, "cancellation", "get_cancellation_policy (Business Fare)")

    call_tool(processor, "search_cancellation_policies", {
        "partition_key": PARTITION_KEY,
        "provider_item_uuid": SAMPLE["provider_item_uuid"],
    }, "cancellation", "search_cancellation_policies")


def run_catalog(processor: MCPHospiRFQProcessor) -> None:
    """Catalog inquiry tool (1)."""
    call_tool(processor, "inquire_catalog", {
        "partition_key": PARTITION_KEY,
        "query_text": SAMPLE["catalog_query"],
        "namespace": SAMPLE["catalog_namespace"],
        "limit": 5,
    }, "catalog", "inquire_catalog")


# Group → runner mapping (preserves logical execution order)
GROUP_RUNNERS = {
    "catalog_discovery": run_catalog_discovery,
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
        description="E2E integration tests for MCP HospiRFQ Processor via silvaengine_gateway"
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
        "--export", type=str, default="docs/live_integration_results.md",
        help="Markdown path for per-function output. Default: docs/live_integration_results.md",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list:
        print("Available tool groups:")
        for g in GROUP_ORDER:
            runner = GROUP_RUNNERS.get(g)
            count = sum(1 for line in runner.__doc__.split("\n") if line.strip().startswith("call_tool") or "tools" in line.lower()) if runner else 0
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
    print(f"  MCP HospiRFQ Processor - E2E Integration Tests")
    print(f"{'=' * 80}")
    print(f"  Gateway:     {GATEWAY_BASE_URL}")
    print(f"  Endpoint:    {ENDPOINT_ID}")
    print(f"  Partition:   {PART_ID}")
    print(f"  GraphQL URL: {GRAPHQL_URL}")
    print(f"  Groups:      {', '.join(run_groups)}")
    print(f"{'=' * 80}\n")

    # ── Authenticate ─────────────────────────────────────────────────────────
    try:
        token = get_gateway_token()
    except Exception as exc:
        print(f"FATAL: Cannot authenticate with gateway: {exc}")
        print(f"Is the gateway running at {GATEWAY_BASE_URL}?")
        sys.exit(1)

    # ── Create processor ─────────────────────────────────────────────────────
    try:
        print(f"\nInitializing MCPHospiRFQProcessor ...")
        processor = MCPHospiRFQProcessor(logger, **SETTING)
        processor.endpoint_id = ENDPOINT_ID
        processor.part_id = PART_ID
        print(f"Processor initialized. endpoint_id={processor.endpoint_id}, part_id={processor.part_id}")
    except Exception as exc:
        print(f"FATAL: Cannot initialize processor: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # ── Patch GraphQLClient for gateway Bearer auth ──────────────────────────
    patch_graphql_client(processor, token)
    print(f"GraphQLClient patched for gateway Bearer auth\n")

    # ── Run tool groups ──────────────────────────────────────────────────────
    for group in run_groups:
        runner = GROUP_RUNNERS.get(group)
        if not runner:
            print(f"WARNING: No runner for group '{group}' - skipping")
            continue

        print(f"\n{'=' * 80}")
        print(f"  GROUP: {group.upper()}")
        print(f"{'=' * 80}")

        try:
            runner(processor)
        except Exception as exc:
            print(f"  FAIL GROUP ERROR: {exc}")
            import traceback
            traceback.print_exc()

    # ── Summary ──────────────────────────────────────────────────────────────
    print_summary()
    if args.export:
        export_results(args.export, run_groups)


if __name__ == "__main__":
    main()
