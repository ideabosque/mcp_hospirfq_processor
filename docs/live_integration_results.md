# MCP HospiRFQ Processor Live Integration Results

- Generated at: `2026-06-18T04:41:15.180334+00:00`
- Gateway: `http://localhost:8765`
- Endpoint: `gpt`
- Partition: `nestaging`
- GraphQL URL: `http://localhost:8765/gpt/nestaging/ai_rfq_graphql`
- Dependency order: `catalog_discovery, items, requests, quotes, pricing, installments, files, segments, availability, bundles, cancellation, catalog`
- Passed: `42`
- Error responses: `0`
- Failed: `0`
- Total calls: `42`
- SOP reference: `docs/integration_scenarios_sop.md` version `0.1.0`, approved by user on `2026-06-17`
- Final certification status: `Integration Certified`

## Executive Summary

End-to-end live integration testing was executed against the local `silvaengine_gateway` route for `mcp_hospirfq_processor` using `.env`-driven connection settings and prepared `../ai_rfq_engine` flight RFQ data. The final dependency-ordered run completed with 42 passing function calls, 0 error responses, and 0 failures. Catalog search was executed first and selected `Flight ATL->ORD Premium Economy`, which was reconciled to `flight_catalog_refs.json` and `flight_products.json` before item, request, quote, pricing, installment, availability, bundle, cancellation, and catalog validation continued. The SOP-scoped integration is certified for the tested local environment.

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
| `ai_rfq_engine` route | internal | yes | yes | yes | yes | 42 GraphQL-backed function calls passed |
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
| Catalog selection consistency | selected catalog hit maps to `flight_catalog_refs.json` item/provider IDs | 0 mismatches | `06041993713794695296` / `39876487618607726720` selected | pass |
| Batch consistency | selected item/provider maps to `flight_products.json` batch and service window | 0 mismatches | `AF6267-20260912`, `2026-09-12T19:00:00Z` to `2026-09-12T23:07:47.008532Z` | pass |
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
- Elapsed: `6789.07 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "query_text": "Air France ATL ORD Premium Economy flight with meal included",
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
            "text": "Flight product: Flight ATL->ORD Premium Economy. Premium Economy class non-stop service from Atlanta (ATL) to Chicago (ORD). Route: ATL to ORD. Cabin class: Premium Economy. Operated by: Air France (AF). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 450.0, child USD 337.5, infant USD 45.0. Scheduled flights: AF6267 departing 2026-09-12T19:00:00Z, 52 seats; AF5319 departing 2026-09-07T12:00:00Z, 37 seats. Premium Economy Fare Cancellation: 168h+: 100% refund; 24h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary DFW->SIN + ATL->ORD + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:25",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:25",
          "score": "0.8713676929473877",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight ATL->ORD Economy. Economy class non-stop service from Atlanta (ATL) to Chicago (ORD). Route: ATL to ORD. Cabin class: Economy. Operated by: Qantas (QF). Baggage allowance: 23 kg. Meal included: no. Fares: adult USD 250.0, child USD 187.5, infant USD 25.0. Scheduled flights: QF1351 departing 2026-07-09T21:45:00Z, 145 seats; QF5796 departing 2026-09-21T19:45:00Z, 169 seats. Economy Fare Cancellation: 168h+: 100% refund; 24h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:17",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:17",
          "score": "0.7910864353179932",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight CDG->JFK Business. Business class non-stop service from Paris (CDG) to New York (JFK). Route: CDG to JFK. Cabin class: Business. Operated by: Air France (AF). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 1800.0, child USD 1350.0, infant USD 180.0. Scheduled flights: AF8751 departing 2026-08-11T08:30:00Z, 30 seats; AF5020 departing 2026-06-16T08:30:00Z, 22 seats. Business Fare Cancellation: 24h+: 100% refund; 2h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary DFW->SIN + ATL->ORD + CDG->JFK, Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:1",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:1",
          "score": "0.7605776190757751",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight LAX->HKG Premium Economy. Premium Economy class non-stop service from Los Angeles (LAX) to Hong Kong (HKG). Route: LAX to HKG. Cabin class: Premium Economy. Operated by: Lufthansa (LH). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 450.0, child USD 337.5, infant USD 45.0. Scheduled flights: LH6452 departing 2026-08-01T21:15:00Z, 34 seats; LH3684 departing 2026-09-26T20:45:00Z, 41 seats. Premium Economy Fare Cancellation: 168h+: 100% refund; 24h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:33",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:33",
          "score": "0.7334754467010498",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight DFW->SIN Business. Business class non-stop service from Dallas (DFW) to Singapore (SIN). Route: DFW to SIN. Cabin class: Business. Operated by: Singapore Airlines (SQ). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 1800.0, child USD 1350.0, infant USD 180.0. Scheduled flights: SQ6901 departing 2026-08-12T13:45:00Z, 33 seats; SQ8511 departing 2026-09-26T19:15:00Z, 30 seats. Business Fare Cancellation: 24h+: 100% refund; 2h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary DFW->SIN + ATL->ORD + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:9",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:9",
          "score": "0.6800907850265503",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-18T04:34:42.872126+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 2. items / search_items (flight type)

- Method: `search_items`
- Status: `pass`
- Elapsed: `3435.57 ms`

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
  "page_size": 10,
  "page_number": 1,
  "total": 5,
  "item_list": [
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "06041993713794695296",
      "item_type": "flight",
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_description": "Premium Economy class non-stop service from Atlanta (ATL) to Chicago (ORD).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-ATL-ORD-PRE",
      "created_at": "2026-06-01T22:19:29.788924",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:29.788924"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "52065619693805781120",
      "item_type": "flight",
      "item_name": "Flight ATL->ORD Economy",
      "item_description": "Economy class non-stop service from Atlanta (ATL) to Chicago (ORD).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-ATL-ORD-ECO",
      "created_at": "2026-06-01T22:19:27.899069",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:27.899069"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "15269325584579182720",
      "item_type": "flight",
      "item_name": "Flight DFW->SIN Business",
      "item_description": "Business class non-stop service from Dallas (DFW) to Singapore (SIN).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-DFW-SIN-BUS",
      "created_at": "2026-06-01T22:19:25.988874",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:25.988874"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "17735923656909930624",
      "item_type": "flight",
      "item_name": "Flight CDG->JFK Business",
      "item_description": "Business class non-stop service from Paris (CDG) to New York (JFK).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-CDG-JFK-BUS",
      "created_at": "2026-06-01T22:19:23.947293",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:23.947293"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "97838712287656951936",
      "item_type": "flight",
      "item_name": "Flight LAX->HKG Premium Economy",
      "item_description": "Premium Economy class non-stop service from Los Angeles (LAX) to Hong Kong (HKG).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-LAX-HKG-PRE",
      "created_at": "2026-06-01T22:19:31.515429",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:31.515429"
    }
  ]
}
```

### 3. items / get_item (Flight ATL->ORD Premium Economy)

- Method: `get_item`
- Status: `pass`
- Elapsed: `3324.36 ms`

Arguments:

```json
{
  "item_uuid": "06041993713794695296"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "item_uuid": "06041993713794695296",
  "item_type": "flight",
  "item_name": "Flight ATL->ORD Premium Economy",
  "item_description": "Premium Economy class non-stop service from Atlanta (ATL) to Chicago (ORD).",
  "pricing_mode": "per_pax_type",
  "uom": "seat",
  "item_external_id": "FLIGHT-ATL-ORD-PRE",
  "created_at": "2026-06-01T22:19:29.788924",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-01T22:19:29.788924"
}
```

### 4. items / get_provider_items (with batches)

- Method: `get_provider_items`
- Status: `pass`
- Elapsed: `6901.26 ms`

Arguments:

```json
{
  "item_uuid": "06041993713794695296"
}
```

Output:

```json
{
  "page_size": 50,
  "page_number": 1,
  "total": 1,
  "provider_item_list": [
    {
      "partition_key": "gpt#nestaging",
      "provider_item_uuid": "39876487618607726720",
      "provider_corp_external_id": "AIRLINE-AF",
      "provider_item_external_id": "AF-ATL-ORD-PRE",
      "base_price_per_uom": 450.0,
      "item_spec": {
        "cabin_class": "Premium Economy",
        "meal_included": true,
        "destination_iata": "ORD",
        "airline_code": "AF",
        "origin_iata": "ATL",
        "airline_name": "Air France",
        "baggage_allowance_kg": "32"
      },
      "availability_mode": "require_hold",
      "item_uuid": "06041993713794695296",
      "item": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "item_uuid": "06041993713794695296",
        "item_type": "flight",
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_description": "Premium Economy class non-stop service from Atlanta (ATL) to Chicago (ORD).",
        "pricing_mode": "per_pax_type",
        "uom": "seat",
        "item_external_id": "FLIGHT-ATL-ORD-PRE",
        "created_at": "2026-06-01T22:19:29.788924",
        "updated_by": "prepare_flight_products",
        "updated_at": "2026-06-01T22:19:29.788924"
      },
      "updated_by": "prepare_flight_products",
      "created_at": "2026-06-01T22:19:30.213419",
      "updated_at": "2026-06-01T22:19:30.213419",
      "batches": []
    }
  ]
}
```

### 5. requests / submit_rfq_request

- Method: `submit_rfq_request`
- Status: `pass`
- Elapsed: `3845.11 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy",
  "request_description": "E2E test request via silvaengine_gateway",
  "items": [
    {
      "item_uuid": "06041993713794695296",
      "item_name": "Flight ATL->ORD Premium Economy",
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
  "request_uuid": "03524304194674638976",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Created by run_integration.py",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T04:34:59.987127",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T04:34:59.987127",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 6. requests / get_rfq_request (seeded)

- Method: `get_rfq_request`
- Status: `pass`
- Elapsed: `3480.62 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "96306650268729098368",
  "email": "jessicacooper@example.com",
  "request_title": "Honeymoon to ORD (updated by integration test)",
  "request_description": "Honeymoon trip for 2 adults. Open to splurge on the outbound in Business if pricing is reasonable.",
  "billing_address": {
    "country": "US",
    "city": "West Amy",
    "phone": "+1-287-493-0405x186",
    "street": "8532 Hernandez Ports",
    "name": "Heidi Garza",
    "state": "MA",
    "postal_code": "40901"
  },
  "shipping_address": {
    "country": "US",
    "city": "Lake Nathanside",
    "phone": "+1-494-213-4598",
    "street": "6159 Joyce Coves Suite 945",
    "name": "Mitchell Carrillo",
    "state": "WY",
    "postal_code": "72270"
  },
  "items": [
    {
      "cabin_preference": "Premium Economy",
      "quantity": "2",
      "item_uuid": "06041993713794695296",
      "provider_items": [],
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "completed",
  "expired_at": "2026-07-25T22:41:32.314663",
  "created_at": "2026-06-01T22:41:32.471123",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T04:32:56.070316",
  "quotes": [
    {
      "final_total_quote_amount": "0",
      "provider_corp_external_id": "AIRLINE-AF",
      "rounds": "0",
      "shipping_amount": "0",
      "status": "disapproved",
      "total_quote_amount": "0",
      "total_quote_discount": "0",
      "created_at": "2026-06-17 19:10:34.347670",
      "notes": "Auto-disapproved: Another quote was confirmed",
      "partition_key": "gpt#nestaging",
      "quote_uuid": "12616028676071374976",
      "request_uuid": "96306650268729098368",
      "updated_at": "2026-06-17 19:12:07.004383",
      "updated_by": "MCP"
    },
    {
      "final_total_quote_amount": "0",
      "provider_corp_external_id": "AIRLINE-LH",
      "rounds": "0",
      "shipping_amount": "0",
      "status": "disapproved",
      "total_quote_amount": "0",
      "total_quote_discount": "0",
      "created_at": "2026-06-01 22:43:00.075462",
      "currency": "USD",
      "display_currency": "CAD",
      "fx_rate": "1.335005",
      "fx_rate_locked_at": "2026-06-01 22:42:59.985871",
      "notes": "Auto-disapproved: Another quote was confirmed",
      "partition_key": "gpt#nestaging",
      "quote_uuid": "42458963099238023296",
      "request_uuid": "96306650268729098368",
      "sales_rep_email": "kimberly71@example.org",
      "updated_at": "2026-06-17 19:11:59.548180",
      "updated_by": "MCP"
    },
    {
      "final_total_quote_amount": "25",
      "provider_corp_external_id": "AIRLINE-QF",
      "rounds": "0",
      "shipping_amount": "25",
      "status": "completed",
      "total_quote_amount": "0",
      "total_quote_discount": "0",
      "created_at": "2026-06-01 22:42:59.864855",
      "currency": "USD",
      "display_currency": "CNY",
      "fx_rate": "7.081345",
      "fx_rate_locked_at": "2026-06-01 22:42:59.540604",
      "notes": "Auto-completed: All installments paid",
      "partition_key": "gpt#nestaging",
      "quote_uuid": "83893620897501692032",
      "request_uuid": "96306650268729098368",
      "sales_rep_email": "jordan99@example.net",
      "shipping_method": "ticket_delivery",
      "updated_at": "2026-06-18 04:32:44.719388",
      "updated_by": "MCP"
    }
  ],
  "files": [
    {
      "created_at": "2026-06-17 19:11:33.981790",
      "email": "jessicacooper@example.com",
      "file_name": "integration_test_spec.pdf",
      "partition_key": "gpt#nestaging",
      "request_uuid": "96306650268729098368",
      "updated_at": "2026-06-18 04:32:59.754592",
      "updated_by": "MCP"
    }
  ],
  "bundle": null
}
```

### 7. requests / search_rfq_requests

- Method: `search_rfq_requests`
- Status: `pass`
- Elapsed: `4062.71 ms`

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
  "page_size": 5,
  "page_number": 1,
  "total": 23,
  "request_list": [
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "87119168162060320896",
      "email": "beannorma@example.com",
      "request_title": "Honeymoon to ORD",
      "request_description": "Honeymoon trip for 2 adults. Open to splurge on the outbound in Business if pricing is reasonable.",
      "billing_address": {
        "country": "US",
        "city": "East Cheyennemouth",
        "phone": "491-252-8236x931",
        "street": "885 Collins Avenue",
        "name": "Jason Guzman",
        "state": "NJ",
        "postal_code": "23488"
      },
      "shipping_address": {
        "country": "US",
        "city": "South Loriton",
        "phone": "266-439-8592",
        "street": "899 Morgan Lodge Apt. 070",
        "name": "Bryan King",
        "state": "MT",
        "postal_code": "87031"
      },
      "items": [
        {
          "cabin_preference": "Economy",
          "bundle_component_uuid": "80197043753719971968",
          "quantity": "2",
          "item_uuid": "52065619693805781120",
          "provider_items": [
            {
              "provider_item_uuid": "94764066649319424128",
              "quantity": "2"
            }
          ],
          "pax_breakdown": {
            "adult": "2"
          }
        },
        {
          "cabin_preference": "Economy",
          "bundle_component_uuid": "26138792054410461312",
          "quantity": "2",
          "item_uuid": "97838712287656951936",
          "provider_items": [
            {
              "provider_item_uuid": "93970690058365190272",
              "quantity": "2"
            }
          ],
          "pax_breakdown": {
            "adult": "2"
          }
        },
        {
          "cabin_preference": "Economy",
          "bundle_component_uuid": "05615016170826514560",
          "quantity": "2",
          "item_uuid": "17735923656909930624",
          "provider_items": [
            {
              "provider_item_uuid": "55349863084404523136",
              "quantity": "2",
              "batch_no": "AF5020-20260616"
            }
          ],
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Technology bar question military because away whole draw build worker star.",
      "bundle_uuid": "49956565412585947264",
      "status": "initial",
      "expired_at": "2026-07-06T22:41:32.864151",
      "created_at": "2026-06-01T22:41:33.316535",
      "updated_by": "prepare_requests",
      "updated_at": "2026-06-01T22:41:33.316535",
      "quotes": [
        {
          "final_total_quote_amount": "950",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "0",
          "shipping_amount": "0",
          "status": "initial",
          "total_quote_amount": "1000",
          "total_quote_discount": "50",
          "created_at": "2026-06-01 22:43:00.287972",
          "currency": "USD",
          "notes": "Future I industry school significant sea to month avoid serve much anyone box wall song.",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "51485446173562519680",
          "request_uuid": "87119168162060320896",
          "sales_rep_email": "williamsgary@example.net",
          "updated_at": "2026-06-17 20:17:20.488195",
          "updated_by": "prepare_quotes"
        }
      ],
      "files": [],
      "bundle": {
        "partition_key": "gpt#nestaging",
        "bundle_uuid": "49956565412585947264",
        "bundle_code": "FLT-ITIN-002",
        "bundle_name": "Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK",
        "bundle_type": "flight_itinerary",
        "description": "Multi-leg flight itinerary template composed of independently priced flight legs.",
        "extra": {
          "routes": [
            "ATL->ORD",
            "LAX->HKG",
            "CDG->JFK"
          ],
          "source": "prepare_flight_products",
          "leg_count": "3",
          "item_external_ids": [
            "FLIGHT-ATL-ORD-ECO",
            "FLIGHT-LAX-HKG-PRE",
            "FLIGHT-CDG-JFK-BUS"
          ]
        },
        "status": "active",
        "created_at": "2026-06-01T22:19:34.512270",
        "updated_by": "prepare_flight_products",
        "updated_at": "2026-06-01T22:19:34.512270",
        "components": [
          {
            "partition_key": "gpt#nestaging",
            "bundle_component_uuid": "80197043753719971968",
            "bundle_uuid": "49956565412585947264",
            "item_uuid": "52065619693805781120",
            "provider_item_uuid": "94764066649319424128",
            "component_role": "flight_leg",
            "required": true,
            "default_qty": 1.0,
            "sort_order": 1.0,
            "extra": {
              "route": "ATL->ORD",
              "item_external_id": "FLIGHT-ATL-ORD-ECO",
              "provider_item_external_id": "QF-ATL-ORD-ECO"
            },
            "status": "active",
            "created_at": "2026-06-01T22:19:34.949372",
            "updated_by": "prepare_flight_products",
            "updated_at": "2026-06-01T22:19:34.949372"
          },
          {
            "partition_key": "gpt#nestaging",
            "bundle_component_uuid": "26138792054410461312",
            "bundle_uuid": "49956565412585947264",
            "item_uuid": "97838712287656951936",
            "provider_item_uuid": "93970690058365190272",
            "component_role": "flight_leg",
            "required": true,
            "default_qty": 1.0,
            "sort_order": 2.0,
            "extra": {
              "route": "LAX->HKG",
              "item_external_id": "FLIGHT-LAX-HKG-PRE",
              "provider_item_external_id": "LH-LAX-HKG-PRE"
            },
            "status": "active",
            "created_at": "2026-06-01T22:19:35.230969",
            "updated_by": "prepare_flight_products",
            "updated_at": "2026-06-01T22:19:35.230969"
          },
          {
            "partition_key": "gpt#nestaging",
            "bundle_component_uuid": "05615016170826514560",
            "bundle_uuid": "49956565412585947264",
            "item_uuid": "17735923656909930624",
            "provider_item_uuid": "55349863084404523136",
            "component_role": "flight_leg",
            "required": true,
            "default_qty": 1.0,
            "sort_order": 3.0,
            "extra": {
              "route": "CDG->JFK",
              "item_external_id": "FLIGHT-CDG-JFK-BUS",
              "provider_item_external_id": "AF-CDG-JFK-BUS"
            },
            "status": "active",
            "created_at": "2026-06-01T22:19:35.518661",
            "updated_by": "prepare_flight_products",
            "updated_at": "2026-06-01T22:19:35.518661"
          }
        ]
      }
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "74921795627915427968",
      "email": "beannorma@example.com",
      "request_title": "Business trip LAX to HKG November",
      "request_description": "Business travel for 2 attendee(s) attending offsite meetings in HKG. Prefer Business or Premium Economy to allow productive flight time.",
      "billing_address": {
        "country": "US",
        "city": "Jamesport",
        "phone": "975.274.0279x15049",
        "street": "721 Theresa Crescent Apt. 105",
        "name": "Candace Nelson",
        "state": "AZ",
        "postal_code": "60136"
      },
      "shipping_address": {
        "country": "US",
        "city": "Port Michael",
        "phone": "700-444-5957x3273",
        "street": "392 Daniel Brook",
        "name": "Jennifer Walker",
        "state": "MP",
        "postal_code": "73736"
      },
      "items": [
        {
          "cabin_preference": "Premium Economy",
          "quantity": "2",
          "item_uuid": "97838712287656951936",
          "provider_items": [
            {
              "provider_item_uuid": "93970690058365190272",
              "quantity": "2"
            }
          ],
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Outside year industry officer wall month teacher performance site smile add beat first.",
      "bundle_uuid": null,
      "status": "initial",
      "expired_at": "2026-08-12T22:41:33.608681",
      "created_at": "2026-06-01T22:41:33.752676",
      "updated_by": "prepare_requests",
      "updated_at": "2026-06-01T22:41:33.752676",
      "quotes": [
        {
          "final_total_quote_amount": "0",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "0",
          "shipping_amount": "34.09",
          "status": "initial",
          "total_quote_amount": "0",
          "total_quote_discount": "0",
          "created_at": "2026-06-01 22:43:01.039803",
          "currency": "USD",
          "display_currency": "JPY",
          "fx_rate": "153.416905",
          "fx_rate_locked_at": "2026-06-01 22:43:00.600322",
          "notes": "Relationship us girl common market teacher like.",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "31038949121456095360",
          "request_uuid": "74921795627915427968",
          "sales_rep_email": "elizabeth68@example.net",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-01 22:43:01.039803",
          "updated_by": "prepare_quotes"
        },
        {
          "final_total_quote_amount": "1800",
          "provider_corp_external_id": "AIRLINE-LH",
          "rounds": "0",
          "shipping_amount": "0",
          "status": "initial",
          "total_quote_amount": "1800",
          "total_quote_discount": "0",
          "created_at": "2026-06-01 22:43:00.494956",
          "currency": "USD",
          "notes": "Try member magazine campaign among owner far return best lot today expect song source perform.",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "98513172062733877376",
          "request_uuid": "74921795627915427968",
          "sales_rep_email": "patriciareed@example.com",
          "updated_at": "2026-06-01 22:46:23.305644",
          "updated_by": "prepare_quotes"
        }
      ],
      "files": [],
      "bundle": null
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "46915773638499123328",
      "email": "jessicacooper@example.com",
      "request_title": "Business trip ATL to ORD August",
      "request_description": "Business travel for 1 attendee(s) attending offsite meetings in ORD. Prefer Business or Premium Economy to allow productive flight time.",
      "billing_address": {
        "country": "US",
        "city": "Lake John",
        "phone": "4207609557",
        "street": "974 Janet Rue Suite 436",
        "name": "Jacqueline Burgess",
        "state": "OH",
        "postal_code": "92451"
      },
      "shipping_address": {
        "country": "US",
        "city": "Kimberlyshire",
        "phone": "3918134809",
        "street": "65959 Tony Manors",
        "name": "Christopher Swanson",
        "state": "AS",
        "postal_code": "65311"
      },
      "items": [
        {
          "cabin_preference": "Premium Economy",
          "quantity": "1",
          "item_uuid": "06041993713794695296",
          "provider_items": [
            {
              "provider_item_uuid": "39876487618607726720",
              "quantity": "1"
            }
          ],
          "pax_breakdown": {
            "adult": "1"
          }
        }
      ],
      "notes": "Leave administration well exactly she nice bed trade maintain know.",
      "bundle_uuid": null,
      "status": "initial",
      "expired_at": "2026-08-30T22:41:34.072125",
      "created_at": "2026-06-01T22:41:34.211289",
      "updated_by": "prepare_requests",
      "updated_at": "2026-06-01T22:41:34.211289",
      "
... (truncated)
```

### 8. requests / update_rfq_request

- Method: `update_rfq_request`
- Status: `pass`
- Elapsed: `7270.87 ms`

Arguments:

```json
{
  "request_uuid": "03524304194674638976",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "notes": "Updated via run_integration.py"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "03524304194674638976",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T04:34:59.987127",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T04:35:14.796479",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 9. requests / add_item_to_rfq_request

- Method: `add_item_to_rfq_request`
- Status: `pass`
- Elapsed: `7425.88 ms`

Arguments:

```json
{
  "request_uuid": "03524304194674638976",
  "item": {
    "item_uuid": "52065619693805781120",
    "item_name": "Flight ATL->ORD Economy",
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
  "request_uuid": "03524304194674638976",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    },
    {
      "item_name": "Flight ATL->ORD Economy",
      "item_uuid": "52065619693805781120",
      "provider_items": [],
      "qty": "1"
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T04:34:59.987127",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T04:35:22.238324",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 10. requests / remove_item_from_rfq_request

- Method: `remove_item_from_rfq_request`
- Status: `pass`
- Elapsed: `7599.28 ms`

Arguments:

```json
{
  "request_uuid": "03524304194674638976",
  "item_uuid": "52065619693805781120"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "03524304194674638976",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T04:34:59.987127",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T04:35:29.820721",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 11. requests / assign_provider_item_to_request_item

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `11273.95 ms`

Arguments:

```json
{
  "request_uuid": "03524304194674638976",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720",
  "provider_corp_external_id": "AIRLINE-AF",
  "qty": 2,
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "03524304194674638976",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "provider_items": [
        {
          "provider_item_uuid": "39876487618607726720",
          "provider_corp_external_id": "AIRLINE-AF",
          "batch_no": "AF6267-20260912",
          "qty": "2"
        }
      ],
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T04:34:59.987127",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T04:35:41.108976",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 12. requests / remove_provider_item_from_request_item

- Method: `remove_provider_item_from_request_item`
- Status: `pass`
- Elapsed: `8415.8 ms`

Arguments:

```json
{
  "request_uuid": "03524304194674638976",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "03524304194674638976",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "provider_items": [],
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T04:34:59.987127",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T04:35:49.493640",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 13. requests / assign_provider_item_to_request_item (for quote workflow)

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `10975.59 ms`

Arguments:

```json
{
  "request_uuid": "03524304194674638976",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720",
  "provider_corp_external_id": "AIRLINE-AF",
  "qty": 2,
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "03524304194674638976",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "provider_items": [
        {
          "provider_item_uuid": "39876487618607726720",
          "provider_corp_external_id": "AIRLINE-AF",
          "batch_no": "AF6267-20260912",
          "qty": "2"
        }
      ],
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T04:34:59.987127",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T04:36:00.508754",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 14. quotes / confirm_request_and_create_quotes

- Method: `confirm_request_and_create_quotes`
- Status: `pass`
- Elapsed: `39996.53 ms`

Arguments:

```json
{
  "request_uuid": "03524304194674638976",
  "provider_corp_external_ids": [
    "AIRLINE-AF"
  ],
  "segment_uuid": "61268299727527493760",
  "batch_no": "AF6267-20260912",
  "service_start_at": "2026-09-12T19:00:00Z",
  "service_end_at": "2026-09-12T23:07:47.008532Z"
}
```

Output:

```json
{
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "03524304194674638976",
    "email": "jessicacooper@example.com",
    "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_uuid": "06041993713794695296",
        "provider_items": [
          {
            "provider_item_uuid": "39876487618607726720",
            "provider_corp_external_id": "AIRLINE-AF",
            "batch_no": "AF6267-20260912",
            "qty": "2"
          }
        ],
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        }
      }
    ],
    "notes": "Updated via run_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-18T04:34:59.987127",
    "updated_by": "MCP",
    "updated_at": "2026-06-18T04:36:11.492477",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "created_quotes": [
    {
      "request_uuid": "03524304194674638976",
      "quote_uuid": "33381958003215843456",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-AF",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 900.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 900.0,
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
        "request_uuid": "03524304194674638976",
        "email": "jessicacooper@example.com",
        "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
        "request_description": "E2E test request via silvaengine_gateway",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "item_name": "Flight ATL->ORD Premium Economy",
            "item_uuid": "06041993713794695296",
            "provider_items": [
              {
                "provider_item_uuid": "39876487618607726720",
                "provider_corp_external_id": "AIRLINE-AF",
                "batch_no": "AF6267-20260912",
                "qty": "2"
              }
            ],
            "qty": "2",
            "pax_breakdown": {
              "adult": "2"
            }
          }
        ],
        "notes": "Updated via run_integration.py",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-18T04:34:59.987127",
        "updated_by": "MCP",
        "updated_at": "2026-06-18T04:36:11.492477",
        "quotes": [
          {
            "final_total_quote_amount": "900",
            "provider_corp_external_id": "AIRLINE-AF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "in_progress",
            "total_quote_amount": "900",
            "total_quote_discount": "0",
            "created_at": "2026-06-18 04:36:18.984795",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "33381958003215843456",
            "request_uuid": "03524304194674638976",
            "updated_at": "2026-06-18 04:36:36.383032",
            "updated_by": "MCP"
          }
        ],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "batch_no": "AF6267-20260912",
          "created_at": "2026-06-18 04:36:26.864931",
          "final_subtotal": "900",
          "hold_expires_at": "2026-06-18 04:51:27.231810",
          "hold_token": "b7f0d809f2652ff3b85a59b9549dbef2",
          "item_uuid": "06041993713794695296",
          "partition_key": "gpt#nestaging",
          "pax_breakdown": {
            "adult": "2"
          },
          "price_per_uom": "450",
          "provider_item_uuid": "39876487618607726720",
          "qty": "2",
          "quote_item_uuid": "99624906928751132800",
          "quote_uuid": "33381958003215843456",
          "request_data": {
            "cancellation_policy_snapshot": {
              "tiers": {
                "tiers": [
                  {
                    "hours_before_departure_gte": "168",
                    "refund_pct": "1"
                  },
                  {
                    "hours_before_departure_gte": "24",
                    "refund_pct": "0.5"
                  },
                  {
                    "hours_before_departure_gte": "0",
                    "refund_pct": "0"
                  }
                ]
              },
              "notes_template_uuid": null,
              "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
              "label": "Premium Economy Fare Cancellation",
              "content_hash": "b161d765b3089e5e",
              "policy_uuid": "14167382355785826432",
              "snapshotted_at": "2026-06-18 04:36:27.479155"
            }
          },
          "request_uuid": "03524304194674638976",
          "subtotal": "900",
          "subtotal_discount": "0",
          "subtotal_native": "900",
          "updated_at": "2026-06-18 04:36:26.864931",
          "updated_by": "MCP"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "priority": "10",
          "status": "active",
          "conditions": [
            "is_refundable == false",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.614708",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
          "discount_prompt_uuid": "29118858989597114496",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "2.5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.614708",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'",
            "min_passengers >= 20",
            "loyalty_tier in ['gold', 'platinum']"
          ],
          "created_at": "2026-06-01 22:24:16.312582",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
          "discount_prompt_uuid": "39743702329131548800",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "5000"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.312582",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "7",
          "status": "active",
          "conditions": [
            "min_passengers >= 20",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.462599",
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
          "discount_prompt_uuid": "34741236891406844032",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "1000"
            },
            {
              "greater_than": "1000",
              "max_discount_percentage": "10",
              "less_than": "3500"
            },
            {
              "greater_than": "3500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.462599",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "6",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "min_passengers >= 10",
            "is_refundable == false"
          ],
          "created_at": "2026-06-01 22:24:16.923030",
          "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
          "discount_prompt_uuid": "81566856437527756928",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "500"
            },
            {
              "greater_than": "500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "segment",
          "tags": [
            "61268299727527493760"
          ],
          "updated_at": "2026-06-01 22:24:16.923030",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "5",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:18.730783",
          "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
          "discount_prompt_uuid": "87759969798493061248",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "2500"
            },
            {
              "greater_than": "2500",
              "max_discount_percentage": "10",
              "less_than": "7500"
            },
            {
              "greater_than": "7500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "item",
          "tags": [
            "06041993713794695296"
          ],
          "updated_at": "2026-06-01 22:24:18.730783",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'"
          ],
          "created_at": "2026-06-01 22:24:18.882404",
          "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
          "discount_prompt_uuid": "88308794075899773056",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5",
              "less_than": "20000"
            },
            {
              "greater_than": "20000",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "provider_item",
          "tags": [
         
... (truncated)
```

### 15. quotes / get_quote

- Method: `get_quote`
- Status: `pass`
- Elapsed: `3994.75 ms`

Arguments:

```json
{
  "quote_uuid": "33381958003215843456",
  "request_uuid": "03524304194674638976"
}
```

Output:

```json
{
  "request_uuid": "03524304194674638976",
  "quote_uuid": "33381958003215843456",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-AF",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": null,
  "shipping_amount": 0.0,
  "total_quote_amount": 900.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 900.0,
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
    "request_uuid": "03524304194674638976",
    "email": "jessicacooper@example.com",
    "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_uuid": "06041993713794695296",
        "provider_items": [
          {
            "provider_item_uuid": "39876487618607726720",
            "provider_corp_external_id": "AIRLINE-AF",
            "batch_no": "AF6267-20260912",
            "qty": "2"
          }
        ],
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        }
      }
    ],
    "notes": "Updated via run_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-18T04:34:59.987127",
    "updated_by": "MCP",
    "updated_at": "2026-06-18T04:36:11.492477",
    "quotes": [
      {
        "final_total_quote_amount": "900",
        "provider_corp_external_id": "AIRLINE-AF",
        "rounds": "0",
        "shipping_amount": "0",
        "status": "in_progress",
        "total_quote_amount": "900",
        "total_quote_discount": "0",
        "created_at": "2026-06-18 04:36:18.984795",
        "partition_key": "gpt#nestaging",
        "quote_uuid": "33381958003215843456",
        "request_uuid": "03524304194674638976",
        "updated_at": "2026-06-18 04:36:36.383032",
        "updated_by": "MCP"
      }
    ],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "batch_no": "AF6267-20260912",
      "created_at": "2026-06-18 04:36:26.864931",
      "final_subtotal": "900",
      "hold_expires_at": "2026-06-18 04:51:27.231810",
      "hold_token": "b7f0d809f2652ff3b85a59b9549dbef2",
      "item_uuid": "06041993713794695296",
      "partition_key": "gpt#nestaging",
      "pax_breakdown": {
        "adult": "2"
      },
      "price_per_uom": "450",
      "provider_item_uuid": "39876487618607726720",
      "qty": "2",
      "quote_item_uuid": "99624906928751132800",
      "quote_uuid": "33381958003215843456",
      "request_data": {
        "cancellation_policy_snapshot": {
          "tiers": {
            "tiers": [
              {
                "hours_before_departure_gte": "168",
                "refund_pct": "1"
              },
              {
                "hours_before_departure_gte": "24",
                "refund_pct": "0.5"
              },
              {
                "hours_before_departure_gte": "0",
                "refund_pct": "0"
              }
            ]
          },
          "notes_template_uuid": null,
          "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
          "label": "Premium Economy Fare Cancellation",
          "content_hash": "b161d765b3089e5e",
          "policy_uuid": "14167382355785826432",
          "snapshotted_at": "2026-06-18 04:36:27.479155"
        }
      },
      "request_uuid": "03524304194674638976",
      "subtotal": "900",
      "subtotal_discount": "0",
      "subtotal_native": "900",
      "updated_at": "2026-06-18 04:36:26.864931",
      "updated_by": "MCP"
    }
  ],
  "installments": [],
  "discount_prompts": [
    {
      "priority": "10",
      "status": "active",
      "conditions": [
        "is_refundable == false",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.614708",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
      "discount_prompt_uuid": "29118858989597114496",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.614708",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'",
        "min_passengers >= 20",
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "created_at": "2026-06-01 22:24:16.312582",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
      "discount_prompt_uuid": "39743702329131548800",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "5000"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.312582",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "7",
      "status": "active",
      "conditions": [
        "min_passengers >= 20",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.462599",
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
      "discount_prompt_uuid": "34741236891406844032",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "10",
          "less_than": "3500"
        },
        {
          "greater_than": "3500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.462599",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "6",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "min_passengers >= 10",
        "is_refundable == false"
      ],
      "created_at": "2026-06-01 22:24:16.923030",
      "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
      "discount_prompt_uuid": "81566856437527756928",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "500"
        },
        {
          "greater_than": "500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "segment",
      "tags": [
        "61268299727527493760"
      ],
      "updated_at": "2026-06-01 22:24:16.923030",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "5",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:18.730783",
      "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
      "discount_prompt_uuid": "87759969798493061248",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "10",
          "less_than": "7500"
        },
        {
          "greater_than": "7500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "item",
      "tags": [
        "06041993713794695296"
      ],
      "updated_at": "2026-06-01 22:24:18.730783",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'"
      ],
      "created_at": "2026-06-01 22:24:18.882404",
      "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
      "discount_prompt_uuid": "88308794075899773056",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5",
          "less_than": "20000"
        },
        {
          "greater_than": "20000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "provider_item",
      "tags": [
        "39876487618607726720"
      ],
      "updated_at": "2026-06-01 22:24:18.882404",
      "updated_by": "prepare_discount_prompts"
    }
  ],
  "updated_by": "MCP",
  "created_at": "2026-06-18T04:36:18.984795",
  "updated_at": "2026-06-18T04:36:36.383032"
}
```

### 16. quotes / search_quotes

- Method: `search_quotes`
- Status: `pass`
- Elapsed: `4017.63 ms`

Arguments:

```json
{
  "request_uuid": "03524304194674638976",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": 10,
  "page_number": 1,
  "total": 1,
  "quote_list": [
    {
      "request_uuid": "03524304194674638976",
      "quote_uuid": "33381958003215843456",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-AF",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 900.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 900.0,
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
        "request_uuid": "03524304194674638976",
        "email": "jessicacooper@example.com",
        "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
        "request_description": "E2E test request via silvaengine_gateway",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "item_name": "Flight ATL->ORD Premium Economy",
            "item_uuid": "06041993713794695296",
            "provider_items": [
              {
                "provider_item_uuid": "39876487618607726720",
                "provider_corp_external_id": "AIRLINE-AF",
                "batch_no": "AF6267-20260912",
                "qty": "2"
              }
            ],
            "qty": "2",
            "pax_breakdown": {
              "adult": "2"
            }
          }
        ],
        "notes": "Updated via run_integration.py",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-18T04:34:59.987127",
        "updated_by": "MCP",
        "updated_at": "2026-06-18T04:36:11.492477",
        "quotes": [
          {
            "final_total_quote_amount": "900",
            "provider_corp_external_id": "AIRLINE-AF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "in_progress",
            "total_quote_amount": "900",
            "total_quote_discount": "0",
            "created_at": "2026-06-18 04:36:18.984795",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "33381958003215843456",
            "request_uuid": "03524304194674638976",
            "updated_at": "2026-06-18 04:36:36.383032",
            "updated_by": "MCP"
          }
        ],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "batch_no": "AF6267-20260912",
          "created_at": "2026-06-18 04:36:26.864931",
          "final_subtotal": "900",
          "hold_expires_at": "2026-06-18 04:51:27.231810",
          "hold_token": "b7f0d809f2652ff3b85a59b9549dbef2",
          "item_uuid": "06041993713794695296",
          "partition_key": "gpt#nestaging",
          "pax_breakdown": {
            "adult": "2"
          },
          "price_per_uom": "450",
          "provider_item_uuid": "39876487618607726720",
          "qty": "2",
          "quote_item_uuid": "99624906928751132800",
          "quote_uuid": "33381958003215843456",
          "request_data": {
            "cancellation_policy_snapshot": {
              "tiers": {
                "tiers": [
                  {
                    "hours_before_departure_gte": "168",
                    "refund_pct": "1"
                  },
                  {
                    "hours_before_departure_gte": "24",
                    "refund_pct": "0.5"
                  },
                  {
                    "hours_before_departure_gte": "0",
                    "refund_pct": "0"
                  }
                ]
              },
              "notes_template_uuid": null,
              "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
              "label": "Premium Economy Fare Cancellation",
              "content_hash": "b161d765b3089e5e",
              "policy_uuid": "14167382355785826432",
              "snapshotted_at": "2026-06-18 04:36:27.479155"
            }
          },
          "request_uuid": "03524304194674638976",
          "subtotal": "900",
          "subtotal_discount": "0",
          "subtotal_native": "900",
          "updated_at": "2026-06-18 04:36:26.864931",
          "updated_by": "MCP"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "priority": "10",
          "status": "active",
          "conditions": [
            "is_refundable == false",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.614708",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
          "discount_prompt_uuid": "29118858989597114496",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "2.5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.614708",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'",
            "min_passengers >= 20",
            "loyalty_tier in ['gold', 'platinum']"
          ],
          "created_at": "2026-06-01 22:24:16.312582",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
          "discount_prompt_uuid": "39743702329131548800",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "5000"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.312582",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "7",
          "status": "active",
          "conditions": [
            "min_passengers >= 20",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.462599",
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
          "discount_prompt_uuid": "34741236891406844032",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "1000"
            },
            {
              "greater_than": "1000",
              "max_discount_percentage": "10",
              "less_than": "3500"
            },
            {
              "greater_than": "3500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.462599",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "6",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "min_passengers >= 10",
            "is_refundable == false"
          ],
          "created_at": "2026-06-01 22:24:16.923030",
          "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
          "discount_prompt_uuid": "81566856437527756928",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "500"
            },
            {
              "greater_than": "500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "segment",
          "tags": [
            "61268299727527493760"
          ],
          "updated_at": "2026-06-01 22:24:16.923030",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "5",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:18.730783",
          "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
          "discount_prompt_uuid": "87759969798493061248",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "2500"
            },
            {
              "greater_than": "2500",
              "max_discount_percentage": "10",
              "less_than": "7500"
            },
            {
              "greater_than": "7500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "item",
          "tags": [
            "06041993713794695296"
          ],
          "updated_at": "2026-06-01 22:24:18.730783",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'"
          ],
          "created_at": "2026-06-01 22:24:18.882404",
          "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
          "discount_prompt_uuid": "88308794075899773056",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5",
              "less_than": "20000"
            },
            {
              "greater_than": "20000",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "provider_item",
          "tags": [
            "39876487618607726720"
          ],
          "updated_at": "2026-06-01 22:24:18.882404",
          "updated_by": "prepare_discount_prompts"
        }
      ],
      "updated_by": "MCP",
      "created_at": "2026-06-18T04:36:18.984795",
      "updated_at": "2026-06-18T04:36:36.383032"
    }
  ]
}
```

### 17. quotes / update_quote

- Method: `update_quote`
- Status: `pass`
- Elapsed: `8584.31 ms`

Arguments:

```json
{
  "request_uuid": "03524304194674638976",
  "quote_uuid": "33381958003215843456",
  "notes": "Updated via integration test",
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0
}
```

Output:

```json
{
  "request_uuid": "03524304194674638976",
  "quote_uuid": "33381958003215843456",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-AF",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0,
  "total_quote_amount": 900.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 925.0,
  "currency": null,
  "display_currency": null,
  "fx_rate": null,
  "fx_rate_locked_at": null,
  "notes": "Updated via integration test",
  "status": "in_progress",
  "expired_at": null,
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "03524304194674638976",
    "email": "jessicacooper@example.com",
    "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_uuid": "06041993713794695296",
        "provider_items": [
          {
            "provider_item_uuid": "39876487618607726720",
            "provider_corp_external_id": "AIRLINE-AF",
            "batch_no": "AF6267-20260912",
            "qty": "2"
          }
        ],
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        }
      }
    ],
    "notes": "Updated via run_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-18T04:34:59.987127",
    "updated_by": "MCP",
    "updated_at": "2026-06-18T04:36:11.492477",
    "quotes": [
      {
        "final_total_quote_amount": "925",
        "provider_corp_external_id": "AIRLINE-AF",
        "rounds": "0",
        "shipping_amount": "25",
        "status": "in_progress",
        "total_quote_amount": "900",
        "total_quote_discount": "0",
        "created_at": "2026-06-18 04:36:18.984795",
        "notes": "Updated via integration test",
        "partition_key": "gpt#nestaging",
        "quote_uuid": "33381958003215843456",
        "request_uuid": "03524304194674638976",
        "shipping_method": "ticket_delivery",
        "updated_at": "2026-06-18 04:36:56.852493",
        "updated_by": "MCP"
      }
    ],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "batch_no": "AF6267-20260912",
      "created_at": "2026-06-18 04:36:26.864931",
      "final_subtotal": "900",
      "hold_expires_at": "2026-06-18 04:51:27.231810",
      "hold_token": "b7f0d809f2652ff3b85a59b9549dbef2",
      "item_uuid": "06041993713794695296",
      "partition_key": "gpt#nestaging",
      "pax_breakdown": {
        "adult": "2"
      },
      "price_per_uom": "450",
      "provider_item_uuid": "39876487618607726720",
      "qty": "2",
      "quote_item_uuid": "99624906928751132800",
      "quote_uuid": "33381958003215843456",
      "request_data": {
        "cancellation_policy_snapshot": {
          "tiers": {
            "tiers": [
              {
                "hours_before_departure_gte": "168",
                "refund_pct": "1"
              },
              {
                "hours_before_departure_gte": "24",
                "refund_pct": "0.5"
              },
              {
                "hours_before_departure_gte": "0",
                "refund_pct": "0"
              }
            ]
          },
          "notes_template_uuid": null,
          "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
          "label": "Premium Economy Fare Cancellation",
          "content_hash": "b161d765b3089e5e",
          "policy_uuid": "14167382355785826432",
          "snapshotted_at": "2026-06-18 04:36:27.479155"
        }
      },
      "request_uuid": "03524304194674638976",
      "subtotal": "900",
      "subtotal_discount": "0",
      "subtotal_native": "900",
      "updated_at": "2026-06-18 04:36:26.864931",
      "updated_by": "MCP"
    }
  ],
  "installments": [],
  "discount_prompts": [
    {
      "priority": "10",
      "status": "active",
      "conditions": [
        "is_refundable == false",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.614708",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
      "discount_prompt_uuid": "29118858989597114496",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.614708",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'",
        "min_passengers >= 20",
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "created_at": "2026-06-01 22:24:16.312582",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
      "discount_prompt_uuid": "39743702329131548800",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "5000"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.312582",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "7",
      "status": "active",
      "conditions": [
        "min_passengers >= 20",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.462599",
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
      "discount_prompt_uuid": "34741236891406844032",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "10",
          "less_than": "3500"
        },
        {
          "greater_than": "3500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.462599",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "6",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "min_passengers >= 10",
        "is_refundable == false"
      ],
      "created_at": "2026-06-01 22:24:16.923030",
      "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
      "discount_prompt_uuid": "81566856437527756928",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "500"
        },
        {
          "greater_than": "500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "segment",
      "tags": [
        "61268299727527493760"
      ],
      "updated_at": "2026-06-01 22:24:16.923030",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "5",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:18.730783",
      "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
      "discount_prompt_uuid": "87759969798493061248",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "10",
          "less_than": "7500"
        },
        {
          "greater_than": "7500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "item",
      "tags": [
        "06041993713794695296"
      ],
      "updated_at": "2026-06-01 22:24:18.730783",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'"
      ],
      "created_at": "2026-06-01 22:24:18.882404",
      "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
      "discount_prompt_uuid": "88308794075899773056",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5",
          "less_than": "20000"
        },
        {
          "greater_than": "20000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "provider_item",
      "tags": [
        "39876487618607726720"
      ],
      "updated_at": "2026-06-01 22:24:18.882404",
      "updated_by": "prepare_discount_prompts"
    }
  ],
  "updated_by": "MCP",
  "created_at": "2026-06-18T04:36:18.984795",
  "updated_at": "2026-06-18T04:36:56.852493"
}
```

### 18. quotes / update_quote_item

- Method: `update_quote_item`
- Status: `pass`
- Elapsed: `8521.11 ms`

Arguments:

```json
{
  "quote_uuid": "33381958003215843456",
  "quote_item_uuid": "99624906928751132800",
  "request_uuid": "03524304194674638976",
  "discount_amount": 50.0,
  "notes": "Integration test discount"
}
```

Output:

```json
{
  "quote_uuid": "33381958003215843456",
  "quote_item_uuid": "99624906928751132800",
  "provider_item_uuid": "39876487618607726720",
  "item_uuid": "06041993713794695296",
  "partition_key": "gpt#nestaging",
  "batch_no": "AF6267-20260912",
  "request_uuid": "03524304194674638976",
  "qty": 2.0,
  "pax_breakdown": {
    "adult": "2"
  },
  "bundle_uuid": null,
  "bundle_label": null,
  "bundle_component_uuid": null,
  "price_per_uom": 450.0,
  "subtotal": 900.0,
  "subtotal_discount": 50.0,
  "final_subtotal": 850.0,
  "currency": null,
  "subtotal_native": 900.0,
  "notes": "Integration test discount",
  "hold_token": "b7f0d809f2652ff3b85a59b9549dbef2",
  "hold_expires_at": "2026-06-18T04:51:27.231810",
  "guardrail_price_per_uom": 306.69,
  "slow_move_item": false,
  "quote": {
    "request_uuid": "03524304194674638976",
    "quote_uuid": "33381958003215843456",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-AF",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 900.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 875.0,
    "currency": null,
    "display_currency": null,
    "fx_rate": null,
    "fx_rate_locked_at": null,
    "notes": "Updated via integration test",
    "status": "in_progress",
    "expired_at": null,
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "03524304194674638976",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight ATL->ORD Premium Economy",
          "item_uuid": "06041993713794695296",
          "provider_items": [
            {
              "provider_item_uuid": "39876487618607726720",
              "provider_corp_external_id": "AIRLINE-AF",
              "batch_no": "AF6267-20260912",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-18T04:34:59.987127",
      "updated_by": "MCP",
      "updated_at": "2026-06-18T04:36:11.492477",
      "quotes": [
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "in_progress",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-18 04:36:18.984795",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "33381958003215843456",
          "request_uuid": "03524304194674638976",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 04:37:05.161921",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF6267-20260912",
        "created_at": "2026-06-18 04:36:26.864931",
        "final_subtotal": "850",
        "hold_expires_at": "2026-06-18 04:51:27.231810",
        "hold_token": "b7f0d809f2652ff3b85a59b9549dbef2",
        "item_uuid": "06041993713794695296",
        "notes": "Integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "99624906928751132800",
        "quote_uuid": "33381958003215843456",
        "request_data": {
          "cancellation_policy_snapshot": {
            "tiers": {
              "tiers": [
                {
                  "hours_before_departure_gte": "168",
                  "refund_pct": "1"
                },
                {
                  "hours_before_departure_gte": "24",
                  "refund_pct": "0.5"
                },
                {
                  "hours_before_departure_gte": "0",
                  "refund_pct": "0"
                }
              ]
            },
            "notes_template_uuid": null,
            "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
            "label": "Premium Economy Fare Cancellation",
            "content_hash": "b161d765b3089e5e",
            "policy_uuid": "14167382355785826432",
            "snapshotted_at": "2026-06-18 04:36:27.479155"
          }
        },
        "request_uuid": "03524304194674638976",
        "subtotal": "900",
        "subtotal_discount": "50",
        "subtotal_native": "900",
        "updated_at": "2026-06-18 04:37:04.966545",
        "updated_by": "MCP"
      }
    ],
    "installments": [],
    "discount_prompts": [
      {
        "priority": "10",
        "status": "active",
        "conditions": [
          "is_refundable == false",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.614708",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
        "discount_prompt_uuid": "29118858989597114496",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.614708",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'",
          "min_passengers >= 20",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-01 22:24:16.312582",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
        "discount_prompt_uuid": "39743702329131548800",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "5000"
          },
          {
            "greater_than": "5000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.312582",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "7",
        "status": "active",
        "conditions": [
          "min_passengers >= 20",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.462599",
        "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
        "discount_prompt_uuid": "34741236891406844032",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "1000"
          },
          {
            "greater_than": "1000",
            "max_discount_percentage": "10",
            "less_than": "3500"
          },
          {
            "greater_than": "3500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.462599",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "6",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "min_passengers >= 10",
          "is_refundable == false"
        ],
        "created_at": "2026-06-01 22:24:16.923030",
        "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
        "discount_prompt_uuid": "81566856437527756928",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "500"
          },
          {
            "greater_than": "500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "segment",
        "tags": [
          "61268299727527493760"
        ],
        "updated_at": "2026-06-01 22:24:16.923030",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "5",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:18.730783",
        "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
        "discount_prompt_uuid": "87759969798493061248",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "item",
        "tags": [
          "06041993713794695296"
        ],
        "updated_at": "2026-06-01 22:24:18.730783",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'"
        ],
        "created_at": "2026-06-01 22:24:18.882404",
        "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
        "discount_prompt_uuid": "88308794075899773056",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5",
            "less_than": "20000"
          },
          {
            "greater_than": "20000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "provider_item",
        "tags": [
          "39876487618607726720"
        ],
        "updated_at": "2026-06-01 22:24:18.882404",
        "updated_by": "prepare_discount_prompts"
      }
    ],
    "updated_by": "MCP",
    "created_at": "2026-06-18T04:36:18.984795",
    "updated_at": "2026-06-18T04:37:05.161921"
  },
  "item": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "item_uuid": "06041993713794695296",
    "item_type": "flight",
    "item_name": "Flight ATL->ORD Premium Economy",
    "item_description": "Premium Economy class non-stop service from Atlanta (ATL) to Chicago (ORD).",
    "pricing_mode": "per_pax_type",
    "uom": "seat",
    "item_external_id": "FLIGHT-ATL-ORD-PRE",
    "created_at": "2026-06-01T22:19:29.788924",
    "updated_by": "prepare_flight_products",
    "updated_at": "2026-06-01T22:19:29.788924"
  
... (truncated)
```

### 19. pricing / get_item_price_tiers

- Method: `get_item_price_tiers`
- Status: `pass`
- Elapsed: `3515.58 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "quote_items": [
    {
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720",
      "qty": 2
    }
  ]
}
```

Output:

```json
{
  "item_price_tiers": [
    {
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720",
      "item_price_tier_uuid": "10913421828051452032",
      "quantity_greater_then": 0.0,
      "quantity_less_then": null,
      "price_per_uom": 45.0,
      "margin_per_uom": null,
      "provider_item_batches": [],
      "status": "active"
    },
    {
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720",
      "item_price_tier_uuid": "23774464543545114752",
      "quantity_greater_then": 0.0,
      "quantity_less_then": null,
      "price_per_uom": 450.0,
      "margin_per_uom": null,
      "provider_item_batches": [],
      "status": "active"
    },
    {
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720",
      "item_price_tier_uuid": "76852609247750406272",
      "quantity_greater_then": 0.0,
      "quantity_less_then": null,
      "price_per_uom": 337.5,
      "margin_per_uom": null,
      "provider_item_batches": [],
      "status": "active"
    }
  ]
}
```

### 20. pricing / get_discount_prompts

- Method: `get_discount_prompts`
- Status: `pass`
- Elapsed: `3756.61 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "quote_items": [
    {
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720"
    }
  ]
}
```

Output:

```json
{
  "discount_prompts": [
    {
      "discount_prompt_uuid": "29118858989597114496",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
      "conditions": [
        "is_refundable == false",
        "channel == 'direct'"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5"
        }
      ],
      "priority": 10,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "39743702329131548800",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
      "conditions": [
        "season != 'peak'",
        "min_passengers >= 20",
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "5000"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "10"
        }
      ],
      "priority": 2,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "34741236891406844032",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
      "conditions": [
        "min_passengers >= 20",
        "channel == 'direct'"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "10",
          "less_than": "3500"
        },
        {
          "greater_than": "3500",
          "max_discount_percentage": "12.5"
        }
      ],
      "priority": 7,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "81566856437527756928",
      "scope": "segment",
      "tags": [
        "61268299727527493760"
      ],
      "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "min_passengers >= 10",
        "is_refundable == false"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "500"
        },
        {
          "greater_than": "500",
          "max_discount_percentage": "12.5"
        }
      ],
      "priority": 6,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "87759969798493061248",
      "scope": "item",
      "tags": [
        "06041993713794695296"
      ],
      "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "channel == 'direct'"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "10",
          "less_than": "7500"
        },
        {
          "greater_than": "7500",
          "max_discount_percentage": "12.5"
        }
      ],
      "priority": 5,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "88308794075899773056",
      "scope": "provider_item",
      "tags": [
        "39876487618607726720"
      ],
      "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
      "conditions": [
        "season != 'peak'"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5",
          "less_than": "20000"
        },
        {
          "greater_than": "20000",
          "max_discount_percentage": "10"
        }
      ],
      "priority": 2,
      "status": "active"
    }
  ]
}
```

### 21. pricing / calculate_quote_pricing

- Method: `calculate_quote_pricing`
- Status: `pass`
- Elapsed: `3593.53 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "email": "jessicacooper@example.com"
}
```

Output:

```json
{
  "request_uuid": "96306650268729098368",
  "groups": []
}
```

### 22. installments / confirm_quote_and_create_installments

- Method: `confirm_quote_and_create_installments`
- Status: `pass`
- Elapsed: `32071.67 ms`

Arguments:

```json
{
  "request_uuid": "03524304194674638976",
  "quote_uuid": "33381958003215843456",
  "create_single_installment": true,
  "payment_method": "bank_transfer"
}
```

Output:

```json
{
  "quote": {
    "request_uuid": "03524304194674638976",
    "quote_uuid": "33381958003215843456",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-AF",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 900.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 875.0,
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
      "request_uuid": "03524304194674638976",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight ATL->ORD Premium Economy",
          "item_uuid": "06041993713794695296",
          "provider_items": [
            {
              "provider_item_uuid": "39876487618607726720",
              "provider_corp_external_id": "AIRLINE-AF",
              "batch_no": "AF6267-20260912",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-18T04:34:59.987127",
      "updated_by": "MCP",
      "updated_at": "2026-06-18T04:36:11.492477",
      "quotes": [
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-18 04:36:18.984795",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "33381958003215843456",
          "request_uuid": "03524304194674638976",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 04:37:28.524360",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF6267-20260912",
        "created_at": "2026-06-18 04:36:26.864931",
        "final_subtotal": "850",
        "hold_expires_at": "2026-06-18 04:51:27.231810",
        "hold_token": "b7f0d809f2652ff3b85a59b9549dbef2",
        "item_uuid": "06041993713794695296",
        "notes": "Integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "99624906928751132800",
        "quote_uuid": "33381958003215843456",
        "request_data": {
          "cancellation_policy_snapshot": {
            "tiers": {
              "tiers": [
                {
                  "hours_before_departure_gte": "168",
                  "refund_pct": "1"
                },
                {
                  "hours_before_departure_gte": "24",
                  "refund_pct": "0.5"
                },
                {
                  "hours_before_departure_gte": "0",
                  "refund_pct": "0"
                }
              ]
            },
            "notes_template_uuid": null,
            "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
            "label": "Premium Economy Fare Cancellation",
            "content_hash": "b161d765b3089e5e",
            "policy_uuid": "14167382355785826432",
            "snapshotted_at": "2026-06-18 04:36:27.479155"
          }
        },
        "request_uuid": "03524304194674638976",
        "subtotal": "900",
        "subtotal_discount": "50",
        "subtotal_native": "900",
        "updated_at": "2026-06-18 04:37:04.966545",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "875",
        "installment_ratio": "100",
        "priority": "0",
        "status": "pending",
        "created_at": "2026-06-18 04:37:44.129229",
        "installment_uuid": "16364181980747677824",
        "partition_key": "gpt#nestaging",
        "payment_method": "bank_transfer",
        "quote_uuid": "33381958003215843456",
        "request_uuid": "03524304194674638976",
        "scheduled_date": "2026-06-18 04:37:40",
        "updated_at": "2026-06-18 04:37:44.129229",
        "updated_by": "MCP"
      }
    ],
    "discount_prompts": [
      {
        "priority": "10",
        "status": "active",
        "conditions": [
          "is_refundable == false",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.614708",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
        "discount_prompt_uuid": "29118858989597114496",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.614708",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'",
          "min_passengers >= 20",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-01 22:24:16.312582",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
        "discount_prompt_uuid": "39743702329131548800",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "5000"
          },
          {
            "greater_than": "5000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.312582",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "7",
        "status": "active",
        "conditions": [
          "min_passengers >= 20",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.462599",
        "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
        "discount_prompt_uuid": "34741236891406844032",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "1000"
          },
          {
            "greater_than": "1000",
            "max_discount_percentage": "10",
            "less_than": "3500"
          },
          {
            "greater_than": "3500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.462599",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "6",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "min_passengers >= 10",
          "is_refundable == false"
        ],
        "created_at": "2026-06-01 22:24:16.923030",
        "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
        "discount_prompt_uuid": "81566856437527756928",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "500"
          },
          {
            "greater_than": "500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "segment",
        "tags": [
          "61268299727527493760"
        ],
        "updated_at": "2026-06-01 22:24:16.923030",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "5",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:18.730783",
        "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
        "discount_prompt_uuid": "87759969798493061248",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "item",
        "tags": [
          "06041993713794695296"
        ],
        "updated_at": "2026-06-01 22:24:18.730783",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'"
        ],
        "created_at": "2026-06-01 22:24:18.882404",
        "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
        "discount_prompt_uuid": "88308794075899773056",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5",
            "less_than": "20000"
          },
          {
            "greater_than": "20000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "provider_item",
        "tags": [
          "39876487618607726720"
        ],
        "updated_at": "2026-06-01 22:24:18.882404",
        "updated_by": "prepare_discount_prompts"
      }
    ],
    "updated_by": "MCP",
    "created_at": "2026-06-18T04:36:18.984795",
    "updated_at": "2026-06-18T04:37:28.524360"
  },
  "installments": [
    {
      "quote_uuid": "33381958003215843456",
      "installment_uuid": "16364181980747677824",
      "request_uuid": "03524304194674638976",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 875.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-18T04:37:40",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-18T04:37:44.129229",
      "updated_at": "2026-06-18T04:37:44.129229",
      "quote": {
        "request_uuid": "03524304194674638976",
        "quote_uuid": "33381958003215843456",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_id": "AIRLINE-AF",
        "sales_rep_em
... (truncated)
```

### 23. installments / get_installments

- Method: `get_installments`
- Status: `pass`
- Elapsed: `4062.67 ms`

Arguments:

```json
{
  "quote_uuid": "33381958003215843456",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": 10,
  "page_number": 1,
  "total": 1,
  "installment_list": [
    {
      "quote_uuid": "33381958003215843456",
      "installment_uuid": "16364181980747677824",
      "request_uuid": "03524304194674638976",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 875.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-18T04:37:40",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-18T04:37:44.129229",
      "updated_at": "2026-06-18T04:37:44.129229",
      "quote": {
        "request_uuid": "03524304194674638976",
        "quote_uuid": "33381958003215843456",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_id": "AIRLINE-AF",
        "sales_rep_email": null,
        "rounds": 0,
        "shipping_method": "ticket_delivery",
        "shipping_amount": 25.0,
        "total_quote_amount": 900.0,
        "total_quote_discount": 50.0,
        "final_total_quote_amount": 875.0,
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
          "request_uuid": "03524304194674638976",
          "email": "jessicacooper@example.com",
          "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
          "request_description": "E2E test request via silvaengine_gateway",
          "billing_address": null,
          "shipping_address": null,
          "items": [
            {
              "item_name": "Flight ATL->ORD Premium Economy",
              "item_uuid": "06041993713794695296",
              "provider_items": [
                {
                  "provider_item_uuid": "39876487618607726720",
                  "provider_corp_external_id": "AIRLINE-AF",
                  "batch_no": "AF6267-20260912",
                  "qty": "2"
                }
              ],
              "qty": "2",
              "pax_breakdown": {
                "adult": "2"
              }
            }
          ],
          "notes": "Updated via run_integration.py",
          "bundle_uuid": null,
          "status": "confirmed",
          "expired_at": "2026-12-31T23:59:59",
          "created_at": "2026-06-18T04:34:59.987127",
          "updated_by": "MCP",
          "updated_at": "2026-06-18T04:36:11.492477",
          "quotes": [
            {
              "final_total_quote_amount": "875",
              "provider_corp_external_id": "AIRLINE-AF",
              "rounds": "0",
              "shipping_amount": "25",
              "status": "confirmed",
              "total_quote_amount": "900",
              "total_quote_discount": "50",
              "created_at": "2026-06-18 04:36:18.984795",
              "notes": "Updated via integration test",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "33381958003215843456",
              "request_uuid": "03524304194674638976",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-18 04:37:28.524360",
              "updated_by": "MCP"
            }
          ],
          "files": [],
          "bundle": null
        },
        "quote_items": [
          {
            "batch_no": "AF6267-20260912",
            "created_at": "2026-06-18 04:36:26.864931",
            "final_subtotal": "850",
            "hold_expires_at": "2026-06-18 04:51:27.231810",
            "hold_token": "b7f0d809f2652ff3b85a59b9549dbef2",
            "item_uuid": "06041993713794695296",
            "notes": "Integration test discount",
            "partition_key": "gpt#nestaging",
            "pax_breakdown": {
              "adult": "2"
            },
            "price_per_uom": "450",
            "provider_item_uuid": "39876487618607726720",
            "qty": "2",
            "quote_item_uuid": "99624906928751132800",
            "quote_uuid": "33381958003215843456",
            "request_data": {
              "cancellation_policy_snapshot": {
                "tiers": {
                  "tiers": [
                    {
                      "hours_before_departure_gte": "168",
                      "refund_pct": "1"
                    },
                    {
                      "hours_before_departure_gte": "24",
                      "refund_pct": "0.5"
                    },
                    {
                      "hours_before_departure_gte": "0",
                      "refund_pct": "0"
                    }
                  ]
                },
                "notes_template_uuid": null,
                "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
                "label": "Premium Economy Fare Cancellation",
                "content_hash": "b161d765b3089e5e",
                "policy_uuid": "14167382355785826432",
                "snapshotted_at": "2026-06-18 04:36:27.479155"
              }
            },
            "request_uuid": "03524304194674638976",
            "subtotal": "900",
            "subtotal_discount": "50",
            "subtotal_native": "900",
            "updated_at": "2026-06-18 04:37:04.966545",
            "updated_by": "MCP"
          }
        ],
        "installments": [
          {
            "installment_amount": "875",
            "installment_ratio": "100",
            "priority": "0",
            "status": "pending",
            "created_at": "2026-06-18 04:37:44.129229",
            "installment_uuid": "16364181980747677824",
            "partition_key": "gpt#nestaging",
            "payment_method": "bank_transfer",
            "quote_uuid": "33381958003215843456",
            "request_uuid": "03524304194674638976",
            "scheduled_date": "2026-06-18 04:37:40",
            "updated_at": "2026-06-18 04:37:44.129229",
            "updated_by": "MCP"
          }
        ],
        "discount_prompts": [
          {
            "priority": "10",
            "status": "active",
            "conditions": [
              "is_refundable == false",
              "channel == 'direct'"
            ],
            "created_at": "2026-06-01 22:24:16.614708",
            "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
            "discount_prompt_uuid": "29118858989597114496",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "2.5",
                "less_than": "10000"
              },
              {
                "greater_than": "10000",
                "max_discount_percentage": "7.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-01 22:24:16.614708",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "2",
            "status": "active",
            "conditions": [
              "season != 'peak'",
              "min_passengers >= 20",
              "loyalty_tier in ['gold', 'platinum']"
            ],
            "created_at": "2026-06-01 22:24:16.312582",
            "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
            "discount_prompt_uuid": "39743702329131548800",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "5",
                "less_than": "5000"
              },
              {
                "greater_than": "5000",
                "max_discount_percentage": "10"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-01 22:24:16.312582",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "7",
            "status": "active",
            "conditions": [
              "min_passengers >= 20",
              "channel == 'direct'"
            ],
            "created_at": "2026-06-01 22:24:16.462599",
            "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
            "discount_prompt_uuid": "34741236891406844032",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "7.5",
                "less_than": "1000"
              },
              {
                "greater_than": "1000",
                "max_discount_percentage": "10",
                "less_than": "3500"
              },
              {
                "greater_than": "3500",
                "max_discount_percentage": "12.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-01 22:24:16.462599",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "6",
            "status": "active",
            "conditions": [
              "payment_method in ['wire_transfer', 'credit_card']",
              "min_passengers >= 10",
              "is_refundable == false"
            ],
            "created_at": "2026-06-01 22:24:16.923030",
            "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
            "discount_prompt_uuid": "81566856437527756928",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "7.5",
                "less_than": "500"
              },
              {
                "greater_than": "500",
                "max_discount_percentage": "12.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "segment",
            "tags": [
              "61268299727527493760"
            ],
            "updated_at": "2026-06-01 22:24:16.923030",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "5",
            "status": "active",
            "conditions": [
              "payment_method in ['wire_transfer', 'credit_card']",
              "channel == 'direct'"
            ],
            "created_at": "2026-06-01 22:24:18.730783",
            "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
            "discount_prompt_uuid": "87759969798493061248",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "7.5",
                "less_than": "2500"
              },
              {
                "greater_than": "2500",
                "max_discount_percentage": "10",
                "less_than": "7500"
              },
              {
                "greater_than": "7500",
                "max_discount_percentage": "12.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "item",
            "tags": [
              "06041993713794695296"
            ],
            "updated_at": "2026-06-01 22:24:18.730783",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "2",
            "status": "active",
            "conditions": [
              "season != 'peak'"
          
... (truncated)
```

### 24. installments / create_installment

- Method: `_create_installment`
- Status: `pass`
- Elapsed: `11793.92 ms`

Arguments:

```json
{
  "quote_uuid": "46818404653468762240",
  "request_uuid": "03524304194674638976",
  "installment_amount": 100.0,
  "payment_method": "credit_card"
}
```

Output:

```json
{
  "quote_uuid": "46818404653468762240",
  "installment_uuid": "68851166643776143488",
  "request_uuid": "03524304194674638976",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 100.0,
  "installment_ratio": 8.333333333333332,
  "salesorder_no": null,
  "scheduled_date": "2026-06-18T04:39:24",
  "payment_method": "credit_card",
  "status": "pending",
  "updated_by": "MCP",
  "created_at": "2026-06-18T04:39:27.812684",
  "updated_at": "2026-06-18T04:39:27.812684",
  "quote": {
    "request_uuid": "03524304194674638976",
    "quote_uuid": "46818404653468762240",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-AF",
    "sales_rep_email": null,
    "rounds": 1,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 300.0,
    "total_quote_amount": 900.0,
    "total_quote_discount": 0.0,
    "final_total_quote_amount": 1200.0,
    "currency": null,
    "display_currency": null,
    "fx_rate": null,
    "fx_rate_locked_at": null,
    "notes": "Confirmed setup quote for create_installment",
    "status": "confirmed",
    "expired_at": null,
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "03524304194674638976",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight ATL->ORD Premium Economy",
          "item_uuid": "06041993713794695296",
          "provider_items": [
            {
              "provider_item_uuid": "39876487618607726720",
              "provider_corp_external_id": "AIRLINE-AF",
              "batch_no": "AF6267-20260912",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-18T04:34:59.987127",
      "updated_by": "MCP",
      "updated_at": "2026-06-18T04:36:11.492477",
      "quotes": [
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-18 04:36:18.984795",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "33381958003215843456",
          "request_uuid": "03524304194674638976",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 04:37:28.524360",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "1200",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "1",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "0",
          "created_at": "2026-06-18 04:38:00.133076",
          "notes": "Confirmed setup quote for create_installment",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "46818404653468762240",
          "request_uuid": "03524304194674638976",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 04:38:34.052437",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "1200",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "2",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "0",
          "created_at": "2026-06-18 04:38:41.794498",
          "notes": "Confirmed setup quote for create_installments",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "90871222124412944512",
          "request_uuid": "03524304194674638976",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 04:39:16.281547",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF6267-20260912",
        "created_at": "2026-06-18 04:38:08.037572",
        "final_subtotal": "900",
        "hold_expires_at": "2026-06-18 04:53:08.374875",
        "hold_token": "d36223365d39e4f74cbad040dbf6aadb",
        "item_uuid": "06041993713794695296",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "67280637522575638656",
        "quote_uuid": "46818404653468762240",
        "request_data": {
          "cancellation_policy_snapshot": {
            "tiers": {
              "tiers": [
                {
                  "hours_before_departure_gte": "168",
                  "refund_pct": "1"
                },
                {
                  "hours_before_departure_gte": "24",
                  "refund_pct": "0.5"
                },
                {
                  "hours_before_departure_gte": "0",
                  "refund_pct": "0"
                }
              ]
            },
            "notes_template_uuid": null,
            "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
            "label": "Premium Economy Fare Cancellation",
            "content_hash": "b161d765b3089e5e",
            "policy_uuid": "14167382355785826432",
            "snapshotted_at": "2026-06-18 04:38:08.633483"
          }
        },
        "request_uuid": "03524304194674638976",
        "subtotal": "900",
        "subtotal_discount": "0",
        "subtotal_native": "900",
        "updated_at": "2026-06-18 04:38:08.037572",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "100",
        "installment_ratio": "8.333333333333332",
        "priority": "0",
        "status": "pending",
        "created_at": "2026-06-18 04:39:27.812684",
        "installment_uuid": "68851166643776143488",
        "partition_key": "gpt#nestaging",
        "payment_method": "credit_card",
        "quote_uuid": "46818404653468762240",
        "request_uuid": "03524304194674638976",
        "scheduled_date": "2026-06-18 04:39:24",
        "updated_at": "2026-06-18 04:39:27.812684",
        "updated_by": "MCP"
      }
    ],
    "discount_prompts": [
      {
        "priority": "10",
        "status": "active",
        "conditions": [
          "is_refundable == false",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.614708",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
        "discount_prompt_uuid": "29118858989597114496",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.614708",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'",
          "min_passengers >= 20",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-01 22:24:16.312582",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
        "discount_prompt_uuid": "39743702329131548800",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "5000"
          },
          {
            "greater_than": "5000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.312582",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "7",
        "status": "active",
        "conditions": [
          "min_passengers >= 20",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.462599",
        "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
        "discount_prompt_uuid": "34741236891406844032",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "1000"
          },
          {
            "greater_than": "1000",
            "max_discount_percentage": "10",
            "less_than": "3500"
          },
          {
            "greater_than": "3500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.462599",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "6",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "min_passengers >= 10",
          "is_refundable == false"
        ],
        "created_at": "2026-06-01 22:24:16.923030",
        "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
        "discount_prompt_uuid": "81566856437527756928",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "500"
          },
          {
            "greater_than": "500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "segment",
        "tags": [
          "61268299727527493760"
        ],
        "updated_at": "2026-06-01 22:24:16.923030",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "5",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:18.730783",
        "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
        "discount_prompt_uuid": "87759969798493061248",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "item",
        "tags": [
          "06041993713794695296"
        ],
        "updated_at": "2026-06-01 22:24:18.730783",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season !
... (truncated)
```

### 25. installments / create_installments

- Method: `_create_installments`
- Status: `pass`
- Elapsed: `19701.33 ms`

Arguments:

```json
{
  "quote_uuid": "90871222124412944512",
  "request_uuid": "03524304194674638976",
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
      "quote_uuid": "90871222124412944512",
      "installment_uuid": "49990536923765031040",
      "request_uuid": "03524304194674638976",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 400.0,
      "installment_ratio": 33.33333333333333,
      "salesorder_no": null,
      "scheduled_date": "2026-08-15T04:39:36",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-18T04:39:39.378919",
      "updated_at": "2026-06-18T04:39:39.378919",
      "quote": {
        "request_uuid": "03524304194674638976",
        "quote_uuid": "90871222124412944512",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_id": "AIRLINE-AF",
        "sales_rep_email": null,
        "rounds": 2,
        "shipping_method": "ticket_delivery",
        "shipping_amount": 300.0,
        "total_quote_amount": 900.0,
        "total_quote_discount": 0.0,
        "final_total_quote_amount": 1200.0,
        "currency": null,
        "display_currency": null,
        "fx_rate": null,
        "fx_rate_locked_at": null,
        "notes": "Confirmed setup quote for create_installments",
        "status": "confirmed",
        "expired_at": null,
        "request": {
          "partition_key": "gpt#nestaging",
          "endpoint_id": "gpt",
          "part_id": "nestaging",
          "request_uuid": "03524304194674638976",
          "email": "jessicacooper@example.com",
          "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
          "request_description": "E2E test request via silvaengine_gateway",
          "billing_address": null,
          "shipping_address": null,
          "items": [
            {
              "item_name": "Flight ATL->ORD Premium Economy",
              "item_uuid": "06041993713794695296",
              "provider_items": [
                {
                  "provider_item_uuid": "39876487618607726720",
                  "provider_corp_external_id": "AIRLINE-AF",
                  "batch_no": "AF6267-20260912",
                  "qty": "2"
                }
              ],
              "qty": "2",
              "pax_breakdown": {
                "adult": "2"
              }
            }
          ],
          "notes": "Updated via run_integration.py",
          "bundle_uuid": null,
          "status": "confirmed",
          "expired_at": "2026-12-31T23:59:59",
          "created_at": "2026-06-18T04:34:59.987127",
          "updated_by": "MCP",
          "updated_at": "2026-06-18T04:36:11.492477",
          "quotes": [
            {
              "final_total_quote_amount": "875",
              "provider_corp_external_id": "AIRLINE-AF",
              "rounds": "0",
              "shipping_amount": "25",
              "status": "confirmed",
              "total_quote_amount": "900",
              "total_quote_discount": "50",
              "created_at": "2026-06-18 04:36:18.984795",
              "notes": "Updated via integration test",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "33381958003215843456",
              "request_uuid": "03524304194674638976",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-18 04:37:28.524360",
              "updated_by": "MCP"
            },
            {
              "final_total_quote_amount": "1200",
              "provider_corp_external_id": "AIRLINE-AF",
              "rounds": "1",
              "shipping_amount": "300",
              "status": "confirmed",
              "total_quote_amount": "900",
              "total_quote_discount": "0",
              "created_at": "2026-06-18 04:38:00.133076",
              "notes": "Confirmed setup quote for create_installment",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "46818404653468762240",
              "request_uuid": "03524304194674638976",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-18 04:38:34.052437",
              "updated_by": "MCP"
            },
            {
              "final_total_quote_amount": "1200",
              "provider_corp_external_id": "AIRLINE-AF",
              "rounds": "2",
              "shipping_amount": "300",
              "status": "confirmed",
              "total_quote_amount": "900",
              "total_quote_discount": "0",
              "created_at": "2026-06-18 04:38:41.794498",
              "notes": "Confirmed setup quote for create_installments",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "90871222124412944512",
              "request_uuid": "03524304194674638976",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-18 04:39:16.281547",
              "updated_by": "MCP"
            }
          ],
          "files": [],
          "bundle": null
        },
        "quote_items": [
          {
            "batch_no": "AF6267-20260912",
            "created_at": "2026-06-18 04:38:50.646894",
            "final_subtotal": "900",
            "hold_expires_at": "2026-06-18 04:53:50.984273",
            "hold_token": "d0955aebf4abcfaeb17dd5721930f96e",
            "item_uuid": "06041993713794695296",
            "partition_key": "gpt#nestaging",
            "pax_breakdown": {
              "adult": "2"
            },
            "price_per_uom": "450",
            "provider_item_uuid": "39876487618607726720",
            "qty": "2",
            "quote_item_uuid": "38031674089967468672",
            "quote_uuid": "90871222124412944512",
            "request_data": {
              "cancellation_policy_snapshot": {
                "tiers": {
                  "tiers": [
                    {
                      "hours_before_departure_gte": "168",
                      "refund_pct": "1"
                    },
                    {
                      "hours_before_departure_gte": "24",
                      "refund_pct": "0.5"
                    },
                    {
                      "hours_before_departure_gte": "0",
                      "refund_pct": "0"
                    }
                  ]
                },
                "notes_template_uuid": null,
                "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
                "label": "Premium Economy Fare Cancellation",
                "content_hash": "b161d765b3089e5e",
                "policy_uuid": "14167382355785826432",
                "snapshotted_at": "2026-06-18 04:38:51.247958"
              }
            },
            "request_uuid": "03524304194674638976",
            "subtotal": "900",
            "subtotal_discount": "0",
            "subtotal_native": "900",
            "updated_at": "2026-06-18 04:38:50.646894",
            "updated_by": "MCP"
          }
        ],
        "installments": [
          {
            "installment_amount": "400",
            "installment_ratio": "33.33333333333333",
            "priority": "0",
            "status": "pending",
            "created_at": "2026-06-18 04:39:39.378919",
            "installment_uuid": "49990536923765031040",
            "partition_key": "gpt#nestaging",
            "payment_method": "bank_transfer",
            "quote_uuid": "90871222124412944512",
            "request_uuid": "03524304194674638976",
            "scheduled_date": "2026-08-15 04:39:36",
            "updated_at": "2026-06-18 04:39:39.378919",
            "updated_by": "MCP"
          }
        ],
        "discount_prompts": [
          {
            "priority": "10",
            "status": "active",
            "conditions": [
              "is_refundable == false",
              "channel == 'direct'"
            ],
            "created_at": "2026-06-01 22:24:16.614708",
            "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
            "discount_prompt_uuid": "29118858989597114496",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "2.5",
                "less_than": "10000"
              },
              {
                "greater_than": "10000",
                "max_discount_percentage": "7.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-01 22:24:16.614708",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "2",
            "status": "active",
            "conditions": [
              "season != 'peak'",
              "min_passengers >= 20",
              "loyalty_tier in ['gold', 'platinum']"
            ],
            "created_at": "2026-06-01 22:24:16.312582",
            "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
            "discount_prompt_uuid": "39743702329131548800",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "5",
                "less_than": "5000"
              },
              {
                "greater_than": "5000",
                "max_discount_percentage": "10"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-01 22:24:16.312582",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "7",
            "status": "active",
            "conditions": [
              "min_passengers >= 20",
              "channel == 'direct'"
            ],
            "created_at": "2026-06-01 22:24:16.462599",
            "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
            "discount_prompt_uuid": "34741236891406844032",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "7.5",
                "less_than": "1000"
              },
              {
                "greater_than": "1000",
                "max_discount_percentage": "10",
                "less_than": "3500"
              },
              {
                "greater_than": "3500",
                "max_discount_percentage": "12.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-01 22:24:16.462599",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "6",
            "status": "active",
            "conditions": [
              "payment_method in ['wire_transfer', 'credit_card']",
              "min_passengers >= 10",
              "is_refundable == false"
            ],
            "created_at": "2026-06-01 22:24:16.923030",
            "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
            "discount_prompt_uuid": "81566856437527756928",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "7.5",
                "less_than": "500"
              },
              {
                "greater_than": "500",
                "max_discount_percentage": "12.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "segment",
            "tags": [
              "61268299727527493760"
            ],
            "updated_at": "2026-06-01 22:24
... (truncated)
```

### 26. installments / update_installment (uuid=163641819807...)

- Method: `update_installment`
- Status: `pass`
- Elapsed: `30894.79 ms`

Arguments:

```json
{
  "quote_uuid": "33381958003215843456",
  "installment_uuid": "16364181980747677824",
  "status": "paid"
}
```

Output:

```json
{
  "quote_uuid": "33381958003215843456",
  "installment_uuid": "16364181980747677824",
  "request_uuid": "03524304194674638976",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 875.0,
  "installment_ratio": 100.0,
  "salesorder_no": null,
  "scheduled_date": "2026-06-18T04:37:40",
  "payment_method": "bank_transfer",
  "status": "paid",
  "updated_by": "MCP",
  "created_at": "2026-06-18T04:37:44.129229",
  "updated_at": "2026-06-18T04:39:55.530564",
  "quote": {
    "request_uuid": "03524304194674638976",
    "quote_uuid": "33381958003215843456",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-AF",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 900.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 875.0,
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
      "request_uuid": "03524304194674638976",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight ATL->ORD Premium Economy",
          "item_uuid": "06041993713794695296",
          "provider_items": [
            {
              "provider_item_uuid": "39876487618607726720",
              "provider_corp_external_id": "AIRLINE-AF",
              "batch_no": "AF6267-20260912",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-18T04:34:59.987127",
      "updated_by": "MCP",
      "updated_at": "2026-06-18T04:36:11.492477",
      "quotes": [
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-18 04:36:18.984795",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "33381958003215843456",
          "request_uuid": "03524304194674638976",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 04:37:28.524360",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "1200",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "1",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "0",
          "created_at": "2026-06-18 04:38:00.133076",
          "notes": "Confirmed setup quote for create_installment",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "46818404653468762240",
          "request_uuid": "03524304194674638976",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 04:38:34.052437",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "1200",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "2",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "0",
          "created_at": "2026-06-18 04:38:41.794498",
          "notes": "Confirmed setup quote for create_installments",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "90871222124412944512",
          "request_uuid": "03524304194674638976",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 04:39:16.281547",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF6267-20260912",
        "created_at": "2026-06-18 04:36:26.864931",
        "final_subtotal": "850",
        "hold_expires_at": "2026-06-18 04:51:27.231810",
        "hold_token": "b7f0d809f2652ff3b85a59b9549dbef2",
        "item_uuid": "06041993713794695296",
        "notes": "Integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "99624906928751132800",
        "quote_uuid": "33381958003215843456",
        "request_data": {
          "cancellation_policy_snapshot": {
            "tiers": {
              "tiers": [
                {
                  "hours_before_departure_gte": "168",
                  "refund_pct": "1"
                },
                {
                  "hours_before_departure_gte": "24",
                  "refund_pct": "0.5"
                },
                {
                  "hours_before_departure_gte": "0",
                  "refund_pct": "0"
                }
              ]
            },
            "notes_template_uuid": null,
            "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
            "label": "Premium Economy Fare Cancellation",
            "content_hash": "b161d765b3089e5e",
            "policy_uuid": "14167382355785826432",
            "snapshotted_at": "2026-06-18 04:36:27.479155"
          }
        },
        "request_uuid": "03524304194674638976",
        "subtotal": "900",
        "subtotal_discount": "50",
        "subtotal_native": "900",
        "updated_at": "2026-06-18 04:37:04.966545",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "875",
        "installment_ratio": "100",
        "priority": "0",
        "status": "paid",
        "created_at": "2026-06-18 04:37:44.129229",
        "installment_uuid": "16364181980747677824",
        "partition_key": "gpt#nestaging",
        "payment_method": "bank_transfer",
        "quote_uuid": "33381958003215843456",
        "request_uuid": "03524304194674638976",
        "scheduled_date": "2026-06-18 04:37:40",
        "updated_at": "2026-06-18 04:39:55.530564",
        "updated_by": "MCP"
      }
    ],
    "discount_prompts": [
      {
        "priority": "10",
        "status": "active",
        "conditions": [
          "is_refundable == false",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.614708",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
        "discount_prompt_uuid": "29118858989597114496",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.614708",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'",
          "min_passengers >= 20",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-01 22:24:16.312582",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
        "discount_prompt_uuid": "39743702329131548800",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "5000"
          },
          {
            "greater_than": "5000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.312582",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "7",
        "status": "active",
        "conditions": [
          "min_passengers >= 20",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.462599",
        "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
        "discount_prompt_uuid": "34741236891406844032",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "1000"
          },
          {
            "greater_than": "1000",
            "max_discount_percentage": "10",
            "less_than": "3500"
          },
          {
            "greater_than": "3500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.462599",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "6",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "min_passengers >= 10",
          "is_refundable == false"
        ],
        "created_at": "2026-06-01 22:24:16.923030",
        "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
        "discount_prompt_uuid": "81566856437527756928",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "500"
          },
          {
            "greater_than": "500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "segment",
        "tags": [
          "61268299727527493760"
        ],
        "updated_at": "2026-06-01 22:24:16.923030",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "5",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:18.730783",
        "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
        "discount_prompt_uuid": "87759969798493061248",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "item",
        "tags": [
          "06041993713794695296"
        ],
        "updated_at": "2026-06-01 22:24:18.730783",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season
... (truncated)
```

### 27. files / upload_rfq_file

- Method: `upload_rfq_file`
- Status: `pass`
- Elapsed: `3585.85 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "file_name": "integration_test_spec.pdf",
  "email": "jessicacooper@example.com"
}
```

Output:

```json
{
  "file": {
    "request_uuid": "96306650268729098368",
    "file_name": "integration_test_spec.pdf",
    "email": "jessicacooper@example.com",
    "partition_key": "gpt#nestaging",
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "96306650268729098368",
      "email": "jessicacooper@example.com",
      "request_title": "Honeymoon to ORD (updated by integration test)",
      "request_description": "Honeymoon trip for 2 adults. Open to splurge on the outbound in Business if pricing is reasonable.",
      "billing_address": {
        "country": "US",
        "city": "West Amy",
        "phone": "+1-287-493-0405x186",
        "street": "8532 Hernandez Ports",
        "name": "Heidi Garza",
        "state": "MA",
        "postal_code": "40901"
      },
      "shipping_address": {
        "country": "US",
        "city": "Lake Nathanside",
        "phone": "+1-494-213-4598",
        "street": "6159 Joyce Coves Suite 945",
        "name": "Mitchell Carrillo",
        "state": "WY",
        "postal_code": "72270"
      },
      "items": [
        {
          "cabin_preference": "Premium Economy",
          "quantity": "2",
          "item_uuid": "06041993713794695296",
          "provider_items": [],
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "completed",
      "expired_at": "2026-07-25T22:41:32.314663",
      "created_at": "2026-06-01T22:41:32.471123",
      "updated_by": "MCP",
      "updated_at": "2026-06-18T04:32:56.070316",
      "quotes": [
        {
          "final_total_quote_amount": "0",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "0",
          "status": "disapproved",
          "total_quote_amount": "0",
          "total_quote_discount": "0",
          "created_at": "2026-06-17 19:10:34.347670",
          "notes": "Auto-disapproved: Another quote was confirmed",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "12616028676071374976",
          "request_uuid": "96306650268729098368",
          "updated_at": "2026-06-17 19:12:07.004383",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "0",
          "provider_corp_external_id": "AIRLINE-LH",
          "rounds": "0",
          "shipping_amount": "0",
          "status": "disapproved",
          "total_quote_amount": "0",
          "total_quote_discount": "0",
          "created_at": "2026-06-01 22:43:00.075462",
          "currency": "USD",
          "display_currency": "CAD",
          "fx_rate": "1.335005",
          "fx_rate_locked_at": "2026-06-01 22:42:59.985871",
          "notes": "Auto-disapproved: Another quote was confirmed",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "42458963099238023296",
          "request_uuid": "96306650268729098368",
          "sales_rep_email": "kimberly71@example.org",
          "updated_at": "2026-06-17 19:11:59.548180",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "25",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "completed",
          "total_quote_amount": "0",
          "total_quote_discount": "0",
          "created_at": "2026-06-01 22:42:59.864855",
          "currency": "USD",
          "display_currency": "CNY",
          "fx_rate": "7.081345",
          "fx_rate_locked_at": "2026-06-01 22:42:59.540604",
          "notes": "Auto-completed: All installments paid",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "83893620897501692032",
          "request_uuid": "96306650268729098368",
          "sales_rep_email": "jordan99@example.net",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 04:32:44.719388",
          "updated_by": "MCP"
        }
      ],
      "files": [
        {
          "created_at": "2026-06-17 19:11:33.981790",
          "email": "jessicacooper@example.com",
          "file_name": "integration_test_spec.pdf",
          "partition_key": "gpt#nestaging",
          "request_uuid": "96306650268729098368",
          "updated_at": "2026-06-18 04:40:22.620940",
          "updated_by": "MCP"
        }
      ],
      "bundle": null
    },
    "updated_by": "MCP",
    "created_at": "2026-06-17T19:11:33.981790",
    "updated_at": "2026-06-18T04:40:22.620940"
  }
}
```

### 28. files / get_rfq_files

- Method: `get_rfq_files`
- Status: `pass`
- Elapsed: `3460.12 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": 10,
  "page_number": 1,
  "total": 1,
  "file_list": [
    {
      "request_uuid": "96306650268729098368",
      "file_name": "integration_test_spec.pdf",
      "email": "jessicacooper@example.com",
      "partition_key": "gpt#nestaging",
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "96306650268729098368",
        "email": "jessicacooper@example.com",
        "request_title": "Honeymoon to ORD (updated by integration test)",
        "request_description": "Honeymoon trip for 2 adults. Open to splurge on the outbound in Business if pricing is reasonable.",
        "billing_address": {
          "country": "US",
          "city": "West Amy",
          "phone": "+1-287-493-0405x186",
          "street": "8532 Hernandez Ports",
          "name": "Heidi Garza",
          "state": "MA",
          "postal_code": "40901"
        },
        "shipping_address": {
          "country": "US",
          "city": "Lake Nathanside",
          "phone": "+1-494-213-4598",
          "street": "6159 Joyce Coves Suite 945",
          "name": "Mitchell Carrillo",
          "state": "WY",
          "postal_code": "72270"
        },
        "items": [
          {
            "cabin_preference": "Premium Economy",
            "quantity": "2",
            "item_uuid": "06041993713794695296",
            "provider_items": [],
            "pax_breakdown": {
              "adult": "2"
            }
          }
        ],
        "notes": "Updated via run_integration.py",
        "bundle_uuid": null,
        "status": "completed",
        "expired_at": "2026-07-25T22:41:32.314663",
        "created_at": "2026-06-01T22:41:32.471123",
        "updated_by": "MCP",
        "updated_at": "2026-06-18T04:32:56.070316",
        "quotes": [
          {
            "final_total_quote_amount": "0",
            "provider_corp_external_id": "AIRLINE-AF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "disapproved",
            "total_quote_amount": "0",
            "total_quote_discount": "0",
            "created_at": "2026-06-17 19:10:34.347670",
            "notes": "Auto-disapproved: Another quote was confirmed",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "12616028676071374976",
            "request_uuid": "96306650268729098368",
            "updated_at": "2026-06-17 19:12:07.004383",
            "updated_by": "MCP"
          },
          {
            "final_total_quote_amount": "0",
            "provider_corp_external_id": "AIRLINE-LH",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "disapproved",
            "total_quote_amount": "0",
            "total_quote_discount": "0",
            "created_at": "2026-06-01 22:43:00.075462",
            "currency": "USD",
            "display_currency": "CAD",
            "fx_rate": "1.335005",
            "fx_rate_locked_at": "2026-06-01 22:42:59.985871",
            "notes": "Auto-disapproved: Another quote was confirmed",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "42458963099238023296",
            "request_uuid": "96306650268729098368",
            "sales_rep_email": "kimberly71@example.org",
            "updated_at": "2026-06-17 19:11:59.548180",
            "updated_by": "MCP"
          },
          {
            "final_total_quote_amount": "25",
            "provider_corp_external_id": "AIRLINE-QF",
            "rounds": "0",
            "shipping_amount": "25",
            "status": "completed",
            "total_quote_amount": "0",
            "total_quote_discount": "0",
            "created_at": "2026-06-01 22:42:59.864855",
            "currency": "USD",
            "display_currency": "CNY",
            "fx_rate": "7.081345",
            "fx_rate_locked_at": "2026-06-01 22:42:59.540604",
            "notes": "Auto-completed: All installments paid",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "83893620897501692032",
            "request_uuid": "96306650268729098368",
            "sales_rep_email": "jordan99@example.net",
            "shipping_method": "ticket_delivery",
            "updated_at": "2026-06-18 04:32:44.719388",
            "updated_by": "MCP"
          }
        ],
        "files": [
          {
            "created_at": "2026-06-17 19:11:33.981790",
            "email": "jessicacooper@example.com",
            "file_name": "integration_test_spec.pdf",
            "partition_key": "gpt#nestaging",
            "request_uuid": "96306650268729098368",
            "updated_at": "2026-06-18 04:40:22.620940",
            "updated_by": "MCP"
          }
        ],
        "bundle": null
      },
      "updated_by": "MCP",
      "created_at": "2026-06-17T19:11:33.981790",
      "updated_at": "2026-06-18T04:40:22.620940"
    }
  ]
}
```

### 29. segments / get_segment_contacts

- Method: `get_segment_contacts`
- Status: `pass`
- Elapsed: `3657.96 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": 10,
  "page_number": 1,
  "total": 15,
  "segment_contact_list": [
    {
      "partition_key": "gpt#nestaging",
      "email": "andrew64@example.net",
      "contact_uuid": null,
      "consumer_corp_external_id": "CUST-7233",
      "segment_uuid": "42260216389897830528",
      "segment": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "segment_uuid": "42260216389897830528",
        "provider_corp_external_id": "PROV-3991",
        "segment_name": "Jordan Group Tier",
        "segment_description": "Expanded regional architecture",
        "created_at": "2026-05-28T22:28:17.108418",
        "updated_by": "prepare_segments_and_contacts",
        "updated_at": "2026-05-28T22:28:17.108418",
        "contacts": [
          {
            "consumer_corp_external_id": "CUST-3758",
            "created_at": "2026-05-28 22:28:17.914494",
            "email": "haydenanthony@example.org",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "42260216389897830528",
            "updated_at": "2026-05-28 22:28:17.914494",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-7233",
            "created_at": "2026-05-28 22:28:18.066369",
            "email": "andrew64@example.net",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "42260216389897830528",
            "updated_at": "2026-05-28 22:28:18.066369",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-4818",
            "created_at": "2026-05-28 22:28:17.614481",
            "email": "anne23@example.org",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "42260216389897830528",
            "updated_at": "2026-05-28 22:28:17.614481",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-3250",
            "created_at": "2026-05-28 22:28:18.439958",
            "email": "dbeck@example.com",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "42260216389897830528",
            "updated_at": "2026-05-28 22:28:18.439958",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-7648",
            "created_at": "2026-05-28 22:28:17.765282",
            "email": "mercedessullivan@example.net",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "42260216389897830528",
            "updated_at": "2026-05-28 22:28:17.765282",
            "updated_by": "prepare_segments_and_contacts"
          }
        ]
      },
      "updated_by": "prepare_segments_and_contacts",
      "created_at": "2026-05-28T22:28:18.066369",
      "updated_at": "2026-05-28T22:28:18.066369"
    },
    {
      "partition_key": "gpt#nestaging",
      "email": "anne23@example.org",
      "contact_uuid": null,
      "consumer_corp_external_id": "CUST-4818",
      "segment_uuid": "42260216389897830528",
      "segment": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "segment_uuid": "42260216389897830528",
        "provider_corp_external_id": "PROV-3991",
        "segment_name": "Jordan Group Tier",
        "segment_description": "Expanded regional architecture",
        "created_at": "2026-05-28T22:28:17.108418",
        "updated_by": "prepare_segments_and_contacts",
        "updated_at": "2026-05-28T22:28:17.108418",
        "contacts": [
          {
            "consumer_corp_external_id": "CUST-3758",
            "created_at": "2026-05-28 22:28:17.914494",
            "email": "haydenanthony@example.org",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "42260216389897830528",
            "updated_at": "2026-05-28 22:28:17.914494",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-7233",
            "created_at": "2026-05-28 22:28:18.066369",
            "email": "andrew64@example.net",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "42260216389897830528",
            "updated_at": "2026-05-28 22:28:18.066369",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-4818",
            "created_at": "2026-05-28 22:28:17.614481",
            "email": "anne23@example.org",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "42260216389897830528",
            "updated_at": "2026-05-28 22:28:17.614481",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-3250",
            "created_at": "2026-05-28 22:28:18.439958",
            "email": "dbeck@example.com",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "42260216389897830528",
            "updated_at": "2026-05-28 22:28:18.439958",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-7648",
            "created_at": "2026-05-28 22:28:17.765282",
            "email": "mercedessullivan@example.net",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "42260216389897830528",
            "updated_at": "2026-05-28 22:28:17.765282",
            "updated_by": "prepare_segments_and_contacts"
          }
        ]
      },
      "updated_by": "prepare_segments_and_contacts",
      "created_at": "2026-05-28T22:28:17.614481",
      "updated_at": "2026-05-28T22:28:17.614481"
    },
    {
      "partition_key": "gpt#nestaging",
      "email": "asnyder@example.net",
      "contact_uuid": null,
      "consumer_corp_external_id": "CUST-4005",
      "segment_uuid": "39877485344341377152",
      "segment": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "segment_uuid": "39877485344341377152",
        "provider_corp_external_id": "PROV-8990",
        "segment_name": "Bailey and Sons Tier",
        "segment_description": "Configurable maximized firmware",
        "created_at": "2026-05-28T22:28:18.592140",
        "updated_by": "prepare_segments_and_contacts",
        "updated_at": "2026-05-28T22:28:18.592140",
        "contacts": [
          {
            "consumer_corp_external_id": "CUST-4005",
            "created_at": "2026-05-28 22:28:19.250405",
            "email": "asnyder@example.net",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "39877485344341377152",
            "updated_at": "2026-05-28 22:28:19.250405",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-3079",
            "created_at": "2026-05-28 22:28:19.412300",
            "email": "orichmond@example.com",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "39877485344341377152",
            "updated_at": "2026-05-28 22:28:19.412300",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-7811",
            "created_at": "2026-05-28 22:28:19.557544",
            "email": "carolyn72@example.org",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "39877485344341377152",
            "updated_at": "2026-05-28 22:28:19.557544",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-8417",
            "created_at": "2026-05-28 22:28:19.701382",
            "email": "elizabeth59@example.com",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "39877485344341377152",
            "updated_at": "2026-05-28 22:28:19.701382",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-8444",
            "created_at": "2026-05-28 22:28:19.106989",
            "email": "hgiles@example.com",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "39877485344341377152",
            "updated_at": "2026-05-28 22:28:19.106989",
            "updated_by": "prepare_segments_and_contacts"
          }
        ]
      },
      "updated_by": "prepare_segments_and_contacts",
      "created_at": "2026-05-28T22:28:19.250405",
      "updated_at": "2026-05-28T22:28:19.250405"
    },
    {
      "partition_key": "gpt#nestaging",
      "email": "beannorma@example.com",
      "contact_uuid": null,
      "consumer_corp_external_id": "CUST-2064",
      "segment_uuid": "61268299727527493760",
      "segment": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "segment_uuid": "61268299727527493760",
        "provider_corp_external_id": "PROV-9998",
        "segment_name": "Johnson, Riley and Lozano Tier",
        "segment_description": "Extended background focus group",
        "created_at": "2026-05-28T22:28:15.824664",
        "updated_by": "prepare_segments_and_contacts",
        "updated_at": "2026-05-28T22:28:15.824664",
        "contacts": [
          {
            "consumer_corp_external_id": "CUST-2621",
            "created_at": "2026-05-28 22:28:16.526197",
            "email": "deanna17@example.org",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "61268299727527493760",
            "updated_at": "2026-05-28 22:28:16.526197",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-5061",
            "created_at": "2026-05-28 22:28:16.676757",
            "email": "jessicacooper@example.com",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "61268299727527493760",
            "updated_at": "2026-05-28 22:28:16.676757",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-2567",
            "created_at": "2026-05-28 22:28:16.963958",
            "email": "hamiltontimothy@example.org",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "61268299727527493760",
            "updated_at": "2026-05-28 22:28:16.963958",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-2064",
            "created_at": "2026-05-28 22:28:16.820079",
            "email": "beannorma@example.com",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "61268299727527493760",
            "updated_at": "2026-05-28 22:28:16.820079",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-8256",
            "created_at": "2026-05-28 22:28:16.371502",
            "email": "golson@example.net",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "61268299727527493760",
            "updated_at": "2026-05-28 22:28:16.371502",
            "updated_by": "prepare_segments_and_contacts"
          }
        ]
      },
      "updated_by": "prepare_segments_and_contacts",
      "created_at": "2026-05-28T22:28:16.820079",
      "updated_at": "2026-05-28T22:28:16.820079"
    },
    {
      "partition_key": "gpt#nestaging",
      "email": "carolyn72@example.org",
      "contact_uuid": null,
      "consumer_corp_external_id": "CUST-7811",
      "segment_uuid": "39877485344341377152",
      "segment": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "segment_uuid": "39877485344341377152",
        "provider_corp_external_id": "PROV-8990",
        "segment_n
... (truncated)
```

### 30. availability / check_availability

- Method: `check_availability`
- Status: `pass`
- Elapsed: `3336.19 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720",
  "service_start_at": "2026-09-12T19:00:00Z",
  "service_end_at": "2026-09-12T23:07:47.008532Z",
  "batch_no": "AF6267-20260912",
  "qty": 2
}
```

Output:

```json
{
  "operation": "check",
  "provider_item_uuid": "39876487618607726720",
  "batch_no": "AF6267-20260912",
  "service_start_at": "2026-09-12T19:00:00+00:00",
  "service_end_at": "2026-09-12T23:07:47.008532+00:00",
  "available": true,
  "hold_token": null,
  "expires_at": null,
  "payload": {
    "reason": "available",
    "matched_batches": 1,
    "available_batches": 1,
    "total_available_qty": 12.0,
    "slow_move": false
  },
  "fetched_at": "2026-06-18T04:40:33.314795+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 31. availability / acquire_availability_hold

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `3494.57 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720",
  "service_start_at": "2026-09-12T19:00:00Z",
  "service_end_at": "2026-09-12T23:07:47.008532Z",
  "qty": 2,
  "batch_no": "AF6267-20260912",
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
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
    "service_start_at": "2026-09-12T19:00:00+00:00",
    "service_end_at": "2026-09-12T23:07:47.008532+00:00",
    "available": true,
    "hold_token": "6c0221285929b66829849c5fdc4e7e0e",
    "expires_at": "2026-06-18T04:55:36.696951+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 12.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-18T04:40:36.809603+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 32. availability / confirm_availability_hold

- Method: `confirm_availability_hold`
- Status: `pass`
- Elapsed: `3360.68 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "6c0221285929b66829849c5fdc4e7e0e",
  "provider_item_uuid": "39876487618607726720",
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "availability": {
    "operation": "confirm_hold",
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
    "service_start_at": null,
    "service_end_at": null,
    "available": true,
    "hold_token": "6c0221285929b66829849c5fdc4e7e0e",
    "expires_at": null,
    "payload": {
      "reason": "hold_confirmed"
    },
    "fetched_at": "2026-06-18T04:40:40.170867+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```

### 33. availability / acquire_availability_hold (for release test)

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `3480.51 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720",
  "service_start_at": "2026-09-12T19:00:00Z",
  "service_end_at": "2026-09-12T23:07:47.008532Z",
  "qty": 1,
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
    "service_start_at": "2026-09-12T19:00:00+00:00",
    "service_end_at": "2026-09-12T23:07:47.008532+00:00",
    "available": true,
    "hold_token": "d4aa9e2b655bb69293527d94d204291d",
    "expires_at": "2026-06-18T04:55:43.539484+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 10.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-18T04:40:43.651146+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 34. availability / release_availability_hold

- Method: `release_availability_hold`
- Status: `pass`
- Elapsed: `3386.98 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "d4aa9e2b655bb69293527d94d204291d",
  "provider_item_uuid": "39876487618607726720",
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "availability": {
    "operation": "release_hold",
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
    "service_start_at": null,
    "service_end_at": null,
    "available": true,
    "hold_token": "d4aa9e2b655bb69293527d94d204291d",
    "expires_at": null,
    "payload": {
      "reason": "hold_released"
    },
    "fetched_at": "2026-06-18T04:40:47.039331+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```

### 35. availability / acquire_availability_hold (for expire test)

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `3431.28 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720",
  "service_start_at": "2026-09-12T19:00:00Z",
  "service_end_at": "2026-09-12T23:07:47.008532Z",
  "qty": 1,
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
    "service_start_at": "2026-09-12T19:00:00+00:00",
    "service_end_at": "2026-09-12T23:07:47.008532+00:00",
    "available": true,
    "hold_token": "2081531564c213131f385071e7497184",
    "expires_at": "2026-06-18T04:55:50.362411+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 10.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-18T04:40:50.470269+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 36. availability / expire_availability_hold

- Method: `expire_availability_hold`
- Status: `pass`
- Elapsed: `3310.66 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "2081531564c213131f385071e7497184",
  "provider_item_uuid": "39876487618607726720",
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "availability": {
    "operation": "expire_hold",
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
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
- Elapsed: `3222.66 ms`

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
  "page_size": 100,
  "page_number": 1,
  "total": 0,
  "bundle_list": []
}
```

### 38. bundles / get_bundle (FLT-ITIN-001)

- Method: `get_bundle`
- Status: `pass`
- Elapsed: `3391.44 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "80092055917037633664"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "80092055917037633664",
  "bundle_code": "FLT-ITIN-001",
  "bundle_name": "Flight Itinerary DFW->SIN + ATL->ORD + CDG->JFK",
  "bundle_type": "flight_itinerary",
  "description": "Multi-leg flight itinerary template composed of independently priced flight legs.",
  "extra": {
    "routes": [
      "DFW->SIN",
      "ATL->ORD",
      "CDG->JFK"
    ],
    "source": "prepare_flight_products",
    "leg_count": "3",
    "item_external_ids": [
      "FLIGHT-DFW-SIN-BUS",
      "FLIGHT-ATL-ORD-PRE",
      "FLIGHT-CDG-JFK-BUS"
    ]
  },
  "status": "active",
  "created_at": "2026-06-01T22:19:33.335196",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-01T22:19:33.335196",
  "components": [
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "16716490355832275072",
      "bundle_uuid": "80092055917037633664",
      "item_uuid": "17735923656909930624",
      "provider_item_uuid": "55349863084404523136",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 3.0,
      "extra": {
        "route": "CDG->JFK",
        "item_external_id": "FLIGHT-CDG-JFK-BUS",
        "provider_item_external_id": "AF-CDG-JFK-BUS"
      },
      "status": "active",
      "created_at": "2026-06-01T22:19:34.360997",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:34.360997"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "18213661061617303680",
      "bundle_uuid": "80092055917037633664",
      "item_uuid": "15269325584579182720",
      "provider_item_uuid": "48138115986131796096",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 1.0,
      "extra": {
        "route": "DFW->SIN",
        "item_external_id": "FLIGHT-DFW-SIN-BUS",
        "provider_item_external_id": "SQ-DFW-SIN-BUS"
      },
      "status": "active",
      "created_at": "2026-06-01T22:19:33.797121",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:33.797121"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "54618154874979762304",
      "bundle_uuid": "80092055917037633664",
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 2.0,
      "extra": {
        "route": "ATL->ORD",
        "item_external_id": "FLIGHT-ATL-ORD-PRE",
        "provider_item_external_id": "AF-ATL-ORD-PRE"
      },
      "status": "active",
      "created_at": "2026-06-01T22:19:34.077258",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:34.077258"
    }
  ]
}
```

### 39. bundles / search_bundle_components

- Method: `search_bundle_components`
- Status: `pass`
- Elapsed: `3306.89 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "80092055917037633664"
}
```

Output:

```json
{
  "page_size": 100,
  "page_number": 1,
  "total": 3,
  "bundle_component_list": [
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "16716490355832275072",
      "bundle_uuid": "80092055917037633664",
      "item_uuid": "17735923656909930624",
      "provider_item_uuid": "55349863084404523136",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 3.0,
      "extra": {
        "route": "CDG->JFK",
        "item_external_id": "FLIGHT-CDG-JFK-BUS",
        "provider_item_external_id": "AF-CDG-JFK-BUS"
      },
      "status": "active",
      "created_at": "2026-06-01T22:19:34.360997",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:34.360997"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "18213661061617303680",
      "bundle_uuid": "80092055917037633664",
      "item_uuid": "15269325584579182720",
      "provider_item_uuid": "48138115986131796096",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 1.0,
      "extra": {
        "route": "DFW->SIN",
        "item_external_id": "FLIGHT-DFW-SIN-BUS",
        "provider_item_external_id": "SQ-DFW-SIN-BUS"
      },
      "status": "active",
      "created_at": "2026-06-01T22:19:33.797121",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:33.797121"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "54618154874979762304",
      "bundle_uuid": "80092055917037633664",
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 2.0,
      "extra": {
        "route": "ATL->ORD",
        "item_external_id": "FLIGHT-ATL-ORD-PRE",
        "provider_item_external_id": "AF-ATL-ORD-PRE"
      },
      "status": "active",
      "created_at": "2026-06-01T22:19:34.077258",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:34.077258"
    }
  ]
}
```

### 40. cancellation / get_cancellation_policy (Business Fare)

- Method: `get_cancellation_policy`
- Status: `pass`
- Elapsed: `3244.63 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "policy_uuid": "14167382355785826432"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "policy_uuid": "14167382355785826432",
  "provider_item_uuid": null,
  "label": "Premium Economy Fare Cancellation",
  "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
  "tiers": {
    "tiers": [
      {
        "hours_before_departure_gte": "168",
        "refund_pct": "1"
      },
      {
        "hours_before_departure_gte": "24",
        "refund_pct": "0.5"
      },
      {
        "hours_before_departure_gte": "0",
        "refund_pct": "0"
      }
    ]
  },
  "notes_template_uuid": null,
  "status": "active",
  "created_at": "2026-06-01T22:19:29.641481",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-01T22:19:29.641481"
}
```

### 41. cancellation / search_cancellation_policies

- Method: `search_cancellation_policies`
- Status: `pass`
- Elapsed: `3273.97 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720"
}
```

Output:

```json
{
  "page_size": 100,
  "page_number": 1,
  "total": 0,
  "cancellation_policy_list": []
}
```

### 42. catalog / inquire_catalog

- Method: `inquire_catalog`
- Status: `pass`
- Elapsed: `4956.44 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "query_text": "Air France ATL ORD Premium Economy flight with meal included",
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
            "text": "Flight product: Flight ATL->ORD Premium Economy. Premium Economy class non-stop service from Atlanta (ATL) to Chicago (ORD). Route: ATL to ORD. Cabin class: Premium Economy. Operated by: Air France (AF). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 450.0, child USD 337.5, infant USD 45.0. Scheduled flights: AF6267 departing 2026-09-12T19:00:00Z, 52 seats; AF5319 departing 2026-09-07T12:00:00Z, 37 seats. Premium Economy Fare Cancellation: 168h+: 100% refund; 24h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary DFW->SIN + ATL->ORD + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:25",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:25",
          "score": "0.8713676929473877",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight ATL->ORD Economy. Economy class non-stop service from Atlanta (ATL) to Chicago (ORD). Route: ATL to ORD. Cabin class: Economy. Operated by: Qantas (QF). Baggage allowance: 23 kg. Meal included: no. Fares: adult USD 250.0, child USD 187.5, infant USD 25.0. Scheduled flights: QF1351 departing 2026-07-09T21:45:00Z, 145 seats; QF5796 departing 2026-09-21T19:45:00Z, 169 seats. Economy Fare Cancellation: 168h+: 100% refund; 24h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:17",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:17",
          "score": "0.7910864353179932",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight CDG->JFK Business. Business class non-stop service from Paris (CDG) to New York (JFK). Route: CDG to JFK. Cabin class: Business. Operated by: Air France (AF). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 1800.0, child USD 1350.0, infant USD 180.0. Scheduled flights: AF8751 departing 2026-08-11T08:30:00Z, 30 seats; AF5020 departing 2026-06-16T08:30:00Z, 22 seats. Business Fare Cancellation: 24h+: 100% refund; 2h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary DFW->SIN + ATL->ORD + CDG->JFK, Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:1",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:1",
          "score": "0.7605776190757751",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight LAX->HKG Premium Economy. Premium Economy class non-stop service from Los Angeles (LAX) to Hong Kong (HKG). Route: LAX to HKG. Cabin class: Premium Economy. Operated by: Lufthansa (LH). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 450.0, child USD 337.5, infant USD 45.0. Scheduled flights: LH6452 departing 2026-08-01T21:15:00Z, 34 seats; LH3684 departing 2026-09-26T20:45:00Z, 41 seats. Premium Economy Fare Cancellation: 168h+: 100% refund; 24h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:33",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:33",
          "score": "0.7334754467010498",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight DFW->SIN Business. Business class non-stop service from Dallas (DFW) to Singapore (SIN). Route: DFW to SIN. Cabin class: Business. Operated by: Singapore Airlines (SQ). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 1800.0, child USD 1350.0, infant USD 180.0. Scheduled flights: SQ6901 departing 2026-08-12T13:45:00Z, 33 seats; SQ8511 departing 2026-09-26T19:15:00Z, 30 seats. Business Fare Cancellation: 24h+: 100% refund; 2h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary DFW->SIN + ATL->ORD + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:9",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:9",
          "score": "0.6800907850265503",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-18T04:41:15.176336+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```
