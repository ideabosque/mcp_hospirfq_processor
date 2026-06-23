# MCP HospiRFQ Processor

`mcp_hospirfq_processor` exposes RFQ, travel, and hospitality operations as
SilvaEngine MCP tools backed by the `rfq_engine` GraphQL API.

The package provides a processor facade and MCP configuration for a host
runtime. It is not a standalone MCP server executable.

## Capabilities

The module registers 38 tools across these areas:

- RFQ request creation, updates, item assignment, and quote generation
- Item and provider inventory lookup
- Quote updates, pricing, discounts, and installments
- Availability checks and hold lifecycle management
- Bundle and itinerary discovery
- Cancellation policy lookup
- Hospitality catalog inquiry
- RFQ file and segment-contact operations

Flights use the same tools as other hospitality products. Domain behavior is
expressed through item data such as `item_type="flight"`,
`pricing_mode="per_pax_type"`, `uom="seat"`, dated batches, and passenger
breakdowns.

## Architecture

`MCPHospiRFQProcessor` composes domain mixins over a shared
`GraphQLBackedProcessor`:

```text
MCP host
  -> MCP_CONFIGURATION
  -> MCPHospiRFQProcessor
  -> domain mixins
  -> GraphQLClient
  -> rfq_engine
```

Each mixin owns one domain concern and uses the shared GraphQL client. The
facade initializes that client once and exposes the combined tool surface.

## Installation

Python 3.11 or later is required.

```powershell
python -m pip install -e ".[dev]"
```

`silvaengine-utility` must be available from the configured package source.

## Configuration

The host creates the processor with a logger and settings dictionary, then
assigns the request-specific endpoint and partition identifiers:

```python
import logging

from mcp_hospirfq_processor import MCPHospiRFQProcessor

settings = {
    "graphql_modules": {
        "rfq_engine": {
            "class_name": "RFQEngine",
            "endpoint": "https://example.test/graphql/{endpoint_id}",
            "x_api_key": "replace-me",
        }
    },
    "sales_rep_emails": {},
}

processor = MCPHospiRFQProcessor(logging.getLogger(__name__), **settings)
processor.endpoint_id = "endpoint-id"
processor.part_id = "partition-id"
```

The GraphQL module key must be `rfq_engine`. The endpoint template may use
`{endpoint_id}`. Requests send `x-api-key` and `Part-Id` headers.

## Usage

The MCP host loads:

```python
from mcp_hospirfq_processor import MCP_CONFIGURATION, MCPHospiRFQProcessor
```

Tool arguments use snake_case. The processor converts GraphQL variables to the
backend's expected camelCase fields and converts response keys back to
snake_case.

Availability and cancellation operations require a `partition_key`. Holds
also require a provider item, service window, and quantity. A hold should be
confirmed when a booking is committed, released when abandoned, or expired by
the operational expiry process.

## Development

Run the local mocked test suite:

```powershell
python -m pytest -q
python -m compileall -q mcp_hospirfq_processor
```

The current tests mock GraphQL execution. They verify tool registration,
argument mapping, response normalization, error propagation, status
transitions, and flight/hospitality conventions. They do not validate a live
`rfq_engine` deployment, network authentication, inventory contention, or
scheduled hold expiry.

See [docs/DEVELOPMENT_PLAN.md](docs/DEVELOPMENT_PLAN.md) for implementation
status, ownership boundaries, and remaining validation work.
