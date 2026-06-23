# MCP HospiRFQ Processor — Live Integration Results (PostgreSQL Backend)

- Generated at: `2026-06-23T20:33:17.066346+00:00`
- Gateway: `http://localhost:8765`
- Endpoint: `gpt`
- Partition: `nestaging`
- GraphQL URL: `http://localhost:8765/gpt/rfq_graphql`
- Dependency order: `catalog_discovery, items, requests, quotes, pricing, installments, files, segments, availability, bundles, cancellation, catalog`
- Passed: `42`
- Error responses: `0`
- Failed: `0`
- Total calls: `42`
- SOP reference: `docs/integration_scenarios_sop_postgresql.md` version `0.1.0`, approved by user on `2026-06-23`
- Persistence backend: `PostgreSQL` (`DB_BACKEND=postgresql`) via `silvaengine_gateway` route `/{endpoint_id}/rfq_graphql`
- Alembic schema revision: `assumed at head` (not directly observed from this shell; validated indirectly by successful PostgreSQL create/read-back across items, requests, quotes, quote items, installments, files, and availability holds)
- Availability batch selection: highest-capacity matching batch `DL4822-20260918` (runner now prefers max `availabilityQty`; the 7-seat `DL4000-20260905` was exhausted by prior-run confirmed holds)
- Final certification status: `Integration Certified`

## Executive Summary

End-to-end live integration testing was executed against the local `silvaengine_gateway` route for `mcp_hospirfq_processor` using `.env`-driven connection settings and prepared `../rfq_engine` flight RFQ data. The final dependency-ordered run completed with 42 passing function calls, 0 error responses, and 0 failures. Catalog search was executed first and selected `Flight NRT->CDG First`, which was reconciled to `flight_catalog_refs.json` and `flight_products.json` before item, request, quote, pricing, installment, availability, bundle, cancellation, and catalog validation continued. The SOP-scoped integration is certified for the tested local environment.

## Scope

- In scope: MCP HospiRFQ processor facade, local gateway GraphQL path, catalog discovery, item/provider lookup, RFQ request lifecycle, quote lifecycle, pricing, installments, file APIs, segment contacts, availability holds, bundles, cancellation policies, and catalog readback.
- Out of scope: production validation, destructive cleanup of generated test entities, load testing, UI testing, third-party production side effects, and cloud provisioning.
- Phases executed: SOP approval, environment validation, prepared-data reconciliation, dependency order validation, live E2E execution, defect repair, retest, final full-suite export.
- Phases assumed/skipped: schema provisioning and destructive data cleanup were skipped by SOP policy; backing-store internals were validated only through gateway/API behavior.

## Dependency Readiness

| Dependency | Type | Available | Configured | Initialized | Operational | Notes |
|---|---|---|---|---|---|---|
| Python test environment | infrastructure | yes | yes | yes | yes | Unit tests passed: 62 passed |
| `silvaengine_gateway` local instance | internal | yes | yes | yes | yes | `/auth/token` returned 200 and GraphQL calls completed |
| `rfq_engine` route | internal | yes | yes | yes | yes | GraphQL-backed function calls passed |
| prepared flight data | test data | yes | yes | yes | yes | Catalog-selected item mapped to prepared refs and batch data |
| catalog/KGE path | internal | yes | yes | yes | yes | `inquire_catalog` returned ranked `FLIGHTS` results |

Non-blocking environment warning: Pynamo/HybridCache logged disk-cache permission errors under `%LOCALAPPDATA%\Temp\silvaengine_cache`; live API behavior remained operational and the final suite passed.

## End-to-End Workflow Validation

| Workflow | Steps executed | Validation points | Result |
|---|---|---|---|
| Catalog-first item discovery | `inquire_catalog` -> map result to prepared refs -> select batch/service window | selected `itemUuid`, `providerItemUuid`, `batchNo`, service window | pass |
| RFQ request lifecycle | submit -> get/search -> update -> add/remove item -> assign/remove/reassign provider item | generated request UUID, provider assignment, prepared item linkage | pass |
| Quote lifecycle | confirm request/create quote -> get/search quote -> update quote -> update quote item | quote UUID, quote item UUID, pricing and discount update | pass |
| Pricing and installments | price tiers/prompts/calculation -> confirm quote -> create/get/update installments | positive balance, installment creation, paid update | pass |
| Availability hold lifecycle | check -> acquire -> confirm -> acquire/release -> acquire/expire | available batch, hold token transitions, expected immediate-expire no-op | pass |
| Reference APIs | file, segment, bundle, cancellation, catalog readbacks | seeded reference records and catalog payloads | pass |

## Data Reconciliation

| Check | Rule | Tolerance | Observed | Result |
|---|---|---|---|---|
| Catalog selection consistency | selected catalog hit maps to `flight_catalog_refs.json` item/provider IDs | 0 mismatches | `9f965bf9-7302-4f1d-8d37-6f335f880c58` / `24529e36-bd9c-4427-ac05-d1d545ad8963` selected | pass |
| Batch consistency | selected item/provider maps to `flight_products.json` batch and service window | 0 mismatches | `DL4822-20260918`, `2026-09-18T14:45:00Z` to `2026-09-18T23:28:08.831283Z` | pass |
| Quote item linkage | generated quote item belongs to generated quote/request | 0 mismatches | quote and quote item used by downstream pricing/installments | pass |
| Installment consistency | created installments fit quote balance | amount: 0.01 | installment calls passed with positive quote totals | pass |
| Error envelope check | no unexpected top-level `error` or in-band `error_code` | 0 unexpected | 0 error responses in final run | pass |

## Coverage Analysis

| Area | Covered | Total | % | Notes |
|---|---:|---:|---:|---|
| API/function operations | 42 | 42 | 100 | All SOP runner calls executed |
| Workflow operations | 5 | 5 | 100 | Catalog, request, quote, installment, availability |
| Reference read APIs | 6 | 6 | 100 | Files, segments, bundles, cancellation, catalog |
| Failure/resilience checks | 3 | 3 | 100 | Expected live no-op and repaired defects covered |

## Open Risks and Mitigation Plan

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Local disk-cache permission warnings recur | medium | low | fix `%LOCALAPPDATA%\Temp\silvaengine_cache` permissions or redirect cache path | project owner |
| Live test data capacity can be consumed by repeated runs | medium | medium | keep catalog-first availability-aware selection and refresh prepared data as needed | project owner |
| Generated live entities remain in local staging data | high | low | add approved cleanup workflow if isolation becomes required | project owner |

## Certification Decision

- Status: `Integration Certified`
- Rationale: Final SOP-scoped full suite passed with 42/42 calls passing, 0 error responses, and 0 failures after defects were fixed and retested.
- Conditions: Certification applies to the approved local staging-equivalent environment and the SOP-defined workflow only.
- Evidence sources: this report's per-function arguments/outputs, command results from live runs, unit test output, `docs/integration_scenarios_sop.md`, `mcp_hospirfq_processor/tests/run_integration.py`, `mcp_hospirfq_processor/request_mixin.py`, and `mcp_hospirfq_processor/quote_mixin.py`.

## Function Results

### 1. catalog_discovery / inquire_catalog (select primary item)

- Method: `inquire_catalog`
- Status: `pass`
- Elapsed: `3850.71 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "query_text": "Delta Air Lines NRT CDG First class flight with meal included",
  "namespace": "FLIGHTS",
  "limit": 5
}
```

Output:

```json
{
  "namespace": "FLIGHTS",
  "node_id": null,
  "payload": {
    "results": [
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Delta Air Lines (DL) operates flight service Flight NRT->CDG First from NRT to CDG in First class. First class non-stop service from Tokyo (NRT) to Paris (CDG). Base price $4500.0 USD per seat. Baggage allowance 32kg, meal included: True. Pricing tiers:   - adult: $4500.0 USD;   - child: $3375.0 USD;   - infant: $450.0 USD. Scheduled flights:\n  - Flight DL4000 departing 2026-09-05T21:15:00Z arriving 2026-09-06T08:30:40.740402Z with 7 seats available. Cancellation policy: First Fare Cancellation.\n  - Flight DL4822 departing 2026-09-18T14:45:00Z arriving 2026-09-18T23:28:08.831283Z with 7 seats available. Cancellation policy: First Fare Cancellation.\nThis is a First class flight product offered by Delta Air Lines on the NRT->CDG route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:45",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:45",
          "score": "0.8775168061256409",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Cathay Pacific (CX) operates flight service Flight DFW->CDG Business from DFW to CDG in Business class. Business class non-stop service from Dallas (DFW) to Paris (CDG). Base price $1800.0 USD per seat. Baggage allowance 32kg, meal included: True. Pricing tiers:   - adult: $1800.0 USD;   - child: $1350.0 USD;   - infant: $180.0 USD. Scheduled flights:\n  - Flight CX9953 departing 2026-09-14T17:15:00Z arriving 2026-09-15T01:02:33.438418Z with 31 seats available. Cancellation policy: Business Fare Cancellation.\n  - Flight CX6206 departing 2026-07-23T09:15:00Z arriving 2026-07-23T18:29:38.488182Z with 31 seats available. Cancellation policy: Business Fare Cancellation.\nThis is a Business class flight product offered by Cathay Pacific on the DFW->CDG route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:9",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:9",
          "score": "0.7617387175559998",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight itinerary bundle FLT-ITIN-001 named 'Flight Itinerary CDG->ORD + NRT->BOS + NRT->CDG'. Multi-leg flight itinerary template composed of independently priced flight legs. It contains 3 flight legs:\n  - Leg 1: CDG->ORD\n  - Leg 2: NRT->BOS\n  - Leg 3: NRT->CDG"
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:57",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:57",
          "score": "0.7401881217956543",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight itinerary bundle FLT-ITIN-002 named 'Flight Itinerary NRT->BOS + DFW->CDG + NRT->CDG'. Multi-leg flight itinerary template composed of independently priced flight legs. It contains 3 flight legs:\n  - Leg 1: NRT->BOS\n  - Leg 2: DFW->CDG\n  - Leg 3: NRT->CDG"
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:50",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:50",
          "score": "0.7400848269462585",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Singapore Airlines (SQ) operates flight service Flight CDG->ORD Economy from CDG to ORD in Economy class. Economy class non-stop service from Paris (CDG) to Chicago (ORD). Base price $250.0 USD per seat. Baggage allowance 23kg, meal included: False. Pricing tiers:   - adult: $250.0 USD;   - child: $187.5 USD;   - infant: $25.0 USD. Scheduled flights:\n  - Flight SQ493 departing 2026-08-07T19:30:00Z arriving 2026-08-08T06:44:03.940745Z with 232 seats available. Cancellation policy: Economy Fare Cancellation.\n  - Flight SQ2020 departing 2026-10-18T12:15:00Z arriving 2026-10-18T21:20:33.363503Z with 149 seats available. Cancellation policy: Economy Fare Cancellation.\nThis is a Economy class flight product offered by Singapore Airlines on the CDG->ORD route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:32",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:32",
          "score": "0.7254980206489563",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-23T20:29:19.966438+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 2. items / search_items (flight type)

- Method: `search_items`
- Status: `pass`
- Elapsed: `2248.1 ms`

Arguments:

```json
{
  "item_type": "flight",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 5,
  "item_list": [
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "item_type": "flight",
      "item_name": "Flight NRT->CDG First",
      "item_description": "First class non-stop service from Tokyo (NRT) to Paris (CDG).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-NRT-CDG-FIR",
      "created_at": "2026-06-22T21:14:26.858302",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:26.858302"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1",
      "item_type": "flight",
      "item_name": "Flight CDG->ORD Economy",
      "item_description": "Economy class non-stop service from Paris (CDG) to Chicago (ORD).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-CDG-ORD-ECO",
      "created_at": "2026-06-22T21:14:26.774444",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:26.774444"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "898dad8f-2ccf-445c-a55e-5f7f96105840",
      "item_type": "flight",
      "item_name": "Flight ORD->BOS Business",
      "item_description": "Business class non-stop service from Chicago (ORD) to Boston (BOS).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-ORD-BOS-BUS",
      "created_at": "2026-06-22T21:14:26.691981",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:26.691981"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "34f8a79e-abc7-4e0e-901d-855e9b13ed1c",
      "item_type": "flight",
      "item_name": "Flight DFW->CDG Business",
      "item_description": "Business class non-stop service from Dallas (DFW) to Paris (CDG).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-DFW-CDG-BUS",
      "created_at": "2026-06-22T21:14:26.569475",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:26.569475"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "48d374c4-588d-49b9-a005-36caa41706eb",
      "item_type": "flight",
      "item_name": "Flight NRT->BOS Business",
      "item_description": "Business class non-stop service from Tokyo (NRT) to Boston (BOS).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-NRT-BOS-BUS",
      "created_at": "2026-06-22T21:14:26.463273",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:26.463273"
    }
  ]
}
```

### 3. items / get_item (Flight NRT->CDG First)

- Method: `get_item`
- Status: `pass`
- Elapsed: `2260.62 ms`

Arguments:

```json
{
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "item_type": "flight",
  "item_name": "Flight NRT->CDG First",
  "item_description": "First class non-stop service from Tokyo (NRT) to Paris (CDG).",
  "pricing_mode": "per_pax_type",
  "uom": "seat",
  "item_external_id": "FLIGHT-NRT-CDG-FIR",
  "created_at": "2026-06-22T21:14:26.858302",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-22T21:14:26.858302"
}
```

### 4. items / get_provider_items (with batches)

- Method: `get_provider_items`
- Status: `pass`
- Elapsed: `4515.68 ms`

Arguments:

```json
{
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58"
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 1,
  "provider_item_list": [
    {
      "partition_key": "gpt#nestaging",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
      "provider_corp_external_id": "AIRLINE-DL",
      "provider_item_external_id": "DL-NRT-CDG-FIR",
      "base_price_per_uom": 4500.0,
      "item_spec": {
        "cabin_class": "First",
        "origin_iata": "NRT",
        "airline_code": "DL",
        "airline_name": "Delta Air Lines",
        "meal_included": true,
        "destination_iata": "CDG",
        "baggage_allowance_kg": "32"
      },
      "availability_mode": "require_hold",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "item": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "item_type": "flight",
        "item_name": "Flight NRT->CDG First",
        "item_description": "First class non-stop service from Tokyo (NRT) to Paris (CDG).",
        "pricing_mode": "per_pax_type",
        "uom": "seat",
        "item_external_id": "FLIGHT-NRT-CDG-FIR",
        "created_at": "2026-06-22T21:14:26.858302",
        "updated_by": "prepare_flight_products",
        "updated_at": "2026-06-22T21:14:26.858302"
      },
      "updated_by": "prepare_flight_products",
      "created_at": "2026-06-22T21:14:26.867812",
      "updated_at": "2026-06-22T21:14:26.867812",
      "batches": []
    }
  ]
}
```

### 5. requests / submit_rfq_request

- Method: `submit_rfq_request`
- Status: `pass`
- Elapsed: `2287.81 ms`

Arguments:

```json
{
  "email": "zbrown@example.org",
  "request_title": "Integration test: Flight NRT->CDG First",
  "request_description": "E2E test request via silvaengine_gateway",
  "items": [
    {
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "item_name": "Flight NRT->CDG First",
      "qty": 2,
      "pax_breakdown": {
        "adult": 2
      }
    }
  ],
  "notes": "Created by run_integration.py",
  "expired_at": "2026-12-31T23:59:59Z"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "email": "zbrown@example.org",
  "request_title": "Integration test: Flight NRT->CDG First",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Created by run_integration.py",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-23T20:29:31.226145",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T20:29:31.227242",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 6. requests / get_rfq_request (seeded)

- Method: `get_rfq_request`
- Status: `pass`
- Elapsed: `2285.29 ms`

Arguments:

```json
{
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
  "email": "zbrown@example.org",
  "request_title": "Business trip NRT to CDG November",
  "request_description": "Business travel for 2 attendee(s) attending offsite meetings in CDG. Prefer Business or Premium Economy to allow productive flight time.",
  "billing_address": {
    "city": "Maxwellhaven",
    "name": "Keith Chen",
    "phone": "001-314-580-8409x8991",
    "state": "LA",
    "street": "079 Karen Skyway",
    "country": "US",
    "postal_code": "50014"
  },
  "shipping_address": {
    "city": "Anaton",
    "name": "John Bradford",
    "phone": "(723)810-6891",
    "state": "AR",
    "street": "95551 Vaughn Villages Apt. 446",
    "country": "US",
    "postal_code": "83528"
  },
  "items": [
    {
      "quantity": "2",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      },
      "provider_items": [
        {
          "quantity": "2",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
        }
      ],
      "cabin_preference": "Business"
    }
  ],
  "notes": "Eye kitchen entire member music finish despite letter eight while little win.",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-08-18T21:14:31.376040",
  "created_at": "2026-06-22T21:14:31.410885",
  "updated_by": "prepare_requests",
  "updated_at": "2026-06-22T21:14:31.410885",
  "quotes": [
    {
      "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
      "quote_uuid": "9e8378fa-f6b3-4353-bf9a-af2ff6036ff8",
      "provider_corp_external_id": "AIRLINE-DL",
      "sales_rep_email": "terri16@example.com",
      "partition_key": "gpt#nestaging",
      "shipping_method": null,
      "shipping_amount": "0",
      "total_quote_amount": "9000",
      "total_quote_discount": "111",
      "final_total_quote_amount": "8889",
      "currency": "USD",
      "display_currency": null,
      "fx_rate": null,
      "fx_rate_locked_at": null,
      "rounds": "0",
      "notes": "Auto-completed: All installments paid",
      "status": "completed",
      "created_at": "2026-06-22 21:14:32.731930",
      "updated_by": "MCP",
      "updated_at": "2026-06-23 06:54:27.199452"
    }
  ],
  "files": [
    {
      "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
      "file_name": "integration_test_spec.pdf",
      "email": "zbrown@example.org",
      "partition_key": "gpt#nestaging",
      "created_at": "2026-06-23 06:48:47.795038",
      "updated_by": "MCP",
      "updated_at": "2026-06-23 20:14:52.789726"
    }
  ],
  "bundle": null
}
```

### 7. requests / search_rfq_requests

- Method: `search_rfq_requests`
- Status: `pass`
- Elapsed: `2287.08 ms`

Arguments:

```json
{
  "limit": 5,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 12,
  "request_list": [
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
      "email": "zbrown@example.org",
      "request_title": "Integration test: Flight NRT->CDG First",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "2",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Created by run_integration.py",
      "bundle_uuid": null,
      "status": "initial",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-23T20:29:31.226145",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T20:29:31.227242",
      "quotes": [],
      "files": [],
      "bundle": null
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "b5f9a643-a2c8-4d7b-acfe-9b8c3e971954",
      "email": "zbrown@example.org",
      "request_title": "Integration test: Flight NRT->CDG First (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "2",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "2"
          },
          "provider_items": [
            {
              "qty": "2",
              "batch_no": "DL4000-20260905",
              "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
              "provider_corp_external_id": "AIRLINE-DL"
            }
          ]
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "completed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-23T20:11:35.264222",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T20:14:50.517290",
      "quotes": [
        {
          "request_uuid": "b5f9a643-a2c8-4d7b-acfe-9b8c3e971954",
          "quote_uuid": "e30ae257-5924-4a0b-9c61-0cf6f1ab2cfb",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "25",
          "total_quote_amount": "9000",
          "total_quote_discount": "50",
          "final_total_quote_amount": "9025",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Auto-completed: All installments paid",
          "status": "completed",
          "created_at": "2026-06-23 20:12:24.080877",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 20:14:43.647397"
        },
        {
          "request_uuid": "b5f9a643-a2c8-4d7b-acfe-9b8c3e971954",
          "quote_uuid": "be46f2a4-cbe9-42a6-a40d-ae1550c26740",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "300",
          "total_quote_amount": "9000",
          "total_quote_discount": "0",
          "final_total_quote_amount": "9000",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Confirmed setup quote for create_installments",
          "status": "confirmed",
          "created_at": "2026-06-23 20:13:53.154642",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 20:14:12.537871"
        },
        {
          "request_uuid": "b5f9a643-a2c8-4d7b-acfe-9b8c3e971954",
          "quote_uuid": "12562567-231e-4a1e-969a-61688da3dd29",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "300",
          "total_quote_amount": "9000",
          "total_quote_discount": "0",
          "final_total_quote_amount": "9000",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Confirmed setup quote for create_installment",
          "status": "confirmed",
          "created_at": "2026-06-23 20:13:28.258935",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 20:13:48.230284"
        }
      ],
      "files": [],
      "bundle": null
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "7be1ba7e-b059-4133-846e-f5ce3fa8ee74",
      "email": "zbrown@example.org",
      "request_title": "Integration test: Flight NRT->CDG First (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "2",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "2"
          },
          "provider_items": [
            {
              "qty": "2",
              "batch_no": "DL4000-20260905",
              "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
              "provider_corp_external_id": "AIRLINE-DL"
            }
          ]
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "completed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-23T18:54:11.338880",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T18:57:31.389623",
      "quotes": [
        {
          "request_uuid": "7be1ba7e-b059-4133-846e-f5ce3fa8ee74",
          "quote_uuid": "8d03092d-0d61-4795-9e28-322285363927",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "25",
          "total_quote_amount": "9000",
          "total_quote_discount": "50",
          "final_total_quote_amount": "9025",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Auto-completed: All installments paid",
          "status": "completed",
          "created_at": "2026-06-23 18:55:01.521562",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 18:57:23.939954"
        },
        {
          "request_uuid": "7be1ba7e-b059-4133-846e-f5ce3fa8ee74",
          "quote_uuid": "2d5a2f51-0184-4c88-84a0-d389e9ef2180",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "300",
          "total_quote_amount": "9000",
          "total_quote_discount": "0",
          "final_total_quote_amount": "9000",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Confirmed setup quote for create_installments",
          "status": "confirmed",
          "created_at": "2026-06-23 18:56:31.059586",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 18:56:51.352535"
        },
        {
          "request_uuid": "7be1ba7e-b059-4133-846e-f5ce3fa8ee74",
          "quote_uuid": "4440225c-0544-4b94-b003-6ad6779a7e18",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "300",
          "total_quote_amount": "9000",
          "total_quote_discount": "0",
          "final_total_quote_amount": "9000",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Confirmed setup quote for create_installment",
          "status": "confirmed",
          "created_at": "2026-06-23 18:56:05.971614",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 18:56:26.189539"
        }
      ],
      "files": [],
      "bundle": null
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "93d75c8a-341d-4905-bc83-d818559df39b",
      "email": "zbrown@example.org",
      "request_title": "Integration test: Flight NRT->CDG First (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "2",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "2"
          },
          "provider_items": [
            {
              "qty": "2",
              "batch_no": "DL4000-20260905",
              "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
              "provider_corp_external_id": "AIRLINE-DL"
            }
          ]
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "completed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-23T18:45:19.806124",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T18:48:29.703446",
      "quotes": [
        {
          "request_uuid": "93d75c8a-341d-4905-bc83-d818559df39b",
          "quote_uuid": "68862cd7-f5a8-4f47-b5ca-4e79979061a3",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "25",
          "total_quote_amount": "9000",
          "total_quote_discount": "50",
          "final_total_quote_amount": "9025",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Auto-completed: All installments paid",
          "status": "completed",
          "created_at": "2026-06-23 18:46:07.916683",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 18:48:22.153222"
        },
        {
          "request_uuid": "93d75c8a-341d-4905-bc83-d818559df39b",
          "quote_uuid": "955d7bb7-9ffc-4f5b-82d0-60a40fbd48e1",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "300",
          "total_quote_amount": "9000",
          "total_quote_discount": "0",
          "final_total_quote_amount": "9000",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Confirmed setup quote for create_installments",
          "status": "confirmed",
          "created_at": "2026-06-23 18:47:31.403747",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 18:47:50.093697"
        },
        {
          "request_uuid": "93d75c8a-341d-4905-bc83-d818559df39b",
          "quote_
... (truncated)
```

### 8. requests / update_rfq_request

- Method: `update_rfq_request`
- Status: `pass`
- Elapsed: `4507.57 ms`

Arguments:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "request_title": "Integration test: Flight NRT->CDG First (updated)",
  "notes": "Updated via run_integration.py"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "email": "zbrown@example.org",
  "request_title": "Integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-23T20:29:31.226145",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T20:29:40.354643",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 9. requests / add_item_to_rfq_request

- Method: `add_item_to_rfq_request`
- Status: `pass`
- Elapsed: `4833.69 ms`

Arguments:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "item": {
    "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1",
    "item_name": "Flight CDG->ORD Economy",
    "qty": 1,
    "provider_items": []
  }
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "email": "zbrown@example.org",
  "request_title": "Integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      }
    },
    {
      "qty": "1",
      "item_name": "Flight CDG->ORD Economy",
      "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1",
      "provider_items": []
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-23T20:29:31.226145",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T20:29:45.186424",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 10. requests / remove_item_from_rfq_request

- Method: `remove_item_from_rfq_request`
- Status: `pass`
- Elapsed: `4584.7 ms`

Arguments:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "email": "zbrown@example.org",
  "request_title": "Integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-23T20:29:31.226145",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T20:29:49.765636",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 11. requests / assign_provider_item_to_request_item

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `6823.81 ms`

Arguments:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "provider_corp_external_id": "AIRLINE-DL",
  "qty": 2,
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "email": "zbrown@example.org",
  "request_title": "Integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      },
      "provider_items": [
        {
          "qty": "2",
          "batch_no": "DL4822-20260918",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "provider_corp_external_id": "AIRLINE-DL"
        }
      ]
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-23T20:29:31.226145",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T20:29:56.592869",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 12. requests / remove_provider_item_from_request_item

- Method: `remove_provider_item_from_request_item`
- Status: `pass`
- Elapsed: `4524.8 ms`

Arguments:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "email": "zbrown@example.org",
  "request_title": "Integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      },
      "provider_items": []
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-23T20:29:31.226145",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T20:30:01.115026",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 13. requests / assign_provider_item_to_request_item (for quote workflow)

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `7128.88 ms`

Arguments:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "provider_corp_external_id": "AIRLINE-DL",
  "qty": 2,
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "email": "zbrown@example.org",
  "request_title": "Integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      },
      "provider_items": [
        {
          "qty": "2",
          "batch_no": "DL4822-20260918",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "provider_corp_external_id": "AIRLINE-DL"
        }
      ]
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-23T20:29:31.226145",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T20:30:08.230933",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 14. quotes / confirm_request_and_create_quotes

- Method: `confirm_request_and_create_quotes`
- Status: `pass`
- Elapsed: `24237.98 ms`

Arguments:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "provider_corp_external_ids": [
    "AIRLINE-DL"
  ],
  "segment_uuid": "323dec2b-1f03-4d42-a5ef-73ef9e17c4e6",
  "batch_no": "DL4822-20260918",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z"
}
```

Output:

```json
{
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
    "email": "zbrown@example.org",
    "request_title": "Integration test: Flight NRT->CDG First (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "qty": "2",
        "item_name": "Flight NRT->CDG First",
        "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "pax_breakdown": {
          "adult": "2"
        },
        "provider_items": [
          {
            "qty": "2",
            "batch_no": "DL4822-20260918",
            "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
            "provider_corp_external_id": "AIRLINE-DL"
          }
        ]
      }
    ],
    "notes": "Updated via run_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-23T20:29:31.226145",
    "updated_by": "MCP",
    "updated_at": "2026-06-23T20:30:15.471319",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "created_quotes": [
    {
      "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
      "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-DL",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 9000.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 9000.0,
      "currency": null,
      "display_currency": null,
      "fx_rate": null,
      "fx_rate_locked_at": null,
      "notes": null,
      "status": "in_progress",
      "expired_at": null,
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
        "email": "zbrown@example.org",
        "request_title": "Integration test: Flight NRT->CDG First (updated)",
        "request_description": "E2E test request via silvaengine_gateway",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "qty": "2",
            "item_name": "Flight NRT->CDG First",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "pax_breakdown": {
              "adult": "2"
            },
            "provider_items": [
              {
                "qty": "2",
                "batch_no": "DL4822-20260918",
                "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
                "provider_corp_external_id": "AIRLINE-DL"
              }
            ]
          }
        ],
        "notes": "Updated via run_integration.py",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-23T20:29:31.226145",
        "updated_by": "MCP",
        "updated_at": "2026-06-23T20:30:15.471319",
        "quotes": [],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
          "quote_item_uuid": "bfa45c83-15eb-433a-8c45-121db36d8b6b",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "batch_no": "DL4822-20260918",
          "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
          "partition_key": "gpt#nestaging",
          "request_data": {
            "cancellation_policy_snapshot": {
              "label": "First Fare Cancellation",
              "tiers": {
                "tiers": [
                  {
                    "refund_pct": "1",
                    "hours_before_departure_gte": "24"
                  },
                  {
                    "refund_pct": "0.5",
                    "hours_before_departure_gte": "2"
                  },
                  {
                    "refund_pct": "0",
                    "hours_before_departure_gte": "0"
                  }
                ]
              },
              "description": "Job service instead mention whatever between seek chance back.",
              "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
              "snapshotted_at": "2026-06-23 20:30:25.226978",
              "notes_template_uuid": null
            }
          },
          "price_per_uom": "4500",
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          },
          "bundle_uuid": null,
          "bundle_label": null,
          "bundle_component_uuid": null,
          "subtotal": "9000",
          "subtotal_discount": "0",
          "final_subtotal": "9000",
          "currency": null,
          "subtotal_native": "9000",
          "notes": null,
          "hold_token": null,
          "hold_expires_at": null,
          "created_at": "2026-06-23 20:30:25.146670",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 20:30:25.146670"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
          "conditions": [
            "min_passengers >= 20",
            "payment_method in ['wire_transfer', 'credit_card']",
            "is_refundable == false"
          ],
          "discount_rules": [
            {
              "less_than": "10000",
              "greater_than": "0",
              "max_discount_percentage": "5"
            },
            {
              "less_than": "11000",
              "greater_than": "10000",
              "max_discount_percentage": "10"
            },
            {
              "greater_than": "11000",
              "max_discount_percentage": "15"
            }
          ],
          "priority": "6",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.888325",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.888325"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
          "conditions": [
            "season != 'peak'",
            "channel == 'direct'"
          ],
          "discount_rules": [
            {
              "less_than": "5000",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "5"
            }
          ],
          "priority": "4",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.970326",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.970326"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
          "conditions": [
            "loyalty_tier in ['gold', 'platinum']",
            "booking_lead_days >= 7"
          ],
          "discount_rules": [
            {
              "less_than": "2500",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "less_than": "12500",
              "greater_than": "2500",
              "max_discount_percentage": "7.5"
            },
            {
              "less_than": "22500",
              "greater_than": "12500",
              "max_discount_percentage": "12.5"
            },
            {
              "greater_than": "22500",
              "max_discount_percentage": "17.5"
            }
          ],
          "priority": "1",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.958795",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.958795"
        }
      ],
      "updated_by": "MCP",
      "created_at": "2026-06-23T20:30:20.308436",
      "updated_at": "2026-06-23T20:30:29.909388"
    }
  ],
  "total_quotes_created": 1,
  "total_quotes_requested": 1
}
```

### 15. quotes / get_quote

- Method: `get_quote`
- Status: `pass`
- Elapsed: `2292.58 ms`

Arguments:

```json
{
  "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976"
}
```

Output:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-DL",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": null,
  "shipping_amount": 0.0,
  "total_quote_amount": 9000.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 9000.0,
  "currency": null,
  "display_currency": null,
  "fx_rate": null,
  "fx_rate_locked_at": null,
  "notes": null,
  "status": "in_progress",
  "expired_at": null,
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
    "email": "zbrown@example.org",
    "request_title": "Integration test: Flight NRT->CDG First (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "qty": "2",
        "item_name": "Flight NRT->CDG First",
        "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "pax_breakdown": {
          "adult": "2"
        },
        "provider_items": [
          {
            "qty": "2",
            "batch_no": "DL4822-20260918",
            "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
            "provider_corp_external_id": "AIRLINE-DL"
          }
        ]
      }
    ],
    "notes": "Updated via run_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-23T20:29:31.226145",
    "updated_by": "MCP",
    "updated_at": "2026-06-23T20:30:15.471319",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
      "quote_item_uuid": "bfa45c83-15eb-433a-8c45-121db36d8b6b",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "batch_no": "DL4822-20260918",
      "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
      "partition_key": "gpt#nestaging",
      "request_data": {
        "cancellation_policy_snapshot": {
          "label": "First Fare Cancellation",
          "tiers": {
            "tiers": [
              {
                "refund_pct": "1",
                "hours_before_departure_gte": "24"
              },
              {
                "refund_pct": "0.5",
                "hours_before_departure_gte": "2"
              },
              {
                "refund_pct": "0",
                "hours_before_departure_gte": "0"
              }
            ]
          },
          "description": "Job service instead mention whatever between seek chance back.",
          "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
          "snapshotted_at": "2026-06-23 20:30:25.226978",
          "notes_template_uuid": null
        }
      },
      "price_per_uom": "4500",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      },
      "bundle_uuid": null,
      "bundle_label": null,
      "bundle_component_uuid": null,
      "subtotal": "9000",
      "subtotal_discount": "0",
      "final_subtotal": "9000",
      "currency": null,
      "subtotal_native": "9000",
      "notes": null,
      "hold_token": null,
      "hold_expires_at": null,
      "created_at": "2026-06-23 20:30:25.146670",
      "updated_by": "MCP",
      "updated_at": "2026-06-23 20:30:25.146670"
    }
  ],
  "installments": [],
  "discount_prompts": [
    {
      "partition_key": "gpt#nestaging",
      "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
      "conditions": [
        "min_passengers >= 20",
        "payment_method in ['wire_transfer', 'credit_card']",
        "is_refundable == false"
      ],
      "discount_rules": [
        {
          "less_than": "10000",
          "greater_than": "0",
          "max_discount_percentage": "5"
        },
        {
          "less_than": "11000",
          "greater_than": "10000",
          "max_discount_percentage": "10"
        },
        {
          "greater_than": "11000",
          "max_discount_percentage": "15"
        }
      ],
      "priority": "6",
      "status": "active",
      "created_at": "2026-06-22 21:14:29.888325",
      "updated_by": "prepare_discount_prompts",
      "updated_at": "2026-06-22 21:14:29.888325"
    },
    {
      "partition_key": "gpt#nestaging",
      "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
      "conditions": [
        "season != 'peak'",
        "channel == 'direct'"
      ],
      "discount_rules": [
        {
          "less_than": "5000",
          "greater_than": "0",
          "max_discount_percentage": "2.5"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "5"
        }
      ],
      "priority": "4",
      "status": "active",
      "created_at": "2026-06-22 21:14:29.970326",
      "updated_by": "prepare_discount_prompts",
      "updated_at": "2026-06-22 21:14:29.970326"
    },
    {
      "partition_key": "gpt#nestaging",
      "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
      "conditions": [
        "loyalty_tier in ['gold', 'platinum']",
        "booking_lead_days >= 7"
      ],
      "discount_rules": [
        {
          "less_than": "2500",
          "greater_than": "0",
          "max_discount_percentage": "2.5"
        },
        {
          "less_than": "12500",
          "greater_than": "2500",
          "max_discount_percentage": "7.5"
        },
        {
          "less_than": "22500",
          "greater_than": "12500",
          "max_discount_percentage": "12.5"
        },
        {
          "greater_than": "22500",
          "max_discount_percentage": "17.5"
        }
      ],
      "priority": "1",
      "status": "active",
      "created_at": "2026-06-22 21:14:29.958795",
      "updated_by": "prepare_discount_prompts",
      "updated_at": "2026-06-22 21:14:29.958795"
    }
  ],
  "updated_by": "MCP",
  "created_at": "2026-06-23T20:30:20.308436",
  "updated_at": "2026-06-23T20:30:29.909388"
}
```

### 16. quotes / search_quotes

- Method: `search_quotes`
- Status: `pass`
- Elapsed: `2291.73 ms`

Arguments:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 1,
  "quote_list": [
    {
      "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
      "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-DL",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 9000.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 9000.0,
      "currency": null,
      "display_currency": null,
      "fx_rate": null,
      "fx_rate_locked_at": null,
      "notes": null,
      "status": "in_progress",
      "expired_at": null,
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
        "email": "zbrown@example.org",
        "request_title": "Integration test: Flight NRT->CDG First (updated)",
        "request_description": "E2E test request via silvaengine_gateway",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "qty": "2",
            "item_name": "Flight NRT->CDG First",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "pax_breakdown": {
              "adult": "2"
            },
            "provider_items": [
              {
                "qty": "2",
                "batch_no": "DL4822-20260918",
                "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
                "provider_corp_external_id": "AIRLINE-DL"
              }
            ]
          }
        ],
        "notes": "Updated via run_integration.py",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-23T20:29:31.226145",
        "updated_by": "MCP",
        "updated_at": "2026-06-23T20:30:15.471319",
        "quotes": [],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
          "quote_item_uuid": "bfa45c83-15eb-433a-8c45-121db36d8b6b",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "batch_no": "DL4822-20260918",
          "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
          "partition_key": "gpt#nestaging",
          "request_data": {
            "cancellation_policy_snapshot": {
              "label": "First Fare Cancellation",
              "tiers": {
                "tiers": [
                  {
                    "refund_pct": "1",
                    "hours_before_departure_gte": "24"
                  },
                  {
                    "refund_pct": "0.5",
                    "hours_before_departure_gte": "2"
                  },
                  {
                    "refund_pct": "0",
                    "hours_before_departure_gte": "0"
                  }
                ]
              },
              "description": "Job service instead mention whatever between seek chance back.",
              "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
              "snapshotted_at": "2026-06-23 20:30:25.226978",
              "notes_template_uuid": null
            }
          },
          "price_per_uom": "4500",
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          },
          "bundle_uuid": null,
          "bundle_label": null,
          "bundle_component_uuid": null,
          "subtotal": "9000",
          "subtotal_discount": "0",
          "final_subtotal": "9000",
          "currency": null,
          "subtotal_native": "9000",
          "notes": null,
          "hold_token": null,
          "hold_expires_at": null,
          "created_at": "2026-06-23 20:30:25.146670",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 20:30:25.146670"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
          "conditions": [
            "min_passengers >= 20",
            "payment_method in ['wire_transfer', 'credit_card']",
            "is_refundable == false"
          ],
          "discount_rules": [
            {
              "less_than": "10000",
              "greater_than": "0",
              "max_discount_percentage": "5"
            },
            {
              "less_than": "11000",
              "greater_than": "10000",
              "max_discount_percentage": "10"
            },
            {
              "greater_than": "11000",
              "max_discount_percentage": "15"
            }
          ],
          "priority": "6",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.888325",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.888325"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
          "conditions": [
            "season != 'peak'",
            "channel == 'direct'"
          ],
          "discount_rules": [
            {
              "less_than": "5000",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "5"
            }
          ],
          "priority": "4",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.970326",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.970326"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
          "conditions": [
            "loyalty_tier in ['gold', 'platinum']",
            "booking_lead_days >= 7"
          ],
          "discount_rules": [
            {
              "less_than": "2500",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "less_than": "12500",
              "greater_than": "2500",
              "max_discount_percentage": "7.5"
            },
            {
              "less_than": "22500",
              "greater_than": "12500",
              "max_discount_percentage": "12.5"
            },
            {
              "greater_than": "22500",
              "max_discount_percentage": "17.5"
            }
          ],
          "priority": "1",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.958795",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.958795"
        }
      ],
      "updated_by": "MCP",
      "created_at": "2026-06-23T20:30:20.308436",
      "updated_at": "2026-06-23T20:30:29.909388"
    }
  ]
}
```

### 17. quotes / update_quote

- Method: `update_quote`
- Status: `pass`
- Elapsed: `4588.37 ms`

Arguments:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
  "notes": "Updated via integration test",
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0
}
```

Output:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-DL",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0,
  "total_quote_amount": 9000.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 9000.0,
  "currency": null,
  "display_currency": null,
  "fx_rate": null,
  "fx_rate_locked_at": null,
  "notes": "Updated via integration test",
  "status": "in_progress",
  "expired_at": null,
  "request": null,
  "quote_items": [],
  "installments": [],
  "discount_prompts": [],
  "updated_by": "MCP",
  "created_at": "2026-06-23T20:30:20.308436",
  "updated_at": "2026-06-23T20:30:41.661232"
}
```

### 18. quotes / update_quote_item

- Method: `update_quote_item`
- Status: `pass`
- Elapsed: `4595.85 ms`

Arguments:

```json
{
  "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
  "quote_item_uuid": "bfa45c83-15eb-433a-8c45-121db36d8b6b",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "discount_amount": 50.0,
  "notes": "Integration test discount"
}
```

Output:

```json
{
  "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
  "quote_item_uuid": "bfa45c83-15eb-433a-8c45-121db36d8b6b",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "partition_key": "gpt#nestaging",
  "batch_no": "DL4822-20260918",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "qty": 2.0,
  "pax_breakdown": {
    "adult": "2"
  },
  "bundle_uuid": null,
  "bundle_label": null,
  "bundle_component_uuid": null,
  "price_per_uom": 4500.0,
  "subtotal": 9000.0,
  "subtotal_discount": 50.0,
  "final_subtotal": 9000.0,
  "currency": null,
  "subtotal_native": 9000.0,
  "notes": "Integration test discount",
  "hold_token": null,
  "hold_expires_at": null,
  "guardrail_price_per_uom": null,
  "slow_move_item": null,
  "request_data": {
    "cancellation_policy_snapshot": {
      "label": "First Fare Cancellation",
      "tiers": {
        "tiers": [
          {
            "refund_pct": "1.0",
            "hours_before_departure_gte": "24"
          },
          {
            "refund_pct": "0.5",
            "hours_before_departure_gte": "2"
          },
          {
            "refund_pct": "0.0",
            "hours_before_departure_gte": "0"
          }
        ]
      },
      "description": "Job service instead mention whatever between seek chance back.",
      "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
      "snapshotted_at": "2026-06-23 20:30:25.226978",
      "notes_template_uuid": null
    }
  },
  "quote": null,
  "item": null,
  "provider_item": null,
  "provider_item_batch": null,
  "bundle": null,
  "bundle_component": null,
  "updated_by": "MCP",
  "created_at": "2026-06-23T20:30:25.146670",
  "updated_at": "2026-06-23T20:30:46.240117"
}
```

### 19. pricing / get_item_price_tiers

- Method: `get_item_price_tiers`
- Status: `pass`
- Elapsed: `2277.22 ms`

Arguments:

```json
{
  "email": "zbrown@example.org",
  "quote_items": [
    {
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
      "qty": 2
    }
  ]
}
```

Output:

```json
{
  "item_price_tiers": []
}
```

### 20. pricing / get_discount_prompts

- Method: `get_discount_prompts`
- Status: `pass`
- Elapsed: `2289.27 ms`

Arguments:

```json
{
  "email": "zbrown@example.org",
  "quote_items": [
    {
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
    }
  ]
}
```

Output:

```json
{
  "discount_prompts": [
    {
      "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
      "conditions": [
        "min_passengers >= 20",
        "payment_method in ['wire_transfer', 'credit_card']",
        "is_refundable == false"
      ],
      "discount_rules": [
        {
          "less_than": "10000",
          "greater_than": "0",
          "max_discount_percentage": "5"
        },
        {
          "less_than": "11000",
          "greater_than": "10000",
          "max_discount_percentage": "10"
        },
        {
          "greater_than": "11000",
          "max_discount_percentage": "15"
        }
      ],
      "priority": 6,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
      "conditions": [
        "season != 'peak'",
        "channel == 'direct'"
      ],
      "discount_rules": [
        {
          "less_than": "5000",
          "greater_than": "0",
          "max_discount_percentage": "2.5"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "5"
        }
      ],
      "priority": 4,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
      "conditions": [
        "loyalty_tier in ['gold', 'platinum']",
        "booking_lead_days >= 7"
      ],
      "discount_rules": [
        {
          "less_than": "2500",
          "greater_than": "0",
          "max_discount_percentage": "2.5"
        },
        {
          "less_than": "12500",
          "greater_than": "2500",
          "max_discount_percentage": "7.5"
        },
        {
          "less_than": "22500",
          "greater_than": "12500",
          "max_discount_percentage": "12.5"
        },
        {
          "greater_than": "22500",
          "max_discount_percentage": "17.5"
        }
      ],
      "priority": 1,
      "status": "active"
    }
  ]
}
```

### 21. pricing / calculate_quote_pricing

- Method: `calculate_quote_pricing`
- Status: `pass`
- Elapsed: `4539.51 ms`

Arguments:

```json
{
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
  "email": "zbrown@example.org"
}
```

Output:

```json
{
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
  "groups": []
}
```

### 22. installments / confirm_quote_and_create_installments

- Method: `confirm_quote_and_create_installments`
- Status: `pass`
- Elapsed: `18420.06 ms`

Arguments:

```json
{
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
  "create_single_installment": true,
  "payment_method": "bank_transfer"
}
```

Output:

```json
{
  "quote": {
    "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
    "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-DL",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 9000.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 9025.0,
    "currency": null,
    "display_currency": null,
    "fx_rate": null,
    "fx_rate_locked_at": null,
    "notes": "Updated via integration test",
    "status": "confirmed",
    "expired_at": null,
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
      "email": "zbrown@example.org",
      "request_title": "Integration test: Flight NRT->CDG First (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "2",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "2"
          },
          "provider_items": [
            {
              "qty": "2",
              "batch_no": "DL4822-20260918",
              "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
              "provider_corp_external_id": "AIRLINE-DL"
            }
          ]
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-23T20:29:31.226145",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T20:30:15.471319",
      "quotes": [],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
        "quote_item_uuid": "bfa45c83-15eb-433a-8c45-121db36d8b6b",
        "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
        "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "batch_no": "DL4822-20260918",
        "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
        "partition_key": "gpt#nestaging",
        "request_data": {
          "cancellation_policy_snapshot": {
            "label": "First Fare Cancellation",
            "tiers": {
              "tiers": [
                {
                  "refund_pct": "1",
                  "hours_before_departure_gte": "24"
                },
                {
                  "refund_pct": "0.5",
                  "hours_before_departure_gte": "2"
                },
                {
                  "refund_pct": "0",
                  "hours_before_departure_gte": "0"
                }
              ]
            },
            "description": "Job service instead mention whatever between seek chance back.",
            "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
            "snapshotted_at": "2026-06-23 20:30:25.226978",
            "notes_template_uuid": null
          }
        },
        "price_per_uom": "4500",
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        },
        "bundle_uuid": null,
        "bundle_label": null,
        "bundle_component_uuid": null,
        "subtotal": "9000",
        "subtotal_discount": "50",
        "final_subtotal": "9000",
        "currency": null,
        "subtotal_native": "9000",
        "notes": "Integration test discount",
        "hold_token": null,
        "hold_expires_at": null,
        "created_at": "2026-06-23 20:30:25.146670",
        "updated_by": "MCP",
        "updated_at": "2026-06-23 20:30:46.240117"
      }
    ],
    "installments": [
      {
        "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
        "installment_uuid": "b21e8897-936b-4d09-84e3-87c0ee902014",
        "partition_key": "gpt#nestaging",
        "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
        "priority": "0",
        "salesorder_no": null,
        "payment_method": "bank_transfer",
        "scheduled_date": "2026-06-23 20:31:09",
        "installment_ratio": "100",
        "installment_amount": "9025",
        "status": "pending",
        "created_at": "2026-06-23 20:31:11.429245",
        "updated_by": "MCP",
        "updated_at": "2026-06-23 20:31:11.429245"
      }
    ],
    "discount_prompts": [
      {
        "partition_key": "gpt#nestaging",
        "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
        "scope": "global",
        "tags": [],
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
        "conditions": [
          "min_passengers >= 20",
          "payment_method in ['wire_transfer', 'credit_card']",
          "is_refundable == false"
        ],
        "discount_rules": [
          {
            "less_than": "10000",
            "greater_than": "0",
            "max_discount_percentage": "5"
          },
          {
            "less_than": "11000",
            "greater_than": "10000",
            "max_discount_percentage": "10"
          },
          {
            "greater_than": "11000",
            "max_discount_percentage": "15"
          }
        ],
        "priority": "6",
        "status": "active",
        "created_at": "2026-06-22 21:14:29.888325",
        "updated_by": "prepare_discount_prompts",
        "updated_at": "2026-06-22 21:14:29.888325"
      },
      {
        "partition_key": "gpt#nestaging",
        "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
        "scope": "global",
        "tags": [],
        "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
        "conditions": [
          "season != 'peak'",
          "channel == 'direct'"
        ],
        "discount_rules": [
          {
            "less_than": "5000",
            "greater_than": "0",
            "max_discount_percentage": "2.5"
          },
          {
            "greater_than": "5000",
            "max_discount_percentage": "5"
          }
        ],
        "priority": "4",
        "status": "active",
        "created_at": "2026-06-22 21:14:29.970326",
        "updated_by": "prepare_discount_prompts",
        "updated_at": "2026-06-22 21:14:29.970326"
      },
      {
        "partition_key": "gpt#nestaging",
        "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
        "scope": "global",
        "tags": [],
        "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
        "conditions": [
          "loyalty_tier in ['gold', 'platinum']",
          "booking_lead_days >= 7"
        ],
        "discount_rules": [
          {
            "less_than": "2500",
            "greater_than": "0",
            "max_discount_percentage": "2.5"
          },
          {
            "less_than": "12500",
            "greater_than": "2500",
            "max_discount_percentage": "7.5"
          },
          {
            "less_than": "22500",
            "greater_than": "12500",
            "max_discount_percentage": "12.5"
          },
          {
            "greater_than": "22500",
            "max_discount_percentage": "17.5"
          }
        ],
        "priority": "1",
        "status": "active",
        "created_at": "2026-06-22 21:14:29.958795",
        "updated_by": "prepare_discount_prompts",
        "updated_at": "2026-06-22 21:14:29.958795"
      }
    ],
    "updated_by": "MCP",
    "created_at": "2026-06-23T20:30:20.308436",
    "updated_at": "2026-06-23T20:31:02.250375"
  },
  "installments": [
    {
      "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
      "installment_uuid": "b21e8897-936b-4d09-84e3-87c0ee902014",
      "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 9025.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-23T20:31:09",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-23T20:31:11.429245",
      "updated_at": "2026-06-23T20:31:11.429245",
      "quote": null
    }
  ],
  "total_installments_created": 1,
  "installment_amount_per": 9025.0,
  "total_installment_amount": 9025.0,
  "installment_type": "single"
}
```

### 23. installments / get_installments

- Method: `get_installments`
- Status: `pass`
- Elapsed: `2556.39 ms`

Arguments:

```json
{
  "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 1,
  "installment_list": [
    {
      "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
      "installment_uuid": "b21e8897-936b-4d09-84e3-87c0ee902014",
      "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 9025.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-23T20:31:09",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-23T20:31:11.429245",
      "updated_at": "2026-06-23T20:31:11.429245",
      "quote": {
        "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
        "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_id": "AIRLINE-DL",
        "sales_rep_email": null,
        "rounds": 0,
        "shipping_method": "ticket_delivery",
        "shipping_amount": 25.0,
        "total_quote_amount": 9000.0,
        "total_quote_discount": 50.0,
        "final_total_quote_amount": 9025.0,
        "currency": null,
        "display_currency": null,
        "fx_rate": null,
        "fx_rate_locked_at": null,
        "notes": "Updated via integration test",
        "status": "confirmed",
        "expired_at": null,
        "request": {
          "partition_key": "gpt#nestaging",
          "endpoint_id": "gpt",
          "part_id": "nestaging",
          "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
          "email": "zbrown@example.org",
          "request_title": "Integration test: Flight NRT->CDG First (updated)",
          "request_description": "E2E test request via silvaengine_gateway",
          "billing_address": null,
          "shipping_address": null,
          "items": [
            {
              "qty": "2",
              "item_name": "Flight NRT->CDG First",
              "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
              "pax_breakdown": {
                "adult": "2"
              },
              "provider_items": [
                {
                  "qty": "2",
                  "batch_no": "DL4822-20260918",
                  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
                  "provider_corp_external_id": "AIRLINE-DL"
                }
              ]
            }
          ],
          "notes": "Updated via run_integration.py",
          "bundle_uuid": null,
          "status": "confirmed",
          "expired_at": "2026-12-31T23:59:59",
          "created_at": "2026-06-23T20:29:31.226145",
          "updated_by": "MCP",
          "updated_at": "2026-06-23T20:30:15.471319",
          "quotes": [],
          "files": [],
          "bundle": null
        },
        "quote_items": [
          {
            "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
            "quote_item_uuid": "bfa45c83-15eb-433a-8c45-121db36d8b6b",
            "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "batch_no": "DL4822-20260918",
            "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
            "partition_key": "gpt#nestaging",
            "request_data": {
              "cancellation_policy_snapshot": {
                "label": "First Fare Cancellation",
                "tiers": {
                  "tiers": [
                    {
                      "refund_pct": "1",
                      "hours_before_departure_gte": "24"
                    },
                    {
                      "refund_pct": "0.5",
                      "hours_before_departure_gte": "2"
                    },
                    {
                      "refund_pct": "0",
                      "hours_before_departure_gte": "0"
                    }
                  ]
                },
                "description": "Job service instead mention whatever between seek chance back.",
                "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
                "snapshotted_at": "2026-06-23 20:30:25.226978",
                "notes_template_uuid": null
              }
            },
            "price_per_uom": "4500",
            "qty": "2",
            "pax_breakdown": {
              "adult": "2"
            },
            "bundle_uuid": null,
            "bundle_label": null,
            "bundle_component_uuid": null,
            "subtotal": "9000",
            "subtotal_discount": "50",
            "final_subtotal": "9000",
            "currency": null,
            "subtotal_native": "9000",
            "notes": "Integration test discount",
            "hold_token": null,
            "hold_expires_at": null,
            "created_at": "2026-06-23 20:30:25.146670",
            "updated_by": "MCP",
            "updated_at": "2026-06-23 20:30:46.240117"
          }
        ],
        "installments": [
          {
            "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
            "installment_uuid": "b21e8897-936b-4d09-84e3-87c0ee902014",
            "partition_key": "gpt#nestaging",
            "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
            "priority": "0",
            "salesorder_no": null,
            "payment_method": "bank_transfer",
            "scheduled_date": "2026-06-23 20:31:09",
            "installment_ratio": "100",
            "installment_amount": "9025",
            "status": "pending",
            "created_at": "2026-06-23 20:31:11.429245",
            "updated_by": "MCP",
            "updated_at": "2026-06-23 20:31:11.429245"
          }
        ],
        "discount_prompts": [
          {
            "partition_key": "gpt#nestaging",
            "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
            "scope": "global",
            "tags": [],
            "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
            "conditions": [
              "min_passengers >= 20",
              "payment_method in ['wire_transfer', 'credit_card']",
              "is_refundable == false"
            ],
            "discount_rules": [
              {
                "less_than": "10000",
                "greater_than": "0",
                "max_discount_percentage": "5"
              },
              {
                "less_than": "11000",
                "greater_than": "10000",
                "max_discount_percentage": "10"
              },
              {
                "greater_than": "11000",
                "max_discount_percentage": "15"
              }
            ],
            "priority": "6",
            "status": "active",
            "created_at": "2026-06-22 21:14:29.888325",
            "updated_by": "prepare_discount_prompts",
            "updated_at": "2026-06-22 21:14:29.888325"
          },
          {
            "partition_key": "gpt#nestaging",
            "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
            "scope": "global",
            "tags": [],
            "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
            "conditions": [
              "season != 'peak'",
              "channel == 'direct'"
            ],
            "discount_rules": [
              {
                "less_than": "5000",
                "greater_than": "0",
                "max_discount_percentage": "2.5"
              },
              {
                "greater_than": "5000",
                "max_discount_percentage": "5"
              }
            ],
            "priority": "4",
            "status": "active",
            "created_at": "2026-06-22 21:14:29.970326",
            "updated_by": "prepare_discount_prompts",
            "updated_at": "2026-06-22 21:14:29.970326"
          },
          {
            "partition_key": "gpt#nestaging",
            "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
            "scope": "global",
            "tags": [],
            "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
            "conditions": [
              "loyalty_tier in ['gold', 'platinum']",
              "booking_lead_days >= 7"
            ],
            "discount_rules": [
              {
                "less_than": "2500",
                "greater_than": "0",
                "max_discount_percentage": "2.5"
              },
              {
                "less_than": "12500",
                "greater_than": "2500",
                "max_discount_percentage": "7.5"
              },
              {
                "less_than": "22500",
                "greater_than": "12500",
                "max_discount_percentage": "12.5"
              },
              {
                "greater_than": "22500",
                "max_discount_percentage": "17.5"
              }
            ],
            "priority": "1",
            "status": "active",
            "created_at": "2026-06-22 21:14:29.958795",
            "updated_by": "prepare_discount_prompts",
            "updated_at": "2026-06-22 21:14:29.958795"
          }
        ],
        "updated_by": "MCP",
        "created_at": "2026-06-23T20:30:20.308436",
        "updated_at": "2026-06-23T20:31:02.250375"
      }
    }
  ]
}
```

### 24. installments / create_installment

- Method: `_create_installment`
- Status: `pass`
- Elapsed: `6836.13 ms`

Arguments:

```json
{
  "quote_uuid": "c4496c8a-7db1-4ca4-b8c9-bafa8833b52f",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "installment_amount": 100.0,
  "payment_method": "credit_card"
}
```

Output:

```json
{
  "quote_uuid": "c4496c8a-7db1-4ca4-b8c9-bafa8833b52f",
  "installment_uuid": "28d7279d-c924-4df6-8cb1-cdd85e4301a9",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 100.0,
  "installment_ratio": 1.1111111111111112,
  "salesorder_no": null,
  "scheduled_date": "2026-06-23T20:32:07",
  "payment_method": "credit_card",
  "status": "pending",
  "updated_by": "MCP",
  "created_at": "2026-06-23T20:32:09.420512",
  "updated_at": "2026-06-23T20:32:09.420512",
  "quote": null
}
```

### 25. installments / create_installments

- Method: `_create_installments`
- Status: `pass`
- Elapsed: `11408.03 ms`

Arguments:

```json
{
  "quote_uuid": "066b6b9a-ce2c-407b-85b5-6d9a7b0ff5ca",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "interval_num": 3,
  "total_pay_period": 6,
  "payment_method": "bank_transfer"
}
```

Output:

```json
{
  "installments": [
    {
      "quote_uuid": "066b6b9a-ce2c-407b-85b5-6d9a7b0ff5ca",
      "installment_uuid": "8ee1cf28-8c4f-479a-80da-7136aad58c99",
      "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 3000.0,
      "installment_ratio": 33.33333333333333,
      "salesorder_no": null,
      "scheduled_date": "2026-08-15T20:32:14",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-23T20:32:16.262739",
      "updated_at": "2026-06-23T20:32:16.262739",
      "quote": null
    },
    {
      "quote_uuid": "066b6b9a-ce2c-407b-85b5-6d9a7b0ff5ca",
      "installment_uuid": "25f73bc6-5930-4f9b-b01f-7c81e2fe2ba0",
      "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
      "priority": 1,
      "partition_key": "gpt#nestaging",
      "installment_amount": 3000.0,
      "installment_ratio": 33.33333333333333,
      "salesorder_no": null,
      "scheduled_date": "2026-10-15T20:32:14",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-23T20:32:18.522168",
      "updated_at": "2026-06-23T20:32:18.522168",
      "quote": null
    },
    {
      "quote_uuid": "066b6b9a-ce2c-407b-85b5-6d9a7b0ff5ca",
      "installment_uuid": "a7597631-c398-48bf-a586-abae01714c1e",
      "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
      "priority": 2,
      "partition_key": "gpt#nestaging",
      "installment_amount": 3000.0,
      "installment_ratio": 33.33333333333333,
      "salesorder_no": null,
      "scheduled_date": "2026-12-15T20:32:14",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-23T20:32:20.814878",
      "updated_at": "2026-06-23T20:32:20.815388",
      "quote": null
    }
  ],
  "total_created": 3,
  "installment_amount_per": 3000.0,
  "total_installment_amount": 9000.0
}
```

### 26. installments / update_installment (uuid=b21e8897-936...)

- Method: `update_installment`
- Status: `pass`
- Elapsed: `18448.47 ms`

Arguments:

```json
{
  "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
  "installment_uuid": "b21e8897-936b-4d09-84e3-87c0ee902014",
  "status": "paid"
}
```

Output:

```json
{
  "quote_uuid": "fd512189-d8c7-4acd-b158-9e06d2e766da",
  "installment_uuid": "b21e8897-936b-4d09-84e3-87c0ee902014",
  "request_uuid": "f0d31c5e-6d80-4f43-8056-1ff340d17976",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 9025.0,
  "installment_ratio": 100.0,
  "salesorder_no": null,
  "scheduled_date": "2026-06-23T20:31:09",
  "payment_method": "bank_transfer",
  "status": "paid",
  "updated_by": "MCP",
  "created_at": "2026-06-23T20:31:11.429245",
  "updated_at": "2026-06-23T20:32:25.450181",
  "quote": null
}
```

### 27. files / upload_rfq_file

- Method: `upload_rfq_file`
- Status: `pass`
- Elapsed: `2286.91 ms`

Arguments:

```json
{
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
  "file_name": "integration_test_spec.pdf",
  "email": "zbrown@example.org"
}
```

Output:

```json
{
  "file": {
    "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
    "file_name": "integration_test_spec.pdf",
    "email": "zbrown@example.org",
    "partition_key": "gpt#nestaging",
    "request": null,
    "updated_by": "MCP",
    "created_at": "2026-06-23T06:48:47.795038",
    "updated_at": "2026-06-23T20:32:41.609090"
  }
}
```

### 28. files / get_rfq_files

- Method: `get_rfq_files`
- Status: `pass`
- Elapsed: `2263.46 ms`

Arguments:

```json
{
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 1,
  "file_list": [
    {
      "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
      "file_name": "integration_test_spec.pdf",
      "email": "zbrown@example.org",
      "partition_key": "gpt#nestaging",
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
        "email": "zbrown@example.org",
        "request_title": "Business trip NRT to CDG November",
        "request_description": "Business travel for 2 attendee(s) attending offsite meetings in CDG. Prefer Business or Premium Economy to allow productive flight time.",
        "billing_address": {
          "city": "Maxwellhaven",
          "name": "Keith Chen",
          "phone": "001-314-580-8409x8991",
          "state": "LA",
          "street": "079 Karen Skyway",
          "country": "US",
          "postal_code": "50014"
        },
        "shipping_address": {
          "city": "Anaton",
          "name": "John Bradford",
          "phone": "(723)810-6891",
          "state": "AR",
          "street": "95551 Vaughn Villages Apt. 446",
          "country": "US",
          "postal_code": "83528"
        },
        "items": [
          {
            "quantity": "2",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "pax_breakdown": {
              "adult": "2"
            },
            "provider_items": [
              {
                "quantity": "2",
                "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
              }
            ],
            "cabin_preference": "Business"
          }
        ],
        "notes": "Eye kitchen entire member music finish despite letter eight while little win.",
        "bundle_uuid": null,
        "status": "initial",
        "expired_at": "2026-08-18T21:14:31.376040",
        "created_at": "2026-06-22T21:14:31.410885",
        "updated_by": "prepare_requests",
        "updated_at": "2026-06-22T21:14:31.410885",
        "quotes": [
          {
            "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
            "quote_uuid": "9e8378fa-f6b3-4353-bf9a-af2ff6036ff8",
            "provider_corp_external_id": "AIRLINE-DL",
            "sales_rep_email": "terri16@example.com",
            "partition_key": "gpt#nestaging",
            "shipping_method": null,
            "shipping_amount": "0",
            "total_quote_amount": "9000",
            "total_quote_discount": "111",
            "final_total_quote_amount": "8889",
            "currency": "USD",
            "display_currency": null,
            "fx_rate": null,
            "fx_rate_locked_at": null,
            "rounds": "0",
            "notes": "Auto-completed: All installments paid",
            "status": "completed",
            "created_at": "2026-06-22 21:14:32.731930",
            "updated_by": "MCP",
            "updated_at": "2026-06-23 06:54:27.199452"
          }
        ],
        "files": [
          {
            "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
            "file_name": "integration_test_spec.pdf",
            "email": "zbrown@example.org",
            "partition_key": "gpt#nestaging",
            "created_at": "2026-06-23 06:48:47.795038",
            "updated_by": "MCP",
            "updated_at": "2026-06-23 20:32:41.609090"
          }
        ],
        "bundle": null
      },
      "updated_by": "MCP",
      "created_at": "2026-06-23T06:48:47.795038",
      "updated_at": "2026-06-23T20:32:41.609090"
    }
  ]
}
```

### 29. segments / get_segment_contacts

- Method: `get_segment_contacts`
- Status: `pass`
- Elapsed: `2557.95 ms`

Arguments:

```json
{
  "email": "zbrown@example.org",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 1,
  "segment_contact_list": [
    {
      "partition_key": "gpt#nestaging",
      "email": "zbrown@example.org",
      "contact_uuid": null,
      "consumer_corp_external_id": "CUST-7437",
      "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
      "segment": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
        "provider_corp_external_id": "PROV-3980",
        "segment_name": "King Group Tier",
        "segment_description": "Visionary well-modulated moratorium",
        "created_at": "2026-06-22T21:14:24.785967",
        "updated_by": "prepare_segments_and_contacts",
        "updated_at": "2026-06-22T21:14:24.785967",
        "contacts": [
          {
            "partition_key": "gpt#nestaging",
            "email": "tmeyers@example.com",
            "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
            "contact_uuid": null,
            "consumer_corp_external_id": "CUST-5927",
            "created_at": "2026-06-22 21:14:24.897500",
            "updated_by": "prepare_segments_and_contacts",
            "updated_at": "2026-06-22 21:14:24.897500"
          },
          {
            "partition_key": "gpt#nestaging",
            "email": "zwhitaker@example.com",
            "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
            "contact_uuid": null,
            "consumer_corp_external_id": "CUST-5194",
            "created_at": "2026-06-22 21:14:24.912588",
            "updated_by": "prepare_segments_and_contacts",
            "updated_at": "2026-06-22 21:14:24.912588"
          },
          {
            "partition_key": "gpt#nestaging",
            "email": "jason58@example.com",
            "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
            "contact_uuid": null,
            "consumer_corp_external_id": "CUST-2826",
            "created_at": "2026-06-22 21:14:24.924103",
            "updated_by": "prepare_segments_and_contacts",
            "updated_at": "2026-06-22 21:14:24.924103"
          },
          {
            "partition_key": "gpt#nestaging",
            "email": "ortizjoseph@example.com",
            "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
            "contact_uuid": null,
            "consumer_corp_external_id": "CUST-9689",
            "created_at": "2026-06-22 21:14:24.935089",
            "updated_by": "prepare_segments_and_contacts",
            "updated_at": "2026-06-22 21:14:24.935089"
          },
          {
            "partition_key": "gpt#nestaging",
            "email": "zbrown@example.org",
            "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
            "contact_uuid": null,
            "consumer_corp_external_id": "CUST-7437",
            "created_at": "2026-06-22 21:14:24.947242",
            "updated_by": "prepare_segments_and_contacts",
            "updated_at": "2026-06-22 21:14:24.947242"
          }
        ]
      },
      "updated_by": "prepare_segments_and_contacts",
      "created_at": "2026-06-22T21:14:24.947242",
      "updated_at": "2026-06-22T21:14:24.947242"
    }
  ]
}
```

### 30. availability / check_availability

- Method: `check_availability`
- Status: `pass`
- Elapsed: `2271.7 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z",
  "batch_no": "DL4822-20260918",
  "qty": 2
}
```

Output:

```json
{
  "operation": "check",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "batch_no": "DL4822-20260918",
  "service_start_at": "2026-09-18T14:45:00+00:00",
  "service_end_at": "2026-09-18T23:28:08.831283+00:00",
  "available": true,
  "hold_token": null,
  "expires_at": null,
  "payload": {
    "reason": "available",
    "matched_batches": 1,
    "available_batches": 1,
    "total_available_qty": 7.0,
    "slow_move": false
  },
  "fetched_at": "2026-06-23T20:32:48.713509+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 31. availability / acquire_availability_hold

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `2288.71 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z",
  "qty": 2,
  "batch_no": "DL4822-20260918",
  "pax_breakdown": {
    "adult": 2
  }
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": "2026-09-18T14:45:00+00:00",
    "service_end_at": "2026-09-18T23:28:08.831283+00:00",
    "available": true,
    "hold_token": "5d16c14af1df638d7677c01b0404e77d",
    "expires_at": "2026-06-23T20:47:50.987082+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 7.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-23T20:32:51.003080+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 32. availability / confirm_availability_hold

- Method: `confirm_availability_hold`
- Status: `pass`
- Elapsed: `2277.49 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "5d16c14af1df638d7677c01b0404e77d",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "availability": {
    "operation": "confirm_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": null,
    "service_end_at": null,
    "available": true,
    "hold_token": "5d16c14af1df638d7677c01b0404e77d",
    "expires_at": null,
    "payload": {
      "reason": "hold_confirmed"
    },
    "fetched_at": "2026-06-23T20:32:53.280279+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```

### 33. availability / acquire_availability_hold (for release test)

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `2318.86 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z",
  "qty": 1,
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": "2026-09-18T14:45:00+00:00",
    "service_end_at": "2026-09-18T23:28:08.831283+00:00",
    "available": true,
    "hold_token": "092e2155f1badec66992e8a47428801d",
    "expires_at": "2026-06-23T20:47:55.584278+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 5.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-23T20:32:55.599280+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 34. availability / release_availability_hold

- Method: `release_availability_hold`
- Status: `pass`
- Elapsed: `2284.39 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "092e2155f1badec66992e8a47428801d",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "availability": {
    "operation": "release_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": null,
    "service_end_at": null,
    "available": true,
    "hold_token": "092e2155f1badec66992e8a47428801d",
    "expires_at": null,
    "payload": {
      "reason": "hold_released"
    },
    "fetched_at": "2026-06-23T20:32:57.883768+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```

### 35. availability / acquire_availability_hold (for expire test)

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `2267.56 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z",
  "qty": 1,
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": "2026-09-18T14:45:00+00:00",
    "service_end_at": "2026-09-18T23:28:08.831283+00:00",
    "available": true,
    "hold_token": "2b81cece551742462ad390b93d7376a6",
    "expires_at": "2026-06-23T20:48:00.133240+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 5.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-23T20:33:00.151232+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 36. availability / expire_availability_hold

- Method: `expire_availability_hold`
- Status: `pass`
- Elapsed: `2271.13 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "2b81cece551742462ad390b93d7376a6",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "availability": {
    "operation": "expire_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": null,
    "service_end_at": null,
    "available": null,
    "hold_token": null,
    "expires_at": null,
    "payload": null,
    "fetched_at": null,
    "ttl_seconds": null,
    "error_code": "unknown_hold",
    "error_message": "Availability hold has not expired"
  }
}
```

### 37. bundles / search_bundles (itinerary type)

- Method: `search_bundles`
- Status: `pass`
- Elapsed: `2267.63 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_type": "itinerary"
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 0,
  "bundle_list": []
}
```

### 38. bundles / get_bundle (FLT-ITIN-001)

- Method: `get_bundle`
- Status: `pass`
- Elapsed: `2268.22 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
  "bundle_code": "FLT-ITIN-001",
  "bundle_name": "Flight Itinerary CDG->ORD + NRT->BOS + NRT->CDG",
  "bundle_type": "flight_itinerary",
  "description": "Multi-leg flight itinerary template composed of independently priced flight legs.",
  "extra": {
    "routes": [
      "CDG->ORD",
      "NRT->BOS",
      "NRT->CDG"
    ],
    "source": "prepare_flight_products",
    "leg_count": "3",
    "item_external_ids": [
      "FLIGHT-CDG-ORD-ECO",
      "FLIGHT-NRT-BOS-BUS",
      "FLIGHT-NRT-CDG-FIR"
    ]
  },
  "status": "active",
  "created_at": "2026-06-22T21:14:26.931029",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-22T21:14:26.931029",
  "components": [
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "1cb9800a-53ba-44c8-965d-2cc90bb71842",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 3.0,
      "extra": {
        "route": "NRT->CDG",
        "item_external_id": "FLIGHT-NRT-CDG-FIR",
        "provider_item_external_id": "DL-NRT-CDG-FIR"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.048923",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.048923"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "c8ec10e4-f0e2-48bd-aa43-dfcaac88c6c9",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "48d374c4-588d-49b9-a005-36caa41706eb",
      "provider_item_uuid": "d5c08211-7dcf-42fd-8e98-00ac75aba027",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 2.0,
      "extra": {
        "route": "NRT->BOS",
        "item_external_id": "FLIGHT-NRT-BOS-BUS",
        "provider_item_external_id": "CX-NRT-BOS-BUS"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.037290",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.037290"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "19fbf77d-5ce2-4032-b4be-a15cb64917a6",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1",
      "provider_item_uuid": "bad12922-6da1-4117-95ec-5ee0284a5d95",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 1.0,
      "extra": {
        "route": "CDG->ORD",
        "item_external_id": "FLIGHT-CDG-ORD-ECO",
        "provider_item_external_id": "SQ-CDG-ORD-ECO"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.016699",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.016699"
    }
  ]
}
```

### 39. bundles / search_bundle_components

- Method: `search_bundle_components`
- Status: `pass`
- Elapsed: `2273.09 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639"
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 3,
  "bundle_component_list": [
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "1cb9800a-53ba-44c8-965d-2cc90bb71842",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 3.0,
      "extra": {
        "route": "NRT->CDG",
        "item_external_id": "FLIGHT-NRT-CDG-FIR",
        "provider_item_external_id": "DL-NRT-CDG-FIR"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.048923",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.048923"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "c8ec10e4-f0e2-48bd-aa43-dfcaac88c6c9",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "48d374c4-588d-49b9-a005-36caa41706eb",
      "provider_item_uuid": "d5c08211-7dcf-42fd-8e98-00ac75aba027",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 2.0,
      "extra": {
        "route": "NRT->BOS",
        "item_external_id": "FLIGHT-NRT-BOS-BUS",
        "provider_item_external_id": "CX-NRT-BOS-BUS"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.037290",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.037290"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "19fbf77d-5ce2-4032-b4be-a15cb64917a6",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1",
      "provider_item_uuid": "bad12922-6da1-4117-95ec-5ee0284a5d95",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 1.0,
      "extra": {
        "route": "CDG->ORD",
        "item_external_id": "FLIGHT-CDG-ORD-ECO",
        "provider_item_external_id": "SQ-CDG-ORD-ECO"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.016699",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.016699"
    }
  ]
}
```

### 40. cancellation / get_cancellation_policy (Business Fare)

- Method: `get_cancellation_policy`
- Status: `pass`
- Elapsed: `2297.93 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
  "provider_item_uuid": null,
  "label": "First Fare Cancellation",
  "description": "Job service instead mention whatever between seek chance back.",
  "tiers": {
    "tiers": [
      {
        "refund_pct": "1",
        "hours_before_departure_gte": "24"
      },
      {
        "refund_pct": "0.5",
        "hours_before_departure_gte": "2"
      },
      {
        "refund_pct": "0",
        "hours_before_departure_gte": "0"
      }
    ]
  },
  "notes_template_uuid": null,
  "status": "active",
  "created_at": "2026-06-22T21:14:26.847774",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-22T21:14:26.847774"
}
```

### 41. cancellation / search_cancellation_policies

- Method: `search_cancellation_policies`
- Status: `pass`
- Elapsed: `2288.31 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 0,
  "cancellation_policy_list": []
}
```

### 42. catalog / inquire_catalog

- Method: `inquire_catalog`
- Status: `pass`
- Elapsed: `3246.13 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "query_text": "Delta Air Lines NRT CDG First class flight with meal included",
  "namespace": "FLIGHTS",
  "limit": 5
}
```

Output:

```json
{
  "namespace": "FLIGHTS",
  "node_id": null,
  "payload": {
    "results": [
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Delta Air Lines (DL) operates flight service Flight NRT->CDG First from NRT to CDG in First class. First class non-stop service from Tokyo (NRT) to Paris (CDG). Base price $4500.0 USD per seat. Baggage allowance 32kg, meal included: True. Pricing tiers:   - adult: $4500.0 USD;   - child: $3375.0 USD;   - infant: $450.0 USD. Scheduled flights:\n  - Flight DL4000 departing 2026-09-05T21:15:00Z arriving 2026-09-06T08:30:40.740402Z with 7 seats available. Cancellation policy: First Fare Cancellation.\n  - Flight DL4822 departing 2026-09-18T14:45:00Z arriving 2026-09-18T23:28:08.831283Z with 7 seats available. Cancellation policy: First Fare Cancellation.\nThis is a First class flight product offered by Delta Air Lines on the NRT->CDG route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:45",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:45",
          "score": "0.8775168061256409",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Cathay Pacific (CX) operates flight service Flight DFW->CDG Business from DFW to CDG in Business class. Business class non-stop service from Dallas (DFW) to Paris (CDG). Base price $1800.0 USD per seat. Baggage allowance 32kg, meal included: True. Pricing tiers:   - adult: $1800.0 USD;   - child: $1350.0 USD;   - infant: $180.0 USD. Scheduled flights:\n  - Flight CX9953 departing 2026-09-14T17:15:00Z arriving 2026-09-15T01:02:33.438418Z with 31 seats available. Cancellation policy: Business Fare Cancellation.\n  - Flight CX6206 departing 2026-07-23T09:15:00Z arriving 2026-07-23T18:29:38.488182Z with 31 seats available. Cancellation policy: Business Fare Cancellation.\nThis is a Business class flight product offered by Cathay Pacific on the DFW->CDG route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:9",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:9",
          "score": "0.7617387175559998",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight itinerary bundle FLT-ITIN-001 named 'Flight Itinerary CDG->ORD + NRT->BOS + NRT->CDG'. Multi-leg flight itinerary template composed of independently priced flight legs. It contains 3 flight legs:\n  - Leg 1: CDG->ORD\n  - Leg 2: NRT->BOS\n  - Leg 3: NRT->CDG"
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:57",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:57",
          "score": "0.7401881217956543",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight itinerary bundle FLT-ITIN-002 named 'Flight Itinerary NRT->BOS + DFW->CDG + NRT->CDG'. Multi-leg flight itinerary template composed of independently priced flight legs. It contains 3 flight legs:\n  - Leg 1: NRT->BOS\n  - Leg 2: DFW->CDG\n  - Leg 3: NRT->CDG"
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:50",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:50",
          "score": "0.7400848269462585",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Singapore Airlines (SQ) operates flight service Flight CDG->ORD Economy from CDG to ORD in Economy class. Economy class non-stop service from Paris (CDG) to Chicago (ORD). Base price $250.0 USD per seat. Baggage allowance 23kg, meal included: False. Pricing tiers:   - adult: $250.0 USD;   - child: $187.5 USD;   - infant: $25.0 USD. Scheduled flights:\n  - Flight SQ493 departing 2026-08-07T19:30:00Z arriving 2026-08-08T06:44:03.940745Z with 232 seats available. Cancellation policy: Economy Fare Cancellation.\n  - Flight SQ2020 departing 2026-10-18T12:15:00Z arriving 2026-10-18T21:20:33.363503Z with 149 seats available. Cancellation policy: Economy Fare Cancellation.\nThis is a Economy class flight product offered by Singapore Airlines on the CDG->ORD route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:32",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:32",
          "score": "0.7254980206489563",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-23T20:33:17.063833+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```
