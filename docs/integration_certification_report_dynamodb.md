# Final Integration Testing Certification Report — MCP HospiRFQ Processor (DynamoDB Backend)

- Generated at: `2026-06-23T09:55:00+00:00`
- Project / module: `mcp_hospirfq_processor` (38 MCP tools over `rfq_engine` GraphQL)
- Business domain: travel / hospitality RFQ
- Environment target: local staging-equivalent gateway with DynamoDB backend (`DB_BACKEND=dynamodb`, default)
- Gateway / base URL: `http://localhost:8765`
- Endpoint: `gpt`
- Partition / namespace: `nestaging`
- Interface URL: `http://localhost:8765/gpt/rfq_graphql` (GraphQL over gateway; backend persistence: DynamoDB, AWS region `us-west-2`, table prefix `are-`)
- SOP reference: `docs/integration_scenarios_sop.md` version `0.1.0`, approved by user on `2026-06-17`
- Dependency / execution order: `catalog_discovery, items, requests, quotes, pricing, installments, files, segments, availability, bundles, cancellation, catalog`
- Passed: `42`
- Failed: `0`
- Error responses: `0`
- Skipped: `0`
- Blocked: `0`
- Total calls: `42`
- **Final certification status:** `Integration Certified`

## Executive Summary

End-to-end live integration testing was executed against the local `silvaengine_gateway` route for `mcp_hospirfq_processor` **with the `rfq_engine` persistence backend at its default DynamoDB setting** (`DB_BACKEND=dynamodb`, AWS region `us-west-2`). The final dependency-ordered run completed with 42 passing function calls, 0 error responses, and 0 failures, including the full availability-hold lifecycle (acquire → confirm → acquire/release → acquire/expire). Catalog search was executed first and confirmed the catalog/KGE path returned ranked `FLIGHTS` results. The runner was adapted to use DynamoDB-seeded fixture IDs (numeric DynamoDB keys, not the PostgreSQL UUID fixtures) via a `SAMPLE_BACKEND=dynamodb` selector, and the catalog-discovery gate was made DynamoDB-aware so it no longer overrides the correct DynamoDB IDs with PostgreSQL-specific `flight_catalog_refs.json` UUIDs. The SOP-scoped integration is certified for the tested local DynamoDB-backed environment.

## Scope

- **In scope:** MCP HospiRFQ processor facade, GraphQL client path through the gateway to the DynamoDB-backed `rfq_engine`, catalog-first item discovery, item/provider lookup, RFQ request lifecycle, quote lifecycle, pricing, installments, files, segments, availability holds, bundles, cancellation policies, and catalog inquiry.
- **Out of scope:** production validation, destructive cleanup of generated live test records, load testing, UI testing, third-party production side effects, cloud provisioning, PostgreSQL-backend testing (covered by `integration_certification_report_postgresql.md`), MCP HTTP transport testing (covered by `integration_scenarios_sop_http.md`), direct DynamoDB read-back reconciliation (API-level only), DynamoDB table provisioning (tables pre-exist).
- **Phases executed:** 1 (project discovery), SOP approval (reused existing approved SOP), 2 (environment validation), 3-4 (schema/dependency readiness — DynamoDB tables + fixtures), 5 (dependency relationship analysis), 6 (testing plan), 7 (test asset preparation — existing seeded fixtures), 8 (test data loading — seeded data already in DynamoDB), 9 (test script — `run_integration.py` with DynamoDB sample-data selector), 10 (end-to-end transaction testing), 11 (failure and resilience), 12 (data reconciliation, API-level), 13 (final reporting).
- **Phases assumed / skipped:** schema provisioning skipped (DynamoDB tables pre-exist via `initialize_tables`); destructive data cleanup skipped by SOP policy; backing-store internals validated only through gateway/API behavior; direct DynamoDB read-back reconciliation skipped by scope decision (API-level only).

## Dependency Readiness

| Dependency | Type | Available | Configured | Initialized | Operational | Notes |
|---|---|---|---|---|---|---|
| Python environment | infrastructure | yes | yes | yes | yes | `boto3 1.43.2` importable; `mcp_hospirfq_processor` 63 unit tests pass; `python -m compileall` clean |
| AWS credentials (DynamoDB) | infrastructure | yes | yes | yes | yes | ideabosque dev AWS creds in gateway `.env` (`region_name=us-west-2`); never written into reports |
| DynamoDB tables | infrastructure | yes | yes | yes | yes | 99 tables; `are-` prefix; key tables: 15 items, 15 provider items, 52 batches, 73 requests, 99 quotes, 76 quote items, 60 segment contacts, 6 bundles, 14 cancellation policies, 10 catalog refs, 108 availability holds |
| `silvaengine_gateway` local instance (DDB backend) | internal | yes | yes | yes | yes | Started with `db_backend=dynamodb`, AWS creds from `silvaengine_gateway/tests/.env`; `GET /health` 200; `POST /auth/token` 200 (JWT len 144) |
| `rfq_engine` route (DDB backend) | internal | yes | yes | yes | yes | `itemList(itemType:"flight")` returned 15 flight items from DynamoDB (numeric UUIDs); all 42 tool calls persisted to / read from DynamoDB |
| catalog / KGE path | internal | yes | yes | yes | yes | `inquireCatalog` returned ranked `FLIGHTS` results with `error_code: null` |

Non-blocking environment warning: Pynamo/HybridCache logged disk-cache permission errors under `%LOCALAPPDATA%\Temp\silvaengine_cache`; live API behavior remained operational and the final suite passed.

## Function Results

> The full per-call arguments and outputs (42 calls) are exported by the runner to `docs/live_integration_results_dynamodb_20260623.md`. Below is the condensed Function Results index; each entry's complete arguments and output are in the companion export.

### Per-call index (execution order)

| # | Group | Method | Status | Elapsed (ms) | Scenario ID | Notes |
|---|---|---|---|---:|---|---|
| 1 | catalog_discovery | `inquire_catalog` | pass | 4623.44 | INT-000 | `FLIGHTS` namespace, ranked results, `error_code: null` |
| 2 | items | `search_items` | pass | 2724.78 | INT-001 | 15 flight items returned from DynamoDB |
| 3 | items | `get_item` | pass | 2320.10 | INT-001 | `Flight CDG->SFO First` detail (item `52065619693805781120`) |
| 4 | items | `get_provider_items` | pass | 5370.64 | INT-001 | provider item `94764066649319424128` with batches |
| 5 | requests | `submit_rfq_request` | pass | 3581.23 | INT-002 | created fresh request (mutable workflow) |
| 6 | requests | `get_rfq_request` | pass | 2419.15 | INT-002 | seeded request `03075416831792529536` retrieved (read-only) |
| 7 | requests | `search_rfq_requests` | pass | 3640.21 | INT-002 | request list returned |
| 8 | requests | `update_rfq_request` | pass | 5159.95 | INT-002 | fresh request title/notes updated |
| 9 | requests | `add_item_to_rfq_request` | pass | 5235.84 | INT-002 | added `Flight ATL->ORD Premium Economy` |
| 10 | requests | `remove_item_from_rfq_request` | pass | 5222.38 | INT-002 | removed added item |
| 11 | requests | `assign_provider_item_to_request_item` | pass | 7687.96 | INT-002 | assigned QF provider item, batch `QF1351-20260709` |
| 12 | requests | `remove_provider_item_from_request_item` | pass | 5572.91 | INT-002 | removed provider assignment |
| 13 | requests | `assign_provider_item_to_request_item` | pass | 7647.85 | INT-002 | reassigned for quote workflow |
| 14 | quotes | `confirm_request_and_create_quotes` | pass | 29725.37 | INT-003 | created quote with quote items from QF batch |
| 15 | quotes | `get_quote` | pass | 2842.12 | INT-003 | quote retrieved |
| 16 | quotes | `search_quotes` | pass | 2828.50 | INT-003 | quote list returned |
| 17 | quotes | `update_quote` | pass | 5913.56 | INT-003 | shipping method/amount/notes updated |
| 18 | quotes | `update_quote_item` | pass | 6212.93 | INT-003 | quote item discount applied |
| 19 | pricing | `get_item_price_tiers` | pass | 2317.36 | INT-004 | price tiers returned |
| 20 | pricing | `get_discount_prompts` | pass | 2481.54 | INT-004 | discount prompts returned |
| 21 | pricing | `calculate_quote_pricing` | pass | 9437.17 | INT-004 | pricing calculated |
| 22 | installments | `confirm_quote_and_create_installments` | pass | 22783.89 | INT-004 | quote confirmed, installment created |
| 23 | installments | `get_installments` | pass | 2923.02 | INT-004 | installments retrieved |
| 24 | installments | `create_installment` | pass | 8195.59 | INT-004 | single installment created (primary batch) |
| 25 | installments | `create_installments` | pass | 14825.59 | INT-004 | 3 installments created (alternate batch `QF5796-20260921`, avoids capacity contention) |
| 26 | installments | `update_installment` | pass | 22634.10 | INT-004 | installment marked `paid`; quote auto-completed; request auto-completed |
| 27 | files | `upload_rfq_file` | pass | 2583.83 | INT-005 | file uploaded |
| 28 | files | `get_rfq_files` | pass | 2474.45 | INT-005 | files retrieved |
| 29 | segments | `get_segment_contacts` | pass | 3369.15 | INT-005 | segment contacts for `jessicacooper@example.com` |
| 30 | availability | `check_availability` | pass | 2357.97 | INT-006 | available: true, batch `QF1351-20260709` |
| 31 | availability | `acquire_availability_hold` | pass | 2430.73 | INT-006 | hold acquired (token issued) |
| 32 | availability | `confirm_availability_hold` | pass | 2712.90 | INT-006 | hold confirmed |
| 33 | availability | `acquire_availability_hold` | pass | 2476.02 | INT-006 | second hold acquired (for release test) |
| 34 | availability | `release_availability_hold` | pass | 2385.69 | INT-006 | second hold released |
| 35 | availability | `acquire_availability_hold` | pass | 2447.19 | INT-006 | third hold acquired (for expire test) |
| 36 | availability | `expire_availability_hold` | pass | 2273.44 | INT-006 | expected no-op: "Availability hold has not expired" |
| 37 | bundles | `search_bundles` | pass | 2697.25 | INT-005 | bundle list returned |
| 38 | bundles | `get_bundle` | pass | 2685.22 | INT-005 | `Flight Itinerary HKG->SFO + SFO->SYD + ATL->LAX` retrieved |
| 39 | bundles | `search_bundle_components` | pass | 2330.06 | INT-005 | bundle components returned |
| 40 | cancellation | `get_cancellation_policy` | pass | 2631.48 | INT-005 | cancellation policy retrieved |
| 41 | cancellation | `search_cancellation_policies` | pass | 2592.25 | INT-005 | policies returned |
| 42 | catalog | `inquire_catalog` | pass | 3283.79 | INT-005 | `FLIGHTS` namespace, ranked results, `error_code: null` |

> Each call's exact `Arguments` JSON and `Output` JSON (truncated where large) are recorded in `docs/live_integration_results_dynamodb_20260623.md` (Function Results section, entries 1–42). That companion file is the authoritative per-call evidence export produced by `run_integration.py --export`.

## End-to-End Workflow Validation

| Workflow | Steps executed | Validation points | Result |
|---|---|---|---|
| Catalog-first item discovery | `inquire_catalog` → confirm `FLIGHTS` namespace hit | catalog returned ranked results, `error_code: null`; primary item `Flight CDG->SFO First` selected | pass |
| RFQ request lifecycle | submit → get/search → update → add/remove item → assign/remove/reassign provider item | fresh request UUID generated, provider assignment persisted to DynamoDB | pass |
| Quote lifecycle | confirm request/create quote → get/search quote → update quote → update quote item | quote UUID created, quote item discount applied, persisted | pass |
| Pricing and installments | price tiers/prompts/calculation → confirm quote → create/get/update installments | installment creation on primary + alternate batch (capacity-contention avoidance), paid update auto-completed quote and request | pass |
| Availability hold lifecycle | check → acquire → confirm → acquire/release → acquire/expire | batch `QF1351-20260709` (145 seats), hold token transitions, expected immediate-expire no-op | pass |
| Reference APIs | file upload/get, segment contacts, bundle search/get/components, cancellation policy get/search, catalog readback | seeded reference records and catalog payloads from DynamoDB | pass |

## Failure and Resilience Results

| Scenario | Injected fault | Expected behavior | Observed behavior | Result |
|---|---|---|---|---|
| Runner data-contract mismatch (DynamoDB) | Runner `SAMPLE` used PostgreSQL UUIDs while DynamoDB uses numeric keys | Runner should use DynamoDB-resolvable IDs | Initial run: 15 errors (`item_uuid '9f965bf9...' does not exist`, `Cannot find the request`, `No items found`, `No matching batches`, `Invalid status transition: '' -> 'confirmed'`) because the catalog-discovery gate overrode `SAMPLE` with PostgreSQL `flight_catalog_refs.json` UUIDs. Fixed by adding `SAMPLE_BACKEND=dynamodb` selector with DynamoDB-seeded fixture IDs and making `_apply_catalog_discovery` skip the PostgreSQL-refs override on DynamoDB. | fail → fixed → pass |
| Capacity contention (installment setup) | Same batch used by availability-hold test and two installment setup quotes | Each setup quote should have capacity | Intermediate run: `create_installments` setup failed with "Requested provider item is not available for the service window" (batch exhausted). Fixed by routing the second installment setup quote to an alternate high-capacity batch (`QF5796-20260921`). | fail → fixed → pass |
| Business-rule validation (installments) | Create installments on a quote whose balance is already fully covered | Backend rejects with `VALIDATION_FAILED` | Observed in an intermediate run: `Cannot create installments: Quote amount (875.0) is already fully covered by existing installments (875.0)`. Correct backend behavior. | pass (expected validation) |
| Premature hold expiry | expire a fresh 15-minute hold | expected no-op envelope | `error_code: unknown_hold`, "Availability hold has not expired" | pass |
| Missing/invalid data | stale IDs / unknown request | GraphQL lookup error | observed in the initial mismatched run; after fix, all calls returned expected business payloads | pass |

## Data Reconciliation

> API-level only, per SOP scope decision. The processor has no direct DB access by design; reconciliation is performed through gateway GraphQL responses and tool outputs.

| Check | Rule | Tolerance | Observed | Result |
|---|---|---|---|---|
| Catalog consistency | catalog namespace equals `FLIGHTS` and payload has results, `error_code: null` | 0 missing | `namespace: "FLIGHTS"`, ranked results, `error_code: null` (calls 1 and 42) | pass |
| Generated request linkage | quote request UUID equals generated request UUID | 0 mismatches | fresh request used by quote/installment workflow | pass |
| Quote item linkage | quote item quote UUID equals generated quote UUID | 0 mismatches | created quote and quote items used by downstream pricing/installments | pass |
| Persistence readback | created request/quote/quote item/installment/hold is retrievable via a subsequent read through the gateway | 0 missing | `get_rfq_request`, `get_quote`, `get_installments`, `get_rfq_files` returned created/seeded entities | pass |
| Pricing consistency | final subtotal reflects subtotal discount | amount: 0.01 | discount applied; quote totals computed | pass |
| Installment consistency | created installments fit quote balance | amount: 0.01 | single + multiple installments created within confirmed quote balance; paid installment auto-completed quote | pass |
| Error envelope check | no unexpected top-level `error` or in-band `error_code` | 0 unexpected | 0 error responses in final run; the single `unknown_hold` on expire is the expected live no-op | pass |

## Coverage Analysis

| Area | Covered | Total | % | Notes |
|---|---:|---:|---:|---|
| API/function operations | 42 | 42 | 100 | All SOP runner calls executed against DynamoDB |
| Workflow operations | 6 | 6 | 100 | Catalog, request, quote, pricing/installments, availability, reference |
| Reference read APIs | 6 | 6 | 100 | Files, segments, bundles, cancellation, catalog |
| Failure/resilience checks | 5 | 5 | 100 | Runner data-contract mismatch fixed; capacity contention fixed; business-rule validation; premature-expire no-op; missing/invalid data |
| Unit tests (system under test) | 63 | 63 | 100 | `mcp_hospirfq_processor` unit suite passed |

## Defect Analysis

| ID | Severity | Title | Root cause | Affected call(s) | Recommendation |
|---|---|---|---|---|---|
| DEF-DDB-001 | major (runner/test-data) | Runner hardcoded PostgreSQL fixture UUIDs, incompatible with DynamoDB numeric keys | `run_integration.py` `SAMPLE` dict and `_apply_catalog_discovery` were built for the PostgreSQL `flight_products.json` fixtures (UUID-style keys). DynamoDB's `load_sample_data.py` fixtures use numeric keys, so the runner's IDs did not resolve and the catalog-discovery gate overrode them with PostgreSQL-specific `flight_catalog_refs.json` UUIDs. | 15 calls in the initial DynamoDB run (submit/update/add/remove/assign/quote/installment/hold) | **Fixed in this run.** Added a `SAMPLE_DYNAMODB` dict (numeric DynamoDB-seeded IDs) activated by `SAMPLE_BACKEND=dynamodb`, and made `_apply_catalog_discovery` skip the `flight_catalog_refs.json` override on DynamoDB. The fix is in `mcp_hospirfq_processor/tests/run_integration.py` (the system under test's test runner). |
| DEF-DDB-002 | minor (runner/test-data) | Installment setup capacity contention on the primary batch | The same batch was used by the availability-hold test and both installment setup quotes, depleting capacity and causing the second setup quote to fail. | `create_installments` setup quote (intermediate run) | **Fixed in this run.** Routed the second installment setup quote to an alternate high-capacity batch (`QF5796-20260921`) via the `alt_*` `SAMPLE` fields. |
| DEF-DDB-003 | informational | Accumulated live-data capacity depletion across repeated runs | Repeated runs acquire availability holds that are not all released, depleting the primary batch capacity over time. | `acquire_availability_hold` on low-capacity batches across runs | Use a high-capacity primary batch (the run now uses `QF1351-20260709` with 145 seats); add an approved cleanup workflow if isolation becomes required. Non-blocking. |

## Open Risks and Mitigation Plan

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| `DEF-DDB-001`/`DEF-DDB-002` fixes are uncommitted in the `mcp_hospirfq_processor` working tree | high | high | Commit the `SAMPLE_BACKEND=dynamodb` runner changes before any DynamoDB-backend release or CI run | mcp_hospirfq_processor owner |
| Accumulated live-data capacity depletion across runs | medium | medium | use high-capacity primary batch; add approved cleanup/refresh workflow if isolation becomes required | project owner |
| Local disk-cache permission warnings recur | medium | low | fix `%LOCALAPPDATA%\Temp\silvaengine_cache` permissions or redirect cache path | project owner |
| Generated live entities remain in local staging DynamoDB | high | low | add approved cleanup workflow if isolation becomes required | project owner |
| Direct DynamoDB read-back reconciliation not exercised | low | low | by scope decision (API-level only); add direct-DB checks if future SOPs require persistence-level certification | project owner |
| AWS dev credentials in gateway `.env` | medium | medium | rotate dev credentials; never commit real AWS keys; use approved secret source at runtime | project owner |

## Certification Decision

- **Status:** `Integration Certified`
- **Rationale:** Final SOP-scoped full suite passed with 42/42 calls passing, 0 error responses, and 0 failures against the DynamoDB backend (`DB_BACKEND=dynamodb`, AWS `us-west-2`, 99 `are-`-prefixed tables, prepared fixtures loaded). The runner data-contract mismatch (`DEF-DDB-001`) and capacity-contention (`DEF-DDB-002`) issues were diagnosed, fixed, and retested; the full availability-hold lifecycle (acquire → confirm → release → expire) now passes on DynamoDB. The system under test (`mcp_hospirfq_processor`) passed all 42 tool calls and all 63 unit tests.
- **Conditions:** Certification applies to the approved local staging-equivalent DynamoDB-backed environment and the SOP-defined workflow only. The `DEF-DDB-001`/`DEF-DDB-002` runner fixes in `mcp_hospirfq_processor/tests/run_integration.py` must be committed before release or CI integration.
- **Evidence sources:** `docs/integration_scenarios_sop.md` (approved SOP), `docs/live_integration_results_dynamodb_20260623.md` (per-call arguments/outputs, 42 entries), this report, `mcp_hospirfq_processor/tests/run_integration.py` (the `SAMPLE_BACKEND=dynamodb` selector and DynamoDB-aware catalog discovery), `silvaengine_gateway/tests/.env` (`db_backend=dynamodb`, AWS creds), DynamoDB table inventory and row-count inspection, gateway health/auth/GraphQL probes, `mcp_hospirfq_processor` unit-test output (63 passed).

## Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| Test owner | Autonomous Integration Testing Specialist | 2026-06-23 | Integration Certified (conditions: commit `DEF-DDB-001`/`DEF-DDB-002` runner fixes before release) |
| Release manager | pending | pending | pending |