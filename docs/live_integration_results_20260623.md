# MCP HospiRFQ Processor Live Integration Results

- Generated at: `2026-06-23T06:32:33.275823+00:00`
- Gateway: `http://localhost:8765`
- Endpoint: `gpt`
- Partition: `nestaging`
- GraphQL URL: `http://localhost:8765/gpt/rfq_graphql`
- Dependency order: `catalog_discovery, items, requests, quotes, pricing, installments, files, segments, availability, bundles, cancellation, catalog`
- Passed: `1`
- Error responses: `0`
- Failed: `0`
- Total calls: `1`
- SOP reference: `docs/integration_scenarios_sop.md` version `0.1.0`, approved by user on `2026-06-17`
- Final certification status: `Integration Certified`

## Executive Summary

End-to-end live integration testing was executed against the local `silvaengine_gateway` route for `mcp_hospirfq_processor` using `.env`-driven connection settings and prepared `../rfq_engine` flight RFQ data. The final dependency-ordered run completed with 1 passing function calls, 0 error responses, and 0 failures. Catalog search was executed first and selected `Flight CDG->JFK Business`, which was reconciled to `flight_catalog_refs.json` and `flight_products.json` before item, request, quote, pricing, installment, availability, bundle, cancellation, and catalog validation continued. The SOP-scoped integration is certified for the tested local environment.

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
| Catalog selection consistency | selected catalog hit maps to `flight_catalog_refs.json` item/provider IDs | 0 mismatches | `17735923656909930624` / `55349863084404523136` selected | pass |
| Batch consistency | selected item/provider maps to `flight_products.json` batch and service window | 0 mismatches | `AF8751-20260811`, `2026-08-11T08:30:00Z` to `2026-08-11T20:57:51.046308Z` | pass |
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
- Elapsed: `3040.15 ms`

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
            "text": "Delta Air Lines (DL) operates flight service Flight NRT->CDG First from NRT to CDG in First class. First class non-stop service from Tokyo (NRT) to Paris (CDG). Base price $4500.0 USD per seat. Baggage allowance 32kg, meal included: True. Pricing tiers:   - adult: $4500.0 USD;   - child: $3375.0 USD;   - infant: $450.0 USD. Scheduled flights:\n  - Flight DL4000 departing 2026-09-05T21:15:00Z arriving 2026-09-06T08:30:40.740402Z with 7 seats available. Cancellation policy: First Fare Cancellation.\n  - Flight DL4822 departing 2026-09-18T14:45:00Z arriving 2026-09-18T23:28:08.831283Z with 7 seats available. Cancellation policy: First Fare Cancellation.\nThis is a First class flight product offered by Delta Air Lines on the NRT->CDG route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:45",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:45",
          "score": "0.7341679930686951",
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
          "score": "0.7325248122215271",
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
          "score": "0.7050315737724304",
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
          "score": "0.7014548778533936",
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
          "score": "0.700347900390625",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-23T06:32:33.271830+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```
