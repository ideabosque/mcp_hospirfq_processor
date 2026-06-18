# Continuous Integration Scenarios SOP - MCP HospiRFQ Processor (MCP HTTP Transport)

## 1. Document Control

| Field | Value |
|---|---|
| SOP title | MCP HospiRFQ Processor Live Integration SOP — MCP HTTP Transport (MCPHttpClient) |
| Version | 0.1.0 |
| Owner / contact | assumed: project owner |
| Last updated | 2026-06-17 |
| Business domain | travel / hospitality RFQ |
| Target environment | local staging-equivalent gateway using `mcp_hospirfq_processor/tests/.env` |
| Approval status | approved by user on 2026-06-18 |
| Companion SOP | `integration_scenarios_sop.md` (direct in-process transport) |
| Test script | `mcp_hospirfq_processor/tests/run_http_integration.py` |

## 2. Purpose and Scope

This SOP defines the ordered live integration scenarios used to validate `mcp_hospirfq_processor` through the **MCP HTTP transport layer** — the same JSON-RPC path (`initialize`, `tools/list`, `tools/call`) that a real AI agent uses to invoke tools via the gateway REST endpoint. Unlike the companion SOP (which calls `MCPHospiRFQProcessor` methods directly in-process and configures GraphQL access), this SOP exercises only the `MCPHttpClient → gateway /mcp → dispatch_mcp → MCPHospiRFQProcessor` path. No GraphQL endpoints, `GraphQLClient` configuration, or `ai_rfq_engine` imports are involved from the test script's perspective — the gateway handles backend dispatch internally.

- **In scope:** MCP JSON-RPC protocol (initialize, tools/list, tools/call), gateway MCP dispatch layer, `MCPHttpClient` async transport, SSE/JSON response parsing, Bearer token auth through `MCPHttpClient`, all 38 processor tools across 11 tool groups.
- **Out of scope:** production testing, destructive cleanup of generated live test records, cloud provisioning, third-party production side effects, UI testing, load testing, direct in-process method calls (covered by companion SOP), GraphQL endpoint configuration (handled internally by the gateway).
- **System(s) under test:** `mcp_http_client.MCPHttpClient`, `silvaengine_gateway` REST MCP route (`/{endpoint_id}/{part_id}/mcp`), `mcp_daemon_engine` dispatch, `mcp_hospirfq_processor`.
- **Transport validation:** this SOP validates that the gateway correctly dispatches JSON-RPC `tools/call` requests to the MCP daemon engine, which instantiates and invokes `MCPHospiRFQProcessor` methods, serializes results into MCP `content` arrays, and returns them over HTTP. The test script never accesses GraphQL directly.

## 2.1 Controlling End-to-End Testing Procedure

The following procedure is authoritative for this MCP HTTP transport SOP:

1. Execute the end-to-end live integration testing with the script `mcp_hospirfq_processor/tests/run_http_integration.py`, which uses `MCPHttpClient` to drive all tool calls through the gateway REST/JSON-RPC MCP endpoint.
2. Use variables from `mcp_hospirfq_processor/tests/.env` to target the local integration instance. Do not hard-code credentials, endpoint IDs, partition IDs, or gateway URLs in generated reports.
3. Read and use the prepared test data as the reference dataset and dependency source for function inputs, expected relationships, and scenario ordering.
4. Before any tool group is executed, verify that `MCPHttpClient` can successfully complete the JSON-RPC `initialize` handshake with the gateway. This confirms the MCP transport layer is operational.
5. Optionally run with `--list-tools` to verify that `tools/list` returns the expected 38 registered tools before proceeding to `tools/call` scenarios.
6. Build the function dependency map before execution, then derive the test sequence priority from that dependency map rather than file-discovery order.
7. Perform end-to-end live integration testing in dependency order via async `tools/call` invocations.
8. Address any implementation, runner, data-contract, MCP transport, or scenario-ordering issues found during live execution.
9. Retest affected scenarios, then rerun the full dependency-ordered suite until all required calls pass with zero unexpected error responses.
10. Export the final per-function arguments and outputs into the project `docs/` directory.

## 3. Environment and Access

| Item | Value / source |
|---|---|
| Environment target | local gateway instance |
| MCP REST endpoint | `MCP_REST_URL` from `.env`, default `{GATEWAY_BASE_URL}/{endpoint_id}/{part_id}/mcp` |
| Credential source | `.env` variable names only; do not write secret values into reports |
| Auth flow | `MCPHttpClient` obtains JWT Bearer token from `{GATEWAY_BASE_URL}/auth/token` using `TOKEN_USERNAME` / `TOKEN_PASSWORD` (or uses `GATEWAY_TOKEN` if set); token is sent as `Authorization: Bearer ***` header on all JSON-RPC requests |
| Required env vars | `base_dir`, `GATEWAY_BASE_URL`, `TOKEN_USERNAME`, `TOKEN_PASSWORD`, `GATEWAY_TOKEN`, `endpoint_id`, `part_id`, `MCP_REST_URL` (optional, derived by default) |
| Data stores | assumed: backing stores configured through local gateway (not accessed directly by the test script) |
| Messaging / events | none verified |
| Access constraints | local process access to gateway; `mcp_http_client` package must be importable (on `sys.path`) |
| Provisioning policy | manual approval required for new services or destructive cleanup |
| MCP client config | `base_url` = `MCP_REST_URL`, `bearer_token` = gateway JWT, `headers` = `{"Part-Id": PART_ID}` |

## 4. Dependency Readiness Requirements

| Dependency | Type | Health check | Required readiness | Owner |
|---|---|---|---|---|
| Python environment | infrastructure | import `MCPHttpClient` and `run_http_integration` module | operational | project owner |
| `mcp_http_client` package | library | importable on `sys.path` (added by script from `base_dir/mcp_http_client`) | operational | project owner |
| `silvaengine_gateway` local instance | internal | `POST /auth/token` returns JWT; `POST /mcp` JSON-RPC `initialize` returns protocol version | operational | project owner |
| MCP daemon engine configuration | internal | `tools/list` via `MCPHttpClient` returns 38 tools from `mcp_hospirfq_processor` module | loaded and operational | project owner |
| prepared flight data | test data | item, provider item, request, quote, bundle, policy IDs resolve via `tools/call` responses | initialized | project owner |
| catalog / KGE path | internal dependency | `tools/call inquire_catalog` returns payload without `errorCode` | operational | project owner |
| aiohttp | library | importable (required by `MCPHttpClient` for async HTTP) | installed | project owner |

## 5. Test Data Requirements

| Asset type | Count | Notes / constraints |
|---|---|---|
| flight items | 5 prepared | sourced from prepared flight test data fixtures |
| provider items / batches | at least 1 usable provider item and batch | required for quote items and availability holds |
| RFQ request | generated per run | runner creates a fresh request for mutable workflow tests via `submit_rfq_request` tool call |
| quote / quote item | generated per run | quote item must include `pax_breakdown` for `per_pax_type` pricing |
| installments | generated per run | setup quotes must have positive quote balance |
| catalog refs | prepared | namespace `FLIGHTS` |

- **Load order:** MCP initialize handshake → (optional) tools/list verification → items → requests → quotes → pricing → installments → files → segments → availability → bundles → cancellation → catalog.
- **Data source:** prepared flight data fixtures plus generated live request/quote/installment entities created via `tools/call` invocations.
- **Reference requirement:** before live execution, inspect the relevant prepared data fixtures and verify that every function input used by the integration runner is backed by available prepared data or by a generated entity created earlier in the same run.

> **Note:** Unlike the companion SOP, this HTTP transport SOP does not include a catalog-discovery-first gate as a mandatory first step. The `run_http_integration.py` script uses the same hardcoded sample UUIDs from prepared data. Catalog discovery can be added as a scenario extension if dynamic item selection is needed via `tools/call`.

## 6. Execution Order

```text
[initialize handshake] → items → requests → quotes → pricing → installments → files → segments → availability → bundles → cancellation → catalog
```

**Reason for ordering:** this project is an RFQ processor facade; item/provider validation must precede request creation, request/provider assignment must precede quote creation, quote pricing must precede installment validation, and bundle/policy/catalog readbacks are reference checks. The MCP `initialize` handshake is implicit — `MCPHttpClient.__aenter__` calls `initialize()` automatically before any `tools/call`.

**Sequence construction rule:** the execution order must be rebuilt or revalidated before each certification run from the actual function dependencies in the runner and codebase. Static file order is not sufficient.

## 7. Integration Scenarios

| Field | Value |
|---|---|
| **ID** | INT-MCP-000 |
| **Name** | MCP transport initialization and tool discovery |
| **Priority** | P0 |
| **Type** | MCP protocol / transport |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Gateway is running; `mcp_hospirfq_processor` is loaded into MCP daemon engine |
| **Dependencies** | gateway, mcp_daemon_engine, mcp_hospirfq_processor module |
| **Test data** | none (protocol handshake only) |
| **Steps** | run `run_http_integration.py --list-tools`; verify `initialize` JSON-RPC handshake completes; verify `tools/list` returns 38 tools; verify tool names match `mcp_configuration.py` |
| **Expected behavior** | `MCPHttpClient` enters async context, sends `initialize`, receives protocol version `2024-11-05`; `tools/list` returns all 38 registered tool names with descriptions and input schemas |
| **Validation points** | protocol version, tool count (38), tool names match configuration |
| **Cross-system checks** | gateway MCP dispatch correctly resolves `mcp_hospirfq_processor` module and class |

| Field | Value |
|---|---|
| **ID** | INT-MCP-001 |
| **Name** | Flight item discovery via tools/call |
| **Priority** | P1 |
| **Type** | MCP tools/call |
| **CI trigger** | manual / pre-release |
| **Preconditions** | MCP transport initialized (INT-MCP-000); prepared flight data exists |
| **Dependencies** | gateway, INT-MCP-000 |
| **Test data** | prepared flight item UUID, item type |
| **Steps** | `tools/call search_items` with `item_type=flight`; `tools/call get_item` with prepared `item_uuid`; `tools/call get_provider_items` with prepared `item_uuid` |
| **Expected behavior** | all three `tools/call` invocations return MCP `content` arrays with decoded JSON payloads; no JSON-RPC error envelopes |
| **Validation points** | item list total, item detail, provider item detail, MCP content parsing |
| **Cross-system checks** | returned partition matches `.env` endpoint/part |

| Field | Value |
|---|---|
| **ID** | INT-MCP-002 |
| **Name** | RFQ request lifecycle via tools/call |
| **Priority** | P1 |
| **Type** | workflow / MCP tools/call |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Flight item exists (INT-MCP-001) |
| **Dependencies** | item data, request mutations |
| **Test data** | generated RFQ request via `submit_rfq_request` tool call |
| **Steps** | `tools/call submit_rfq_request`; `tools/call get_rfq_request`; `tools/call search_rfq_requests`; `tools/call update_rfq_request`; `tools/call add_item_to_rfq_request`; `tools/call remove_item_from_rfq_request`; `tools/call assign_provider_item_to_request_item`; `tools/call remove_provider_item_from_request_item`; `tools/call assign_provider_item_to_request_item` (for quote workflow) |
| **Expected behavior** | all `tools/call` invocations return MCP content with decoded business payloads; request mutations succeed and final request has provider assignment |
| **Validation points** | request UUID, status transitions, item array, provider item assignment, MCP content text decoding |
| **Cross-system checks** | provider item belongs to the selected item |

| Field | Value |
|---|---|
| **ID** | INT-MCP-003 |
| **Name** | Quote lifecycle via tools/call |
| **Priority** | P1 |
| **Type** | workflow / MCP tools/call |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Generated request has provider item assignment (INT-MCP-002) |
| **Dependencies** | request workflow, quote mutations, price tier rules |
| **Test data** | generated request/quote/quote item |
| **Steps** | `tools/call confirm_request_and_create_quotes`; `tools/call get_quote`; `tools/call search_quotes`; `tools/call update_quote`; `tools/call update_quote_item` |
| **Expected behavior** | all `tools/call` invocations succeed; quote reaches updateable state and quote item accepts discount |
| **Validation points** | quote UUID, quote item UUID, final subtotal, MCP content payload structure |
| **Cross-system checks** | quote item pricing uses provider item fare and pax breakdown |

| Field | Value |
|---|---|
| **ID** | INT-MCP-004 |
| **Name** | Pricing and installment workflow via tools/call |
| **Priority** | P1 |
| **Type** | workflow / MCP tools/call |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Quote exists with positive balance (INT-MCP-003) |
| **Dependencies** | pricing, quote, installment mutations |
| **Test data** | generated setup quotes and installments |
| **Steps** | `tools/call get_item_price_tiers`; `tools/call get_discount_prompts`; `tools/call calculate_quote_pricing`; `tools/call confirm_quote_and_create_installments`; `tools/call get_installments`; `tools/call create_installment`; `tools/call create_installments`; `tools/call update_installment` |
| **Expected behavior** | all pricing and installment `tools/call` invocations succeed |
| **Validation points** | installment UUIDs, amount fields, status updates, MCP content decoding |
| **Cross-system checks** | installment totals do not exceed quote balance |

| Field | Value |
|---|---|
| **ID** | INT-MCP-005 |
| **Name** | Reference and support APIs via tools/call |
| **Priority** | P2 |
| **Type** | MCP tools/call |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Prepared flight reference data exists |
| **Dependencies** | file, segment, bundle, cancellation, catalog resolvers |
| **Test data** | seeded request, segment, bundle, cancellation policy, catalog refs |
| **Steps** | `tools/call upload_rfq_file`; `tools/call get_rfq_files`; `tools/call get_segment_contacts`; `tools/call search_bundles`; `tools/call get_bundle`; `tools/call search_bundle_components`; `tools/call get_cancellation_policy`; `tools/call search_cancellation_policies`; `tools/call inquire_catalog` |
| **Expected behavior** | all `tools/call` invocations return successful MCP content payloads; catalog payload has no `errorCode` |
| **Validation points** | file list, segment contact list, bundle components, policy, catalog results, MCP content text decoding |
| **Cross-system checks** | catalog result namespace is `FLIGHTS` |

| Field | Value |
|---|---|
| **ID** | INT-MCP-006 |
| **Name** | Availability hold lifecycle via tools/call |
| **Priority** | P1 |
| **Type** | workflow / MCP tools/call |
| **CI trigger** | manual / pre-release |
| **Preconditions** | Provider item batch has capacity |
| **Dependencies** | availability query/mutations |
| **Test data** | prepared provider item and batch |
| **Steps** | `tools/call check_availability`; `tools/call acquire_availability_hold`; `tools/call confirm_availability_hold`; `tools/call acquire_availability_hold` (for release); `tools/call release_availability_hold`; `tools/call acquire_availability_hold` (for expire); `tools/call expire_availability_hold` |
| **Expected behavior** | check/acquire/confirm/release succeed; immediate expire returns expected live no-op because TTL has not elapsed |
| **Validation points** | hold token extraction from MCP content, status/reason payloads, available quantity |
| **Cross-system checks** | capacity changes remain coherent across hold lifecycle |

## 8. Failure and Resilience Scenarios

| Scenario | Injected fault | Expected behavior |
|---|---|---|
| missing gateway | stop gateway before live execution | `MCPHttpClient` connection fails; `_get_gateway_token` raises `ConnectionError`; script exits with FATAL message |
| invalid credentials | bad auth env values | `/auth/token` returns 401; token request fails; no tests execute |
| MCP daemon not loaded | `mcp_hospirfq_processor` not loaded into daemon engine | `tools/list` returns 0 tools or `tools/call` returns JSON-RPC error with method-not-found |
| stale seeded IDs | prepared IDs missing | affected `tools/call` returns MCP content with in-band error envelope |
| MCP content parse failure | gateway returns non-JSON text in MCP content | `_parse_mcp_content` returns raw string; result tracking records it |
| SSE response instead of JSON | gateway returns `text/event-stream` | `MCPHttpClient._parse_sse_response` extracts JSON-RPC payload from SSE data lines |
| premature hold expiry | expire a fresh 15-minute hold | expected no-op envelope is recorded via `tools/call expire_availability_hold` |

## 9. Data Reconciliation Checks

| Check | Rule | Tolerance |
|---|---|---|
| Generated request linkage | quote request UUID equals generated request UUID | 0 mismatches |
| Quote item linkage | quote item quote UUID equals generated quote UUID | 0 mismatches |
| Pricing consistency | final subtotal reflects subtotal discount | amount: 0.01 |
| Installment consistency | created installments fit quote balance | amount: 0.01 |
| Catalog consistency | catalog namespace equals `FLIGHTS` and payload has results | 0 missing |
| Error envelope check | no unexpected top-level `error` or in-band `error_code` in MCP content | 0 unexpected |
| MCP content structure | every `tools/call` response has a `content` array with at least one `text` item | 0 missing |
| Tool count verification | `tools/list` returns exactly 38 tools matching `mcp_configuration.py` | 0 mismatches |

## 10. Entry and Exit Criteria

**Entry criteria (testing may begin when):**
- SOP is approved.
- Local gateway is running and reachable.
- `mcp_hospirfq_processor` is loaded into the MCP daemon engine (verified via `tools/list`).
- `.env` names are configured (`GATEWAY_BASE_URL`, `TOKEN_USERNAME`, `TOKEN_PASSWORD`, `endpoint_id`, `part_id`).
- Prepared flight data fixtures exist.
- Authentication succeeds (`/auth/token` returns JWT).
- `MCPHttpClient` can complete `initialize` JSON-RPC handshake.
- No destructive cleanup is required.

**Exit criteria (certification may be issued when):**
- All P0 and P1 scenarios pass.
- `tools/list` returns all 38 expected tools.
- No unexpected error responses remain.
- Any defects or data-contract issues found during execution have been fixed and retested.
- The final full dependency-ordered live suite has passed after the last fix.
- Per-call function results are exported to `docs/`.
- Any expected live no-op behavior is explicitly documented.
- Open environment warnings are listed as non-blocking or resolved.

## 11. CI Trigger and Cadence

| Trigger | Scope run | Required to pass |
|---|---|---|
| Manual local validation | full live suite via `run_http_integration.py` | yes for certification |
| Pre-release | full live suite plus report export (`--export`) | yes |
| Pull request | assumed: unit tests plus optional smoke subset (`--only items,requests`) | assumed |
| Nightly | assumed: full suite against isolated test tenant | assumed |
| MCP transport change | full live suite plus `--list-tools` verification | yes |

## 12. Reporting and Certification Expectations

- **Report format:** Markdown.
- **Report artifact:** `docs/http_integration_results.md` (default export path from `run_http_integration.py --export`).
- **Required certification decision:** `Integration Certified`, `Ready for UAT`, `Ready for Production`, `Ready with Conditions`, or `Not Ready`.
- **Distribution:** assumed: project owner / release owner.
- **Required content:** per-function tool name, MCP method (`tools/call`), arguments, decoded MCP content payload, elapsed time, pass/error/fail status.
- **Additional transport-level evidence:** `initialize` protocol version, `tools/list` tool count and names, any SSE-vs-JSON response observations.

## 13. Comparison with Companion SOP (Direct In-Process Transport)

| Aspect | Companion SOP (`integration_scenarios_sop.md`) | This SOP (`integration_scenarios_sop_http.md`) |
|---|---|---|
| Test script | `run_integration.py` | `run_http_integration.py` |
| Transport | direct in-process method calls on `MCPHospiRFQProcessor` | `MCPHttpClient` async HTTP JSON-RPC through gateway `/mcp` |
| MCP protocol exercised | no | yes (`initialize`, `tools/list`, `tools/call`) |
| Auth | `GraphQLClient.get_gateway_token()` for in-process GraphQL | `MCPHttpClient` Bearer token from `/auth/token` (no GraphQL access) |
| Catalog discovery gate | mandatory first step (INT-000) | optional (can be added as extension) |
| Report artifact | `docs/live_integration_results.md` | `docs/http_integration_results.md` |
| Execution model | synchronous | asynchronous (`asyncio`) |
| Tool groups | 12 (includes catalog_discovery) | 11 (items through catalog) |
| Additional validation | — | MCP transport layer, JSON-RPC dispatch, content parsing |

## 14. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| Test owner | project owner | pending | pending |
| Release manager | pending | pending | pending |
