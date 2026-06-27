# Continuous Integration Scenarios SOP - MCP HospiRFQ Processor

## 1. Document Control

| Field | Value |
|---|---|
| SOP title | MCP HospiRFQ Processor Live Integration SOP |
| Version | 0.2.0 |
| Owner / contact | assumed: project owner |
| Last updated | 2026-06-26 |
| Business domain | travel / hospitality RFQ |
| Target environment | local staging-equivalent gateway using `mcp_hospirfq_processor/tests/.env` |
| Approval status | approved by user on 2026-06-17 (consolidated 2026-06-26) |
| Companion SOP | `integration_scenarios_sop_http.md` (MCP HTTP transport) |
| Test script | `mcp_hospirfq_processor/tests/run_integration.py` |

## 2. Purpose and Scope

This SOP defines the ordered live integration scenarios used to validate `mcp_hospirfq_processor` against the local `silvaengine_gateway` route for `rfq_engine`, using the integration testing scripts under the project test directory and prepared flight RFQ data from `../rfq_engine`.

The runner, transport, and tool surface are identical regardless of backend. The active persistence backend is selected by gateway environment (`DB_BACKEND`), not by the runner. When `DB_BACKEND=postgresql`, the gateway uses SQLAlchemy/Alembic-backed PostgreSQL repositories; otherwise DynamoDB (default). The runner only talks to the gateway GraphQL route — it has no direct database access.

- **In scope:** MCP HospiRFQ processor facade, GraphQL client path through the gateway, catalog-first item discovery, item/provider lookup, RFQ request lifecycle, quote lifecycle, pricing, installments, files, segments, availability holds, bundles, cancellation policies, and catalog inquiry.
- **Out of scope:** production testing, destructive cleanup of generated live test records, cloud provisioning, third-party production side effects, UI testing, load testing, MCP HTTP transport testing (covered by `integration_scenarios_sop_http.md`), direct database connection from the test runner (reconciliation is API-level only), data migration between backends, backend tuning/HA configuration.
- **System(s) under test:** `mcp_hospirfq_processor`, local `silvaengine_gateway`, `rfq_engine`, and catalog/KGE-backed inquiry path reachable through `rfq_engine`.

## 2.1 Controlling End-to-End Testing Procedure

The following procedure is authoritative for this project-specific SOP:

1. Confirm the gateway is running and reachable before any test execution (environment validation gate).
2. When the backend is PostgreSQL, confirm the schema is at the latest Alembic revision (`alembic -c migration/alembic.ini upgrade head` applied) before any tool execution (migration readiness gate — dependency state `initialized`).
3. Confirm the prepared `../rfq_engine` flight fixtures have been loaded into the active backend (data initialization gate — dependency state `initialized`).
4. Execute the end-to-end live integration testing with the script `mcp_hospirfq_processor/tests/run_integration.py`, which drives the processor tools in-process through the gateway GraphQL route.
5. Use variables from `mcp_hospirfq_processor/tests/.env` to target the local integration instance. Do not hard-code credentials, endpoint IDs, partition IDs, gateway URLs, or `DATABASE_URL` values in generated reports.
6. Read and use the prepared data in `../rfq_engine` as the reference dataset and dependency source for function inputs, expected relationships, and scenario ordering.
7. Before any item/request/quote workflow is executed, perform catalog search first and use the catalog result to identify the primary item and provider item for the remainder of the test run.
8. Reconcile the catalog result to prepared data in `../rfq_engine`, especially `flight_catalog_refs.json`, so the selected catalog node maps back to known `itemUuid`, `providerItemUuid`, provider, bundle, and reference data.
9. Build the function dependency map before execution, then derive the test sequence priority from that dependency map rather than file-discovery order.
10. Perform end-to-end live integration testing in dependency order.
11. Address any implementation, runner, data-contract, repository, or scenario-ordering issues found during live execution.
12. Retest affected scenarios, then rerun the full dependency-ordered suite until all required calls pass with zero unexpected error responses.
13. Export the final per-function arguments and outputs into the project `docs/` directory as a dated results file.

## 3. Environment and Access

| Item | Value / source |
|---|---|
| Environment target | local gateway instance |
| Base URLs / endpoints | `GATEWAY_BASE_URL`, `/{endpoint_id}/rfq_graphql` from `.env` |
| Credential source | `.env` variable names only; do not write secret values into reports |
| Auth flow | `GraphQLClient` obtains JWT Bearer token from `{GATEWAY_BASE_URL}/auth/token` using `TOKEN_USERNAME` / `TOKEN_PASSWORD` (or uses `GATEWAY_TOKEN` if set) |
| Required env vars (runner) | `base_dir`, `GATEWAY_BASE_URL`, `TOKEN_USERNAME`, `TOKEN_PASSWORD`, `endpoint_id`, `part_id`, `RFQ_ENGINE_CLASS_NAME`, `RFQ_ENGINE_ENDPOINT`, `RFQ_ENGINE_X_API_KEY`, `SALES_REP_EMAILS` |
| Required env vars (gateway, PostgreSQL backend) | `DB_BACKEND=postgresql`, `DATABASE_URL` (or `PG_HOST` / `PG_PORT` / `PG_USER` / `PG_PASSWORD` / `PG_DB`), `RFQ_PG_TABLE_PREFIX` (optional, for shared-schema isolation) |
| Data stores | configured through local gateway (DynamoDB default or PostgreSQL via `DB_BACKEND`) |
| Messaging / events | none verified |
| Access constraints | local process access to gateway and package paths |
| Provisioning policy | manual approval required for new services, destructive cleanup, or any destructive schema change; `alembic upgrade head` is the only approved schema mutation and must be applied before testing |
| Migration tool | Alembic via `rfq_engine/migration/alembic.ini` (PostgreSQL backend only) |

> List **names and sources only** — never paste `DATABASE_URL` values, passwords, tokens, or connection strings into the SOP or generated reports.

## 4. Dependency Readiness Requirements

> Each dependency must reach all four readiness states before testing begins:
> `available -> configured -> initialized -> operational`.

| Dependency | Type | Health check | Required readiness | Owner |
|---|---|---|---|---|
| Python environment | infrastructure | import `MCPHospiRFQProcessor` and `run_integration` module; pytest collection | operational | project owner |
| `silvaengine_gateway` local instance | internal | `POST /auth/token` returns 200; GraphQL route call completes | operational | project owner |
| `rfq_engine` route | internal | GraphQL operations through gateway persist to and read from the active backend | operational | project owner |
| PostgreSQL instance (when `DB_BACKEND=postgresql`) | infrastructure | `DATABASE_URL` reachable; connection test succeeds | available + configured | project owner |
| PostgreSQL schema (Alembic, when applicable) | infrastructure | `alembic -c migration/alembic.ini current` returns head revision; `upgrade head` is idempotent | initialized | project owner |
| prepared flight data | test data | item, provider item, request, quote, bundle, policy IDs resolve against persisted fixtures | initialized | project owner |
| catalog / KGE path | internal dependency | `inquireCatalog` returns payload without `errorCode` | operational | project owner |

**Mandatory gate:** no test execution (Phase 8 onward) may begin until the gateway + `rfq_engine` route are `operational` against the active backend, prepared fixtures are `initialized`, and (when PostgreSQL) the Alembic schema is `initialized` (at head).

## 5. Test Data Requirements

| Asset type | Count | Notes / constraints |
|---|---|---|
| flight items | 5 prepared | sourced from `../rfq_engine` prepared data, persisted into the active backend |
| provider items / batches | at least 1 usable provider item and batch | required for quote items and availability holds |
| RFQ request | generated per run | runner creates a fresh request for mutable workflow tests |
| quote / quote item | generated per run | quote item must include `pax_breakdown` for `per_pax_type` pricing |
| installments | generated per run | setup quotes must have positive quote balance |
| catalog refs | prepared | namespace `FLIGHTS`, reconciled against `flight_catalog_refs.json` |

- **Load order:** provision backend schema (Alembic, if PostgreSQL) → load prepared catalog/flight fixtures → catalog search and item/provider selection → item/provider validation → request → provider assignment → quote → quote item → pricing → installments → file/segment reads → availability → bundle/cancellation/catalog reads.
- **Data source:** existing prepared `../rfq_engine` fixtures loaded into the active backend plus generated live request/quote/installment entities created during the run.
- **Reference requirement:** before live execution, inspect the relevant prepared data in `../rfq_engine` and verify that every function input used by the integration runner is backed by available prepared data or by a generated entity created earlier in the same run. The primary item must be selected from catalog search first and reconciled against `../rfq_engine/rfq_engine/tests/prepare_test_data/flight_catalog_refs.json`.

## 6. Execution Order

```text
catalog_discovery -> items -> requests -> quotes -> pricing -> installments -> files -> segments -> availability -> bundles -> cancellation -> catalog
```

**Reason for deviation from default:** this project is an RFQ processor facade; catalog discovery must identify the primary item before item/provider validation and request creation, request/provider assignment must precede quote creation, quote pricing must precede installment validation, and bundle/policy/catalog readbacks are reference checks. The sequence does not change with backend selection — it only changes where data is persisted.

**Sequence construction rule:** the execution order must be rebuilt or revalidated before each certification run from the actual function dependencies in the runner and codebase. Static file order is not sufficient.

## 7. Integration Scenarios

> Priority drives execution when time is limited (P1 = must pass to certify).

### Scenario INT-000 — Catalog-first primary item discovery

| Field | Value |
|---|---|
| **ID** | INT-000 |
| **Name** | Catalog-first primary item discovery |
| **Priority** | P1 |
| **Type** | API / GraphQL / data reconciliation |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Gateway running; prepared `flight_catalog_refs.json` available |
| **Dependencies** | gateway, rfq_engine, catalog/KGE path, prepared catalog refs |
| **Test data** | catalog query, namespace `FLIGHTS`, prepared catalog refs |
| **Steps** | run `inquire_catalog`; inspect payload results; map selected result to `flight_catalog_refs.json`; set primary item/provider inputs for downstream tests |
| **Expected behavior** | catalog returns payload without unexpected `errorCode`; selected result maps to prepared `itemUuid` and `providerItemUuid` persisted in the active backend |
| **Validation points** | catalog result namespace, selected node/ref, item UUID, provider item UUID |
| **Cross-system checks** | selected catalog node exists in prepared `../rfq_engine` reference data and resolves through the `rfq_engine` route |

### Scenario INT-001 — Flight item discovery

| Field | Value |
|---|---|
| **ID** | INT-001 |
| **Name** | Flight item discovery |
| **Priority** | P1 |
| **Type** | API / GraphQL |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Catalog discovery (INT-000) has selected and reconciled a primary item/provider |
| **Dependencies** | gateway, rfq_engine, INT-000 |
| **Test data** | catalog-selected prepared flight item and provider item IDs |
| **Steps** | search flight items; get one item; get provider items |
| **Expected behavior** | all calls return successful item/provider payloads read from the active backend |
| **Validation points** | item list total, item detail, provider item detail |
| **Cross-system checks** | returned partition matches `.env` endpoint/part; item/provider rows resolve against persisted fixtures |

### Scenario INT-002 — RFQ request lifecycle

| Field | Value |
|---|---|
| **ID** | INT-002 |
| **Name** | RFQ request lifecycle |
| **Priority** | P1 |
| **Type** | workflow |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Flight item exists in the active backend |
| **Dependencies** | item data, request mutations |
| **Test data** | generated RFQ request |
| **Steps** | submit request; get seeded request; search requests; update; add item; remove item; assign provider item; remove provider item; reassign provider item for quote workflow |
| **Expected behavior** | request mutations succeed and persist to the active backend; final request has provider assignment |
| **Validation points** | request UUID, status transitions, item array, provider item assignment |
| **Cross-system checks** | provider item belongs to the selected item; created request is retrievable via a subsequent read (persisted) |

### Scenario INT-003 — Quote lifecycle with per-passenger quote item

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
| **Expected behavior** | quote reaches updateable state and quote item accepts discount; quote and quote item persist to the active backend |
| **Validation points** | quote UUID, quote item UUID, final subtotal, hold token |
| **Cross-system checks** | quote item pricing uses provider item fare and pax breakdown; created quote is retrievable via a subsequent read (persisted) |

### Scenario INT-004 — Pricing and installment workflow

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
| **Expected behavior** | all pricing and installment calls succeed and persist to the active backend |
| **Validation points** | installment UUIDs, amount fields, status updates |
| **Cross-system checks** | installment totals do not exceed quote balance; created installments are retrievable via a subsequent read (persisted) |

### Scenario INT-005 — Reference and support APIs

| Field | Value |
|---|---|
| **ID** | INT-005 |
| **Name** | Reference and support APIs |
| **Priority** | P2 |
| **Type** | API / GraphQL |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Prepared flight reference data exists in the active backend |
| **Dependencies** | file, segment, bundle, cancellation, catalog resolvers |
| **Test data** | seeded request, segment, bundle, cancellation policy, catalog refs |
| **Steps** | upload file; get files; get segment contacts; search/get bundle; search bundle components; get/search cancellation policies; inquire catalog |
| **Expected behavior** | all calls return successful payloads read from the active backend; catalog payload has no `errorCode` |
| **Validation points** | file list, segment contact list, bundle components, policy, catalog results |
| **Cross-system checks** | catalog result namespace is `FLIGHTS` |

### Scenario INT-006 — Availability hold lifecycle

| Field | Value |
|---|---|
| **ID** | INT-006 |
| **Name** | Availability hold lifecycle |
| **Priority** | P1 |
| **Type** | workflow |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Provider item batch has capacity in the active backend |
| **Dependencies** | availability query/mutations |
| **Test data** | prepared provider item and batch |
| **Steps** | check availability; acquire hold; confirm hold; acquire second hold; release second hold; acquire third hold; call expire on unexpired hold |
| **Expected behavior** | check/acquire/confirm/release succeed and persist; immediate expire returns expected live no-op because TTL has not elapsed |
| **Validation points** | hold token, status/reason payloads, available quantity |
| **Cross-system checks** | capacity changes remain coherent across hold lifecycle (verified via API readback; no direct DB query per scope decision) |

> **Note:** Select the highest-capacity matching batch for hold lifecycle tests. Prior cert runs' confirmed holds may exhaust low-capacity batches, causing false failures.

## 8. Failure and Resilience Scenarios

| Scenario | Injected fault | Expected behavior |
|---|---|---|
| missing gateway | stop gateway before live execution | authentication or health validation fails clearly; no tests execute |
| invalid credentials | bad auth env values | token request fails and no tests execute |
| PostgreSQL unreachable (when `DB_BACKEND=postgresql`) | unset `DATABASE_URL` or stop the local Postgres instance | gateway GraphQL calls return a clear persistence error; runner reports blocked; no partial certification |
| schema not at head (when applicable) | skip `alembic upgrade head` | migration readiness gate fails; testing blocked at dependency state `initialized` |
| stale seeded IDs | prepared IDs missing from the active backend | affected scenario fails with GraphQL lookup error |
| missing `pax_breakdown` | omit pax data for flight quote item | GraphQL validation rejects per-pax pricing |
| premature hold expiry | expire a fresh 15-minute hold | expected no-op envelope is recorded |

## 9. Data Reconciliation Checks

> API-level only, by scope decision. The processor has no direct DB access by design; reconciliation is performed through gateway GraphQL responses and tool outputs.

| Check | Rule | Tolerance |
|---|---|---|
| Catalog selection consistency | selected catalog hit maps to `flight_catalog_refs.json` item/provider IDs persisted in the active backend | 0 mismatches |
| Generated request linkage | quote request UUID equals generated request UUID | 0 mismatches |
| Quote item linkage | quote item quote UUID equals generated quote UUID | 0 mismatches |
| Persistence readback | created request/quote/quote item/installment/hold is retrievable via a subsequent read through the gateway | 0 missing |
| Pricing consistency | final subtotal reflects subtotal discount | amount: 0.01 |
| Installment consistency | created installments fit quote balance | amount: 0.01 |
| Catalog consistency | catalog namespace equals `FLIGHTS` and payload has results | 0 missing |
| Error envelope check | no unexpected top-level `error` or in-band `error_code` | 0 unexpected |

## 10. Entry and Exit Criteria

**Entry criteria (testing may begin when):**
- This SOP is approved by the user.
- Local gateway is running and reachable.
- (When `DB_BACKEND=postgresql`) Local PostgreSQL instance is running and `DATABASE_URL` is reachable.
- (When applicable) Alembic schema is at the head revision (`alembic -c migration/alembic.ini current` == head).
- Prepared `../rfq_engine` flight data is loaded into the active backend.
- `.env` names are configured.
- Authentication succeeds.
- No destructive cleanup is required.

**Exit criteria (certification may be issued when):**
- All P1 scenarios (INT-000, INT-001, INT-002, INT-003, INT-004, INT-006) pass.
- INT-005 passes or is documented as skipped with rationale.
- No unexpected error responses remain.
- Any implementation, runner, data-contract, or repository issues found during execution have been fixed and retested.
- The final full dependency-ordered live suite has passed after the last fix, against the active backend.
- Per-call function results are exported to `docs/` as a dated results file.
- Any expected live no-op behavior is explicitly documented.
- Open environment warnings are listed as non-blocking or resolved.

## 11. CI Trigger and Cadence

| Trigger | Scope run | Required to pass |
|---|---|---|
| Manual local validation | full live suite via `run_integration.py` with gateway on active backend | yes for certification |
| Pre-release | full live suite plus report export | yes |
| Backend switch | whenever `DB_BACKEND` changes to/from `postgresql`, rerun the full suite | yes |
| Pull request | assumed: unit tests plus optional smoke subset | assumed |
| Nightly | assumed: full suite against an isolated test tenant | assumed |

## 12. Reporting and Certification Expectations

- **Report format:** Markdown.
- **Required certification decision:** `Integration Certified`, `Ready for UAT`, `Ready for Production`, `Ready with Conditions`, or `Not Ready`.
- **Distribution:** assumed: project owner / release owner.
- **Required artifact:** `docs/test_results/live_integration_results_<YYYYMMDD>.md` (dated) with per-function arguments and output, explicitly noting the active backend and `DB_BACKEND` value.
- **Backend labeling:** every report must state which backend was used via `silvaengine_gateway` and must not be conflated with a different backend certification. When `DB_BACKEND=postgresql`, note the Alembic head revision observed (or `assumed` with rationale if not directly observable).

## 13. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| Test owner | project owner | 2026-06-17 | approved for live E2E integration testing |
| Release manager | pending | pending | pending |