# MCP HospiRFQ Processor Live Integration Results

- Generated at: `2026-06-23T17:06:55.382896+00:00`
- Gateway: `http://localhost:8765`
- Endpoint: `gpt`
- Partition: `nestaging`
- GraphQL URL: `http://localhost:8765/gpt/rfq_graphql`
- Dependency order: `catalog_discovery, items, requests, quotes, pricing, installments, files, segments, availability, bundles, cancellation, catalog`
- Passed: `42`
- Error responses: `0`
- Failed: `0`
- Total calls: `42`
- SOP reference: `docs/integration_scenarios_sop.md` version `0.1.0`, approved by user on `2026-06-17`
- Final certification status: `Integration Certified`

## Executive Summary

End-to-end live integration testing was executed against the local `silvaengine_gateway` route for `mcp_hospirfq_processor` using `.env`-driven connection settings and prepared `../rfq_engine` flight RFQ data. The final dependency-ordered run completed with 42 passing function calls, 0 error responses, and 0 failures. Catalog search was executed first and selected `Flight CDG->SFO First`, which was reconciled to `flight_catalog_refs.json` and `flight_products.json` before item, request, quote, pricing, installment, availability, bundle, cancellation, and catalog validation continued. The SOP-scoped integration is certified for the tested local environment.

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
| Catalog selection consistency | selected catalog hit maps to `flight_catalog_refs.json` item/provider IDs | 0 mismatches | `52065619693805781120` / `94764066649319424128` selected | pass |
| Batch consistency | selected item/provider maps to `flight_products.json` batch and service window | 0 mismatches | `QF1351-20260709`, `2026-07-09T21:45:00Z` to `2026-07-10T03:11:29.751482Z` | pass |
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
- Elapsed: `4623.44 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "query_text": "Qantas CDG SFO First class flight",
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
          "score": "0.7828671932220459",
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
          "score": "0.7722446322441101",
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
          "score": "0.7453662157058716",
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
          "score": "0.6812183856964111",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "British Airways (BA) operates flight service Flight ORD->BOS Business from ORD to BOS in Business class. Business class non-stop service from Chicago (ORD) to Boston (BOS). Base price $1800.0 USD per seat. Baggage allowance 32kg, meal included: True. Pricing tiers:   - adult: $1800.0 USD;   - child: $1350.0 USD;   - infant: $180.0 USD. Scheduled flights:\n  - Flight BA1430 departing 2026-07-17T21:00:00Z arriving 2026-07-18T00:24:58.762088Z with 24 seats available. Cancellation policy: Business Fare Cancellation.\n  - Flight BA7142 departing 2026-08-08T11:00:00Z arriving 2026-08-08T16:28:08.421105Z with 26 seats available. Cancellation policy: Business Fare Cancellation.\nThis is a Business class flight product offered by British Airways on the ORD->BOS route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:20",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:20",
          "score": "0.6810191869735718",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-23T17:02:05.415446+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 2. items / search_items (flight type)

- Method: `search_items`
- Status: `pass`
- Elapsed: `2724.78 ms`

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
  "total": 15,
  "item_list": [
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "57869541269638758528",
      "item_type": "flight",
      "item_name": "Flight HKG->SFO Economy",
      "item_description": "Economy class non-stop service from Hong Kong (HKG) to San Francisco (SFO).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-HKG-SFO-ECO",
      "created_at": "2026-06-22T03:42:33.640959",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T03:42:33.640959"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "61752444679215923328",
      "item_type": "flight",
      "item_name": "Flight SYD->JFK First",
      "item_description": "First class non-stop service from Sydney (SYD) to New York (JFK).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-SYD-JFK-FIR",
      "created_at": "2026-06-21T23:49:54.517021",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-21T23:49:54.518028"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "03407115177205710976",
      "item_type": "flight",
      "item_name": "Flight SFO->SYD First",
      "item_description": "First class non-stop service from San Francisco (SFO) to Sydney (SYD).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-SFO-SYD-FIR",
      "created_at": "2026-06-22T03:42:31.678900",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T03:42:31.678900"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "84800684729391136896",
      "item_type": "flight",
      "item_name": "Flight LAX->MIA Business",
      "item_description": "Business class non-stop service from Los Angeles (LAX) to Miami (MIA).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-LAX-MIA-BUS",
      "created_at": "2026-06-22T03:42:39.139616",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T03:42:39.139616"
    },
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
      "item_uuid": "03615636036750688384",
      "item_type": "flight",
      "item_name": "Flight SFO->BOS Economy",
      "item_description": "Economy class non-stop service from San Francisco (SFO) to Boston (BOS).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-SFO-BOS-ECO",
      "created_at": "2026-06-21T23:49:58.306020",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-21T23:49:58.306020"
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
      "item_uuid": "81113158557154427008",
      "item_type": "flight",
      "item_name": "Flight ATL->LAX Premium Economy",
      "item_description": "Premium Economy class non-stop service from Atlanta (ATL) to Los Angeles (LAX).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-ATL-LAX-PRE",
      "created_at": "2026-06-22T03:42:37.258098",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T03:42:37.258098"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "69015048170408788096",
      "item_type": "flight",
      "item_name": "Flight NRT->SFO Business",
      "item_description": "Business class non-stop service from Tokyo (NRT) to San Francisco (SFO).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-NRT-SFO-BUS",
      "created_at": "2026-06-21T23:50:02.024381",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-21T23:50:02.024381"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "32758768960952877184",
      "item_type": "flight",
      "item_name": "Flight LAX->BOS First",
      "item_description": "First class non-stop service from Los Angeles (LAX) to Boston (BOS).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-LAX-BOS-FIR",
      "created_at": "2026-06-21T23:49:56.375472",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-21T23:49:56.375472"
    }
  ]
}
```

### 3. items / get_item (Flight CDG->SFO First)

- Method: `get_item`
- Status: `pass`
- Elapsed: `2320.1 ms`

Arguments:

```json
{
  "item_uuid": "52065619693805781120"
}
```

Output:

```json
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
}
```

### 4. items / get_provider_items (with batches)

- Method: `get_provider_items`
- Status: `pass`
- Elapsed: `5370.64 ms`

Arguments:

```json
{
  "item_uuid": "52065619693805781120"
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
      "provider_item_uuid": "94764066649319424128",
      "provider_corp_external_id": "AIRLINE-QF",
      "provider_item_external_id": "QF-ATL-ORD-ECO",
      "base_price_per_uom": 250.0,
      "item_spec": {
        "cabin_class": "Economy",
        "meal_included": false,
        "destination_iata": "ORD",
        "airline_code": "QF",
        "origin_iata": "ATL",
        "airline_name": "Qantas",
        "baggage_allowance_kg": "23"
      },
      "availability_mode": "require_hold",
      "item_uuid": "52065619693805781120",
      "item": {
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
      "updated_by": "prepare_flight_products",
      "created_at": "2026-06-01T22:19:28.337451",
      "updated_at": "2026-06-01T22:19:28.337451",
      "batches": [
        {
          "provider_item_uuid": "94764066649319424128",
          "batch_no": "QF5796-20260921",
          "item_uuid": "52065619693805781120",
          "partition_key": "gpt#nestaging",
          "cost_per_uom": 137.5,
          "freight_cost_per_uom": 0.0,
          "additional_cost_per_uom": 15.92,
          "total_cost_per_uom": 153.42,
          "guardrail_margin_per_uom": 0.0,
          "guardrail_price_per_uom": 153.42,
          "in_stock": true,
          "slow_move_item": false,
          "availability_qty": 165.0,
          "expired_at": "2026-09-21T22:44:57.764776",
          "produced_at": "2026-03-25T19:45:00",
          "service_start_at": "2026-09-21T19:45:00",
          "service_end_at": "2026-09-21T22:44:57.764776",
          "currency": "USD",
          "cancellation_policy_uuid": "45519135682445983872",
          "item": {
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
          "provider_item": {
            "partition_key": "gpt#nestaging",
            "provider_item_uuid": "94764066649319424128",
            "provider_corp_external_id": "AIRLINE-QF",
            "provider_item_external_id": "QF-ATL-ORD-ECO",
            "base_price_per_uom": 250.0,
            "item_spec": {
              "cabin_class": "Economy",
              "meal_included": false,
              "destination_iata": "ORD",
              "airline_code": "QF",
              "origin_iata": "ATL",
              "airline_name": "Qantas",
              "baggage_allowance_kg": "23"
            },
            "availability_mode": "require_hold",
            "item_uuid": "52065619693805781120",
            "item": {
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
            "updated_by": "prepare_flight_products",
            "created_at": "2026-06-01T22:19:28.337451",
            "updated_at": "2026-06-01T22:19:28.337451"
          },
          "updated_by": "prepare_flight_products",
          "created_at": "2026-06-01T22:19:28.927355",
          "updated_at": "2026-06-01T22:46:21.699998"
        }
      ]
    }
  ]
}
```

### 5. requests / submit_rfq_request

- Method: `submit_rfq_request`
- Status: `pass`
- Elapsed: `3581.23 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight CDG->SFO First",
  "request_description": "E2E test request via silvaengine_gateway",
  "items": [
    {
      "item_uuid": "52065619693805781120",
      "item_name": "Flight CDG->SFO First",
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
  "request_uuid": "87250279722284761216",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight CDG->SFO First",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight CDG->SFO First",
      "item_uuid": "52065619693805781120",
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
  "created_at": "2026-06-23T17:02:18.464944",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T17:02:18.464944",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 6. requests / get_rfq_request (seeded)

- Method: `get_rfq_request`
- Status: `pass`
- Elapsed: `2419.15 ms`

Arguments:

```json
{
  "request_uuid": "03075416831792529536"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "03075416831792529536",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
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
          "batch_no": "AF5319-20260907",
          "qty": "2"
        }
      ],
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "completed",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T20:52:05.947710",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T16:59:24.824102",
  "quotes": [
    {
      "final_total_quote_amount": "875",
      "provider_corp_external_id": "AIRLINE-AF",
      "rounds": "0",
      "shipping_amount": "25",
      "status": "completed",
      "total_quote_amount": "900",
      "total_quote_discount": "50",
      "created_at": "2026-06-18 20:54:02.795771",
      "notes": "Auto-completed: All installments paid",
      "partition_key": "gpt#nestaging",
      "quote_uuid": "60187438571235328128",
      "request_uuid": "03075416831792529536",
      "shipping_method": "ticket_delivery",
      "updated_at": "2026-06-23 16:59:16.329730",
      "updated_by": "MCP"
    }
  ],
  "files": [
    {
      "created_at": "2026-06-23 16:54:37.215458",
      "email": "jessicacooper@example.com",
      "file_name": "integration_test_spec.pdf",
      "partition_key": "gpt#nestaging",
      "request_uuid": "03075416831792529536",
      "updated_at": "2026-06-23 16:59:27.443979",
      "updated_by": "MCP"
    }
  ],
  "bundle": null
}
```

### 7. requests / search_rfq_requests

- Method: `search_rfq_requests`
- Status: `pass`
- Elapsed: `3640.21 ms`

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
  "total": 76,
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
- Elapsed: `5159.95 ms`

Arguments:

```json
{
  "request_uuid": "87250279722284761216",
  "request_title": "Integration test: Flight CDG->SFO First (updated)",
  "notes": "Updated via run_integration.py"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "87250279722284761216",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight CDG->SFO First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight CDG->SFO First",
      "item_uuid": "52065619693805781120",
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
  "created_at": "2026-06-23T17:02:18.464944",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T17:02:30.230003",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 9. requests / add_item_to_rfq_request

- Method: `add_item_to_rfq_request`
- Status: `pass`
- Elapsed: `5235.84 ms`

Arguments:

```json
{
  "request_uuid": "87250279722284761216",
  "item": {
    "item_uuid": "06041993713794695296",
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
  "request_uuid": "87250279722284761216",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight CDG->SFO First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight CDG->SFO First",
      "item_uuid": "52065619693805781120",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    },
    {
      "item_name": "Flight CDG->ORD Economy",
      "item_uuid": "06041993713794695296",
      "provider_items": [],
      "qty": "1"
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-23T17:02:18.464944",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T17:02:35.481977",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 10. requests / remove_item_from_rfq_request

- Method: `remove_item_from_rfq_request`
- Status: `pass`
- Elapsed: `5222.38 ms`

Arguments:

```json
{
  "request_uuid": "87250279722284761216",
  "item_uuid": "06041993713794695296"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "87250279722284761216",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight CDG->SFO First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight CDG->SFO First",
      "item_uuid": "52065619693805781120",
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
  "created_at": "2026-06-23T17:02:18.464944",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T17:02:40.698371",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 11. requests / assign_provider_item_to_request_item

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `7687.96 ms`

Arguments:

```json
{
  "request_uuid": "87250279722284761216",
  "item_uuid": "52065619693805781120",
  "provider_item_uuid": "94764066649319424128",
  "provider_corp_external_id": "AIRLINE-QF",
  "qty": 2,
  "batch_no": "QF1351-20260709"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "87250279722284761216",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight CDG->SFO First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight CDG->SFO First",
      "item_uuid": "52065619693805781120",
      "provider_items": [
        {
          "provider_item_uuid": "94764066649319424128",
          "provider_corp_external_id": "AIRLINE-QF",
          "batch_no": "QF1351-20260709",
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
  "created_at": "2026-06-23T17:02:18.464944",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T17:02:48.386109",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 12. requests / remove_provider_item_from_request_item

- Method: `remove_provider_item_from_request_item`
- Status: `pass`
- Elapsed: `5572.91 ms`

Arguments:

```json
{
  "request_uuid": "87250279722284761216",
  "item_uuid": "52065619693805781120",
  "provider_item_uuid": "94764066649319424128"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "87250279722284761216",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight CDG->SFO First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight CDG->SFO First",
      "item_uuid": "52065619693805781120",
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
  "created_at": "2026-06-23T17:02:18.464944",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T17:02:53.959262",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 13. requests / assign_provider_item_to_request_item (for quote workflow)

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `7647.85 ms`

Arguments:

```json
{
  "request_uuid": "87250279722284761216",
  "item_uuid": "52065619693805781120",
  "provider_item_uuid": "94764066649319424128",
  "provider_corp_external_id": "AIRLINE-QF",
  "qty": 2,
  "batch_no": "QF1351-20260709"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "87250279722284761216",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight CDG->SFO First (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight CDG->SFO First",
      "item_uuid": "52065619693805781120",
      "provider_items": [
        {
          "provider_item_uuid": "94764066649319424128",
          "provider_corp_external_id": "AIRLINE-QF",
          "batch_no": "QF1351-20260709",
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
  "created_at": "2026-06-23T17:02:18.464944",
  "updated_by": "MCP",
  "updated_at": "2026-06-23T17:03:01.612305",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 14. quotes / confirm_request_and_create_quotes

- Method: `confirm_request_and_create_quotes`
- Status: `pass`
- Elapsed: `29725.37 ms`

Arguments:

```json
{
  "request_uuid": "87250279722284761216",
  "provider_corp_external_ids": [
    "AIRLINE-QF"
  ],
  "segment_uuid": "61268299727527493760",
  "batch_no": "QF1351-20260709",
  "service_start_at": "2026-07-09T21:45:00Z",
  "service_end_at": "2026-07-10T03:11:29.751482Z"
}
```

Output:

```json
{
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "87250279722284761216",
    "email": "jessicacooper@example.com",
    "request_title": "Integration test: Flight CDG->SFO First (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight CDG->SFO First",
        "item_uuid": "52065619693805781120",
        "provider_items": [
          {
            "provider_item_uuid": "94764066649319424128",
            "provider_corp_external_id": "AIRLINE-QF",
            "batch_no": "QF1351-20260709",
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
    "created_at": "2026-06-23T17:02:18.464944",
    "updated_by": "MCP",
    "updated_at": "2026-06-23T17:03:09.262831",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "created_quotes": [
    {
      "request_uuid": "87250279722284761216",
      "quote_uuid": "71820220336656367744",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-QF",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 500.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 500.0,
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
        "request_uuid": "87250279722284761216",
        "email": "jessicacooper@example.com",
        "request_title": "Integration test: Flight CDG->SFO First (updated)",
        "request_description": "E2E test request via silvaengine_gateway",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "item_name": "Flight CDG->SFO First",
            "item_uuid": "52065619693805781120",
            "provider_items": [
              {
                "provider_item_uuid": "94764066649319424128",
                "provider_corp_external_id": "AIRLINE-QF",
                "batch_no": "QF1351-20260709",
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
        "created_at": "2026-06-23T17:02:18.464944",
        "updated_by": "MCP",
        "updated_at": "2026-06-23T17:03:09.262831",
        "quotes": [
          {
            "final_total_quote_amount": "500",
            "provider_corp_external_id": "AIRLINE-QF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "in_progress",
            "total_quote_amount": "500",
            "total_quote_discount": "0",
            "created_at": "2026-06-23 17:03:14.380709",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "71820220336656367744",
            "request_uuid": "87250279722284761216",
            "updated_at": "2026-06-23 17:03:28.350347",
            "updated_by": "MCP"
          }
        ],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "batch_no": "QF1351-20260709",
          "created_at": "2026-06-23 17:03:21.019336",
          "final_subtotal": "500",
          "hold_expires_at": "2026-06-23 17:18:21.681078",
          "hold_token": "2768c361e5c8d7cd4e2eaeeb45e03bd9",
          "item_uuid": "52065619693805781120",
          "partition_key": "gpt#nestaging",
          "pax_breakdown": {
            "adult": "2"
          },
          "price_per_uom": "250",
          "provider_item_uuid": "94764066649319424128",
          "qty": "2",
          "quote_item_uuid": "06863801760542113920",
          "quote_uuid": "71820220336656367744",
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
              "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
              "label": "Economy Fare Cancellation",
              "content_hash": "5a29e5fb9ddcfc65",
              "policy_uuid": "45519135682445983872",
              "snapshotted_at": "2026-06-23 17:03:22.199785"
            }
          },
          "request_uuid": "87250279722284761216",
          "subtotal": "500",
          "subtotal_discount": "0",
          "subtotal_native": "500",
          "updated_at": "2026-06-23 17:03:21.019336",
          "updated_by": "MCP"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "priority": "8",
          "status": "active",
          "conditions": [
            "min_passengers >= 5",
            "booking_lead_days >= 7",
            "loyalty_tier in ['gold', 'platinum']"
          ],
          "created_at": "2026-06-21 23:50:31.742755",
          "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
          "discount_prompt_uuid": "83655032155864580224",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "2.5",
              "less_than": "2500"
            },
            {
              "greater_than": "2500",
              "max_discount_percentage": "7.5",
              "less_than": "7500"
            },
            {
              "greater_than": "7500",
              "max_discount_percentage": "12.5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "17.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-21 23:50:31.742755",
          "updated_by": "prepare_discount_prompts"
        },
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
          "priority": "10",
          "status": "active",
          "conditions": [
            "loyalty_tier in ['gold', 'platinum']"
          ],
          "created_at": "2026-06-21 23:50:31.444070",
          "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
          "discount_prompt_uuid": "74016050403706159232",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "2500"
            },
            {
              "greater_than": "2500",
              "max_discount_percentage": "10",
              "less_than": "12500"
            },
            {
              "greater_than": "12500",
              "max_discount_percentage": "12.5",
              "less_than": "13500"
            },
            {
              "greater_than": "13500",
              "max_discount_percentage": "15"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-21 23:50:31.444070",
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
          "priority": "2",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']"
          ],
          "created_at": "2026-06-22 03:43:11.520488",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-2515-LR)",
          "discount_prompt_uuid": "66044072765552607360",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "10000"
            },
            {
              "grea
... (truncated)
```

### 15. quotes / get_quote

- Method: `get_quote`
- Status: `pass`
- Elapsed: `2842.12 ms`

Arguments:

```json
{
  "quote_uuid": "71820220336656367744",
  "request_uuid": "87250279722284761216"
}
```

Output:

```json
{
  "request_uuid": "87250279722284761216",
  "quote_uuid": "71820220336656367744",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-QF",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": null,
  "shipping_amount": 0.0,
  "total_quote_amount": 500.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 500.0,
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
    "request_uuid": "87250279722284761216",
    "email": "jessicacooper@example.com",
    "request_title": "Integration test: Flight CDG->SFO First (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight CDG->SFO First",
        "item_uuid": "52065619693805781120",
        "provider_items": [
          {
            "provider_item_uuid": "94764066649319424128",
            "provider_corp_external_id": "AIRLINE-QF",
            "batch_no": "QF1351-20260709",
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
    "created_at": "2026-06-23T17:02:18.464944",
    "updated_by": "MCP",
    "updated_at": "2026-06-23T17:03:09.262831",
    "quotes": [
      {
        "final_total_quote_amount": "500",
        "provider_corp_external_id": "AIRLINE-QF",
        "rounds": "0",
        "shipping_amount": "0",
        "status": "in_progress",
        "total_quote_amount": "500",
        "total_quote_discount": "0",
        "created_at": "2026-06-23 17:03:14.380709",
        "partition_key": "gpt#nestaging",
        "quote_uuid": "71820220336656367744",
        "request_uuid": "87250279722284761216",
        "updated_at": "2026-06-23 17:03:28.350347",
        "updated_by": "MCP"
      }
    ],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "batch_no": "QF1351-20260709",
      "created_at": "2026-06-23 17:03:21.019336",
      "final_subtotal": "500",
      "hold_expires_at": "2026-06-23 17:18:21.681078",
      "hold_token": "2768c361e5c8d7cd4e2eaeeb45e03bd9",
      "item_uuid": "52065619693805781120",
      "partition_key": "gpt#nestaging",
      "pax_breakdown": {
        "adult": "2"
      },
      "price_per_uom": "250",
      "provider_item_uuid": "94764066649319424128",
      "qty": "2",
      "quote_item_uuid": "06863801760542113920",
      "quote_uuid": "71820220336656367744",
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
          "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
          "label": "Economy Fare Cancellation",
          "content_hash": "5a29e5fb9ddcfc65",
          "policy_uuid": "45519135682445983872",
          "snapshotted_at": "2026-06-23 17:03:22.199785"
        }
      },
      "request_uuid": "87250279722284761216",
      "subtotal": "500",
      "subtotal_discount": "0",
      "subtotal_native": "500",
      "updated_at": "2026-06-23 17:03:21.019336",
      "updated_by": "MCP"
    }
  ],
  "installments": [],
  "discount_prompts": [
    {
      "priority": "8",
      "status": "active",
      "conditions": [
        "min_passengers >= 5",
        "booking_lead_days >= 7",
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "created_at": "2026-06-21 23:50:31.742755",
      "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
      "discount_prompt_uuid": "83655032155864580224",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "7.5",
          "less_than": "7500"
        },
        {
          "greater_than": "7500",
          "max_discount_percentage": "12.5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "17.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-21 23:50:31.742755",
      "updated_by": "prepare_discount_prompts"
    },
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
      "priority": "10",
      "status": "active",
      "conditions": [
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "created_at": "2026-06-21 23:50:31.444070",
      "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
      "discount_prompt_uuid": "74016050403706159232",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "10",
          "less_than": "12500"
        },
        {
          "greater_than": "12500",
          "max_discount_percentage": "12.5",
          "less_than": "13500"
        },
        {
          "greater_than": "13500",
          "max_discount_percentage": "15"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-21 23:50:31.444070",
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
      "priority": "2",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']"
      ],
      "created_at": "2026-06-22 03:43:11.520488",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-2515-LR)",
      "discount_prompt_uuid": "66044072765552607360",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5",
          "less_than": "12500"
        },
        {
          "greater_than": "12500",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-22 03:43:11.520488",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "5",
      "status": "active",
      "conditions": [
        "season != 'peak'",
        "loyalty_tier in ['gold', 'platinum']",
        "min_passengers >= 5"
      ],
      "created_at": "2026-06-22 03:43:11.227867",
      "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1679-XS)",
      "discount_prompt_uuid": "04111458880109691008",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "10",
          "less_than": "2000"
        },
        {
          "greater_than": "2000",
          "max_discount_percentage": "15",
          "less_than": "4500"
        },
        {
          "greater_than": "4500",
          "max_discount_percentage": "20"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-22 03:43:11.227867",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "7",
      "status": "active",
      "conditions": [
        "channel == 'direct'",
        "loyalty_tier in ['gold', 'platinum']",
        "booking_lead_days >= 7"
      ],
      "created_at": "2026-06-22 03:43:11.378039",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-2051-BI)",
      "discount_prompt_uuid": "53711723630325416064",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "7.5",
          "less_than": "6000"
        },
        {
          "greater_than": "6000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "g
... (truncated)
```

### 16. quotes / search_quotes

- Method: `search_quotes`
- Status: `pass`
- Elapsed: `2828.5 ms`

Arguments:

```json
{
  "request_uuid": "87250279722284761216",
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
      "request_uuid": "87250279722284761216",
      "quote_uuid": "71820220336656367744",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-QF",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 500.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 500.0,
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
        "request_uuid": "87250279722284761216",
        "email": "jessicacooper@example.com",
        "request_title": "Integration test: Flight CDG->SFO First (updated)",
        "request_description": "E2E test request via silvaengine_gateway",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "item_name": "Flight CDG->SFO First",
            "item_uuid": "52065619693805781120",
            "provider_items": [
              {
                "provider_item_uuid": "94764066649319424128",
                "provider_corp_external_id": "AIRLINE-QF",
                "batch_no": "QF1351-20260709",
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
        "created_at": "2026-06-23T17:02:18.464944",
        "updated_by": "MCP",
        "updated_at": "2026-06-23T17:03:09.262831",
        "quotes": [
          {
            "final_total_quote_amount": "500",
            "provider_corp_external_id": "AIRLINE-QF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "in_progress",
            "total_quote_amount": "500",
            "total_quote_discount": "0",
            "created_at": "2026-06-23 17:03:14.380709",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "71820220336656367744",
            "request_uuid": "87250279722284761216",
            "updated_at": "2026-06-23 17:03:28.350347",
            "updated_by": "MCP"
          }
        ],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "batch_no": "QF1351-20260709",
          "created_at": "2026-06-23 17:03:21.019336",
          "final_subtotal": "500",
          "hold_expires_at": "2026-06-23 17:18:21.681078",
          "hold_token": "2768c361e5c8d7cd4e2eaeeb45e03bd9",
          "item_uuid": "52065619693805781120",
          "partition_key": "gpt#nestaging",
          "pax_breakdown": {
            "adult": "2"
          },
          "price_per_uom": "250",
          "provider_item_uuid": "94764066649319424128",
          "qty": "2",
          "quote_item_uuid": "06863801760542113920",
          "quote_uuid": "71820220336656367744",
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
              "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
              "label": "Economy Fare Cancellation",
              "content_hash": "5a29e5fb9ddcfc65",
              "policy_uuid": "45519135682445983872",
              "snapshotted_at": "2026-06-23 17:03:22.199785"
            }
          },
          "request_uuid": "87250279722284761216",
          "subtotal": "500",
          "subtotal_discount": "0",
          "subtotal_native": "500",
          "updated_at": "2026-06-23 17:03:21.019336",
          "updated_by": "MCP"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "priority": "8",
          "status": "active",
          "conditions": [
            "min_passengers >= 5",
            "booking_lead_days >= 7",
            "loyalty_tier in ['gold', 'platinum']"
          ],
          "created_at": "2026-06-21 23:50:31.742755",
          "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
          "discount_prompt_uuid": "83655032155864580224",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "2.5",
              "less_than": "2500"
            },
            {
              "greater_than": "2500",
              "max_discount_percentage": "7.5",
              "less_than": "7500"
            },
            {
              "greater_than": "7500",
              "max_discount_percentage": "12.5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "17.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-21 23:50:31.742755",
          "updated_by": "prepare_discount_prompts"
        },
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
          "priority": "10",
          "status": "active",
          "conditions": [
            "loyalty_tier in ['gold', 'platinum']"
          ],
          "created_at": "2026-06-21 23:50:31.444070",
          "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
          "discount_prompt_uuid": "74016050403706159232",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "2500"
            },
            {
              "greater_than": "2500",
              "max_discount_percentage": "10",
              "less_than": "12500"
            },
            {
              "greater_than": "12500",
              "max_discount_percentage": "12.5",
              "less_than": "13500"
            },
            {
              "greater_than": "13500",
              "max_discount_percentage": "15"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-21 23:50:31.444070",
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
          "priority": "2",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']"
          ],
          "created_at": "2026-06-22 03:43:11.520488",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-2515-LR)",
          "discount_prompt_uuid": "66044072765552607360",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5",
              "less_than": "12500"
            },
            {
              "greater_than": "12500",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-22 03:43:11.520488",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "5",
          "status": "active",
          "conditions": [
            "season != 'peak'",
            "loyalty_tier in ['gold', 'platinum']",
            "min_passengers >= 5"
          ],
          "created_at": "2026-06-22 03:43:11.227867",
          "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1679-XS)",
          "discount_prompt_uuid": "04111458880109691008",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "1000"
            },
       
... (truncated)
```

### 17. quotes / update_quote

- Method: `update_quote`
- Status: `pass`
- Elapsed: `5913.56 ms`

Arguments:

```json
{
  "request_uuid": "87250279722284761216",
  "quote_uuid": "71820220336656367744",
  "notes": "Updated via integration test",
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0
}
```

Output:

```json
{
  "request_uuid": "87250279722284761216",
  "quote_uuid": "71820220336656367744",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-QF",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0,
  "total_quote_amount": 500.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 525.0,
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
    "request_uuid": "87250279722284761216",
    "email": "jessicacooper@example.com",
    "request_title": "Integration test: Flight CDG->SFO First (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight CDG->SFO First",
        "item_uuid": "52065619693805781120",
        "provider_items": [
          {
            "provider_item_uuid": "94764066649319424128",
            "provider_corp_external_id": "AIRLINE-QF",
            "batch_no": "QF1351-20260709",
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
    "created_at": "2026-06-23T17:02:18.464944",
    "updated_by": "MCP",
    "updated_at": "2026-06-23T17:03:09.262831",
    "quotes": [
      {
        "final_total_quote_amount": "525",
        "provider_corp_external_id": "AIRLINE-QF",
        "rounds": "0",
        "shipping_amount": "25",
        "status": "in_progress",
        "total_quote_amount": "500",
        "total_quote_discount": "0",
        "created_at": "2026-06-23 17:03:14.380709",
        "notes": "Updated via integration test",
        "partition_key": "gpt#nestaging",
        "quote_uuid": "71820220336656367744",
        "request_uuid": "87250279722284761216",
        "shipping_method": "ticket_delivery",
        "updated_at": "2026-06-23 17:03:42.727815",
        "updated_by": "MCP"
      }
    ],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "batch_no": "QF1351-20260709",
      "created_at": "2026-06-23 17:03:21.019336",
      "final_subtotal": "500",
      "hold_expires_at": "2026-06-23 17:18:21.681078",
      "hold_token": "2768c361e5c8d7cd4e2eaeeb45e03bd9",
      "item_uuid": "52065619693805781120",
      "partition_key": "gpt#nestaging",
      "pax_breakdown": {
        "adult": "2"
      },
      "price_per_uom": "250",
      "provider_item_uuid": "94764066649319424128",
      "qty": "2",
      "quote_item_uuid": "06863801760542113920",
      "quote_uuid": "71820220336656367744",
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
          "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
          "label": "Economy Fare Cancellation",
          "content_hash": "5a29e5fb9ddcfc65",
          "policy_uuid": "45519135682445983872",
          "snapshotted_at": "2026-06-23 17:03:22.199785"
        }
      },
      "request_uuid": "87250279722284761216",
      "subtotal": "500",
      "subtotal_discount": "0",
      "subtotal_native": "500",
      "updated_at": "2026-06-23 17:03:21.019336",
      "updated_by": "MCP"
    }
  ],
  "installments": [],
  "discount_prompts": [
    {
      "priority": "8",
      "status": "active",
      "conditions": [
        "min_passengers >= 5",
        "booking_lead_days >= 7",
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "created_at": "2026-06-21 23:50:31.742755",
      "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
      "discount_prompt_uuid": "83655032155864580224",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "7.5",
          "less_than": "7500"
        },
        {
          "greater_than": "7500",
          "max_discount_percentage": "12.5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "17.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-21 23:50:31.742755",
      "updated_by": "prepare_discount_prompts"
    },
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
      "priority": "10",
      "status": "active",
      "conditions": [
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "created_at": "2026-06-21 23:50:31.444070",
      "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
      "discount_prompt_uuid": "74016050403706159232",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "10",
          "less_than": "12500"
        },
        {
          "greater_than": "12500",
          "max_discount_percentage": "12.5",
          "less_than": "13500"
        },
        {
          "greater_than": "13500",
          "max_discount_percentage": "15"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-21 23:50:31.444070",
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
      "priority": "2",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']"
      ],
      "created_at": "2026-06-22 03:43:11.520488",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-2515-LR)",
      "discount_prompt_uuid": "66044072765552607360",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5",
          "less_than": "12500"
        },
        {
          "greater_than": "12500",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-22 03:43:11.520488",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "5",
      "status": "active",
      "conditions": [
        "season != 'peak'",
        "loyalty_tier in ['gold', 'platinum']",
        "min_passengers >= 5"
      ],
      "created_at": "2026-06-22 03:43:11.227867",
      "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1679-XS)",
      "discount_prompt_uuid": "04111458880109691008",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "10",
          "less_than": "2000"
        },
        {
          "greater_than": "2000",
          "max_discount_percentage": "15",
          "less_than": "4500"
        },
        {
          "greater_than": "4500",
          "max_discount_percentage": "20"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-22 03:43:11.227867",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "7",
      "status": "active",
      "conditions": [
        "channel == 'direct'",
        "loyalty_tier in ['gold', 'platinum']",
        "booking_lead_days >= 7"
      ],
      "created_at": "2026-06-22 03:43:11.378039",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-2051-BI)",
      "discount_prompt_uuid": "53711723630325416064",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "7.5",
          "less_than": "6000"
     
... (truncated)
```

### 18. quotes / update_quote_item

- Method: `update_quote_item`
- Status: `pass`
- Elapsed: `6212.93 ms`

Arguments:

```json
{
  "quote_uuid": "71820220336656367744",
  "quote_item_uuid": "06863801760542113920",
  "request_uuid": "87250279722284761216",
  "discount_amount": 50.0,
  "notes": "Integration test discount"
}
```

Output:

```json
{
  "quote_uuid": "71820220336656367744",
  "quote_item_uuid": "06863801760542113920",
  "provider_item_uuid": "94764066649319424128",
  "item_uuid": "52065619693805781120",
  "partition_key": "gpt#nestaging",
  "batch_no": "QF1351-20260709",
  "request_uuid": "87250279722284761216",
  "qty": 2.0,
  "pax_breakdown": {
    "adult": "2"
  },
  "bundle_uuid": null,
  "bundle_label": null,
  "bundle_component_uuid": null,
  "price_per_uom": 250.0,
  "subtotal": 500.0,
  "subtotal_discount": 50.0,
  "final_subtotal": 450.0,
  "currency": null,
  "subtotal_native": 500.0,
  "notes": "Integration test discount",
  "hold_token": "2768c361e5c8d7cd4e2eaeeb45e03bd9",
  "hold_expires_at": "2026-06-23T17:18:21.681078",
  "guardrail_price_per_uom": 165.81,
  "slow_move_item": false,
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
      "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
      "label": "Economy Fare Cancellation",
      "content_hash": "5a29e5fb9ddcfc65",
      "policy_uuid": "45519135682445983872",
      "snapshotted_at": "2026-06-23 17:03:22.199785"
    }
  },
  "quote": {
    "request_uuid": "87250279722284761216",
    "quote_uuid": "71820220336656367744",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-QF",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 500.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 475.0,
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
      "request_uuid": "87250279722284761216",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight CDG->SFO First (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight CDG->SFO First",
          "item_uuid": "52065619693805781120",
          "provider_items": [
            {
              "provider_item_uuid": "94764066649319424128",
              "provider_corp_external_id": "AIRLINE-QF",
              "batch_no": "QF1351-20260709",
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
      "created_at": "2026-06-23T17:02:18.464944",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T17:03:09.262831",
      "quotes": [
        {
          "final_total_quote_amount": "475",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "in_progress",
          "total_quote_amount": "500",
          "total_quote_discount": "50",
          "created_at": "2026-06-23 17:03:14.380709",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "71820220336656367744",
          "request_uuid": "87250279722284761216",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-23 17:03:48.690103",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "QF1351-20260709",
        "created_at": "2026-06-23 17:03:21.019336",
        "final_subtotal": "450",
        "hold_expires_at": "2026-06-23 17:18:21.681078",
        "hold_token": "2768c361e5c8d7cd4e2eaeeb45e03bd9",
        "item_uuid": "52065619693805781120",
        "notes": "Integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "250",
        "provider_item_uuid": "94764066649319424128",
        "qty": "2",
        "quote_item_uuid": "06863801760542113920",
        "quote_uuid": "71820220336656367744",
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
            "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
            "label": "Economy Fare Cancellation",
            "content_hash": "5a29e5fb9ddcfc65",
            "policy_uuid": "45519135682445983872",
            "snapshotted_at": "2026-06-23 17:03:22.199785"
          }
        },
        "request_uuid": "87250279722284761216",
        "subtotal": "500",
        "subtotal_discount": "50",
        "subtotal_native": "500",
        "updated_at": "2026-06-23 17:03:48.487952",
        "updated_by": "MCP"
      }
    ],
    "installments": [],
    "discount_prompts": [
      {
        "priority": "8",
        "status": "active",
        "conditions": [
          "min_passengers >= 5",
          "booking_lead_days >= 7",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-21 23:50:31.742755",
        "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
        "discount_prompt_uuid": "83655032155864580224",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "7.5",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "17.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-21 23:50:31.742755",
        "updated_by": "prepare_discount_prompts"
      },
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
        "priority": "10",
        "status": "active",
        "conditions": [
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-21 23:50:31.444070",
        "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
        "discount_prompt_uuid": "74016050403706159232",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "12500"
          },
          {
            "greater_than": "12500",
            "max_discount_percentage": "12.5",
            "less_than": "13500"
          },
          {
            "greater_than": "13500",
            "max_discount_percentage": "15"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-21 23:50:31.444070",
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
        "priority": "2",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']"
        ],
        "created_at": "2026-06-22 03:43:11.520488",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-2515-LR)",
        "discount_prompt_uuid": "66044072765552607360",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
           
... (truncated)
```

### 19. pricing / get_item_price_tiers

- Method: `get_item_price_tiers`
- Status: `pass`
- Elapsed: `2317.36 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "quote_items": [
    {
      "item_uuid": "52065619693805781120",
      "provider_item_uuid": "94764066649319424128",
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
      "item_uuid": "52065619693805781120",
      "provider_item_uuid": "94764066649319424128",
      "item_price_tier_uuid": "81627773388666716288",
      "quantity_greater_then": 0.0,
      "quantity_less_then": null,
      "price_per_uom": 187.5,
      "margin_per_uom": null,
      "provider_item_batches": [],
      "status": "active"
    },
    {
      "item_uuid": "52065619693805781120",
      "provider_item_uuid": "94764066649319424128",
      "item_price_tier_uuid": "75772622582503719040",
      "quantity_greater_then": 0.0,
      "quantity_less_then": null,
      "price_per_uom": 250.0,
      "margin_per_uom": null,
      "provider_item_batches": [],
      "status": "active"
    },
    {
      "item_uuid": "52065619693805781120",
      "provider_item_uuid": "94764066649319424128",
      "item_price_tier_uuid": "07383076159448170624",
      "quantity_greater_then": 0.0,
      "quantity_less_then": null,
      "price_per_uom": 25.0,
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
- Elapsed: `2481.54 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "quote_items": [
    {
      "item_uuid": "52065619693805781120",
      "provider_item_uuid": "94764066649319424128"
    }
  ]
}
```

Output:

```json
{
  "discount_prompts": [
    {
      "discount_prompt_uuid": "83655032155864580224",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
      "conditions": [
        "min_passengers >= 5",
        "booking_lead_days >= 7",
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "7.5",
          "less_than": "7500"
        },
        {
          "greater_than": "7500",
          "max_discount_percentage": "12.5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "17.5"
        }
      ],
      "priority": 8,
      "status": "active"
    },
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
      "discount_prompt_uuid": "74016050403706159232",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
      "conditions": [
        "loyalty_tier in ['gold', 'platinum']"
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
          "less_than": "12500"
        },
        {
          "greater_than": "12500",
          "max_discount_percentage": "12.5",
          "less_than": "13500"
        },
        {
          "greater_than": "13500",
          "max_discount_percentage": "15"
        }
      ],
      "priority": 10,
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
      "discount_prompt_uuid": "66044072765552607360",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-2515-LR)",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']"
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
          "less_than": "12500"
        },
        {
          "greater_than": "12500",
          "max_discount_percentage": "10"
        }
      ],
      "priority": 2,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "04111458880109691008",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1679-XS)",
      "conditions": [
        "season != 'peak'",
        "loyalty_tier in ['gold', 'platinum']",
        "min_passengers >= 5"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "10",
          "less_than": "2000"
        },
        {
          "greater_than": "2000",
          "max_discount_percentage": "15",
          "less_than": "4500"
        },
        {
          "greater_than": "4500",
          "max_discount_percentage": "20"
        }
      ],
      "priority": 5,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "53711723630325416064",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-2051-BI)",
      "conditions": [
        "channel == 'direct'",
        "loyalty_tier in ['gold', 'platinum']",
        "booking_lead_days >= 7"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "7.5",
          "less_than": "6000"
        },
        {
          "greater_than": "6000",
          "max_discount_percentage": "10"
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
      "discount_prompt_uuid": "92704822808028397696",
      "scope": "item",
      "tags": [
        "52065619693805781120"
      ],
      "discount_prompt": "Promotional pricing on 'Flight ATL->ORD Economy': discount scales with booked seat count on this specific route + cabin.",
      "conditions": [
        "season != 'peak'",
        "channel == 'direct'"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "5",
          "less_than": "3500"
        },
        {
          "greater_than": "3500",
          "max_discount_percentage": "7.5"
        }
      ],
      "priority": 1,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "43579183285732917376",
      "scope": "provider_item",
      "tags": [
        "94764066649319424128"
      ],
      "discount_prompt": "Strategic-partner pricing for 'Qantas' on this route: preferred-rate tiers when minimums are met.",
      "conditions": [
        "is_refundable == false",
        "booking_lead_days >= 14"
      ],
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "7.5",
          "less_than": "5000"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "10",
          "less_than": "15000"
        },
        {
          "greater_than": "15000",
          "max_discount_percentage": "12.5"
        }
      ],
      "priority": 6,
      "status": "active"
    }
  ]
}
```

### 21. pricing / calculate_quote_pricing

- Method: `calculate_quote_pricing`
- Status: `pass`
- Elapsed: `9437.17 ms`

Arguments:

```json
{
  "request_uuid": "03075416831792529536",
  "email": "jessicacooper@example.com"
}
```

Output:

```json
{
  "request_uuid": "03075416831792529536",
  "groups": [
    {
      "provider_corp_external_id": "AIRLINE-AF",
      "subtotal": 90.0,
      "items": [
        {
          "item_uuid": "06041993713794695296",
          "item_name": "Flight ATL->ORD Premium Economy",
          "provider_item_uuid": "39876487618607726720",
          "provider_corp_external_id": "AIRLINE-AF",
          "batch_no": "AF5319-20260907",
          "qty": 2.0,
          "base_price_per_uom": 450.0,
          "price_per_uom": 45.0,
          "guardrail_price_per_uom": 450.0,
          "slow_move_item": false,
          "expired_at": null,
          "price_tiers": [
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
          ],
          "subtotal": 90.0
        }
      ]
    }
  ]
}
```

### 22. installments / confirm_quote_and_create_installments

- Method: `confirm_quote_and_create_installments`
- Status: `pass`
- Elapsed: `22783.89 ms`

Arguments:

```json
{
  "request_uuid": "87250279722284761216",
  "quote_uuid": "71820220336656367744",
  "create_single_installment": true,
  "payment_method": "bank_transfer"
}
```

Output:

```json
{
  "quote": {
    "request_uuid": "87250279722284761216",
    "quote_uuid": "71820220336656367744",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-QF",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 500.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 475.0,
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
      "request_uuid": "87250279722284761216",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight CDG->SFO First (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight CDG->SFO First",
          "item_uuid": "52065619693805781120",
          "provider_items": [
            {
              "provider_item_uuid": "94764066649319424128",
              "provider_corp_external_id": "AIRLINE-QF",
              "batch_no": "QF1351-20260709",
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
      "created_at": "2026-06-23T17:02:18.464944",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T17:03:09.262831",
      "quotes": [
        {
          "final_total_quote_amount": "475",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "500",
          "total_quote_discount": "50",
          "created_at": "2026-06-23 17:03:14.380709",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "71820220336656367744",
          "request_uuid": "87250279722284761216",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-23 17:04:11.812855",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "QF1351-20260709",
        "created_at": "2026-06-23 17:03:21.019336",
        "final_subtotal": "450",
        "hold_expires_at": "2026-06-23 17:18:21.681078",
        "hold_token": "2768c361e5c8d7cd4e2eaeeb45e03bd9",
        "item_uuid": "52065619693805781120",
        "notes": "Integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "250",
        "provider_item_uuid": "94764066649319424128",
        "qty": "2",
        "quote_item_uuid": "06863801760542113920",
        "quote_uuid": "71820220336656367744",
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
            "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
            "label": "Economy Fare Cancellation",
            "content_hash": "5a29e5fb9ddcfc65",
            "policy_uuid": "45519135682445983872",
            "snapshotted_at": "2026-06-23 17:03:22.199785"
          }
        },
        "request_uuid": "87250279722284761216",
        "subtotal": "500",
        "subtotal_discount": "50",
        "subtotal_native": "500",
        "updated_at": "2026-06-23 17:03:48.487952",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "475",
        "installment_ratio": "100",
        "priority": "0",
        "status": "pending",
        "created_at": "2026-06-23 17:04:22.889696",
        "installment_uuid": "55010851521452589184",
        "partition_key": "gpt#nestaging",
        "payment_method": "bank_transfer",
        "quote_uuid": "71820220336656367744",
        "request_uuid": "87250279722284761216",
        "scheduled_date": "2026-06-23 17:04:20",
        "updated_at": "2026-06-23 17:04:22.889696",
        "updated_by": "MCP"
      }
    ],
    "discount_prompts": [
      {
        "priority": "8",
        "status": "active",
        "conditions": [
          "min_passengers >= 5",
          "booking_lead_days >= 7",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-21 23:50:31.742755",
        "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
        "discount_prompt_uuid": "83655032155864580224",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "7.5",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "17.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-21 23:50:31.742755",
        "updated_by": "prepare_discount_prompts"
      },
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
        "priority": "10",
        "status": "active",
        "conditions": [
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-21 23:50:31.444070",
        "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
        "discount_prompt_uuid": "74016050403706159232",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "12500"
          },
          {
            "greater_than": "12500",
            "max_discount_percentage": "12.5",
            "less_than": "13500"
          },
          {
            "greater_than": "13500",
            "max_discount_percentage": "15"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-21 23:50:31.444070",
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
        "priority": "2",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']"
        ],
        "created_at": "2026-06-22 03:43:11.520488",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-2515-LR)",
        "discount_prompt_uuid": "66044072765552607360",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5",
            "less_than": "12500"
          },
          {
            "greater_than": "12500",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-22 03:43:11.520488",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "5",
        "status": "active",
        "conditions": [
          "season != 'peak'",
          "loyalty_tier in ['gold', 'platinum']",
          "min_passengers >= 5"
        ],
        "created_at": "2026-06-22 03:43:11.227867",
        "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1679-XS)",
        "discount_prompt_uuid": "04111458880109691008",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "1000"
         
... (truncated)
```

### 23. installments / get_installments

- Method: `get_installments`
- Status: `pass`
- Elapsed: `2923.02 ms`

Arguments:

```json
{
  "quote_uuid": "71820220336656367744",
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
      "quote_uuid": "71820220336656367744",
      "installment_uuid": "55010851521452589184",
      "request_uuid": "87250279722284761216",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 475.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-23T17:04:20",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-23T17:04:22.889696",
      "updated_at": "2026-06-23T17:04:22.889696",
      "quote": {
        "request_uuid": "87250279722284761216",
        "quote_uuid": "71820220336656367744",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_id": "AIRLINE-QF",
        "sales_rep_email": null,
        "rounds": 0,
        "shipping_method": "ticket_delivery",
        "shipping_amount": 25.0,
        "total_quote_amount": 500.0,
        "total_quote_discount": 50.0,
        "final_total_quote_amount": 475.0,
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
          "request_uuid": "87250279722284761216",
          "email": "jessicacooper@example.com",
          "request_title": "Integration test: Flight CDG->SFO First (updated)",
          "request_description": "E2E test request via silvaengine_gateway",
          "billing_address": null,
          "shipping_address": null,
          "items": [
            {
              "item_name": "Flight CDG->SFO First",
              "item_uuid": "52065619693805781120",
              "provider_items": [
                {
                  "provider_item_uuid": "94764066649319424128",
                  "provider_corp_external_id": "AIRLINE-QF",
                  "batch_no": "QF1351-20260709",
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
          "created_at": "2026-06-23T17:02:18.464944",
          "updated_by": "MCP",
          "updated_at": "2026-06-23T17:03:09.262831",
          "quotes": [
            {
              "final_total_quote_amount": "475",
              "provider_corp_external_id": "AIRLINE-QF",
              "rounds": "0",
              "shipping_amount": "25",
              "status": "confirmed",
              "total_quote_amount": "500",
              "total_quote_discount": "50",
              "created_at": "2026-06-23 17:03:14.380709",
              "notes": "Updated via integration test",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "71820220336656367744",
              "request_uuid": "87250279722284761216",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-23 17:04:11.812855",
              "updated_by": "MCP"
            }
          ],
          "files": [],
          "bundle": null
        },
        "quote_items": [
          {
            "batch_no": "QF1351-20260709",
            "created_at": "2026-06-23 17:03:21.019336",
            "final_subtotal": "450",
            "hold_expires_at": "2026-06-23 17:18:21.681078",
            "hold_token": "2768c361e5c8d7cd4e2eaeeb45e03bd9",
            "item_uuid": "52065619693805781120",
            "notes": "Integration test discount",
            "partition_key": "gpt#nestaging",
            "pax_breakdown": {
              "adult": "2"
            },
            "price_per_uom": "250",
            "provider_item_uuid": "94764066649319424128",
            "qty": "2",
            "quote_item_uuid": "06863801760542113920",
            "quote_uuid": "71820220336656367744",
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
                "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
                "label": "Economy Fare Cancellation",
                "content_hash": "5a29e5fb9ddcfc65",
                "policy_uuid": "45519135682445983872",
                "snapshotted_at": "2026-06-23 17:03:22.199785"
              }
            },
            "request_uuid": "87250279722284761216",
            "subtotal": "500",
            "subtotal_discount": "50",
            "subtotal_native": "500",
            "updated_at": "2026-06-23 17:03:48.487952",
            "updated_by": "MCP"
          }
        ],
        "installments": [
          {
            "installment_amount": "475",
            "installment_ratio": "100",
            "priority": "0",
            "status": "pending",
            "created_at": "2026-06-23 17:04:22.889696",
            "installment_uuid": "55010851521452589184",
            "partition_key": "gpt#nestaging",
            "payment_method": "bank_transfer",
            "quote_uuid": "71820220336656367744",
            "request_uuid": "87250279722284761216",
            "scheduled_date": "2026-06-23 17:04:20",
            "updated_at": "2026-06-23 17:04:22.889696",
            "updated_by": "MCP"
          }
        ],
        "discount_prompts": [
          {
            "priority": "8",
            "status": "active",
            "conditions": [
              "min_passengers >= 5",
              "booking_lead_days >= 7",
              "loyalty_tier in ['gold', 'platinum']"
            ],
            "created_at": "2026-06-21 23:50:31.742755",
            "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
            "discount_prompt_uuid": "83655032155864580224",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "2.5",
                "less_than": "2500"
              },
              {
                "greater_than": "2500",
                "max_discount_percentage": "7.5",
                "less_than": "7500"
              },
              {
                "greater_than": "7500",
                "max_discount_percentage": "12.5",
                "less_than": "10000"
              },
              {
                "greater_than": "10000",
                "max_discount_percentage": "17.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-21 23:50:31.742755",
            "updated_by": "prepare_discount_prompts"
          },
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
            "priority": "10",
            "status": "active",
            "conditions": [
              "loyalty_tier in ['gold', 'platinum']"
            ],
            "created_at": "2026-06-21 23:50:31.444070",
            "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
            "discount_prompt_uuid": "74016050403706159232",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "7.5",
                "less_than": "2500"
              },
              {
                "greater_than": "2500",
                "max_discount_percentage": "10",
                "less_than": "12500"
              },
              {
                "greater_than": "12500",
                "max_discount_percentage": "12.5",
                "less_than": "13500"
              },
              {
                "greater_than": "13500",
                "max_discount_percentage": "15"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-21 23:50:31.444070",
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
            "partition_key": "gpt#nestaging
... (truncated)
```

### 24. installments / create_installment

- Method: `_create_installment`
- Status: `pass`
- Elapsed: `8195.59 ms`

Arguments:

```json
{
  "quote_uuid": "66077533253247451264",
  "request_uuid": "87250279722284761216",
  "installment_amount": 100.0,
  "payment_method": "credit_card"
}
```

Output:

```json
{
  "quote_uuid": "66077533253247451264",
  "installment_uuid": "70212906945681047680",
  "request_uuid": "87250279722284761216",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 100.0,
  "installment_ratio": 12.5,
  "salesorder_no": null,
  "scheduled_date": "2026-06-23T17:05:33",
  "payment_method": "credit_card",
  "status": "pending",
  "updated_by": "MCP",
  "created_at": "2026-06-23T17:05:35.355322",
  "updated_at": "2026-06-23T17:05:35.355322",
  "quote": {
    "request_uuid": "87250279722284761216",
    "quote_uuid": "66077533253247451264",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-QF",
    "sales_rep_email": null,
    "rounds": 1,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 300.0,
    "total_quote_amount": 500.0,
    "total_quote_discount": 0.0,
    "final_total_quote_amount": 800.0,
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
      "request_uuid": "87250279722284761216",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight CDG->SFO First (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight CDG->SFO First",
          "item_uuid": "52065619693805781120",
          "provider_items": [
            {
              "provider_item_uuid": "94764066649319424128",
              "provider_corp_external_id": "AIRLINE-QF",
              "batch_no": "QF1351-20260709",
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
      "created_at": "2026-06-23T17:02:18.464944",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T17:03:09.262831",
      "quotes": [
        {
          "final_total_quote_amount": "800",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "2",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "500",
          "total_quote_discount": "0",
          "created_at": "2026-06-23 17:05:03.570207",
          "notes": "Confirmed setup quote for create_installments",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "54851062456900403328",
          "request_uuid": "87250279722284761216",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-23 17:05:27.405911",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "800",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "1",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "500",
          "total_quote_discount": "0",
          "created_at": "2026-06-23 17:04:34.252252",
          "notes": "Confirmed setup quote for create_installment",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "66077533253247451264",
          "request_uuid": "87250279722284761216",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-23 17:04:58.240703",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "475",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "500",
          "total_quote_discount": "50",
          "created_at": "2026-06-23 17:03:14.380709",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "71820220336656367744",
          "request_uuid": "87250279722284761216",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-23 17:04:11.812855",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "QF1351-20260709",
        "created_at": "2026-06-23 17:04:39.797162",
        "final_subtotal": "500",
        "hold_expires_at": "2026-06-23 17:19:40.121583",
        "hold_token": "4a5df8cec78ced3366d39ea382af88ce",
        "item_uuid": "52065619693805781120",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "250",
        "provider_item_uuid": "94764066649319424128",
        "qty": "2",
        "quote_item_uuid": "43373305936062988416",
        "quote_uuid": "66077533253247451264",
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
            "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
            "label": "Economy Fare Cancellation",
            "content_hash": "5a29e5fb9ddcfc65",
            "policy_uuid": "45519135682445983872",
            "snapshotted_at": "2026-06-23 17:04:40.371234"
          }
        },
        "request_uuid": "87250279722284761216",
        "subtotal": "500",
        "subtotal_discount": "0",
        "subtotal_native": "500",
        "updated_at": "2026-06-23 17:04:39.797162",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "100",
        "installment_ratio": "12.5",
        "priority": "0",
        "status": "pending",
        "created_at": "2026-06-23 17:05:35.355322",
        "installment_uuid": "70212906945681047680",
        "partition_key": "gpt#nestaging",
        "payment_method": "credit_card",
        "quote_uuid": "66077533253247451264",
        "request_uuid": "87250279722284761216",
        "scheduled_date": "2026-06-23 17:05:33",
        "updated_at": "2026-06-23 17:05:35.355322",
        "updated_by": "MCP"
      }
    ],
    "discount_prompts": [
      {
        "priority": "8",
        "status": "active",
        "conditions": [
          "min_passengers >= 5",
          "booking_lead_days >= 7",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-21 23:50:31.742755",
        "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
        "discount_prompt_uuid": "83655032155864580224",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "7.5",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "17.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-21 23:50:31.742755",
        "updated_by": "prepare_discount_prompts"
      },
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
        "priority": "10",
        "status": "active",
        "conditions": [
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-21 23:50:31.444070",
        "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
        "discount_prompt_uuid": "74016050403706159232",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "12500"
          },
          {
            "greater_than": "12500",
            "max_discount_percentage": "12.5",
            "less_than": "13500"
          },
          {
            "greater_than": "13500",
            "max_discount_percentage": "15"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-21 23:50:31.444070",
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
      
... (truncated)
```

### 25. installments / create_installments

- Method: `_create_installments`
- Status: `pass`
- Elapsed: `14825.59 ms`

Arguments:

```json
{
  "quote_uuid": "54851062456900403328",
  "request_uuid": "87250279722284761216",
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
      "quote_uuid": "54851062456900403328",
      "installment_uuid": "75733957140947157120",
      "request_uuid": "87250279722284761216",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 266.6666666666667,
      "installment_ratio": 33.333333333333336,
      "salesorder_no": null,
      "scheduled_date": "2026-08-15T17:05:41",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-23T17:05:43.909112",
      "updated_at": "2026-06-23T17:05:43.909112",
      "quote": {
        "request_uuid": "87250279722284761216",
        "quote_uuid": "54851062456900403328",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_id": "AIRLINE-QF",
        "sales_rep_email": null,
        "rounds": 2,
        "shipping_method": "ticket_delivery",
        "shipping_amount": 300.0,
        "total_quote_amount": 500.0,
        "total_quote_discount": 0.0,
        "final_total_quote_amount": 800.0,
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
          "request_uuid": "87250279722284761216",
          "email": "jessicacooper@example.com",
          "request_title": "Integration test: Flight CDG->SFO First (updated)",
          "request_description": "E2E test request via silvaengine_gateway",
          "billing_address": null,
          "shipping_address": null,
          "items": [
            {
              "item_name": "Flight CDG->SFO First",
              "item_uuid": "52065619693805781120",
              "provider_items": [
                {
                  "provider_item_uuid": "94764066649319424128",
                  "provider_corp_external_id": "AIRLINE-QF",
                  "batch_no": "QF1351-20260709",
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
          "created_at": "2026-06-23T17:02:18.464944",
          "updated_by": "MCP",
          "updated_at": "2026-06-23T17:03:09.262831",
          "quotes": [
            {
              "final_total_quote_amount": "800",
              "provider_corp_external_id": "AIRLINE-QF",
              "rounds": "2",
              "shipping_amount": "300",
              "status": "confirmed",
              "total_quote_amount": "500",
              "total_quote_discount": "0",
              "created_at": "2026-06-23 17:05:03.570207",
              "notes": "Confirmed setup quote for create_installments",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "54851062456900403328",
              "request_uuid": "87250279722284761216",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-23 17:05:27.405911",
              "updated_by": "MCP"
            },
            {
              "final_total_quote_amount": "800",
              "provider_corp_external_id": "AIRLINE-QF",
              "rounds": "1",
              "shipping_amount": "300",
              "status": "confirmed",
              "total_quote_amount": "500",
              "total_quote_discount": "0",
              "created_at": "2026-06-23 17:04:34.252252",
              "notes": "Confirmed setup quote for create_installment",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "66077533253247451264",
              "request_uuid": "87250279722284761216",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-23 17:04:58.240703",
              "updated_by": "MCP"
            },
            {
              "final_total_quote_amount": "475",
              "provider_corp_external_id": "AIRLINE-QF",
              "rounds": "0",
              "shipping_amount": "25",
              "status": "confirmed",
              "total_quote_amount": "500",
              "total_quote_discount": "50",
              "created_at": "2026-06-23 17:03:14.380709",
              "notes": "Updated via integration test",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "71820220336656367744",
              "request_uuid": "87250279722284761216",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-23 17:04:11.812855",
              "updated_by": "MCP"
            }
          ],
          "files": [],
          "bundle": null
        },
        "quote_items": [
          {
            "batch_no": "QF1351-20260709",
            "created_at": "2026-06-23 17:05:09.040357",
            "final_subtotal": "500",
            "hold_expires_at": "2026-06-23 17:20:09.396351",
            "hold_token": "ca8152cfd8e1d6f1cd4a748a865b4ae9",
            "item_uuid": "52065619693805781120",
            "partition_key": "gpt#nestaging",
            "pax_breakdown": {
              "adult": "2"
            },
            "price_per_uom": "250",
            "provider_item_uuid": "94764066649319424128",
            "qty": "2",
            "quote_item_uuid": "28887600785029873792",
            "quote_uuid": "54851062456900403328",
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
                "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
                "label": "Economy Fare Cancellation",
                "content_hash": "5a29e5fb9ddcfc65",
                "policy_uuid": "45519135682445983872",
                "snapshotted_at": "2026-06-23 17:05:09.651017"
              }
            },
            "request_uuid": "87250279722284761216",
            "subtotal": "500",
            "subtotal_discount": "0",
            "subtotal_native": "500",
            "updated_at": "2026-06-23 17:05:09.040357",
            "updated_by": "MCP"
          }
        ],
        "installments": [
          {
            "installment_amount": "266.6666666666667",
            "installment_ratio": "33.333333333333336",
            "priority": "0",
            "status": "pending",
            "created_at": "2026-06-23 17:05:43.909112",
            "installment_uuid": "75733957140947157120",
            "partition_key": "gpt#nestaging",
            "payment_method": "bank_transfer",
            "quote_uuid": "54851062456900403328",
            "request_uuid": "87250279722284761216",
            "scheduled_date": "2026-08-15 17:05:41",
            "updated_at": "2026-06-23 17:05:43.909112",
            "updated_by": "MCP"
          }
        ],
        "discount_prompts": [
          {
            "priority": "8",
            "status": "active",
            "conditions": [
              "min_passengers >= 5",
              "booking_lead_days >= 7",
              "loyalty_tier in ['gold', 'platinum']"
            ],
            "created_at": "2026-06-21 23:50:31.742755",
            "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
            "discount_prompt_uuid": "83655032155864580224",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "2.5",
                "less_than": "2500"
              },
              {
                "greater_than": "2500",
                "max_discount_percentage": "7.5",
                "less_than": "7500"
              },
              {
                "greater_than": "7500",
                "max_discount_percentage": "12.5",
                "less_than": "10000"
              },
              {
                "greater_than": "10000",
                "max_discount_percentage": "17.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-21 23:50:31.742755",
            "updated_by": "prepare_discount_prompts"
          },
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
            "priority": "10",
            "status": "active",
            "conditions": [
              "loyalty_tier in ['gold', 'platinum']"
            ],
            "created_at": "2026-06-21 23:50:31.444070",
            "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
            "discount_prompt_uuid": "74016050403706159232",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "7.5",
                "less_than": "2500"
              },
              {
                "greater_than": "2500",
                "max_discount_percentage": "10",
                "less_than": "12500"
              },
              {
                "greater_th
... (truncated)
```

### 26. installments / update_installment (uuid=550108515214...)

- Method: `update_installment`
- Status: `pass`
- Elapsed: `22634.1 ms`

Arguments:

```json
{
  "quote_uuid": "71820220336656367744",
  "installment_uuid": "55010851521452589184",
  "status": "paid"
}
```

Output:

```json
{
  "quote_uuid": "71820220336656367744",
  "installment_uuid": "55010851521452589184",
  "request_uuid": "87250279722284761216",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 475.0,
  "installment_ratio": 100.0,
  "salesorder_no": null,
  "scheduled_date": "2026-06-23T17:04:20",
  "payment_method": "bank_transfer",
  "status": "paid",
  "updated_by": "MCP",
  "created_at": "2026-06-23T17:04:22.889696",
  "updated_at": "2026-06-23T17:05:56.207119",
  "quote": {
    "request_uuid": "87250279722284761216",
    "quote_uuid": "71820220336656367744",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-QF",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 500.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 475.0,
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
      "request_uuid": "87250279722284761216",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight CDG->SFO First (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight CDG->SFO First",
          "item_uuid": "52065619693805781120",
          "provider_items": [
            {
              "provider_item_uuid": "94764066649319424128",
              "provider_corp_external_id": "AIRLINE-QF",
              "batch_no": "QF1351-20260709",
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
      "created_at": "2026-06-23T17:02:18.464944",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T17:03:09.262831",
      "quotes": [
        {
          "final_total_quote_amount": "800",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "2",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "500",
          "total_quote_discount": "0",
          "created_at": "2026-06-23 17:05:03.570207",
          "notes": "Confirmed setup quote for create_installments",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "54851062456900403328",
          "request_uuid": "87250279722284761216",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-23 17:05:27.405911",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "800",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "1",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "500",
          "total_quote_discount": "0",
          "created_at": "2026-06-23 17:04:34.252252",
          "notes": "Confirmed setup quote for create_installment",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "66077533253247451264",
          "request_uuid": "87250279722284761216",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-23 17:04:58.240703",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "475",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "500",
          "total_quote_discount": "50",
          "created_at": "2026-06-23 17:03:14.380709",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "71820220336656367744",
          "request_uuid": "87250279722284761216",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-23 17:04:11.812855",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "QF1351-20260709",
        "created_at": "2026-06-23 17:03:21.019336",
        "final_subtotal": "450",
        "hold_expires_at": "2026-06-23 17:18:21.681078",
        "hold_token": "2768c361e5c8d7cd4e2eaeeb45e03bd9",
        "item_uuid": "52065619693805781120",
        "notes": "Integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "250",
        "provider_item_uuid": "94764066649319424128",
        "qty": "2",
        "quote_item_uuid": "06863801760542113920",
        "quote_uuid": "71820220336656367744",
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
            "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
            "label": "Economy Fare Cancellation",
            "content_hash": "5a29e5fb9ddcfc65",
            "policy_uuid": "45519135682445983872",
            "snapshotted_at": "2026-06-23 17:03:22.199785"
          }
        },
        "request_uuid": "87250279722284761216",
        "subtotal": "500",
        "subtotal_discount": "50",
        "subtotal_native": "500",
        "updated_at": "2026-06-23 17:03:48.487952",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "475",
        "installment_ratio": "100",
        "priority": "0",
        "status": "paid",
        "created_at": "2026-06-23 17:04:22.889696",
        "installment_uuid": "55010851521452589184",
        "partition_key": "gpt#nestaging",
        "payment_method": "bank_transfer",
        "quote_uuid": "71820220336656367744",
        "request_uuid": "87250279722284761216",
        "scheduled_date": "2026-06-23 17:04:20",
        "updated_at": "2026-06-23 17:05:56.207119",
        "updated_by": "MCP"
      }
    ],
    "discount_prompts": [
      {
        "priority": "8",
        "status": "active",
        "conditions": [
          "min_passengers >= 5",
          "booking_lead_days >= 7",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-21 23:50:31.742755",
        "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-6517-OM)",
        "discount_prompt_uuid": "83655032155864580224",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "7.5",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "17.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-21 23:50:31.742755",
        "updated_by": "prepare_discount_prompts"
      },
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
        "priority": "10",
        "status": "active",
        "conditions": [
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-21 23:50:31.444070",
        "discount_prompt": "Recurring-customer loyalty incentive: discounts scale with cumulative annual spend across all bookings. (ref: PROMO-5612-FO)",
        "discount_prompt_uuid": "74016050403706159232",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "12500"
          },
          {
            "greater_than": "12500",
            "max_discount_percentage": "12.5",
            "less_than": "13500"
          },
          {
            "greater_than": "13500",
            "max_discount_percentage": "15"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-21 23:50:31.444070",
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
        "partition_
... (truncated)
```

### 27. files / upload_rfq_file

- Method: `upload_rfq_file`
- Status: `pass`
- Elapsed: `2583.83 ms`

Arguments:

```json
{
  "request_uuid": "03075416831792529536",
  "file_name": "integration_test_spec.pdf",
  "email": "jessicacooper@example.com"
}
```

Output:

```json
{
  "file": {
    "request_uuid": "03075416831792529536",
    "file_name": "integration_test_spec.pdf",
    "email": "jessicacooper@example.com",
    "partition_key": "gpt#nestaging",
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "03075416831792529536",
      "email": "jessicacooper@example.com",
      "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
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
              "batch_no": "AF5319-20260907",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_http_integration.py",
      "bundle_uuid": null,
      "status": "completed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-18T20:52:05.947710",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T16:59:24.824102",
      "quotes": [
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "completed",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-18 20:54:02.795771",
          "notes": "Auto-completed: All installments paid",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "60187438571235328128",
          "request_uuid": "03075416831792529536",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-23 16:59:16.329730",
          "updated_by": "MCP"
        }
      ],
      "files": [
        {
          "created_at": "2026-06-23 16:54:37.215458",
          "email": "jessicacooper@example.com",
          "file_name": "integration_test_spec.pdf",
          "partition_key": "gpt#nestaging",
          "request_uuid": "03075416831792529536",
          "updated_at": "2026-06-23 17:06:15.963847",
          "updated_by": "MCP"
        }
      ],
      "bundle": null
    },
    "updated_by": "MCP",
    "created_at": "2026-06-23T16:54:37.215458",
    "updated_at": "2026-06-23T17:06:15.963847"
  }
}
```

### 28. files / get_rfq_files

- Method: `get_rfq_files`
- Status: `pass`
- Elapsed: `2474.45 ms`

Arguments:

```json
{
  "request_uuid": "03075416831792529536",
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
      "request_uuid": "03075416831792529536",
      "file_name": "integration_test_spec.pdf",
      "email": "jessicacooper@example.com",
      "partition_key": "gpt#nestaging",
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "03075416831792529536",
        "email": "jessicacooper@example.com",
        "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
        "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
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
                "batch_no": "AF5319-20260907",
                "qty": "2"
              }
            ],
            "qty": "2",
            "pax_breakdown": {
              "adult": "2"
            }
          }
        ],
        "notes": "Updated via run_http_integration.py",
        "bundle_uuid": null,
        "status": "completed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-18T20:52:05.947710",
        "updated_by": "MCP",
        "updated_at": "2026-06-23T16:59:24.824102",
        "quotes": [
          {
            "final_total_quote_amount": "875",
            "provider_corp_external_id": "AIRLINE-AF",
            "rounds": "0",
            "shipping_amount": "25",
            "status": "completed",
            "total_quote_amount": "900",
            "total_quote_discount": "50",
            "created_at": "2026-06-18 20:54:02.795771",
            "notes": "Auto-completed: All installments paid",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "60187438571235328128",
            "request_uuid": "03075416831792529536",
            "shipping_method": "ticket_delivery",
            "updated_at": "2026-06-23 16:59:16.329730",
            "updated_by": "MCP"
          }
        ],
        "files": [
          {
            "created_at": "2026-06-23 16:54:37.215458",
            "email": "jessicacooper@example.com",
            "file_name": "integration_test_spec.pdf",
            "partition_key": "gpt#nestaging",
            "request_uuid": "03075416831792529536",
            "updated_at": "2026-06-23 17:06:15.963847",
            "updated_by": "MCP"
          }
        ],
        "bundle": null
      },
      "updated_by": "MCP",
      "created_at": "2026-06-23T16:54:37.215458",
      "updated_at": "2026-06-23T17:06:15.963847"
    }
  ]
}
```

### 29. segments / get_segment_contacts

- Method: `get_segment_contacts`
- Status: `pass`
- Elapsed: `3369.15 ms`

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
  "total": 60,
  "segment_contact_list": [
    {
      "partition_key": "gpt#nestaging",
      "email": "amysmith@example.com",
      "contact_uuid": null,
      "consumer_corp_external_id": "CUST-7324",
      "segment_uuid": "79444987658299785344",
      "segment": null,
      "updated_by": "data_loader_script",
      "created_at": "2026-06-21T21:18:31.406954",
      "updated_at": "2026-06-21T21:45:29.147009"
    },
    {
      "partition_key": "gpt#nestaging",
      "email": "andersencatherine@example.com",
      "contact_uuid": null,
      "consumer_corp_external_id": "CUST-8772",
      "segment_uuid": "87871425215007309952",
      "segment": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "segment_uuid": "87871425215007309952",
        "provider_corp_external_id": "PROV-4594",
        "segment_name": "Taylor, Adams and Gibbs Tier",
        "segment_description": "Adaptive full-range intranet",
        "created_at": "2026-06-22T03:42:13.717177",
        "updated_by": "prepare_segments_and_contacts",
        "updated_at": "2026-06-22T03:42:13.717177",
        "contacts": [
          {
            "consumer_corp_external_id": "CUST-9978",
            "created_at": "2026-06-22 03:42:14.487845",
            "email": "harrisbrendan@example.com",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "87871425215007309952",
            "updated_at": "2026-06-22 03:42:14.487845",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-8772",
            "created_at": "2026-06-22 03:42:14.767938",
            "email": "andersencatherine@example.com",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "87871425215007309952",
            "updated_at": "2026-06-22 03:42:14.767938",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-1552",
            "created_at": "2026-06-22 03:42:14.349547",
            "email": "julie22@example.net",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "87871425215007309952",
            "updated_at": "2026-06-22 03:42:14.349547",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-1549",
            "created_at": "2026-06-22 03:42:14.626677",
            "email": "patricia90@example.org",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "87871425215007309952",
            "updated_at": "2026-06-22 03:42:14.626677",
            "updated_by": "prepare_segments_and_contacts"
          },
          {
            "consumer_corp_external_id": "CUST-5726",
            "created_at": "2026-06-22 03:42:14.202678",
            "email": "frazierdaniel@example.org",
            "partition_key": "gpt#nestaging",
            "segment_uuid": "87871425215007309952",
            "updated_at": "2026-06-22 03:42:14.202678",
            "updated_by": "prepare_segments_and_contacts"
          }
        ]
      },
      "updated_by": "prepare_segments_and_contacts",
      "created_at": "2026-06-22T03:42:14.767938",
      "updated_at": "2026-06-22T03:42:14.767938"
    },
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
      "emai
... (truncated)
```

### 30. availability / check_availability

- Method: `check_availability`
- Status: `pass`
- Elapsed: `2357.97 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "94764066649319424128",
  "service_start_at": "2026-07-09T21:45:00Z",
  "service_end_at": "2026-07-10T03:11:29.751482Z",
  "batch_no": "QF1351-20260709",
  "qty": 2
}
```

Output:

```json
{
  "operation": "check",
  "provider_item_uuid": "94764066649319424128",
  "batch_no": "QF1351-20260709",
  "service_start_at": "2026-07-09T21:45:00+00:00",
  "service_end_at": "2026-07-10T03:11:29.751482+00:00",
  "available": true,
  "hold_token": null,
  "expires_at": null,
  "payload": {
    "reason": "available",
    "matched_batches": 1,
    "available_batches": 1,
    "total_available_qty": 141.0,
    "slow_move": false
  },
  "fetched_at": "2026-06-23T17:06:24.428654+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 31. availability / acquire_availability_hold

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `2430.73 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "94764066649319424128",
  "service_start_at": "2026-07-09T21:45:00Z",
  "service_end_at": "2026-07-10T03:11:29.751482Z",
  "qty": 2,
  "batch_no": "QF1351-20260709",
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
    "provider_item_uuid": "94764066649319424128",
    "batch_no": "QF1351-20260709",
    "service_start_at": "2026-07-09T21:45:00+00:00",
    "service_end_at": "2026-07-10T03:11:29.751482+00:00",
    "available": true,
    "hold_token": "fc648d343bc01e5dd6fd7ae2edf1de4a",
    "expires_at": "2026-06-23T17:21:26.750860+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 141.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-23T17:06:26.857214+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 32. availability / confirm_availability_hold

- Method: `confirm_availability_hold`
- Status: `pass`
- Elapsed: `2712.9 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "fc648d343bc01e5dd6fd7ae2edf1de4a",
  "provider_item_uuid": "94764066649319424128",
  "batch_no": "QF1351-20260709"
}
```

Output:

```json
{
  "availability": {
    "operation": "confirm_hold",
    "provider_item_uuid": "94764066649319424128",
    "batch_no": "QF1351-20260709",
    "service_start_at": null,
    "service_end_at": null,
    "available": true,
    "hold_token": "fc648d343bc01e5dd6fd7ae2edf1de4a",
    "expires_at": null,
    "payload": {
      "reason": "hold_confirmed"
    },
    "fetched_at": "2026-06-23T17:06:29.568189+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```

### 33. availability / acquire_availability_hold (for release test)

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `2476.02 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "94764066649319424128",
  "service_start_at": "2026-07-09T21:45:00Z",
  "service_end_at": "2026-07-10T03:11:29.751482Z",
  "qty": 1,
  "batch_no": "QF1351-20260709"
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "94764066649319424128",
    "batch_no": "QF1351-20260709",
    "service_start_at": "2026-07-09T21:45:00+00:00",
    "service_end_at": "2026-07-10T03:11:29.751482+00:00",
    "available": true,
    "hold_token": "642358796089455678ab2233cd52342c",
    "expires_at": "2026-06-23T17:21:31.938396+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 139.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-23T17:06:32.046463+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 34. availability / release_availability_hold

- Method: `release_availability_hold`
- Status: `pass`
- Elapsed: `2385.69 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "642358796089455678ab2233cd52342c",
  "provider_item_uuid": "94764066649319424128",
  "batch_no": "QF1351-20260709"
}
```

Output:

```json
{
  "availability": {
    "operation": "release_hold",
    "provider_item_uuid": "94764066649319424128",
    "batch_no": "QF1351-20260709",
    "service_start_at": null,
    "service_end_at": null,
    "available": true,
    "hold_token": "642358796089455678ab2233cd52342c",
    "expires_at": null,
    "payload": {
      "reason": "hold_released"
    },
    "fetched_at": "2026-06-23T17:06:34.429521+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```

### 35. availability / acquire_availability_hold (for expire test)

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `2447.19 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "94764066649319424128",
  "service_start_at": "2026-07-09T21:45:00Z",
  "service_end_at": "2026-07-10T03:11:29.751482Z",
  "qty": 1,
  "batch_no": "QF1351-20260709"
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "94764066649319424128",
    "batch_no": "QF1351-20260709",
    "service_start_at": "2026-07-09T21:45:00+00:00",
    "service_end_at": "2026-07-10T03:11:29.751482+00:00",
    "available": true,
    "hold_token": "6cecbe7fe8b60a1c5a65d3a3d24eecc3",
    "expires_at": "2026-06-23T17:21:36.775667+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 139.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-23T17:06:36.878778+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 36. availability / expire_availability_hold

- Method: `expire_availability_hold`
- Status: `pass`
- Elapsed: `2273.44 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "6cecbe7fe8b60a1c5a65d3a3d24eecc3",
  "provider_item_uuid": "94764066649319424128",
  "batch_no": "QF1351-20260709"
}
```

Output:

```json
{
  "availability": {
    "operation": "expire_hold",
    "provider_item_uuid": "94764066649319424128",
    "batch_no": "QF1351-20260709",
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
- Elapsed: `2697.25 ms`

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
- Elapsed: `2685.22 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "21965879857802920064"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "21965879857802920064",
  "bundle_code": "FLT-ITIN-002",
  "bundle_name": "Flight Itinerary HKG->SFO + SFO->SYD + ATL->LAX",
  "bundle_type": "flight_itinerary",
  "description": "Multi-leg flight itinerary template composed of independently priced flight legs.",
  "extra": {
    "routes": [
      "HKG->SFO",
      "SFO->SYD",
      "ATL->LAX"
    ],
    "source": "prepare_flight_products",
    "leg_count": "3",
    "item_external_ids": [
      "FLIGHT-HKG-SFO-ECO",
      "FLIGHT-SFO-SYD-FIR",
      "FLIGHT-ATL-LAX-PRE"
    ]
  },
  "status": "active",
  "created_at": "2026-06-22T03:42:42.024787",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-22T03:42:42.024787",
  "components": [
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "00385410950007636096",
      "bundle_uuid": "21965879857802920064",
      "item_uuid": "57869541269638758528",
      "provider_item_uuid": "47661094399809437824",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 1.0,
      "extra": {
        "route": "HKG->SFO",
        "item_external_id": "FLIGHT-HKG-SFO-ECO",
        "provider_item_external_id": "QF-HKG-SFO-ECO"
      },
      "status": "active",
      "created_at": "2026-06-22T03:42:42.468635",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T03:42:42.468635"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "13667089905227939968",
      "bundle_uuid": "21965879857802920064",
      "item_uuid": "81113158557154427008",
      "provider_item_uuid": "67821393777736564864",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 3.0,
      "extra": {
        "route": "ATL->LAX",
        "item_external_id": "FLIGHT-ATL-LAX-PRE",
        "provider_item_external_id": "CX-ATL-LAX-PRE"
      },
      "status": "active",
      "created_at": "2026-06-22T03:42:43.025116",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T03:42:43.025116"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "74857264317459349632",
      "bundle_uuid": "21965879857802920064",
      "item_uuid": "03407115177205710976",
      "provider_item_uuid": "78656939654886998144",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 2.0,
      "extra": {
        "route": "SFO->SYD",
        "item_external_id": "FLIGHT-SFO-SYD-FIR",
        "provider_item_external_id": "CX-SFO-SYD-FIR"
      },
      "status": "active",
      "created_at": "2026-06-22T03:42:42.750540",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T03:42:42.750540"
    }
  ]
}
```

### 39. bundles / search_bundle_components

- Method: `search_bundle_components`
- Status: `pass`
- Elapsed: `2330.06 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "21965879857802920064"
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
      "bundle_component_uuid": "00385410950007636096",
      "bundle_uuid": "21965879857802920064",
      "item_uuid": "57869541269638758528",
      "provider_item_uuid": "47661094399809437824",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 1.0,
      "extra": {
        "route": "HKG->SFO",
        "item_external_id": "FLIGHT-HKG-SFO-ECO",
        "provider_item_external_id": "QF-HKG-SFO-ECO"
      },
      "status": "active",
      "created_at": "2026-06-22T03:42:42.468635",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T03:42:42.468635"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "13667089905227939968",
      "bundle_uuid": "21965879857802920064",
      "item_uuid": "81113158557154427008",
      "provider_item_uuid": "67821393777736564864",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 3.0,
      "extra": {
        "route": "ATL->LAX",
        "item_external_id": "FLIGHT-ATL-LAX-PRE",
        "provider_item_external_id": "CX-ATL-LAX-PRE"
      },
      "status": "active",
      "created_at": "2026-06-22T03:42:43.025116",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T03:42:43.025116"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "74857264317459349632",
      "bundle_uuid": "21965879857802920064",
      "item_uuid": "03407115177205710976",
      "provider_item_uuid": "78656939654886998144",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 2.0,
      "extra": {
        "route": "SFO->SYD",
        "item_external_id": "FLIGHT-SFO-SYD-FIR",
        "provider_item_external_id": "CX-SFO-SYD-FIR"
      },
      "status": "active",
      "created_at": "2026-06-22T03:42:42.750540",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T03:42:42.750540"
    }
  ]
}
```

### 40. cancellation / get_cancellation_policy (Business Fare)

- Method: `get_cancellation_policy`
- Status: `pass`
- Elapsed: `2631.48 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "policy_uuid": "45519135682445983872"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "policy_uuid": "45519135682445983872",
  "provider_item_uuid": null,
  "label": "Economy Fare Cancellation",
  "description": "Arrive get financial subject person better political ground along continue natural chair religious like money cell.",
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
  "created_at": "2026-06-01T22:19:27.748667",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-01T22:19:27.748667"
}
```

### 41. cancellation / search_cancellation_policies

- Method: `search_cancellation_policies`
- Status: `pass`
- Elapsed: `2592.25 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "94764066649319424128"
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
- Elapsed: `3283.79 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "query_text": "Qantas CDG SFO First class flight",
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
          "score": "0.7828671932220459",
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
          "score": "0.7722446322441101",
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
          "score": "0.7453662157058716",
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
          "score": "0.6812183856964111",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "British Airways (BA) operates flight service Flight ORD->BOS Business from ORD to BOS in Business class. Business class non-stop service from Chicago (ORD) to Boston (BOS). Base price $1800.0 USD per seat. Baggage allowance 32kg, meal included: True. Pricing tiers:   - adult: $1800.0 USD;   - child: $1350.0 USD;   - infant: $180.0 USD. Scheduled flights:\n  - Flight BA1430 departing 2026-07-17T21:00:00Z arriving 2026-07-18T00:24:58.762088Z with 24 seats available. Cancellation policy: Business Fare Cancellation.\n  - Flight BA7142 departing 2026-08-08T11:00:00Z arriving 2026-08-08T16:28:08.421105Z with 26 seats available. Cancellation policy: Business Fare Cancellation.\nThis is a Business class flight product offered by British Airways on the ORD->BOS route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:20",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:20",
          "score": "0.6810191869735718",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-23T17:06:55.375895+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```
