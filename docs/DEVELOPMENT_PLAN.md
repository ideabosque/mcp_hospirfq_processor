# MCP HospiRFQ Processor: Architecture and Development Guide

**Version:** 0.1.0  
**Reviewed:** 2026-06-13  
**Status:** Implemented baseline; live backend validation remains  
**License:** MIT

## Purpose

`mcp_hospirfq_processor` adapts the `ai_rfq_engine` GraphQL API into tools for
a SilvaEngine MCP host. It combines generic RFQ workflows with travel and
hospitality operations such as availability holds, passenger and occupancy
pricing inputs, bundles, cancellation policies, and catalog inquiry.

The package is a library integration point. Process lifecycle, MCP transport,
credentials, endpoint selection, and partition selection belong to the host
runtime.

## Current Implementation

The implemented baseline includes:

- 38 tool schemas in `mcp_configuration.py`
- 38 matching module links
- A single `MCPHospiRFQProcessor` facade
- 11 domain mixins over `GraphQLBackedProcessor`
- Lazy GraphQL module configuration and HTTP/2 execution
- Request, quote, pricing, installment, file, and segment workflows
- Availability check, acquire, release, confirm, and expire operations
- Bundle, cancellation policy, and catalog read operations
- Status-transition helpers and structured error responses
- Mocked unit coverage for hospitality and flight conventions

The tool registry, module links, and processor methods were reconciled on
2026-06-13. All 38 configured tools had a unique matching link and a resolvable
processor method.

## Architecture

```text
SilvaEngine MCP host
  |
  +-- MCP_CONFIGURATION
  |
  +-- MCPHospiRFQProcessor
        |
        +-- RequestMixin
        +-- ItemMixin
        +-- AvailabilityMixin
        +-- QuoteMixin
        +-- PricingMixin
        +-- InstallmentMixin
        +-- BundleMixin
        +-- CancellationMixin
        +-- FileMixin
        +-- SegmentMixin
        +-- CatalogMixin
        |
        +-- GraphQLBackedProcessor
              |
              +-- GraphQLClient
                    |
                    +-- ai_rfq_engine GraphQL API
```

The flat mixin composition keeps domain methods separate while sharing logger,
settings, endpoint state, partition state, and GraphQL execution. Mixins may
call methods supplied by another mixin through the facade's method resolution
order.

## Tool Surface

| Area | Tools |
|---|---:|
| Requests and provider assignment | 8 |
| Items and provider inventory | 3 |
| Quotes | 4 |
| Pricing | 3 |
| Installments | 4 |
| Workflow helpers | 2 |
| Files | 2 |
| Segments | 1 |
| Availability | 5 |
| Bundles | 3 |
| Cancellation policies | 2 |
| Catalog | 1 |
| **Total** | **38** |

`create_installment` and `create_installments` are MCP tool names mapped to the
internal `_create_installment` and `_create_installments` methods.

## Hospitality Model

The processor does not create separate APIs for hotels, flights, restaurants,
events, transfers, or activities. These products use the shared RFQ tools and
are differentiated by backend data.

Examples:

| Concern | Representative fields |
|---|---|
| Flight | `item_type="flight"`, `uom="seat"`, dated `batch_no` |
| Passenger pricing | `pricing_mode="per_pax_type"`, `pax_breakdown` |
| Hotel pricing | `pricing_mode="occupancy"`, room-night quantity |
| Controlled inventory | `availability_mode="require_hold"` |
| Itinerary | bundle with ordered flight or hospitality components |
| Cancellation | policy tiers measured before service time |

The backend remains responsible for pricing calculations, capacity
transactions, immutable cancellation snapshots, and persistence.

## Availability Lifecycle

```text
available capacity
  -> acquire hold
  -> held
       -> confirmed
       -> released
       -> expired
```

Acquiring a hold reserves capacity. Confirming must not decrement capacity a
second time. Releasing or expiring a held reservation restores capacity.
Confirmed, released, and expired states are terminal in the local transition
model.

Operational scheduling of stale-hold expiry is outside this package. The host
or backend deployment must run the required scheduler.

## Configuration Contract

The processor receives settings from its host:

```python
settings = {
    "graphql_modules": {
        "ai_rfq_engine": {
            "class_name": "AIRFQEngine",
            "endpoint": "https://example.test/graphql/{endpoint_id}",
            "x_api_key": "replace-me",
        }
    },
    "sales_rep_emails": {},
    "default_batch_expiration_filter_days": 90,
    "installment_scheduled_day": 15,
}
```

Required runtime state:

- `endpoint_id`: assigned to the processor before GraphQL execution
- `part_id`: assigned to the processor and sent as the `Part-Id` header
- `graphql_modules.ai_rfq_engine.endpoint`: GraphQL endpoint template
- `graphql_modules.ai_rfq_engine.class_name`: schema source class
- `graphql_modules.ai_rfq_engine.x_api_key`: API credential

AWS credentials are deployment concerns only when required by the surrounding
host or backend. This package does not read AWS environment variables itself.

## Error Handling

Public operations use the shared `handle_errors` decorator. GraphQL failures
are returned as structured dictionaries with an error message, error code, and
operation details instead of escaping as raw exceptions.

Hospitality-specific codes cover missing or terminal holds, insufficient
capacity, bundle lookup failures, cancellation policy lookup failures, and
catalog inquiry failures.

## Verification

Local verification:

```powershell
python -m pytest -q
python -m compileall -q mcp_hospirfq_processor
```

Verified on 2026-06-13:

- 62 tests passed
- 38 tool schemas were unique
- 38 module links were unique
- Every tool had a matching link
- Every linked method resolved on `MCPHospiRFQProcessor`
- Python compilation completed successfully

The tests mock `_execute_graphql_query`. The following still require a deployed
test environment:

- GraphQL schema compatibility
- Endpoint and API-key authentication
- Real request, quote, pricing, and installment workflows
- Concurrent inventory hold contention
- Idempotent hold release, confirmation, and expiry against persisted data
- Scheduled stale-hold expiry
- Catalog service availability and result mapping

## Next Development Work

1. Add contract tests against a deployed `ai_rfq_engine` schema.
2. Add integration fixtures for hotel, flight, mixed itinerary, and FX cases.
3. Test concurrent hold acquisition and terminal-state idempotency.
4. Validate cancellation snapshots on persisted quote items.
5. Add host-level smoke coverage that loads `MCP_CONFIGURATION`.
6. Define release automation and package publishing checks.

## Out of Scope

- Payment capture and refunds
- PMS, CRS, or GDS synchronization
- Voucher and itinerary document delivery
- Bundle and cancellation policy authoring
- Automatic FX-rate sourcing
- Scheduler deployment for hold expiry
- A standalone MCP transport process
