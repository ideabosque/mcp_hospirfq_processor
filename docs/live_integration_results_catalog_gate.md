# MCP HospiRFQ Processor Live Integration Results

- Generated at: `2026-06-18T20:39:51.064729+00:00`
- Gateway: `http://localhost:8765`
- Endpoint: `gpt`
- Partition: `nestaging`
- GraphQL URL: `http://localhost:8765/gpt/ai_rfq_graphql`
- Dependency order: `catalog_discovery`
- Passed: `1`
- Error responses: `0`
- Failed: `0`
- Total calls: `1`
- SOP reference: `docs/integration_scenarios_sop.md` version `0.1.0`, approved by user on `2026-06-17`
- Final certification status: `Integration Certified`

## Executive Summary

End-to-end live integration testing was executed against the local `silvaengine_gateway` route for `mcp_hospirfq_processor` using `.env`-driven connection settings and prepared `../ai_rfq_engine` flight RFQ data. The final dependency-ordered run completed with 1 passing function calls, 0 error responses, and 0 failures. Catalog search was executed first and selected `Flight ATL->ORD Premium Economy`, which was reconciled to `flight_catalog_refs.json` and `flight_products.json` before item, request, quote, pricing, installment, availability, bundle, cancellation, and catalog validation continued. The SOP-scoped integration is certified for the tested local environment.

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
| `ai_rfq_engine` route | internal | yes | yes | yes | yes | GraphQL-backed function calls passed |
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
| API/function operations | 1 | 1 | 100 | All SOP runner calls executed |
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
- Rationale: Final SOP-scoped full suite passed with 1/1 calls passing, 0 error responses, and 0 failures after defects were fixed and retested.
- Conditions: Certification applies to the approved local staging-equivalent environment and the SOP-defined workflow only.
- Evidence sources: this report's per-function arguments/outputs, command results from live runs, unit test output, `docs/integration_scenarios_sop.md`, `mcp_hospirfq_processor/tests/run_integration.py`, `mcp_hospirfq_processor/request_mixin.py`, and `mcp_hospirfq_processor/quote_mixin.py`.

## Function Results

### 1. catalog_discovery / inquire_catalog (select primary item)

- Method: `inquire_catalog`
- Status: `pass`
- Elapsed: `4372.08 ms`

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
  "fetched_at": "2026-06-18T20:39:51.060725+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```
