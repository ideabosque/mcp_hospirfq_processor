# -*- coding: utf-8 -*-
"""Shared helpers for the direct in-process and MCP HTTP integration runners.

Both ``run_integration.py`` and ``run_http_integration.py`` import from this
module to avoid duplicating:

* `.env` loading and ``sys.path`` setup
* Configuration variables (``GATEWAY_BASE_URL``, ``ENDPOINT_ID``, …)
* Dataset selection (delegates to ``sample_datasets.py``)
* Result-tracking globals and error-detection helpers
* ``print_summary`` and the per-function export renderer
* Argument-builder functions for each tool group (the ``call_tool`` sequence)

Each runner owns only its transport-specific ``call_tool``, auth step,
export header, and ``main`` entry point.
"""
from __future__ import annotations, print_function

__author__ = "Idea Bosque"

import json
import logging
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv

# =============================================================================
# .env loading + sys.path setup (called once by each runner)
# =============================================================================

def load_test_env() -> Path:
    """Load ``tests/.env`` and return the tests directory path."""
    _env_path = Path(__file__).parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path, override=True)
        print(f"Loaded .env from: {_env_path}")
    else:
        print(f"WARNING: .env not found at {_env_path} - using defaults / env vars")
    return _env_path


def setup_sys_path() -> str:
    """Insert silvaengine monorepo roots onto ``sys.path``.

    Returns ``base_dir``.  Each runner may add extra paths (e.g.
    ``rfq_engine`` or ``mcp_http_client``) after calling this.
    """
    base_dir = os.getenv("base_dir", "")
    if not base_dir:
        base_dir = str(Path(__file__).resolve().parent.parent.parent.parent)
    print(f"base_dir: {base_dir}")
    for sub in ("", "silvaengine_utility", "silvaengine_constants",
                "silvaengine_dynamodb_base", "mcp_hospirfq_processor"):
        p = os.path.join(base_dir, sub) if sub else base_dir
        if p not in sys.path:
            sys.path.insert(0, p)
    return base_dir


def setup_logging(name: str) -> logging.Logger:
    """Configure root logging and return a named logger."""
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(name)


# =============================================================================
# Configuration variables (read from env after load_test_env)
# =============================================================================

def load_config() -> Dict[str, Any]:
    """Read gateway/tenant config from environment variables."""
    gateway_base_url = os.getenv("GATEWAY_BASE_URL", "http://localhost:8765")
    endpoint_id = os.getenv("endpoint_id", "gpt")
    part_id = os.getenv("part_id", "nestaging")
    token_username = os.getenv("TOKEN_USERNAME", os.getenv("ADMIN_USERNAME", "admin"))
    token_password = os.getenv("TOKEN_PASSWORD", os.getenv("ADMIN_PASSWORD", "admin123"))
    gateway_token = os.getenv("GATEWAY_TOKEN", os.getenv("ADMIN_STATIC_TOKEN", ""))
    partition_key = f"{endpoint_id}#{part_id}"
    return {
        "GATEWAY_BASE_URL": gateway_base_url,
        "ENDPOINT_ID": endpoint_id,
        "PART_ID": part_id,
        "TOKEN_USERNAME": token_username,
        "TOKEN_PASSWORD": token_password,
        "GATEWAY_TOKEN": gateway_token,
        "PARTITION_KEY": partition_key,
    }


# =============================================================================
# Dataset selection (delegates to sample_datasets.py)
# =============================================================================

def load_dataset() -> Tuple[str, Dict[str, Any], Dict[str, bool]]:
    """Return ``(dataset_key, sample_dict, flags_dict)``."""
    from mcp_hospirfq_processor.tests.sample_datasets import (
        select_dataset, dataset_key,
    )
    key = dataset_key()
    sample = select_dataset()
    flags = {
        "skip_catalog_ref_override": sample.get("skip_catalog_ref_override", False),
        "has_bundles": sample.get("has_bundles", True),
        "use_alt_for_second_installment": sample.get("use_alt_for_second_installment", False),
    }
    return key, sample, flags


# =============================================================================
# Result-tracking globals + helpers
# =============================================================================

_passed: int = 0
_failed: int = 0
_skipped: int = 0
_results: List[Dict[str, Any]] = []


def reset_results() -> None:
    """Reset the global result trackers (call before each run)."""
    global _passed, _failed, _skipped, _results
    _passed = 0
    _failed = 0
    _skipped = 0
    _results = []


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


def _extract_error_msg(result: Any) -> str:
    """Extract a human-readable error message from an error result dict."""
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
        return error_val.get("message", str(error_val))
    return str(error_val)


def make_result_entry(
    display: str,
    method: str,
    group: str,
    arguments: Dict[str, Any],
    status: str,
    elapsed_ms: float,
    result: Any = None,
    error: str = None,
    graphql_calls: List[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a result-entry dict for the export."""
    entry: Dict[str, Any] = {
        "tool": display,
        "method": method,
        "group": group,
        "arguments": arguments,
        "status": status,
        "elapsed_ms": elapsed_ms,
    }
    if error is not None:
        entry["error"] = error
    if result is not None:
        entry["result"] = result
    if graphql_calls is not None:
        entry["graphql_calls"] = graphql_calls
    return entry


# =============================================================================
# print_summary
# =============================================================================

def print_summary(title: str = "INTEGRATION TEST SUMMARY") -> None:
    """Print final summary of all tool calls."""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
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


# =============================================================================
# Export — per-function block renderer (shared by both runners)
# =============================================================================

def render_function_blocks(lines: List[str]) -> None:
    """Append per-function Argument/Error/Output blocks to ``lines``."""
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

        # GraphQL queries (in-process runner only)
        graphql_calls = result.get("graphql_calls", [])
        for gi, gc in enumerate(graphql_calls, start=1):
            lines.extend([
                f"GraphQL Query {gi} (`{gc.get('function_name', '?')}` -> "
                f"`{gc.get('operation_name', '?')}`, type: `{gc.get('operation_type', '?')}`):",
                "",
            ])
            if gc.get("query"):
                lines.extend(["```graphql", str(gc["query"]), "```", ""])
            if gc.get("variables"):
                lines.extend([
                    "Variables:",
                    "",
                    "```json",
                    _safe_json(gc["variables"], max_chars=4000),
                    "```",
                    "",
                ])

        if "error" in result:
            lines.extend(["Error:", "", "```text", str(result["error"]), "```", ""])

        if "result" in result:
            lines.extend(["Output:", "", "```json", _safe_json(result["result"]), "```", ""])


def write_export(path: str, header_lines: List[str], run_groups: List[str]) -> None:
    """Write the full Markdown export to ``path``."""
    from datetime import datetime, timezone
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = list(header_lines)
    render_function_blocks(lines)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Results exported to: {output_path}")


# =============================================================================
# Tool-group argument builders
# =============================================================================
# Each function returns a list of (tool_name, arguments, group, label) tuples.
# The runner iterates the list and calls its transport-specific call_tool.
# This keeps the argument dicts DRY across both runners.

PARTITION_KEY = ""  # set by each runner from load_config()


def _set_partition_key(pk: str) -> None:
    global PARTITION_KEY
    PARTITION_KEY = pk


def build_items(sample: Dict[str, Any]) -> List[Tuple[str, Dict, str, str]]:
    return [
        ("search_items", {
            "item_type": sample["item_type"],
            "limit": 10,
            "page_number": 1,
        }, "items", "search_items (flight type)"),
        ("get_item", {
            "item_uuid": sample["item_uuid"],
        }, "items", f"get_item ({sample['item_name']})"),
        ("get_provider_items", {
            "item_uuid": sample["item_uuid"],
        }, "items", "get_provider_items (with batches)"),
    ]


def build_requests(sample: Dict[str, Any]) -> List[Tuple[str, Dict, str, str]]:
    return [
        ("submit_rfq_request", {
            "email": sample["email"],
            "request_title": f"Integration test: {sample['item_name']}",
            "request_description": "E2E test request via silvaengine_gateway",
            "items": [{
                "item_uuid": sample["item_uuid"],
                "item_name": sample["item_name"],
                "qty": 2,
                "pax_breakdown": {"adult": 2},
            }],
            "notes": "Created by run_integration.py",
            "expired_at": "2026-12-31T23:59:59Z",
        }, "requests", "submit_rfq_request"),
        ("get_rfq_request", {
            "request_uuid": sample["request_uuid"],
        }, "requests", "get_rfq_request (seeded)"),
        ("search_rfq_requests", {
            "limit": 5,
            "page_number": 1,
        }, "requests", "search_rfq_requests"),
    ]


def build_requests_mutable(sample: Dict[str, Any], target_request_uuid: str) -> List[Tuple[str, Dict, str, str]]:
    """The mutable part of the request lifecycle (update/add/remove/assign)."""
    return [
        ("update_rfq_request", {
            "request_uuid": target_request_uuid,
            "request_title": f"Integration test: {sample['item_name']} (updated)",
            "notes": "Updated via run_integration.py",
        }, "requests", "update_rfq_request"),
        ("add_item_to_rfq_request", {
            "request_uuid": target_request_uuid,
            "item": {
                "item_uuid": sample["item_uuid_2"],
                "item_name": sample.get("item_name_2", "Second item"),
                "qty": 1,
            },
        }, "requests", "add_item_to_rfq_request"),
        ("remove_item_from_rfq_request", {
            "request_uuid": target_request_uuid,
            "item_uuid": sample["item_uuid_2"],
        }, "requests", "remove_item_from_rfq_request"),
        ("assign_provider_item_to_request_item", {
            "request_uuid": target_request_uuid,
            "item_uuid": sample["item_uuid"],
            "provider_item_uuid": sample["provider_item_uuid"],
            "provider_corp_external_id": sample["provider_corp_external_id"],
            "qty": 2,
            "batch_no": sample["batch_no"],
        }, "requests", "assign_provider_item_to_request_item"),
        ("remove_provider_item_from_request_item", {
            "request_uuid": target_request_uuid,
            "item_uuid": sample["item_uuid"],
            "provider_item_uuid": sample["provider_item_uuid"],
        }, "requests", "remove_provider_item_from_request_item"),
        ("assign_provider_item_to_request_item", {
            "request_uuid": target_request_uuid,
            "item_uuid": sample["item_uuid"],
            "provider_item_uuid": sample["provider_item_uuid"],
            "provider_corp_external_id": sample["provider_corp_external_id"],
            "qty": 2,
            "batch_no": sample["batch_no"],
        }, "requests", "assign_provider_item_to_request_item (for quote workflow)"),
    ]


def build_quotes(sample: Dict[str, Any], request_uuid: str) -> List[Tuple[str, Dict, str, str]]:
    return [
        ("confirm_request_and_create_quotes", {
            "request_uuid": request_uuid,
            "provider_corp_external_ids": [sample["provider_corp_external_id"]],
            "segment_uuid": sample["segment_uuid"],
            "batch_no": sample["batch_no"],
            "service_start_at": sample["service_start_at"],
            "service_end_at": sample["service_end_at"],
        }, "quotes", "confirm_request_and_create_quotes"),
        ("get_quote", {
            "quote_uuid": sample["quote_uuid"],
            "request_uuid": request_uuid,
        }, "quotes", "get_quote"),
        ("search_quotes", {
            "request_uuid": request_uuid,
            "limit": 10,
            "page_number": 1,
        }, "quotes", "search_quotes"),
        ("update_quote", {
            "request_uuid": request_uuid,
            "quote_uuid": sample["quote_uuid"],
            "notes": "Updated via integration test",
            "shipping_method": "ticket_delivery",
            "shipping_amount": 25.0,
        }, "quotes", "update_quote"),
    ]


def build_pricing(sample: Dict[str, Any]) -> List[Tuple[str, Dict, str, str]]:
    return [
        ("get_item_price_tiers", {
            "email": sample["email"],
            "quote_items": [{
                "item_uuid": sample["item_uuid"],
                "provider_item_uuid": sample["provider_item_uuid"],
                "qty": 2,
            }],
        }, "pricing", "get_item_price_tiers"),
        ("get_discount_prompts", {
            "email": sample["email"],
            "quote_items": [{
                "item_uuid": sample["item_uuid"],
                "provider_item_uuid": sample["provider_item_uuid"],
            }],
        }, "pricing", "get_discount_prompts"),
        ("calculate_quote_pricing", {
            "request_uuid": sample["request_uuid"],
            "email": sample["email"],
        }, "pricing", "calculate_quote_pricing"),
    ]


def build_files(sample: Dict[str, Any]) -> List[Tuple[str, Dict, str, str]]:
    return [
        ("upload_rfq_file", {
            "request_uuid": sample["request_uuid"],
            "file_name": "integration_test_spec.pdf",
            "email": sample["email"],
        }, "files", "upload_rfq_file"),
        ("get_rfq_files", {
            "request_uuid": sample["request_uuid"],
            "limit": 10,
            "page_number": 1,
        }, "files", "get_rfq_files"),
    ]


def build_segments(sample: Dict[str, Any]) -> List[Tuple[str, Dict, str, str]]:
    return [
        ("get_segment_contacts", {
            "email": sample["email"],
            "limit": 10,
            "page_number": 1,
        }, "segments", "get_segment_contacts"),
    ]


def build_availability(sample: Dict[str, Any]) -> List[Tuple[str, Dict, str, str]]:
    # Use avail_* overrides when present (HTTP runner pattern), else primary
    pi_uuid = sample.get("avail_provider_item_uuid", sample["provider_item_uuid"])
    batch_no = sample.get("avail_batch_no", sample["batch_no"])
    ss = sample.get("avail_service_start_at", sample["service_start_at"])
    se = sample.get("avail_service_end_at", sample["service_end_at"])
    calls = [
        ("check_availability", {
            "partition_key": PARTITION_KEY,
            "provider_item_uuid": pi_uuid,
            "service_start_at": ss,
            "service_end_at": se,
            "batch_no": batch_no,
            "qty": 2,
        }, "availability", "check_availability"),
        ("acquire_availability_hold", {
            "partition_key": PARTITION_KEY,
            "provider_item_uuid": pi_uuid,
            "service_start_at": ss,
            "service_end_at": se,
            "qty": 2,
            "batch_no": batch_no,
            "pax_breakdown": {"adult": 2},
        }, "availability", "acquire_availability_hold"),
    ]
    # The confirm/release/expire sub-calls depend on the hold_token extracted
    # at runtime, so they stay in each runner's run_availability function.
    return calls


def build_bundles(sample: Dict[str, Any], has_bundles: bool) -> List[Tuple[str, Dict, str, str]]:
    calls = [
        ("search_bundles", {
            "partition_key": PARTITION_KEY,
            "bundle_type": "itinerary",
        }, "bundles", "search_bundles (itinerary type)"),
    ]
    if has_bundles and sample.get("bundle_uuid"):
        calls.append(("get_bundle", {
            "partition_key": PARTITION_KEY,
            "bundle_uuid": sample["bundle_uuid"],
        }, "bundles", f"get_bundle ({sample['bundle_uuid'][:12]}...)"))
        calls.append(("search_bundle_components", {
            "partition_key": PARTITION_KEY,
            "bundle_uuid": sample["bundle_uuid"],
        }, "bundles", "search_bundle_components"))
    return calls


def build_cancellation(sample: Dict[str, Any]) -> List[Tuple[str, Dict, str, str]]:
    pi_uuid = sample.get("avail_provider_item_uuid", sample["provider_item_uuid"])
    return [
        ("get_cancellation_policy", {
            "partition_key": PARTITION_KEY,
            "policy_uuid": sample["policy_uuid"],
        }, "cancellation", "get_cancellation_policy"),
        ("search_cancellation_policies", {
            "partition_key": PARTITION_KEY,
            "provider_item_uuid": pi_uuid,
        }, "cancellation", "search_cancellation_policies"),
    ]


def build_catalog(sample: Dict[str, Any]) -> List[Tuple[str, Dict, str, str]]:
    return [
        ("inquire_catalog", {
            "partition_key": PARTITION_KEY,
            "query_text": sample["catalog_query"],
            "namespace": sample["catalog_namespace"],
            "limit": 5,
        }, "catalog", "inquire_catalog"),
    ]


# =============================================================================
# GROUP_ORDER (shared definition; runners may extend)
# =============================================================================

GROUP_ORDER: List[str] = [
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


__all__ = [
    "load_test_env", "setup_sys_path", "setup_logging", "load_config",
    "load_dataset", "reset_results", "print_summary", "render_function_blocks",
    "write_export", "make_result_entry", "_safe_json",
    "_result_has_error_payload", "_is_expected_live_noop", "_extract_error_msg",
    "_set_partition_key", "PARTITION_KEY",
    "build_items", "build_requests", "build_requests_mutable",
    "build_quotes", "build_pricing", "build_files", "build_segments",
    "build_availability", "build_bundles", "build_cancellation", "build_catalog",
    "GROUP_ORDER", "GROUPS",
    "_passed", "_failed", "_skipped", "_results",
]