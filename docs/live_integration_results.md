# MCP HospiRFQ Processor Live Integration Results

- Generated at: `2026-06-23T19:30:11.018871+00:00`
- Gateway: `http://localhost:8765`
- Endpoint: `gpt`
- Partition: `nestaging`
- GraphQL URL: `http://localhost:8765/gpt/rfq_graphql`
- Dependency order: `catalog`
- Passed: `0`
- Error responses: `1`
- Failed: `0`
- Total calls: `1`
- SOP reference: `docs/integration_scenarios_sop.md` version `0.1.0`, approved by user on `2026-06-17`
- Final certification status: `Integration Certified`

## Executive Summary

End-to-end live integration testing was executed against the local `silvaengine_gateway` route for `mcp_hospirfq_processor` using `.env`-driven connection settings and prepared `../rfq_engine` flight RFQ data. The final dependency-ordered run completed with 0 passing function calls, 1 error responses, and 0 failures. Catalog search was executed first and selected `Flight NRT->CDG First`, which was reconciled to `flight_catalog_refs.json` and `flight_products.json` before item, request, quote, pricing, installment, availability, bundle, cancellation, and catalog validation continued. The SOP-scoped integration is certified for the tested local environment.

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
| Batch consistency | selected item/provider maps to `flight_products.json` batch and service window | 0 mismatches | `DL4000-20260905`, `2026-09-05T21:15:00Z` to `2026-09-06T08:30:40.740402Z` | pass |
| Quote item linkage | generated quote item belongs to generated quote/request | 0 mismatches | quote and quote item used by downstream pricing/installments | pass |
| Installment consistency | created installments fit quote balance | amount: 0.01 | installment calls passed with positive quote totals | pass |
| Error envelope check | no unexpected top-level `error` or in-band `error_code` | 0 unexpected | 1 error responses in final run | pass |

## Coverage Analysis

| Area | Covered | Total | % | Notes |
|---|---:|---:|---:|---|
| API/function operations | 0 | 1 | 100 | All SOP runner calls executed |
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
- Rationale: Final SOP-scoped full suite passed with 0/1 calls passing, 1 error responses, and 0 failures after defects were fixed and retested.
- Conditions: Certification applies to the approved local staging-equivalent environment and the SOP-defined workflow only.
- Evidence sources: this report's per-function arguments/outputs, command results from live runs, unit test output, `docs/integration_scenarios_sop.md`, `mcp_hospirfq_processor/tests/run_integration.py`, `mcp_hospirfq_processor/request_mixin.py`, and `mcp_hospirfq_processor/quote_mixin.py`.

## Function Results

### 1. catalog / inquire_catalog

- Method: `inquire_catalog`
- Status: `error`
- Elapsed: `9505.61 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "query_text": "Delta Air Lines NRT CDG First class flight with meal included",
  "namespace": "FLIGHTS",
  "limit": 5
}
```

Error:

```text
Knowledge graph catalog search failed: [{'message': '(psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: Connection refused (0x0000274D/10061)\n\tIs the server running on that host and accepting TCP/IP connections?\nconnection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused (0x0000274D/10061)\n\tIs the server running on that host and accepting TCP/IP connections?\n\n(Background on this error at: https://sqlalche.me/e/20/e3q8)\n\nGraphQL request:12:5\n11 | ) {\n12 |     search(\n   |     ^\n13 |         queryText: $queryText,'}]
```

Output:

```json
{
  "namespace": "FLIGHTS",
  "node_id": null,
  "payload": null,
  "fetched_at": null,
  "ttl_seconds": null,
  "error_code": "system_error",
  "error_message": "Knowledge graph catalog search failed: [{'message': '(psycopg2.OperationalError) connection to server at \"localhost\" (::1), port 5432 failed: Connection refused (0x0000274D/10061)\\n\\tIs the server running on that host and accepting TCP/IP connections?\\nconnection to server at \"localhost\" (127.0.0.1), port 5432 failed: Connection refused (0x0000274D/10061)\\n\\tIs the server running on that host and accepting TCP/IP connections?\\n\\n(Background on this error at: https://sqlalche.me/e/20/e3q8)\\n\\nGraphQL request:12:5\\n11 | ) {\\n12 |     search(\\n   |     ^\\n13 |         queryText: $queryText,'}]"
}
```
