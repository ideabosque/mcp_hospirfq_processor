# MCP HospiRFQ Processor HTTP Integration Results (MCPHttpClient)

- Generated at: `2026-06-18T21:11:48.000665+00:00`
- Gateway: `http://localhost:8765`
- MCP REST URL: `http://localhost:8765/gpt/mcp`
- Endpoint: `gpt`
- Partition: `nestaging`
- Transport: MCPHttpClient → JSON-RPC → gateway `/mcp`
- Dependency order: `items`
- Passed: `3`
- Error responses: `0`
- Failed: `0`
- Total calls: `3`

## Executive Summary

End-to-end HTTP integration testing was executed through the `mcp_http_client.MCPHttpClient` against the `silvaengine_gateway` REST/JSON-RPC MCP endpoint (`/{endpoint_id}/mcp`, with `Part-Id` sent as a request header). Each tool was invoked via JSON-RPC `tools/call`, exercising the full agent → gateway → `MCPHospiRFQProcessor` stack. The gateway handles all backend dispatch internally. The run completed with 3 passing function calls, 0 error responses, and 0 failures.

## Scope

- In scope: MCP JSON-RPC transport (initialize, tools/list, tools/call), gateway MCP dispatch, MCPHospiRFQProcessor tool execution. The gateway handles backend dispatch internally.
- Out of scope: production validation, destructive cleanup, load testing, UI testing.

## Function Results

### 1. items / search_items (flight type)

- Method: `search_items`
- Status: `pass`
- Elapsed: `11959.38 ms`

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
  "total": 5,
  "item_list": [
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
      "item_uuid": "15269325584579182720",
      "item_type": "flight",
      "item_name": "Flight DFW->SIN Business",
      "item_description": "Business class non-stop service from Dallas (DFW) to Singapore (SIN).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-DFW-SIN-BUS",
      "created_at": "2026-06-01T22:19:25.988874",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:25.988874"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "17735923656909930624",
      "item_type": "flight",
      "item_name": "Flight CDG->JFK Business",
      "item_description": "Business class non-stop service from Paris (CDG) to New York (JFK).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-CDG-JFK-BUS",
      "created_at": "2026-06-01T22:19:23.947293",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:23.947293"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "97838712287656951936",
      "item_type": "flight",
      "item_name": "Flight LAX->HKG Premium Economy",
      "item_description": "Premium Economy class non-stop service from Los Angeles (LAX) to Hong Kong (HKG).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-LAX-HKG-PRE",
      "created_at": "2026-06-01T22:19:31.515429",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-01T22:19:31.515429"
    }
  ]
}
```

### 2. items / get_item (Flight ATL->ORD Premium Economy)

- Method: `get_item`
- Status: `pass`
- Elapsed: `7528.42 ms`

Arguments:

```json
{
  "item_uuid": "06041993713794695296"
}
```

Output:

```json
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
}
```

### 3. items / get_provider_items (with batches)

- Method: `get_provider_items`
- Status: `pass`
- Elapsed: `7883.56 ms`

Arguments:

```json
{
  "item_uuid": "06041993713794695296"
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
      "provider_item_uuid": "39876487618607726720",
      "provider_corp_external_id": "AIRLINE-AF",
      "provider_item_external_id": "AF-ATL-ORD-PRE",
      "base_price_per_uom": 450.0,
      "item_spec": {
        "cabin_class": "Premium Economy",
        "meal_included": true,
        "destination_iata": "ORD",
        "airline_code": "AF",
        "origin_iata": "ATL",
        "airline_name": "Air France",
        "baggage_allowance_kg": "32"
      },
      "availability_mode": "require_hold",
      "item_uuid": "06041993713794695296",
      "item": {
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
      "updated_by": "prepare_flight_products",
      "created_at": "2026-06-01T22:19:30.213419",
      "updated_at": "2026-06-01T22:19:30.213419",
      "batches": []
    }
  ]
}
```
