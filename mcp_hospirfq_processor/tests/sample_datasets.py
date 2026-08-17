# -*- coding: utf-8 -*-
"""Shared sample-data registry for integration test runners.

Both ``run_integration.py`` (direct in-process transport) and
``run_http_integration.py`` (MCP HTTP transport) import :data:`DATASETS`
and call :func:`select_dataset` to pick the correct fixture UUIDs for the
active backend + dataset combination.

Supported dataset keys
----------------------
``flight-pg``
    PostgreSQL backend with the original ``flight_products.json`` fixtures
    (UUID-style IDs, Delta NRT->CDG First, namespace ``FLIGHTS``).
``flight-ddb``
    DynamoDB backend with ``load_sample_data.py`` fixtures (numeric IDs,
    Qantas CDG->SFO First, namespace ``FLIGHTS``).
``flight-sample-pg``
    PostgreSQL backend with the sample dataset (Chinese B2B airline seats,
    TPE->HKG economy, namespace ``FLIGHTS``).
``dds-pg``
    PostgreSQL backend with the DDS B2B multi-vendor distributor dataset
    (1,190 products, 21 vendors, unit pricing, namespace ``DDS``).

The active dataset is selected via the ``DATASET`` env var or the
``--dataset`` CLI argument on each runner.
"""
from __future__ import annotations, print_function

__author__ = "Idea Bosque"

import os
from typing import Any, Dict


# =============================================================================
# Dataset definitions
# =============================================================================

DATASETS: Dict[str, Dict[str, Any]] = {

    # -------------------------------------------------------------------------
    # flight-pg: PostgreSQL + flight_products.json fixtures (UUID-style)
    # -------------------------------------------------------------------------
    "flight-pg": {
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
        "batch_no": "DL4000-20260905",
        "service_start_at": "2026-09-05T21:15:00Z",
        "service_end_at": "2026-09-06T08:30:40.740402Z",
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
        # Alternate batch for installment setup (avoids capacity contention)
        "alt_provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
        "alt_item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "alt_provider_corp_external_id": "AIRLINE-DL",
        "alt_batch_no": "DL4822-20260918",
        "alt_service_start_at": "2026-09-18T14:45:00Z",
        "alt_service_end_at": "2026-09-18T23:28:08.831283Z",
        # Metadata
        "backend": "postgresql",
        "dataset_name": "flight",
        "has_bundles": True,
        "skip_catalog_ref_override": False,
        "use_alt_for_second_installment": True,
    },

    # -------------------------------------------------------------------------
    # flight-ddb: DynamoDB + load_sample_data.py fixtures (numeric IDs)
    # -------------------------------------------------------------------------
    "flight-ddb": {
        "item_uuid": "52065619693805781120",                        # Flight CDG->SFO First
        "item_uuid_2": "06041993713794695296",                      # Flight ATL->ORD Premium Economy
        "item_uuid_in_request": "06041993713794695296",
        "item_name": "Flight CDG->SFO First",
        "item_type": "flight",
        "provider_item_uuid": "94764066649319424128",               # QF-CDG-SFO-FIR
        "provider_item_uuid_2": "39876487618607726720",             # AF-ATL-ORD-PRE
        "provider_item_uuid_in_request": "39876487618607726720",
        "provider_corp_external_id": "AIRLINE-QF",
        "provider_corp_external_id_2": "AIRLINE-AF",
        "batch_no": "QF1351-20260709",
        "service_start_at": "2026-07-09T21:45:00Z",
        "service_end_at": "2026-07-10T03:11:29.751482Z",
        "request_uuid": "03075416831792529536",
        "email": "jessicacooper@example.com",
        "quote_uuid": "60187438571235328128",
        "quote_uuid_with_items": "60187438571235328128",
        "request_uuid_for_quote_with_items": "03075416831792529536",
        "quote_item_uuid": "86175401676691751040",
        "segment_uuid": "61268299727527493760",
        "bundle_uuid": "21965879857802920064",                      # Flight Itinerary HKG->SFO + SFO->SYD + ATL->LAX
        "bundle_uuid_2": "49956565412585947264",
        "policy_uuid": "45519135682445983872",                      # QF batch policy
        "catalog_query": "Qantas CDG SFO First class flight",
        "catalog_namespace": "FLIGHTS",
        "alt_provider_item_uuid": "94764066649319424128",
        "alt_item_uuid": "52065619693805781120",
        "alt_provider_corp_external_id": "AIRLINE-QF",
        "alt_batch_no": "QF5796-20260921",
        "alt_service_start_at": "2026-09-21T19:45:00Z",
        "alt_service_end_at": "2026-09-21T22:44:57.764776Z",
        "backend": "dynamodb",
        "dataset_name": "flight",
        "has_bundles": True,
        "skip_catalog_ref_override": True,
        "use_alt_for_second_installment": True,
    },

    # -------------------------------------------------------------------------
    # flight-sample-pg: PostgreSQL + sample dataset (Chinese B2B airline seats)
    # -------------------------------------------------------------------------
    "flight-sample-pg": {
        "item_uuid": "ac8ec8c5-e8d2-4bd0-ad9a-2c9ba675e4c4",       # TPE->HKG economy
        "item_uuid_2": "9aad94d1-39aa-4f3e-9a44-3b2a537b70fe",      # TPE->CAN economy
        "item_uuid_in_request": "ac8ec8c5-e8d2-4bd0-ad9a-2c9ba675e4c4",
        "item_name": "Flight TPE->HKG Economy",
        "item_type": "flight",
        "provider_item_uuid": "26c94a98-a915-46e2-b419-aac7acae18b0",  # CX-TPE-HKG-ECO
        "provider_item_uuid_2": "557a25fd-ac83-4ebd-b92b-4e4d9ce5fa01",  # GJ-TPE-HKG-ECO
        "provider_item_uuid_in_request": "26c94a98-a915-46e2-b419-aac7acae18b0",
        "provider_corp_external_id": "AIRLINE-CX",
        "provider_corp_external_id_2": "AIRLINE-GJ",
        "batch_no": "CX443-20260905",
        "service_start_at": "2026-09-05T16:10:00",
        "service_end_at": "2026-09-12T11:10:00",
        "request_uuid": "d0ead0ab-6516-477b-9688-8a16cdd3cf8b",
        "email": "michaela03@example.net",
        "quote_uuid": "9e8378fa-f6b3-4353-bf9a-af2ff6036ff8",
        "quote_uuid_with_items": "9e8378fa-f6b3-4353-bf9a-af2ff6036ff8",
        "request_uuid_for_quote_with_items": "d0ead0ab-6516-477b-9688-8a16cdd3cf8b",
        "quote_item_uuid": "fa63d2f0-8c7b-4602-a4fc-5a0c4405bf40",
        "segment_uuid": "323dec2b-1f03-4d42-a5ef-73ef9e17c4e6",
        "bundle_uuid": "53283de6-215f-4f04-bd28-43e852439b5d",     # CN-ITIN-003
        "bundle_uuid_2": "c4480ddf-ae71-4a26-9c81-15acc9a10ef8",   # CN-ITIN-001
        "policy_uuid": "7cdae692-f084-445f-a5c1-36e4f9030f8e",     # economy group tour cancellation
        "catalog_query": "flight TPE HKG economy",
        "catalog_namespace": "FLIGHTS",
        "alt_provider_item_uuid": "3b957449-244d-4573-bbf3-357006b98799",
        "alt_item_uuid": "e8fcd210-68d3-463f-a9ae-7a4dddf0276f",
        "alt_provider_corp_external_id": "AIRLINE-CA",
        "alt_batch_no": "CA418-20260714",
        "alt_service_start_at": "2026-07-14T18:10:00",
        "alt_service_end_at": "2026-07-21T16:55:00",
        "backend": "postgresql",
        "dataset_name": "flight-sample",
        "has_bundles": True,
        "skip_catalog_ref_override": True,
        "use_alt_for_second_installment": True,
    },

    # -------------------------------------------------------------------------
    # dds-pg: PostgreSQL + DDS B2B multi-vendor distributor dataset
    # -------------------------------------------------------------------------
    "dds-pg": {
        "item_uuid": "85292857-91f0-45d2-911e-9c897d926a37",       # The Minimal Snowboard
        "item_uuid_2": "f25236ff-ae10-41ad-912a-96124744700c",      # M18 FUEL HOLE HAWG
        "item_uuid_in_request": "85292857-91f0-45d2-911e-9c897d926a37",
        "item_name": "The Minimal Snowboard",
        "item_type": "product",
        "provider_item_uuid": "33a65486-ff1c-41de-971e-8cf37b0175a4",  # VENDOR-neprodai
        "provider_item_uuid_2": "dab8ce39-e5ce-4e48-8da9-96aea8c2c3d2",  # VENDOR-milwaukee-tool
        "provider_item_uuid_in_request": "33a65486-ff1c-41de-971e-8cf37b0175a4",
        "provider_corp_external_id": "VENDOR-neprodai",
        "provider_corp_external_id_2": "VENDOR-milwaukee-tool",
        "batch_no": "the-minimal-snowboard",
        "service_start_at": "2026-08-12T20:13:05.091618Z",
        "service_end_at": "2027-08-12T20:13:05.091618Z",
        "request_uuid": "293327d9-40d3-458a-9d33-6945ad9343e1",
        "email": "marychambers@example.com",
        "quote_uuid": "27c0094f-e953-43ab-8cbb-93bca08a9c3e",
        "quote_uuid_with_items": "27c0094f-e953-43ab-8cbb-93bca08a9c3e",
        "request_uuid_for_quote_with_items": "293327d9-40d3-458a-9d33-6945ad9343e1",
        "quote_item_uuid": "",
        "segment_uuid": "1355cbb1-5e63-4da7-8a3e-5af5e8c59e1a",       # Long and Sons Tier
        "bundle_uuid": "",                                             # DDS has 0 bundles
        "bundle_uuid_2": "",
        "policy_uuid": "1a4c757d-eddc-4faa-afce-dd7bd7d42aa6",        # Non-Returnable
        "catalog_query": "minimal snowboard",
        "catalog_namespace": "DDS",
        "alt_provider_item_uuid": "dab8ce39-e5ce-4e48-8da9-96aea8c2c3d2",
        "alt_item_uuid": "f25236ff-ae10-41ad-912a-96124744700c",
        "alt_provider_corp_external_id": "VENDOR-milwaukee-tool",
        "alt_batch_no": "18004",
        "alt_service_start_at": "2026-08-12T20:13:03.223382Z",
        "alt_service_end_at": "2027-08-12T20:13:03.223382Z",
        "backend": "postgresql",
        "dataset_name": "dds",
        "has_bundles": False,
        "skip_catalog_ref_override": True,
        "use_alt_for_second_installment": True,
    },
}


# Default dataset key when neither the env var nor CLI argument is provided.
DEFAULT_DATASET = "flight-pg"


def select_dataset(cli_override: str = None) -> Dict[str, Any]:
    """Return the active SAMPLE dict for the selected dataset.

    Resolution order:
    1. ``cli_override`` (from ``--dataset`` CLI argument)
    2. ``DATASET`` env var
    3. :data:`DEFAULT_DATASET`
    """
    key = (cli_override or os.getenv("DATASET") or DEFAULT_DATASET).strip().lower()
    if key not in DATASETS:
        raise ValueError(
            f"Unknown dataset '{key}'. Available: {sorted(DATASETS.keys())}"
        )
    return dict(DATASETS[key])


def dataset_key(cli_override: str = None) -> str:
    """Return the resolved dataset key string (without copying the dict)."""
    return (cli_override or os.getenv("DATASET") or DEFAULT_DATASET).strip().lower()


__all__ = ["DATASETS", "DEFAULT_DATASET", "select_dataset", "dataset_key"]