# Continuous Integration Scenarios SOP - MCP HospiRFQ Processor

## 1. Document Control

| Field | Value |
|---|---|
| SOP title | MCP HospiRFQ Processor Live Integration SOP |
| Version | 0.1.0 |
| Owner / contact | assumed: project owner |
| Last updated | 2026-06-17 |
| Business domain | travel / hospitality RFQ |
| Target environment | local staging-equivalent gateway using `mcp_hospirfq_processor/tests/.env` |
| Approval status | approved by user on 2026-06-17 |

## 2. Purpose and Scope

This SOP defines the ordered live integration scenarios used to validate `mcp_hospirfq_processor` against the local `silvaengine_gateway` route for `rfq_engine`, using the integration testing scripts under the project test directory and prepared flight RFQ data from `../rfq_engine`.

- **In scope:** MCP HospiRFQ processor facade, GraphQL client path, item search/detail, RFQ request lifecycle, quote lifecycle, pricing, installments, files, segments, availability holds, bundles, cancellation policies, and catalog inquiry.
- **Out of scope:** production testing, destructive cleanup of generated live test records, cloud provisioning, third-party production side effects, UI testing, load testing.
- **System(s) under test:** `mcp_hospirfq_processor`, local `silvaengine_gateway`, `rfq_engine`, and catalog/KGE-backed inquiry path reachable through `rfq_engine`.

## 2.1 Controlling End-to-End Testing Procedure

The following procedure is authoritative for this project-specific SOP:

1. Execute the end-to-end live integration testing with the testing scripts under the project test directory, currently `mcp_hospirfq_processor/tests`.
2. Use variables from `mcp_hospirfq_processor/tests/.env` to target the local integration instance. Do not hard-code credentials, endpoint IDs, partition IDs, or gateway URLs in generated reports.
3. Read and use the prepared data in `../rfq_engine` as the reference dataset and dependency source for function inputs, expected relationships, and scenario ordering.
4. Before any item/request/quote workflow is executed, perform catalog search first and use the catalog result to identify the primary item and provider item for the remainder of the test run.
5. Reconcile the catalog result to prepared data in `../rfq_engine`, especially `flight_catalog_refs.json`, so the selected catalog node maps back to known `itemUuid`, `providerItemUuid`, provider, bundle, and reference data.
6. Build the function dependency map before execution, then derive the test sequence priority from that dependency map rather than file-discovery order.
7. Perform end-to-end live integration testing in dependency order.
8. Address any implementation, runner, data-contract, or scenario-ordering issues found during live execution.
9. Retest affected scenarios, then rerun the full dependency-ordered suite until all required calls pass with zero unexpected error responses.
10. Export the final per-function arguments and outputs into the project `docs/` directory.

## 3. Environment and Access

| Item | Value / source |
|---|---|
| Environment target | local gateway instance |
| Base URLs / endpoints | `GATEWAY_BASE_URL`, `/{endpoint_id}/{part_id}/rfq_graphql` from `.env` |
| Credential source | `.env` variable names only; do not write secret values into reports |
| Required env vars | `base_dir`, `GATEWAY_BASE_URL`, `TOKEN_USERNAME`, `TOKEN_PASSWORD`, `endpoint_id`, `part_id`, `RFQ_ENGINE_CLASS_NAME`, `RFQ_ENGINE_X_API_KEY`, `SALES_REP_EMAILS` |
| Data stores | assumed: `rfq_engine` configured backing stores through local gateway |
| Messaging / events | none verified |
| Access constraints | local process access to gateway and package paths |
| Provisioning policy | manual approval required for new services or destructive cleanup |

## 4. Dependency Readiness Requirements

| Dependency | Type | Health check | Required readiness | Owner |
|---|---|---|---|---|
| Python environment | infrastructure | import and pytest collection | operational | project owner |
| `silvaengine_gateway` local instance | internal | `POST /auth/token`, GraphQL route call | operational | project owner |
| `rfq_engine` route | internal | GraphQL operations through gateway | operational | project owner |
| prepared flight data | test data | item, provider item, request, quote, bundle, policy IDs resolve | initialized | project owner |
| catalog / KGE path | internal dependency | `inquireCatalog` returns payload without `errorCode` | operational | project owner |

## 5. Test Data Requirements

| Asset type | Count | Notes / constraints |
|---|---|---|
| flight items | 5 prepared | sourced from `../rfq_engine` prepared data |
| provider items / batches | at least 1 usable provider item and batch | required for quote items and availability holds |
| RFQ request | generated per run | runner creates a fresh request for mutable workflow tests |
| quote / quote item | generated per run | quote item must include `pax_breakdown` for `per_pax_type` pricing |
| installments | generated per run | setup quotes must have positive quote balance |
| catalog refs | prepared | namespace `FLIGHTS` |

- **Load order:** prepared catalog data -> catalog search and item/provider selection -> item/provider validation -> request -> provider assignment -> quote -> quote item -> pricing -> installments -> file/segment reads -> availability -> bundle/cancellation/catalog reads.
- **Data source:** existing prepared `../rfq_engine` fixtures plus generated live request/quote/installment entities.
- **Reference requirement:** before live execution, inspect the relevant prepared data in `../rfq_engine` and verify that every function input used by the integration runner is backed by available prepared data or by a generated entity created earlier in the same run. The primary item must be selected from catalog search first and reconciled against `../rfq_engine/rfq_engine/tests/prepare_test_data/flight_catalog_refs.json`.

## 6. Execution Order

```text
catalog_discovery -> items -> requests -> quotes -> pricing -> installments -> files -> segments -> availability -> bundles -> cancellation -> catalog
```

**Reason for deviation from default:** this project is an RFQ processor facade; catalog discovery must identify the primary item before item/provider validation and request creation, request/provider assignment must precede quote creation, quote pricing must precede installment validation, and bundle/policy/catalog readbacks are reference checks.

**Sequence construction rule:** the execution order must be rebuilt or revalidated before each certification run from the actual function dependencies in the runner and codebase. Static file order is not sufficient.

## 7. Integration Scenarios

| Field | Value |
|---|---|
| **ID** | INT-000 |
| **Name** | Catalog-first primary item discovery |
| **Priority** | P1 |
| **Type** | API / GraphQL / data reconciliation |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Gateway, catalog/KGE path, and prepared `flight_catalog_refs.json` are available |
| **Dependencies** | gateway, rfq_engine, catalog/KGE path, prepared catalog refs |
| **Test data** | catalog query, namespace `FLIGHTS`, prepared catalog refs |
| **Steps** | run `inquire_catalog`; inspect payload results; map selected result to `flight_catalog_refs.json`; set primary item/provider inputs for downstream tests |
| **Expected behavior** | catalog returns payload without unexpected `errorCode`; selected result maps to prepared `itemUuid` and `providerItemUuid` |
| **Validation points** | catalog result namespace, selected node/ref, item UUID, provider item UUID |
| **Cross-system checks** | selected catalog node exists in prepared `../rfq_engine` reference data |

| Field | Value |
|---|---|
| **ID** | INT-001 |
| **Name** | Flight item discovery |
| **Priority** | P1 |
| **Type** | API / GraphQL |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Catalog discovery has selected and reconciled a primary item/provider |
| **Dependencies** | gateway, rfq_engine, INT-000 |
| **Test data** | catalog-selected prepared flight item and provider item IDs |
| **Steps** | search flight items; get one item; get provider items |
| **Expected behavior** | all calls return successful item/provider payloads |
| **Validation points** | item list total, item detail, provider item detail |
| **Cross-system checks** | returned partition matches `.env` endpoint/part |

| Field | Value |
|---|---|
| **ID** | INT-002 |
| **Name** | RFQ request lifecycle |
| **Priority** | P1 |
| **Type** | workflow |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Flight item exists |
| **Dependencies** | item data, request mutations |
| **Test data** | generated RFQ request |
| **Steps** | submit request; get seeded request; search requests; update; add item; remove item; assign provider item; remove provider item; reassign provider item for quote workflow |
| **Expected behavior** | request mutations succeed and final request has provider assignment |
| **Validation points** | request UUID, status transitions, item array, provider item assignment |
| **Cross-system checks** | provider item belongs to the selected item |

| Field | Value |
|---|---|
| **ID** | INT-003 |
| **Name** | Quote lifecycle with per-passenger quote item |
| **Priority** | P1 |
| **Type** | workflow |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Generated request has provider item and `pax_breakdown` |
| **Dependencies** | request workflow, quote mutations, price tier rules |
| **Test data** | generated request/quote/quote item |
| **Steps** | confirm request and create quote; get quote; search quotes; update quote; add/update quote item discount |
| **Expected behavior** | quote reaches updateable state and quote item accepts discount |
| **Validation points** | quote UUID, quote item UUID, final subtotal, hold token |
| **Cross-system checks** | quote item pricing uses provider item fare and pax breakdown |

| Field | Value |
|---|---|
| **ID** | INT-004 |
| **Name** | Pricing and installment workflow |
| **Priority** | P1 |
| **Type** | workflow |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Quote exists with positive balance |
| **Dependencies** | pricing, quote, installment mutations |
| **Test data** | generated setup quotes and installments |
| **Steps** | get price tiers; get discount prompts; calculate quote pricing; confirm quote and create installments; get installments; create single installment; create multiple installments; update installment paid |
| **Expected behavior** | all pricing and installment calls succeed |
| **Validation points** | installment UUIDs, amount fields, status updates |
| **Cross-system checks** | installment totals do not exceed quote balance |

| Field | Value |
|---|---|
| **ID** | INT-005 |
| **Name** | Reference and support APIs |
| **Priority** | P2 |
| **Type** | API / GraphQL |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Prepared flight reference data exists |
| **Dependencies** | file, segment, bundle, cancellation, catalog resolvers |
| **Test data** | seeded request, segment, bundle, cancellation policy, catalog refs |
| **Steps** | upload file; get files; get segment contacts; search/get bundle; search bundle components; get/search cancellation policies; inquire catalog |
| **Expected behavior** | all calls return successful payloads; catalog payload has no `errorCode` |
| **Validation points** | file list, segment contact list, bundle components, policy, catalog results |
| **Cross-system checks** | catalog result namespace is `FLIGHTS` |

| Field | Value |
|---|---|
| **ID** | INT-006 |
| **Name** | Availability hold lifecycle |
| **Priority** | P1 |
| **Type** | workflow |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Provider item batch has capacity |
| **Dependencies** | availability query/mutations |
| **Test data** | prepared provider item and batch |
| **Steps** | check availability; acquire hold; confirm hold; acquire second hold; release second hold; acquire third hold; call expire on unexpired hold |
| **Expected behavior** | check/acquire/confirm/release succeed; immediate expire returns expected live no-op because TTL has not elapsed |
| **Validation points** | hold token, status/reason payloads, available quantity |
| **Cross-system checks** | capacity changes remain coherent across hold lifecycle |

## 8. Failure and Resilience Scenarios

| Scenario | Injected fault | Expected behavior |
|---|---|---|
| missing gateway | stop before live execution | authentication or health validation fails clearly |
| invalid credentials | bad auth env values | token request fails and no tests execute |
| stale seeded IDs | prepared IDs missing | affected scenario fails with GraphQL lookup error |
| missing `pax_breakdown` | omit pax data for flight quote item | GraphQL validation rejects per-pax pricing |
| premature hold expiry | expire a fresh 15-minute hold | expected no-op envelope is recorded |

## 9. Data Reconciliation Checks

| Check | Rule | Tolerance |
|---|---|---|
| Catalog selection consistency | selected catalog hit maps to `flight_catalog_refs.json` item/provider IDs | 0 mismatches |
| Generated request linkage | quote request UUID equals generated request UUID | 0 mismatches |
| Quote item linkage | quote item quote UUID equals generated quote UUID | 0 mismatches |
| Pricing consistency | final subtotal reflects subtotal discount | amount: 0.01 |
| Installment consistency | created installments fit quote balance | amount: 0.01 |
| Catalog consistency | catalog namespace equals `FLIGHTS` and payload has results | 0 missing |
| Error envelope check | no unexpected top-level `error` or in-band `error_code` | 0 unexpected |

## 10. Entry and Exit Criteria

**Entry criteria (testing may begin when):**
- SOP is approved.
- Local gateway is running and reachable.
- `.env` names are configured.
- Prepared `../rfq_engine` flight data exists.
- Authentication succeeds.
- No destructive cleanup is required.

**Exit criteria (certification may be issued when):**
- All P1 scenarios pass.
- No unexpected error responses remain.
- Any defects or data-contract issues found during execution have been fixed and retested.
- The final full dependency-ordered live suite has passed after the last fix.
- Per-call function results are exported to `docs/`.
- Any expected live no-op behavior is explicitly documented.
- Open environment warnings are listed as non-blocking or resolved.

## 11. CI Trigger and Cadence

| Trigger | Scope run | Required to pass |
|---|---|---|
| Manual local validation | full live suite | yes for certification |
| Pre-release | full live suite plus report export | yes |
| Pull request | assumed: unit tests plus optional smoke subset | assumed |
| Nightly | assumed: full suite against isolated test tenant | assumed |

## 12. Reporting and Certification Expectations

- **Report format:** Markdown.
- **Required certification decision:** `Integration Certified`, `Ready for UAT`, `Ready for Production`, `Ready with Conditions`, or `Not Ready`.
- **Distribution:** assumed: project owner / release owner.
- **Required artifact:** `docs/live_integration_results.md` or dated equivalent with per-function arguments and output.

## 13. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| Test owner | project owner | 2026-06-17 | approved for live E2E integration testing |
| Release manager | pending | pending | pending |
