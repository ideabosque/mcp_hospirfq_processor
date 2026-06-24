# MCP HospiRFQ Processor HTTP Integration Results (MCPHttpClient)

- Generated at: `2026-06-24T05:59:11.602582+00:00`
- Gateway: `http://localhost:8765`
- MCP REST URL: `http://localhost:8765/gpt/mcp`
- Endpoint: `gpt`
- Partition: `nestaging`
- Transport: MCPHttpClient → JSON-RPC → gateway `/mcp`
- Dependency order: `items, requests, quotes, pricing, installments, files, segments, availability, bundles, cancellation, catalog`
- Passed: `49`
- Error responses: `0`
- Failed: `0`
- Total calls: `49`

## Executive Summary

End-to-end HTTP integration testing was executed through the `mcp_http_client.MCPHttpClient` against the `silvaengine_gateway` REST/JSON-RPC MCP endpoint (`/{endpoint_id}/mcp`, with `Part-Id` sent as a request header). Each tool was invoked via JSON-RPC `tools/call`, exercising the full agent → gateway → `MCPHospiRFQProcessor` stack. The gateway handles all backend dispatch internally. The run completed with 49 passing function calls, 0 error responses, and 0 failures.

## Scope

- In scope: MCP JSON-RPC transport (initialize, tools/list, tools/call), gateway MCP dispatch, MCPHospiRFQProcessor tool execution. The gateway handles backend dispatch internally.
- Out of scope: production validation, destructive cleanup, load testing, UI testing.

## Function Results

### 1. items / search_items (flight type)

- Method: `search_items`
- Status: `pass`
- Elapsed: `4519.7 ms`

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
  "page_size": null,
  "page_number": null,
  "total": 5,
  "item_list": [
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "item_type": "flight",
      "item_name": "Flight NRT->CDG First",
      "item_description": "First class non-stop service from Tokyo (NRT) to Paris (CDG).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-NRT-CDG-FIR",
      "created_at": "2026-06-22T21:14:26.858302",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:26.858302"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1",
      "item_type": "flight",
      "item_name": "Flight CDG->ORD Economy",
      "item_description": "Economy class non-stop service from Paris (CDG) to Chicago (ORD).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-CDG-ORD-ECO",
      "created_at": "2026-06-22T21:14:26.774444",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:26.774444"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "898dad8f-2ccf-445c-a55e-5f7f96105840",
      "item_type": "flight",
      "item_name": "Flight ORD->BOS Business",
      "item_description": "Business class non-stop service from Chicago (ORD) to Boston (BOS).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-ORD-BOS-BUS",
      "created_at": "2026-06-22T21:14:26.691981",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:26.691981"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "34f8a79e-abc7-4e0e-901d-855e9b13ed1c",
      "item_type": "flight",
      "item_name": "Flight DFW->CDG Business",
      "item_description": "Business class non-stop service from Dallas (DFW) to Paris (CDG).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-DFW-CDG-BUS",
      "created_at": "2026-06-22T21:14:26.569475",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:26.569475"
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "item_uuid": "48d374c4-588d-49b9-a005-36caa41706eb",
      "item_type": "flight",
      "item_name": "Flight NRT->BOS Business",
      "item_description": "Business class non-stop service from Tokyo (NRT) to Boston (BOS).",
      "pricing_mode": "per_pax_type",
      "uom": "seat",
      "item_external_id": "FLIGHT-NRT-BOS-BUS",
      "created_at": "2026-06-22T21:14:26.463273",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:26.463273"
    }
  ]
}
```

### 2. items / get_item (Flight NRT->CDG First)

- Method: `get_item`
- Status: `pass`
- Elapsed: `4591.25 ms`

Arguments:

```json
{
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "item_type": "flight",
  "item_name": "Flight NRT->CDG First",
  "item_description": "First class non-stop service from Tokyo (NRT) to Paris (CDG).",
  "pricing_mode": "per_pax_type",
  "uom": "seat",
  "item_external_id": "FLIGHT-NRT-CDG-FIR",
  "created_at": "2026-06-22T21:14:26.858302",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-22T21:14:26.858302"
}
```

### 3. items / get_provider_items (with batches)

- Method: `get_provider_items`
- Status: `pass`
- Elapsed: `4681.43 ms`

Arguments:

```json
{
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58"
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 1,
  "provider_item_list": [
    {
      "partition_key": "gpt#nestaging",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
      "provider_corp_external_id": "AIRLINE-DL",
      "provider_item_external_id": "DL-NRT-CDG-FIR",
      "base_price_per_uom": 4500.0,
      "item_spec": {
        "cabin_class": "First",
        "origin_iata": "NRT",
        "airline_code": "DL",
        "airline_name": "Delta Air Lines",
        "meal_included": true,
        "destination_iata": "CDG",
        "baggage_allowance_kg": "32"
      },
      "availability_mode": "require_hold",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "item": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "item_type": "flight",
        "item_name": "Flight NRT->CDG First",
        "item_description": "First class non-stop service from Tokyo (NRT) to Paris (CDG).",
        "pricing_mode": "per_pax_type",
        "uom": "seat",
        "item_external_id": "FLIGHT-NRT-CDG-FIR",
        "created_at": "2026-06-22T21:14:26.858302",
        "updated_by": "prepare_flight_products",
        "updated_at": "2026-06-22T21:14:26.858302"
      },
      "updated_by": "prepare_flight_products",
      "created_at": "2026-06-22T21:14:26.867812",
      "updated_at": "2026-06-22T21:14:26.867812",
      "batches": []
    }
  ]
}
```

### 4. requests / submit_rfq_request

- Method: `submit_rfq_request`
- Status: `pass`
- Elapsed: `4591.12 ms`

Arguments:

```json
{
  "email": "zbrown@example.org",
  "request_title": "HTTP integration test: Flight NRT->CDG First",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "items": [
    {
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "item_name": "Flight NRT->CDG First",
      "qty": 2,
      "pax_breakdown": {
        "adult": 2
      }
    }
  ],
  "notes": "Created by run_http_integration.py",
  "expired_at": "2026-12-31T23:59:59Z"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "email": "zbrown@example.org",
  "request_title": "HTTP integration test: Flight NRT->CDG First",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Created by run_http_integration.py",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:53:11.333785",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:53:11.333785",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 5. requests / get_rfq_request (seeded)

- Method: `get_rfq_request`
- Status: `pass`
- Elapsed: `4527.94 ms`

Arguments:

```json
{
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
  "email": "zbrown@example.org",
  "request_title": "Business trip NRT to CDG November",
  "request_description": "Business travel for 2 attendee(s) attending offsite meetings in CDG. Prefer Business or Premium Economy to allow productive flight time.",
  "billing_address": {
    "city": "Maxwellhaven",
    "name": "Keith Chen",
    "phone": "001-314-580-8409x8991",
    "state": "LA",
    "street": "079 Karen Skyway",
    "country": "US",
    "postal_code": "50014"
  },
  "shipping_address": {
    "city": "Anaton",
    "name": "John Bradford",
    "phone": "(723)810-6891",
    "state": "AR",
    "street": "95551 Vaughn Villages Apt. 446",
    "country": "US",
    "postal_code": "83528"
  },
  "items": [
    {
      "quantity": "2",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      },
      "provider_items": [
        {
          "quantity": "2",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
        }
      ],
      "cabin_preference": "Business"
    }
  ],
  "notes": "Eye kitchen entire member music finish despite letter eight while little win.",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-08-18T21:14:31.376040",
  "created_at": "2026-06-22T21:14:31.410885",
  "updated_by": "prepare_requests",
  "updated_at": "2026-06-22T21:14:31.410885",
  "quotes": [
    {
      "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
      "quote_uuid": "9e8378fa-f6b3-4353-bf9a-af2ff6036ff8",
      "provider_corp_external_id": "AIRLINE-DL",
      "sales_rep_email": "terri16@example.com",
      "partition_key": "gpt#nestaging",
      "shipping_method": null,
      "shipping_amount": "0",
      "total_quote_amount": "9000",
      "total_quote_discount": "111",
      "final_total_quote_amount": "8889",
      "currency": "USD",
      "display_currency": null,
      "fx_rate": null,
      "fx_rate_locked_at": null,
      "rounds": "0",
      "notes": "Auto-completed: All installments paid",
      "status": "completed",
      "created_at": "2026-06-22 21:14:32.731930",
      "updated_by": "MCP",
      "updated_at": "2026-06-23 06:54:27.199452"
    }
  ],
  "files": [
    {
      "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
      "file_name": "integration_test_spec.pdf",
      "email": "zbrown@example.org",
      "partition_key": "gpt#nestaging",
      "created_at": "2026-06-23 06:48:47.795038",
      "updated_by": "MCP",
      "updated_at": "2026-06-23 21:05:05.756244"
    }
  ],
  "bundle": null
}
```

### 6. requests / search_rfq_requests

- Method: `search_rfq_requests`
- Status: `pass`
- Elapsed: `4607.13 ms`

Arguments:

```json
{
  "limit": 5,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 17,
  "request_list": [
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
      "email": "zbrown@example.org",
      "request_title": "HTTP integration test: Flight NRT->CDG First",
      "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "2",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Created by run_http_integration.py",
      "bundle_uuid": null,
      "status": "initial",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-24T05:53:11.333785",
      "updated_by": "MCP",
      "updated_at": "2026-06-24T05:53:11.333785",
      "quotes": [],
      "files": [],
      "bundle": null
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "7b8c8bd1-3531-4b05-a37c-ebb20a9e082c",
      "email": "zbrown@example.org",
      "request_title": "HTTP installment setup (create_installment): Flight NRT->CDG First",
      "request_description": "Setup request for standalone installment tool validation",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "1",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "1"
          },
          "provider_items": [
            {
              "qty": "1",
              "batch_no": "DL4822-20260918",
              "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
              "provider_corp_external_id": "AIRLINE-DL"
            }
          ]
        }
      ],
      "notes": "Created by run_http_integration.py for create_installment",
      "bundle_uuid": null,
      "status": "initial",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-24T05:52:17.613341",
      "updated_by": "MCP",
      "updated_at": "2026-06-24T05:52:26.689175",
      "quotes": [],
      "files": [],
      "bundle": null
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "c8cbcd4b-ad90-4587-982e-47a5f94a3aab",
      "email": "zbrown@example.org",
      "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
      "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "2",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "2"
          },
          "provider_items": [
            {
              "qty": "2",
              "batch_no": "DL4822-20260918",
              "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
              "provider_corp_external_id": "AIRLINE-DL"
            }
          ]
        }
      ],
      "notes": "Updated via run_http_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-24T05:49:43.889831",
      "updated_by": "MCP",
      "updated_at": "2026-06-24T05:50:49.821277",
      "quotes": [
        {
          "request_uuid": "c8cbcd4b-ad90-4587-982e-47a5f94a3aab",
          "quote_uuid": "cee43829-3ed2-4671-912d-b2cc4f5e1f53",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "25",
          "total_quote_amount": "9000",
          "total_quote_discount": "50",
          "final_total_quote_amount": "9025",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Updated via HTTP integration test",
          "status": "confirmed",
          "created_at": "2026-06-24 05:50:54.646347",
          "updated_by": "MCP",
          "updated_at": "2026-06-24 05:51:56.819458"
        }
      ],
      "files": [],
      "bundle": null
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "db006888-4239-40d5-a264-8e573532ae7f",
      "email": "zbrown@example.org",
      "request_title": "Integration test: Flight NRT->CDG First (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "2",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "2"
          },
          "provider_items": [
            {
              "qty": "2",
              "batch_no": "DL4822-20260918",
              "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
              "provider_corp_external_id": "AIRLINE-DL"
            }
          ]
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "completed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-23T21:01:57.001564",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T21:05:03.457601",
      "quotes": [
        {
          "request_uuid": "db006888-4239-40d5-a264-8e573532ae7f",
          "quote_uuid": "d7f8f8e2-2675-458f-9304-6570cf9277ba",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "25",
          "total_quote_amount": "9000",
          "total_quote_discount": "50",
          "final_total_quote_amount": "9025",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Auto-completed: All installments paid",
          "status": "completed",
          "created_at": "2026-06-23 21:02:44.992946",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 21:04:56.555979"
        },
        {
          "request_uuid": "db006888-4239-40d5-a264-8e573532ae7f",
          "quote_uuid": "13b27f53-326f-458f-817e-2a430631394c",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "300",
          "total_quote_amount": "9000",
          "total_quote_discount": "0",
          "final_total_quote_amount": "9000",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Confirmed setup quote for create_installments",
          "status": "confirmed",
          "created_at": "2026-06-23 21:04:08.040737",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 21:04:26.512393"
        },
        {
          "request_uuid": "db006888-4239-40d5-a264-8e573532ae7f",
          "quote_uuid": "69f822a8-df1b-44c2-a0bb-6305347fb22b",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "300",
          "total_quote_amount": "9000",
          "total_quote_discount": "0",
          "final_total_quote_amount": "9000",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Confirmed setup quote for create_installment",
          "status": "confirmed",
          "created_at": "2026-06-23 21:03:44.848104",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 21:04:03.514215"
        }
      ],
      "files": [],
      "bundle": null
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "c78fe37d-a0fa-4b91-ac21-ad769cf356b9",
      "email": "zbrown@example.org",
      "request_title": "Integration test: Flight NRT->CDG First (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "2",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "2"
          },
          "provider_items": [
            {
              "qty": "2",
              "batch_no": "DL4822-20260918",
              "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
              "provider_corp_external_id": "AIRLINE-DL"
            }
          ]
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "completed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-23T20:49:49.412939",
      "updated_by": "MCP",
      "updated_at": "2026-06-23T20:52:55.796692",
      "quotes": [
        {
          "request_uuid": "c78fe37d-a0fa-4b91-ac21-ad769cf356b9",
          "quote_uuid": "13c026d8-01bb-42ae-957a-57233b1892b6",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "25",
          "total_quote_amount": "9000",
          "total_quote_discount": "50",
          "final_total_quote_amount": "9025",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Auto-completed: All installments paid",
          "status": "completed",
          "created_at": "2026-06-23 20:50:37.443710",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 20:52:48.936690"
        },
        {
          "request_uuid": "c78fe37d-a0fa-4b91-ac21-ad769cf356b9",
          "quote_uuid": "372432e1-c15a-4b91-9a1b-dad334c205a6",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "300",
          "total_quote_amount": "9000",
          "total_quote_discount": "0",
          "final_total_quote_amount": "9000",
          "currency": null,
          "display_currency": null,
          "fx_rate": null,
          "fx_rate_locked_at": null,
          "rounds": "0",
          "notes": "Confirmed setup quote for create_installments",
          "status": "confirmed",
          "created_at": "2026-06-23 20:52:00.443957",
          "updated_by": "MCP",
          "updated_at": "2026-06-23 20:52:18.865008"
        },
        {
          "request_uuid": "c78fe37d-a0fa-4b91-ac21-ad769cf356b9",
          "quote_uuid": "4e0b7437-8a12-4df4-b5a4-d246e49904a8",
          "provider_corp_external_id": "AIRLINE-DL",
          "sales_rep_email": null,
          "partition_key": "gpt#nestaging",
          "shipping_method": "ticket_delivery",
          "shipping_amount": "300",
          "total_quote_amount": "9000",
          "total_quote_discount": "0",
          "final_total_quote_amount": "9000",
... (truncated)
```

### 7. requests / update_rfq_request

- Method: `update_rfq_request`
- Status: `pass`
- Elapsed: `6802.84 ms`

Arguments:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
  "notes": "Updated via run_http_integration.py"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "email": "zbrown@example.org",
  "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:53:11.333785",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:53:27.318407",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 8. requests / add_item_to_rfq_request

- Method: `add_item_to_rfq_request`
- Status: `pass`
- Elapsed: `6803.8 ms`

Arguments:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "item": {
    "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1",
    "item_name": "Flight ATL->ORD Economy",
    "qty": 1
  }
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "email": "zbrown@example.org",
  "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      }
    },
    {
      "qty": "1",
      "item_name": "Flight ATL->ORD Economy",
      "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1",
      "provider_items": []
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:53:11.333785",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:53:34.125112",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 9. requests / remove_item_from_rfq_request

- Method: `remove_item_from_rfq_request`
- Status: `pass`
- Elapsed: `6886.7 ms`

Arguments:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "email": "zbrown@example.org",
  "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:53:11.333785",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:53:41.016789",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 10. requests / assign_provider_item_to_request_item

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `9051.1 ms`

Arguments:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "provider_corp_external_id": "AIRLINE-DL",
  "qty": 2,
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "email": "zbrown@example.org",
  "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      },
      "provider_items": [
        {
          "qty": "2",
          "batch_no": "DL4822-20260918",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "provider_corp_external_id": "AIRLINE-DL"
        }
      ]
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:53:11.333785",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:53:50.056437",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 11. requests / remove_provider_item_from_request_item

- Method: `remove_provider_item_from_request_item`
- Status: `pass`
- Elapsed: `6740.23 ms`

Arguments:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "email": "zbrown@example.org",
  "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      },
      "provider_items": []
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:53:11.333785",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:53:56.797401",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 12. requests / assign_provider_item_to_request_item (for quote workflow)

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `9094.99 ms`

Arguments:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "provider_corp_external_id": "AIRLINE-DL",
  "qty": 2,
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "email": "zbrown@example.org",
  "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "2",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "2"
      },
      "provider_items": [
        {
          "qty": "2",
          "batch_no": "DL4822-20260918",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "provider_corp_external_id": "AIRLINE-DL"
        }
      ]
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:53:11.333785",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:54:05.902628",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 13. quotes / confirm_request_and_create_quotes

- Method: `confirm_request_and_create_quotes`
- Status: `pass`
- Elapsed: `25230.76 ms`

Arguments:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "provider_corp_external_ids": [
    "AIRLINE-DL"
  ],
  "segment_uuid": "323dec2b-1f03-4d42-a5ef-73ef9e17c4e6",
  "batch_no": "DL4822-20260918",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z"
}
```

Output:

```json
{
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
    "email": "zbrown@example.org",
    "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
    "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "qty": "2",
        "item_name": "Flight NRT->CDG First",
        "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "pax_breakdown": {
          "adult": "2"
        },
        "provider_items": [
          {
            "qty": "2",
            "batch_no": "DL4822-20260918",
            "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
            "provider_corp_external_id": "AIRLINE-DL"
          }
        ]
      }
    ],
    "notes": "Updated via run_http_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-24T05:53:11.333785",
    "updated_by": "MCP",
    "updated_at": "2026-06-24T05:54:14.916137",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "created_quotes": [
    {
      "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
      "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-DL",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 9000.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 9000.0,
      "currency": null,
      "display_currency": null,
      "fx_rate": null,
      "fx_rate_locked_at": null,
      "notes": null,
      "status": "in_progress",
      "expired_at": null,
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
        "email": "zbrown@example.org",
        "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
        "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "qty": "2",
            "item_name": "Flight NRT->CDG First",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "pax_breakdown": {
              "adult": "2"
            },
            "provider_items": [
              {
                "qty": "2",
                "batch_no": "DL4822-20260918",
                "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
                "provider_corp_external_id": "AIRLINE-DL"
              }
            ]
          }
        ],
        "notes": "Updated via run_http_integration.py",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-24T05:53:11.333785",
        "updated_by": "MCP",
        "updated_at": "2026-06-24T05:54:14.916137",
        "quotes": [],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
          "quote_item_uuid": "b42222c0-8688-425d-b016-6d655311db1a",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "batch_no": "DL4822-20260918",
          "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
          "partition_key": "gpt#nestaging",
          "request_data": {
            "cancellation_policy_snapshot": {
              "label": "First Fare Cancellation",
              "tiers": {
                "tiers": [
                  {
                    "refund_pct": "1",
                    "hours_before_departure_gte": "24"
                  },
                  {
                    "refund_pct": "0.5",
                    "hours_before_departure_gte": "2"
                  },
                  {
                    "refund_pct": "0",
                    "hours_before_departure_gte": "0"
                  }
                ]
              },
              "description": "Job service instead mention whatever between seek chance back.",
              "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
              "snapshotted_at": "2026-06-24 05:54:24.048687",
              "notes_template_uuid": null
            }
          },
          "price_per_uom": "4500",
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          },
          "bundle_uuid": null,
          "bundle_label": null,
          "bundle_component_uuid": null,
          "subtotal": "9000",
          "subtotal_discount": "0",
          "final_subtotal": "9000",
          "currency": null,
          "subtotal_native": "9000",
          "notes": null,
          "hold_token": null,
          "hold_expires_at": null,
          "created_at": "2026-06-24 05:54:23.979302",
          "updated_by": "MCP",
          "updated_at": "2026-06-24 05:54:23.979302"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
          "conditions": [
            "min_passengers >= 20",
            "payment_method in ['wire_transfer', 'credit_card']",
            "is_refundable == false"
          ],
          "discount_rules": [
            {
              "less_than": "10000",
              "greater_than": "0",
              "max_discount_percentage": "5"
            },
            {
              "less_than": "11000",
              "greater_than": "10000",
              "max_discount_percentage": "10"
            },
            {
              "greater_than": "11000",
              "max_discount_percentage": "15"
            }
          ],
          "priority": "6",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.888325",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.888325"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
          "conditions": [
            "season != 'peak'",
            "channel == 'direct'"
          ],
          "discount_rules": [
            {
              "less_than": "5000",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "5"
            }
          ],
          "priority": "4",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.970326",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.970326"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
          "conditions": [
            "loyalty_tier in ['gold', 'platinum']",
            "booking_lead_days >= 7"
          ],
          "discount_rules": [
            {
              "less_than": "2500",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "less_than": "12500",
              "greater_than": "2500",
              "max_discount_percentage": "7.5"
            },
            {
              "less_than": "22500",
              "greater_than": "12500",
              "max_discount_percentage": "12.5"
            },
            {
              "greater_than": "22500",
              "max_discount_percentage": "17.5"
            }
          ],
          "priority": "1",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.958795",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.958795"
        }
      ],
      "updated_by": "MCP",
      "created_at": "2026-06-24T05:54:19.404074",
      "updated_at": "2026-06-24T05:54:28.780794"
    }
  ],
  "total_quotes_created": 1,
  "total_quotes_requested": 1
}
```

### 14. quotes / get_quote

- Method: `get_quote`
- Status: `pass`
- Elapsed: `4589.26 ms`

Arguments:

```json
{
  "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84"
}
```

Output:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-DL",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": null,
  "shipping_amount": 0.0,
  "total_quote_amount": 9000.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 9000.0,
  "currency": null,
  "display_currency": null,
  "fx_rate": null,
  "fx_rate_locked_at": null,
  "notes": null,
  "status": "in_progress",
  "expired_at": null,
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
    "email": "zbrown@example.org",
    "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
    "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "qty": "2",
        "item_name": "Flight NRT->CDG First",
        "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "pax_breakdown": {
          "adult": "2"
        },
        "provider_items": [
          {
            "qty": "2",
            "batch_no": "DL4822-20260918",
            "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
            "provider_corp_external_id": "AIRLINE-DL"
          }
        ]
      }
    ],
    "notes": "Updated via run_http_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-24T05:53:11.333785",
    "updated_by": "MCP",
    "updated_at": "2026-06-24T05:54:14.916137",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
      "quote_item_uuid": "b42222c0-8688-425d-b016-6d655311db1a",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "batch_no": "DL4822-20260918",
      "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
      "partition_key": "gpt#nestaging",
      "request_data": {
        "cancellation_policy_snapshot": {
          "label": "First Fare Cancellation",
          "tiers": {
            "tiers": [
              {
                "refund_pct": "1",
                "hours_before_departure_gte": "24"
              },
              {
                "refund_pct": "0.5",
                "hours_before_departure_gte": "2"
              },
              {
                "refund_pct": "0",
                "hours_before_departure_gte": "0"
              }
            ]
          },
          "description": "Job service instead mention whatever between seek chance back.",
          "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
          "snapshotted_at": "2026-06-24 05:54:24.048687",
          "notes_template_uuid": null
        }
      },
      "price_per_uom": "4500",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      },
      "bundle_uuid": null,
      "bundle_label": null,
      "bundle_component_uuid": null,
      "subtotal": "9000",
      "subtotal_discount": "0",
      "final_subtotal": "9000",
      "currency": null,
      "subtotal_native": "9000",
      "notes": null,
      "hold_token": null,
      "hold_expires_at": null,
      "created_at": "2026-06-24 05:54:23.979302",
      "updated_by": "MCP",
      "updated_at": "2026-06-24 05:54:23.979302"
    }
  ],
  "installments": [],
  "discount_prompts": [
    {
      "partition_key": "gpt#nestaging",
      "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
      "conditions": [
        "min_passengers >= 20",
        "payment_method in ['wire_transfer', 'credit_card']",
        "is_refundable == false"
      ],
      "discount_rules": [
        {
          "less_than": "10000",
          "greater_than": "0",
          "max_discount_percentage": "5"
        },
        {
          "less_than": "11000",
          "greater_than": "10000",
          "max_discount_percentage": "10"
        },
        {
          "greater_than": "11000",
          "max_discount_percentage": "15"
        }
      ],
      "priority": "6",
      "status": "active",
      "created_at": "2026-06-22 21:14:29.888325",
      "updated_by": "prepare_discount_prompts",
      "updated_at": "2026-06-22 21:14:29.888325"
    },
    {
      "partition_key": "gpt#nestaging",
      "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
      "conditions": [
        "season != 'peak'",
        "channel == 'direct'"
      ],
      "discount_rules": [
        {
          "less_than": "5000",
          "greater_than": "0",
          "max_discount_percentage": "2.5"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "5"
        }
      ],
      "priority": "4",
      "status": "active",
      "created_at": "2026-06-22 21:14:29.970326",
      "updated_by": "prepare_discount_prompts",
      "updated_at": "2026-06-22 21:14:29.970326"
    },
    {
      "partition_key": "gpt#nestaging",
      "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
      "conditions": [
        "loyalty_tier in ['gold', 'platinum']",
        "booking_lead_days >= 7"
      ],
      "discount_rules": [
        {
          "less_than": "2500",
          "greater_than": "0",
          "max_discount_percentage": "2.5"
        },
        {
          "less_than": "12500",
          "greater_than": "2500",
          "max_discount_percentage": "7.5"
        },
        {
          "less_than": "22500",
          "greater_than": "12500",
          "max_discount_percentage": "12.5"
        },
        {
          "greater_than": "22500",
          "max_discount_percentage": "17.5"
        }
      ],
      "priority": "1",
      "status": "active",
      "created_at": "2026-06-22 21:14:29.958795",
      "updated_by": "prepare_discount_prompts",
      "updated_at": "2026-06-22 21:14:29.958795"
    }
  ],
  "updated_by": "MCP",
  "created_at": "2026-06-24T05:54:19.404074",
  "updated_at": "2026-06-24T05:54:28.780794"
}
```

### 15. quotes / search_quotes

- Method: `search_quotes`
- Status: `pass`
- Elapsed: `4600.13 ms`

Arguments:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 1,
  "quote_list": [
    {
      "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
      "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-DL",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 9000.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 9000.0,
      "currency": null,
      "display_currency": null,
      "fx_rate": null,
      "fx_rate_locked_at": null,
      "notes": null,
      "status": "in_progress",
      "expired_at": null,
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
        "email": "zbrown@example.org",
        "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
        "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "qty": "2",
            "item_name": "Flight NRT->CDG First",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "pax_breakdown": {
              "adult": "2"
            },
            "provider_items": [
              {
                "qty": "2",
                "batch_no": "DL4822-20260918",
                "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
                "provider_corp_external_id": "AIRLINE-DL"
              }
            ]
          }
        ],
        "notes": "Updated via run_http_integration.py",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-24T05:53:11.333785",
        "updated_by": "MCP",
        "updated_at": "2026-06-24T05:54:14.916137",
        "quotes": [],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
          "quote_item_uuid": "b42222c0-8688-425d-b016-6d655311db1a",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "batch_no": "DL4822-20260918",
          "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
          "partition_key": "gpt#nestaging",
          "request_data": {
            "cancellation_policy_snapshot": {
              "label": "First Fare Cancellation",
              "tiers": {
                "tiers": [
                  {
                    "refund_pct": "1",
                    "hours_before_departure_gte": "24"
                  },
                  {
                    "refund_pct": "0.5",
                    "hours_before_departure_gte": "2"
                  },
                  {
                    "refund_pct": "0",
                    "hours_before_departure_gte": "0"
                  }
                ]
              },
              "description": "Job service instead mention whatever between seek chance back.",
              "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
              "snapshotted_at": "2026-06-24 05:54:24.048687",
              "notes_template_uuid": null
            }
          },
          "price_per_uom": "4500",
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          },
          "bundle_uuid": null,
          "bundle_label": null,
          "bundle_component_uuid": null,
          "subtotal": "9000",
          "subtotal_discount": "0",
          "final_subtotal": "9000",
          "currency": null,
          "subtotal_native": "9000",
          "notes": null,
          "hold_token": null,
          "hold_expires_at": null,
          "created_at": "2026-06-24 05:54:23.979302",
          "updated_by": "MCP",
          "updated_at": "2026-06-24 05:54:23.979302"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
          "conditions": [
            "min_passengers >= 20",
            "payment_method in ['wire_transfer', 'credit_card']",
            "is_refundable == false"
          ],
          "discount_rules": [
            {
              "less_than": "10000",
              "greater_than": "0",
              "max_discount_percentage": "5"
            },
            {
              "less_than": "11000",
              "greater_than": "10000",
              "max_discount_percentage": "10"
            },
            {
              "greater_than": "11000",
              "max_discount_percentage": "15"
            }
          ],
          "priority": "6",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.888325",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.888325"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
          "conditions": [
            "season != 'peak'",
            "channel == 'direct'"
          ],
          "discount_rules": [
            {
              "less_than": "5000",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "5"
            }
          ],
          "priority": "4",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.970326",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.970326"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
          "conditions": [
            "loyalty_tier in ['gold', 'platinum']",
            "booking_lead_days >= 7"
          ],
          "discount_rules": [
            {
              "less_than": "2500",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "less_than": "12500",
              "greater_than": "2500",
              "max_discount_percentage": "7.5"
            },
            {
              "less_than": "22500",
              "greater_than": "12500",
              "max_discount_percentage": "12.5"
            },
            {
              "greater_than": "22500",
              "max_discount_percentage": "17.5"
            }
          ],
          "priority": "1",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.958795",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.958795"
        }
      ],
      "updated_by": "MCP",
      "created_at": "2026-06-24T05:54:19.404074",
      "updated_at": "2026-06-24T05:54:28.780794"
    }
  ]
}
```

### 16. quotes / update_quote

- Method: `update_quote`
- Status: `pass`
- Elapsed: `6865.24 ms`

Arguments:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
  "notes": "Updated via HTTP integration test",
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0
}
```

Output:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-DL",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0,
  "total_quote_amount": 9000.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 9000.0,
  "currency": null,
  "display_currency": null,
  "fx_rate": null,
  "fx_rate_locked_at": null,
  "notes": "Updated via HTTP integration test",
  "status": "in_progress",
  "expired_at": null,
  "request": null,
  "quote_items": [],
  "installments": [],
  "discount_prompts": [],
  "updated_by": "MCP",
  "created_at": "2026-06-24T05:54:19.404074",
  "updated_at": "2026-06-24T05:54:47.176688"
}
```

### 17. quotes / update_quote_item

- Method: `update_quote_item`
- Status: `pass`
- Elapsed: `7069.43 ms`

Arguments:

```json
{
  "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
  "quote_item_uuid": "b42222c0-8688-425d-b016-6d655311db1a",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "discount_amount": 50.0,
  "notes": "HTTP integration test discount"
}
```

Output:

```json
{
  "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
  "quote_item_uuid": "b42222c0-8688-425d-b016-6d655311db1a",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "partition_key": "gpt#nestaging",
  "batch_no": "DL4822-20260918",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "qty": 2.0,
  "pax_breakdown": {
    "adult": "2"
  },
  "bundle_uuid": null,
  "bundle_label": null,
  "bundle_component_uuid": null,
  "price_per_uom": 4500.0,
  "subtotal": 9000.0,
  "subtotal_discount": 50.0,
  "final_subtotal": 9000.0,
  "currency": null,
  "subtotal_native": 9000.0,
  "notes": "HTTP integration test discount",
  "hold_token": null,
  "hold_expires_at": null,
  "guardrail_price_per_uom": null,
  "slow_move_item": null,
  "request_data": {
    "cancellation_policy_snapshot": {
      "label": "First Fare Cancellation",
      "tiers": {
        "tiers": [
          {
            "refund_pct": "1.0",
            "hours_before_departure_gte": "24"
          },
          {
            "refund_pct": "0.5",
            "hours_before_departure_gte": "2"
          },
          {
            "refund_pct": "0.0",
            "hours_before_departure_gte": "0"
          }
        ]
      },
      "description": "Job service instead mention whatever between seek chance back.",
      "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
      "snapshotted_at": "2026-06-24 05:54:24.048687",
      "notes_template_uuid": null
    }
  },
  "quote": null,
  "item": null,
  "provider_item": null,
  "provider_item_batch": null,
  "bundle": null,
  "bundle_component": null,
  "updated_by": "MCP",
  "created_at": "2026-06-24T05:54:23.979302",
  "updated_at": "2026-06-24T05:54:54.247554"
}
```

### 18. pricing / get_item_price_tiers

- Method: `get_item_price_tiers`
- Status: `pass`
- Elapsed: `4569.31 ms`

Arguments:

```json
{
  "email": "zbrown@example.org",
  "quote_items": [
    {
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
      "qty": 2
    }
  ]
}
```

Output:

```json
{
  "item_price_tiers": []
}
```

### 19. pricing / get_discount_prompts

- Method: `get_discount_prompts`
- Status: `pass`
- Elapsed: `4850.88 ms`

Arguments:

```json
{
  "email": "zbrown@example.org",
  "quote_items": [
    {
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
    }
  ]
}
```

Output:

```json
{
  "discount_prompts": [
    {
      "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
      "conditions": [
        "min_passengers >= 20",
        "payment_method in ['wire_transfer', 'credit_card']",
        "is_refundable == false"
      ],
      "discount_rules": [
        {
          "less_than": "10000",
          "greater_than": "0",
          "max_discount_percentage": "5"
        },
        {
          "less_than": "11000",
          "greater_than": "10000",
          "max_discount_percentage": "10"
        },
        {
          "greater_than": "11000",
          "max_discount_percentage": "15"
        }
      ],
      "priority": 6,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
      "conditions": [
        "season != 'peak'",
        "channel == 'direct'"
      ],
      "discount_rules": [
        {
          "less_than": "5000",
          "greater_than": "0",
          "max_discount_percentage": "2.5"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "5"
        }
      ],
      "priority": 4,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
      "conditions": [
        "loyalty_tier in ['gold', 'platinum']",
        "booking_lead_days >= 7"
      ],
      "discount_rules": [
        {
          "less_than": "2500",
          "greater_than": "0",
          "max_discount_percentage": "2.5"
        },
        {
          "less_than": "12500",
          "greater_than": "2500",
          "max_discount_percentage": "7.5"
        },
        {
          "less_than": "22500",
          "greater_than": "12500",
          "max_discount_percentage": "12.5"
        },
        {
          "greater_than": "22500",
          "max_discount_percentage": "17.5"
        }
      ],
      "priority": 1,
      "status": "active"
    }
  ]
}
```

### 20. pricing / calculate_quote_pricing

- Method: `calculate_quote_pricing`
- Status: `pass`
- Elapsed: `7329.97 ms`

Arguments:

```json
{
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
  "email": "zbrown@example.org"
}
```

Output:

```json
{
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
  "groups": []
}
```

### 21. installments / confirm_quote_and_create_installments

- Method: `confirm_quote_and_create_installments`
- Status: `pass`
- Elapsed: `22331.64 ms`

Arguments:

```json
{
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
  "create_single_installment": true,
  "payment_method": "bank_transfer"
}
```

Output:

```json
{
  "quote": {
    "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
    "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-DL",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 9000.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 9025.0,
    "currency": null,
    "display_currency": null,
    "fx_rate": null,
    "fx_rate_locked_at": null,
    "notes": "Updated via HTTP integration test",
    "status": "confirmed",
    "expired_at": null,
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
      "email": "zbrown@example.org",
      "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
      "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "qty": "2",
          "item_name": "Flight NRT->CDG First",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "pax_breakdown": {
            "adult": "2"
          },
          "provider_items": [
            {
              "qty": "2",
              "batch_no": "DL4822-20260918",
              "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
              "provider_corp_external_id": "AIRLINE-DL"
            }
          ]
        }
      ],
      "notes": "Updated via run_http_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-24T05:53:11.333785",
      "updated_by": "MCP",
      "updated_at": "2026-06-24T05:54:14.916137",
      "quotes": [],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
        "quote_item_uuid": "b42222c0-8688-425d-b016-6d655311db1a",
        "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
        "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "batch_no": "DL4822-20260918",
        "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
        "partition_key": "gpt#nestaging",
        "request_data": {
          "cancellation_policy_snapshot": {
            "label": "First Fare Cancellation",
            "tiers": {
              "tiers": [
                {
                  "refund_pct": "1",
                  "hours_before_departure_gte": "24"
                },
                {
                  "refund_pct": "0.5",
                  "hours_before_departure_gte": "2"
                },
                {
                  "refund_pct": "0",
                  "hours_before_departure_gte": "0"
                }
              ]
            },
            "description": "Job service instead mention whatever between seek chance back.",
            "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
            "snapshotted_at": "2026-06-24 05:54:24.048687",
            "notes_template_uuid": null
          }
        },
        "price_per_uom": "4500",
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        },
        "bundle_uuid": null,
        "bundle_label": null,
        "bundle_component_uuid": null,
        "subtotal": "9000",
        "subtotal_discount": "50",
        "final_subtotal": "9000",
        "currency": null,
        "subtotal_native": "9000",
        "notes": "HTTP integration test discount",
        "hold_token": null,
        "hold_expires_at": null,
        "created_at": "2026-06-24 05:54:23.979302",
        "updated_by": "MCP",
        "updated_at": "2026-06-24 05:54:54.247554"
      }
    ],
    "installments": [
      {
        "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
        "installment_uuid": "21270387-bffc-4d6e-afda-6684c9896aa0",
        "partition_key": "gpt#nestaging",
        "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
        "priority": "0",
        "salesorder_no": null,
        "payment_method": "bank_transfer",
        "scheduled_date": "2026-06-24 05:55:28",
        "installment_ratio": "100",
        "installment_amount": "9025",
        "status": "pending",
        "created_at": "2026-06-24 05:55:30.772561",
        "updated_by": "MCP",
        "updated_at": "2026-06-24 05:55:30.772561"
      }
    ],
    "discount_prompts": [
      {
        "partition_key": "gpt#nestaging",
        "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
        "scope": "global",
        "tags": [],
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
        "conditions": [
          "min_passengers >= 20",
          "payment_method in ['wire_transfer', 'credit_card']",
          "is_refundable == false"
        ],
        "discount_rules": [
          {
            "less_than": "10000",
            "greater_than": "0",
            "max_discount_percentage": "5"
          },
          {
            "less_than": "11000",
            "greater_than": "10000",
            "max_discount_percentage": "10"
          },
          {
            "greater_than": "11000",
            "max_discount_percentage": "15"
          }
        ],
        "priority": "6",
        "status": "active",
        "created_at": "2026-06-22 21:14:29.888325",
        "updated_by": "prepare_discount_prompts",
        "updated_at": "2026-06-22 21:14:29.888325"
      },
      {
        "partition_key": "gpt#nestaging",
        "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
        "scope": "global",
        "tags": [],
        "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
        "conditions": [
          "season != 'peak'",
          "channel == 'direct'"
        ],
        "discount_rules": [
          {
            "less_than": "5000",
            "greater_than": "0",
            "max_discount_percentage": "2.5"
          },
          {
            "greater_than": "5000",
            "max_discount_percentage": "5"
          }
        ],
        "priority": "4",
        "status": "active",
        "created_at": "2026-06-22 21:14:29.970326",
        "updated_by": "prepare_discount_prompts",
        "updated_at": "2026-06-22 21:14:29.970326"
      },
      {
        "partition_key": "gpt#nestaging",
        "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
        "scope": "global",
        "tags": [],
        "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
        "conditions": [
          "loyalty_tier in ['gold', 'platinum']",
          "booking_lead_days >= 7"
        ],
        "discount_rules": [
          {
            "less_than": "2500",
            "greater_than": "0",
            "max_discount_percentage": "2.5"
          },
          {
            "less_than": "12500",
            "greater_than": "2500",
            "max_discount_percentage": "7.5"
          },
          {
            "less_than": "22500",
            "greater_than": "12500",
            "max_discount_percentage": "12.5"
          },
          {
            "greater_than": "22500",
            "max_discount_percentage": "17.5"
          }
        ],
        "priority": "1",
        "status": "active",
        "created_at": "2026-06-22 21:14:29.958795",
        "updated_by": "prepare_discount_prompts",
        "updated_at": "2026-06-22 21:14:29.958795"
      }
    ],
    "updated_by": "MCP",
    "created_at": "2026-06-24T05:54:19.404074",
    "updated_at": "2026-06-24T05:55:21.015301"
  },
  "installments": [
    {
      "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
      "installment_uuid": "21270387-bffc-4d6e-afda-6684c9896aa0",
      "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 9025.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-24T05:55:28",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-24T05:55:30.772561",
      "updated_at": "2026-06-24T05:55:30.772561",
      "quote": null
    }
  ],
  "total_installments_created": 1,
  "installment_amount_per": 9025.0,
  "total_installment_amount": 9025.0,
  "installment_type": "single"
}
```

### 22. installments / get_installments

- Method: `get_installments`
- Status: `pass`
- Elapsed: `4988.09 ms`

Arguments:

```json
{
  "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 1,
  "installment_list": [
    {
      "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
      "installment_uuid": "21270387-bffc-4d6e-afda-6684c9896aa0",
      "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 9025.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-24T05:55:28",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-24T05:55:30.772561",
      "updated_at": "2026-06-24T05:55:30.772561",
      "quote": {
        "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
        "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_id": "AIRLINE-DL",
        "sales_rep_email": null,
        "rounds": 0,
        "shipping_method": "ticket_delivery",
        "shipping_amount": 25.0,
        "total_quote_amount": 9000.0,
        "total_quote_discount": 50.0,
        "final_total_quote_amount": 9025.0,
        "currency": null,
        "display_currency": null,
        "fx_rate": null,
        "fx_rate_locked_at": null,
        "notes": "Updated via HTTP integration test",
        "status": "confirmed",
        "expired_at": null,
        "request": {
          "partition_key": "gpt#nestaging",
          "endpoint_id": "gpt",
          "part_id": "nestaging",
          "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
          "email": "zbrown@example.org",
          "request_title": "HTTP integration test: Flight NRT->CDG First (updated)",
          "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
          "billing_address": null,
          "shipping_address": null,
          "items": [
            {
              "qty": "2",
              "item_name": "Flight NRT->CDG First",
              "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
              "pax_breakdown": {
                "adult": "2"
              },
              "provider_items": [
                {
                  "qty": "2",
                  "batch_no": "DL4822-20260918",
                  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
                  "provider_corp_external_id": "AIRLINE-DL"
                }
              ]
            }
          ],
          "notes": "Updated via run_http_integration.py",
          "bundle_uuid": null,
          "status": "confirmed",
          "expired_at": "2026-12-31T23:59:59",
          "created_at": "2026-06-24T05:53:11.333785",
          "updated_by": "MCP",
          "updated_at": "2026-06-24T05:54:14.916137",
          "quotes": [],
          "files": [],
          "bundle": null
        },
        "quote_items": [
          {
            "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
            "quote_item_uuid": "b42222c0-8688-425d-b016-6d655311db1a",
            "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "batch_no": "DL4822-20260918",
            "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
            "partition_key": "gpt#nestaging",
            "request_data": {
              "cancellation_policy_snapshot": {
                "label": "First Fare Cancellation",
                "tiers": {
                  "tiers": [
                    {
                      "refund_pct": "1",
                      "hours_before_departure_gte": "24"
                    },
                    {
                      "refund_pct": "0.5",
                      "hours_before_departure_gte": "2"
                    },
                    {
                      "refund_pct": "0",
                      "hours_before_departure_gte": "0"
                    }
                  ]
                },
                "description": "Job service instead mention whatever between seek chance back.",
                "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
                "snapshotted_at": "2026-06-24 05:54:24.048687",
                "notes_template_uuid": null
              }
            },
            "price_per_uom": "4500",
            "qty": "2",
            "pax_breakdown": {
              "adult": "2"
            },
            "bundle_uuid": null,
            "bundle_label": null,
            "bundle_component_uuid": null,
            "subtotal": "9000",
            "subtotal_discount": "50",
            "final_subtotal": "9000",
            "currency": null,
            "subtotal_native": "9000",
            "notes": "HTTP integration test discount",
            "hold_token": null,
            "hold_expires_at": null,
            "created_at": "2026-06-24 05:54:23.979302",
            "updated_by": "MCP",
            "updated_at": "2026-06-24 05:54:54.247554"
          }
        ],
        "installments": [
          {
            "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
            "installment_uuid": "21270387-bffc-4d6e-afda-6684c9896aa0",
            "partition_key": "gpt#nestaging",
            "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
            "priority": "0",
            "salesorder_no": null,
            "payment_method": "bank_transfer",
            "scheduled_date": "2026-06-24 05:55:28",
            "installment_ratio": "100",
            "installment_amount": "9025",
            "status": "pending",
            "created_at": "2026-06-24 05:55:30.772561",
            "updated_by": "MCP",
            "updated_at": "2026-06-24 05:55:30.772561"
          }
        ],
        "discount_prompts": [
          {
            "partition_key": "gpt#nestaging",
            "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
            "scope": "global",
            "tags": [],
            "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
            "conditions": [
              "min_passengers >= 20",
              "payment_method in ['wire_transfer', 'credit_card']",
              "is_refundable == false"
            ],
            "discount_rules": [
              {
                "less_than": "10000",
                "greater_than": "0",
                "max_discount_percentage": "5"
              },
              {
                "less_than": "11000",
                "greater_than": "10000",
                "max_discount_percentage": "10"
              },
              {
                "greater_than": "11000",
                "max_discount_percentage": "15"
              }
            ],
            "priority": "6",
            "status": "active",
            "created_at": "2026-06-22 21:14:29.888325",
            "updated_by": "prepare_discount_prompts",
            "updated_at": "2026-06-22 21:14:29.888325"
          },
          {
            "partition_key": "gpt#nestaging",
            "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
            "scope": "global",
            "tags": [],
            "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
            "conditions": [
              "season != 'peak'",
              "channel == 'direct'"
            ],
            "discount_rules": [
              {
                "less_than": "5000",
                "greater_than": "0",
                "max_discount_percentage": "2.5"
              },
              {
                "greater_than": "5000",
                "max_discount_percentage": "5"
              }
            ],
            "priority": "4",
            "status": "active",
            "created_at": "2026-06-22 21:14:29.970326",
            "updated_by": "prepare_discount_prompts",
            "updated_at": "2026-06-22 21:14:29.970326"
          },
          {
            "partition_key": "gpt#nestaging",
            "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
            "scope": "global",
            "tags": [],
            "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
            "conditions": [
              "loyalty_tier in ['gold', 'platinum']",
              "booking_lead_days >= 7"
            ],
            "discount_rules": [
              {
                "less_than": "2500",
                "greater_than": "0",
                "max_discount_percentage": "2.5"
              },
              {
                "less_than": "12500",
                "greater_than": "2500",
                "max_discount_percentage": "7.5"
              },
              {
                "less_than": "22500",
                "greater_than": "12500",
                "max_discount_percentage": "12.5"
              },
              {
                "greater_than": "22500",
                "max_discount_percentage": "17.5"
              }
            ],
            "priority": "1",
            "status": "active",
            "created_at": "2026-06-22 21:14:29.958795",
            "updated_by": "prepare_discount_prompts",
            "updated_at": "2026-06-22 21:14:29.958795"
          }
        ],
        "updated_by": "MCP",
        "created_at": "2026-06-24T05:54:19.404074",
        "updated_at": "2026-06-24T05:55:21.015301"
      }
    }
  ]
}
```

### 23. installments / setup submit_rfq_request (create_installment)

- Method: `submit_rfq_request`
- Status: `pass`
- Elapsed: `4589.84 ms`

Arguments:

```json
{
  "email": "zbrown@example.org",
  "request_title": "HTTP installment setup (create_installment): Flight NRT->CDG First",
  "request_description": "Setup request for standalone installment tool validation",
  "items": [
    {
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "item_name": "Flight NRT->CDG First",
      "qty": 1,
      "pax_breakdown": {
        "adult": 1
      }
    }
  ],
  "notes": "Created by run_http_integration.py for create_installment",
  "expired_at": "2026-12-31T23:59:59Z"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
  "email": "zbrown@example.org",
  "request_title": "HTTP installment setup (create_installment): Flight NRT->CDG First",
  "request_description": "Setup request for standalone installment tool validation",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "1",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "1"
      }
    }
  ],
  "notes": "Created by run_http_integration.py for create_installment",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:55:42.840137",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:55:42.840137",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 24. installments / setup assign_provider_item_to_request_item (create_installment)

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `9180.02 ms`

Arguments:

```json
{
  "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "provider_corp_external_id": "AIRLINE-DL",
  "qty": 1,
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
  "email": "zbrown@example.org",
  "request_title": "HTTP installment setup (create_installment): Flight NRT->CDG First",
  "request_description": "Setup request for standalone installment tool validation",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "1",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "1"
      },
      "provider_items": [
        {
          "qty": "1",
          "batch_no": "DL4822-20260918",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "provider_corp_external_id": "AIRLINE-DL"
        }
      ]
    }
  ],
  "notes": "Created by run_http_integration.py for create_installment",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:55:42.840137",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:55:52.098075",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 25. installments / setup confirm_request_and_create_quotes (create_installment)

- Method: `confirm_request_and_create_quotes`
- Status: `pass`
- Elapsed: `25084.14 ms`

Arguments:

```json
{
  "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
  "provider_corp_external_ids": [
    "AIRLINE-DL"
  ],
  "segment_uuid": "323dec2b-1f03-4d42-a5ef-73ef9e17c4e6",
  "batch_no": "DL4822-20260918",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z"
}
```

Output:

```json
{
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
    "email": "zbrown@example.org",
    "request_title": "HTTP installment setup (create_installment): Flight NRT->CDG First",
    "request_description": "Setup request for standalone installment tool validation",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "qty": "1",
        "item_name": "Flight NRT->CDG First",
        "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "pax_breakdown": {
          "adult": "1"
        },
        "provider_items": [
          {
            "qty": "1",
            "batch_no": "DL4822-20260918",
            "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
            "provider_corp_external_id": "AIRLINE-DL"
          }
        ]
      }
    ],
    "notes": "Created by run_http_integration.py for create_installment",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-24T05:55:42.840137",
    "updated_by": "MCP",
    "updated_at": "2026-06-24T05:56:01.078056",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "created_quotes": [
    {
      "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
      "quote_uuid": "fa0f532d-831a-4cca-8be8-22b8d182ad21",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-DL",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 4500.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 4500.0,
      "currency": null,
      "display_currency": null,
      "fx_rate": null,
      "fx_rate_locked_at": null,
      "notes": null,
      "status": "in_progress",
      "expired_at": null,
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
        "email": "zbrown@example.org",
        "request_title": "HTTP installment setup (create_installment): Flight NRT->CDG First",
        "request_description": "Setup request for standalone installment tool validation",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "qty": "1",
            "item_name": "Flight NRT->CDG First",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "pax_breakdown": {
              "adult": "1"
            },
            "provider_items": [
              {
                "qty": "1",
                "batch_no": "DL4822-20260918",
                "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
                "provider_corp_external_id": "AIRLINE-DL"
              }
            ]
          }
        ],
        "notes": "Created by run_http_integration.py for create_installment",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-24T05:55:42.840137",
        "updated_by": "MCP",
        "updated_at": "2026-06-24T05:56:01.078056",
        "quotes": [],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "quote_uuid": "fa0f532d-831a-4cca-8be8-22b8d182ad21",
          "quote_item_uuid": "db5f2901-de34-4351-aec3-e306e7f1e320",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "batch_no": "DL4822-20260918",
          "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
          "partition_key": "gpt#nestaging",
          "request_data": {
            "cancellation_policy_snapshot": {
              "label": "First Fare Cancellation",
              "tiers": {
                "tiers": [
                  {
                    "refund_pct": "1",
                    "hours_before_departure_gte": "24"
                  },
                  {
                    "refund_pct": "0.5",
                    "hours_before_departure_gte": "2"
                  },
                  {
                    "refund_pct": "0",
                    "hours_before_departure_gte": "0"
                  }
                ]
              },
              "description": "Job service instead mention whatever between seek chance back.",
              "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
              "snapshotted_at": "2026-06-24 05:56:10.161616",
              "notes_template_uuid": null
            }
          },
          "price_per_uom": "4500",
          "qty": "1",
          "pax_breakdown": {
            "adult": "1"
          },
          "bundle_uuid": null,
          "bundle_label": null,
          "bundle_component_uuid": null,
          "subtotal": "4500",
          "subtotal_discount": "0",
          "final_subtotal": "4500",
          "currency": null,
          "subtotal_native": "4500",
          "notes": null,
          "hold_token": null,
          "hold_expires_at": null,
          "created_at": "2026-06-24 05:56:10.093446",
          "updated_by": "MCP",
          "updated_at": "2026-06-24 05:56:10.093446"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
          "conditions": [
            "min_passengers >= 20",
            "payment_method in ['wire_transfer', 'credit_card']",
            "is_refundable == false"
          ],
          "discount_rules": [
            {
              "less_than": "10000",
              "greater_than": "0",
              "max_discount_percentage": "5"
            },
            {
              "less_than": "11000",
              "greater_than": "10000",
              "max_discount_percentage": "10"
            },
            {
              "greater_than": "11000",
              "max_discount_percentage": "15"
            }
          ],
          "priority": "6",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.888325",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.888325"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
          "conditions": [
            "season != 'peak'",
            "channel == 'direct'"
          ],
          "discount_rules": [
            {
              "less_than": "5000",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "5"
            }
          ],
          "priority": "4",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.970326",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.970326"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
          "conditions": [
            "loyalty_tier in ['gold', 'platinum']",
            "booking_lead_days >= 7"
          ],
          "discount_rules": [
            {
              "less_than": "2500",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "less_than": "12500",
              "greater_than": "2500",
              "max_discount_percentage": "7.5"
            },
            {
              "less_than": "22500",
              "greater_than": "12500",
              "max_discount_percentage": "12.5"
            },
            {
              "greater_than": "22500",
              "max_discount_percentage": "17.5"
            }
          ],
          "priority": "1",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.958795",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.958795"
        }
      ],
      "updated_by": "MCP",
      "created_at": "2026-06-24T05:56:05.587688",
      "updated_at": "2026-06-24T05:56:14.840268"
    }
  ],
  "total_quotes_created": 1,
  "total_quotes_requested": 1
}
```

### 26. installments / setup update_quote confirmed (create_installment)

- Method: `update_quote`
- Status: `pass`
- Elapsed: `6863.99 ms`

Arguments:

```json
{
  "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
  "quote_uuid": "fa0f532d-831a-4cca-8be8-22b8d182ad21",
  "status": "confirmed",
  "notes": "Confirmed setup quote for create_installment"
}
```

Output:

```json
{
  "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
  "quote_uuid": "fa0f532d-831a-4cca-8be8-22b8d182ad21",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-DL",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": null,
  "shipping_amount": 0.0,
  "total_quote_amount": 4500.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 4500.0,
  "currency": null,
  "display_currency": null,
  "fx_rate": null,
  "fx_rate_locked_at": null,
  "notes": "Confirmed setup quote for create_installment",
  "status": "confirmed",
  "expired_at": null,
  "request": null,
  "quote_items": [],
  "installments": [],
  "discount_prompts": [],
  "updated_by": "MCP",
  "created_at": "2026-06-24T05:56:05.587688",
  "updated_at": "2026-06-24T05:56:24.038365"
}
```

### 27. installments / create_installment

- Method: `create_installment`
- Status: `pass`
- Elapsed: `9210.39 ms`

Arguments:

```json
{
  "quote_uuid": "fa0f532d-831a-4cca-8be8-22b8d182ad21",
  "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
  "installment_amount": 100.0,
  "payment_method": "credit_card"
}
```

Output:

```json
{
  "quote_uuid": "fa0f532d-831a-4cca-8be8-22b8d182ad21",
  "installment_uuid": "94f1777f-9f53-4fef-af43-5489dbba934a",
  "request_uuid": "9c3062a6-44e6-4caf-993e-f435805bce44",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 100.0,
  "installment_ratio": 2.2222222222222223,
  "salesorder_no": null,
  "scheduled_date": "2026-06-24T05:56:30",
  "payment_method": "credit_card",
  "status": "pending",
  "updated_by": "MCP",
  "created_at": "2026-06-24T05:56:33.079170",
  "updated_at": "2026-06-24T05:56:33.079170",
  "quote": null
}
```

### 28. installments / setup submit_rfq_request (create_installments)

- Method: `submit_rfq_request`
- Status: `pass`
- Elapsed: `4546.73 ms`

Arguments:

```json
{
  "email": "zbrown@example.org",
  "request_title": "HTTP installment setup (create_installments): Flight NRT->CDG First",
  "request_description": "Setup request for standalone installment tool validation",
  "items": [
    {
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "item_name": "Flight NRT->CDG First",
      "qty": 1,
      "pax_breakdown": {
        "adult": 1
      }
    }
  ],
  "notes": "Created by run_http_integration.py for create_installments",
  "expired_at": "2026-12-31T23:59:59Z"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
  "email": "zbrown@example.org",
  "request_title": "HTTP installment setup (create_installments): Flight NRT->CDG First",
  "request_description": "Setup request for standalone installment tool validation",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "1",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "1"
      }
    }
  ],
  "notes": "Created by run_http_integration.py for create_installments",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:56:37.765199",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:56:37.765199",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 29. installments / setup assign_provider_item_to_request_item (create_installments)

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `9061.65 ms`

Arguments:

```json
{
  "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
  "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "provider_corp_external_id": "AIRLINE-DL",
  "qty": 1,
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
  "email": "zbrown@example.org",
  "request_title": "HTTP installment setup (create_installments): Flight NRT->CDG First",
  "request_description": "Setup request for standalone installment tool validation",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "qty": "1",
      "item_name": "Flight NRT->CDG First",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "pax_breakdown": {
        "adult": "1"
      },
      "provider_items": [
        {
          "qty": "1",
          "batch_no": "DL4822-20260918",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "provider_corp_external_id": "AIRLINE-DL"
        }
      ]
    }
  ],
  "notes": "Created by run_http_integration.py for create_installments",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-24T05:56:37.765199",
  "updated_by": "MCP",
  "updated_at": "2026-06-24T05:56:46.860312",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 30. installments / setup confirm_request_and_create_quotes (create_installments)

- Method: `confirm_request_and_create_quotes`
- Status: `pass`
- Elapsed: `25382.8 ms`

Arguments:

```json
{
  "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
  "provider_corp_external_ids": [
    "AIRLINE-DL"
  ],
  "segment_uuid": "323dec2b-1f03-4d42-a5ef-73ef9e17c4e6",
  "batch_no": "DL4822-20260918",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z"
}
```

Output:

```json
{
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
    "email": "zbrown@example.org",
    "request_title": "HTTP installment setup (create_installments): Flight NRT->CDG First",
    "request_description": "Setup request for standalone installment tool validation",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "qty": "1",
        "item_name": "Flight NRT->CDG First",
        "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
        "pax_breakdown": {
          "adult": "1"
        },
        "provider_items": [
          {
            "qty": "1",
            "batch_no": "DL4822-20260918",
            "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
            "provider_corp_external_id": "AIRLINE-DL"
          }
        ]
      }
    ],
    "notes": "Created by run_http_integration.py for create_installments",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-24T05:56:37.765199",
    "updated_by": "MCP",
    "updated_at": "2026-06-24T05:56:55.978650",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "created_quotes": [
    {
      "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
      "quote_uuid": "c1b3fd73-a2bc-466a-bf5e-ab48577d1b99",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-DL",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 4500.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 4500.0,
      "currency": null,
      "display_currency": null,
      "fx_rate": null,
      "fx_rate_locked_at": null,
      "notes": null,
      "status": "in_progress",
      "expired_at": null,
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
        "email": "zbrown@example.org",
        "request_title": "HTTP installment setup (create_installments): Flight NRT->CDG First",
        "request_description": "Setup request for standalone installment tool validation",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "qty": "1",
            "item_name": "Flight NRT->CDG First",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "pax_breakdown": {
              "adult": "1"
            },
            "provider_items": [
              {
                "qty": "1",
                "batch_no": "DL4822-20260918",
                "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
                "provider_corp_external_id": "AIRLINE-DL"
              }
            ]
          }
        ],
        "notes": "Created by run_http_integration.py for create_installments",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-24T05:56:37.765199",
        "updated_by": "MCP",
        "updated_at": "2026-06-24T05:56:55.978650",
        "quotes": [],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "quote_uuid": "c1b3fd73-a2bc-466a-bf5e-ab48577d1b99",
          "quote_item_uuid": "4ab26aca-2348-45a8-8570-f31685734bab",
          "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
          "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
          "batch_no": "DL4822-20260918",
          "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
          "partition_key": "gpt#nestaging",
          "request_data": {
            "cancellation_policy_snapshot": {
              "label": "First Fare Cancellation",
              "tiers": {
                "tiers": [
                  {
                    "refund_pct": "1",
                    "hours_before_departure_gte": "24"
                  },
                  {
                    "refund_pct": "0.5",
                    "hours_before_departure_gte": "2"
                  },
                  {
                    "refund_pct": "0",
                    "hours_before_departure_gte": "0"
                  }
                ]
              },
              "description": "Job service instead mention whatever between seek chance back.",
              "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
              "snapshotted_at": "2026-06-24 05:57:05.197105",
              "notes_template_uuid": null
            }
          },
          "price_per_uom": "4500",
          "qty": "1",
          "pax_breakdown": {
            "adult": "1"
          },
          "bundle_uuid": null,
          "bundle_label": null,
          "bundle_component_uuid": null,
          "subtotal": "4500",
          "subtotal_discount": "0",
          "final_subtotal": "4500",
          "currency": null,
          "subtotal_native": "4500",
          "notes": null,
          "hold_token": null,
          "hold_expires_at": null,
          "created_at": "2026-06-24 05:57:05.131352",
          "updated_by": "MCP",
          "updated_at": "2026-06-24 05:57:05.131352"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "76fa1045-9619-4ea6-88e6-e4a85d027300",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 30 days before service receive escalating discounts. (ref: PROMO-6930-XI)",
          "conditions": [
            "min_passengers >= 20",
            "payment_method in ['wire_transfer', 'credit_card']",
            "is_refundable == false"
          ],
          "discount_rules": [
            {
              "less_than": "10000",
              "greater_than": "0",
              "max_discount_percentage": "5"
            },
            {
              "less_than": "11000",
              "greater_than": "10000",
              "max_discount_percentage": "10"
            },
            {
              "greater_than": "11000",
              "max_discount_percentage": "15"
            }
          ],
          "priority": "6",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.888325",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.888325"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "b2474c47-ebe9-467b-9f72-1ca94a058551",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-1368-IA)",
          "conditions": [
            "season != 'peak'",
            "channel == 'direct'"
          ],
          "discount_rules": [
            {
              "less_than": "5000",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "5"
            }
          ],
          "priority": "4",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.970326",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.970326"
        },
        {
          "partition_key": "gpt#nestaging",
          "discount_prompt_uuid": "db54f3f6-3aeb-4d83-b058-27c1d7851143",
          "scope": "global",
          "tags": [],
          "discount_prompt": "Apply a volume-tier discount when the total quote subtotal exceeds the configured thresholds. (ref: PROMO-1118-LM)",
          "conditions": [
            "loyalty_tier in ['gold', 'platinum']",
            "booking_lead_days >= 7"
          ],
          "discount_rules": [
            {
              "less_than": "2500",
              "greater_than": "0",
              "max_discount_percentage": "2.5"
            },
            {
              "less_than": "12500",
              "greater_than": "2500",
              "max_discount_percentage": "7.5"
            },
            {
              "less_than": "22500",
              "greater_than": "12500",
              "max_discount_percentage": "12.5"
            },
            {
              "greater_than": "22500",
              "max_discount_percentage": "17.5"
            }
          ],
          "priority": "1",
          "status": "active",
          "created_at": "2026-06-22 21:14:29.958795",
          "updated_by": "prepare_discount_prompts",
          "updated_at": "2026-06-22 21:14:29.958795"
        }
      ],
      "updated_by": "MCP",
      "created_at": "2026-06-24T05:57:00.472609",
      "updated_at": "2026-06-24T05:57:09.883381"
    }
  ],
  "total_quotes_created": 1,
  "total_quotes_requested": 1
}
```

### 31. installments / setup update_quote confirmed (create_installments)

- Method: `update_quote`
- Status: `pass`
- Elapsed: `6834.35 ms`

Arguments:

```json
{
  "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
  "quote_uuid": "c1b3fd73-a2bc-466a-bf5e-ab48577d1b99",
  "status": "confirmed",
  "notes": "Confirmed setup quote for create_installments"
}
```

Output:

```json
{
  "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
  "quote_uuid": "c1b3fd73-a2bc-466a-bf5e-ab48577d1b99",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-DL",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": null,
  "shipping_amount": 0.0,
  "total_quote_amount": 4500.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 4500.0,
  "currency": null,
  "display_currency": null,
  "fx_rate": null,
  "fx_rate_locked_at": null,
  "notes": "Confirmed setup quote for create_installments",
  "status": "confirmed",
  "expired_at": null,
  "request": null,
  "quote_items": [],
  "installments": [],
  "discount_prompts": [],
  "updated_by": "MCP",
  "created_at": "2026-06-24T05:57:00.472609",
  "updated_at": "2026-06-24T05:57:19.077223"
}
```

### 32. installments / create_installments

- Method: `create_installments`
- Status: `pass`
- Elapsed: `13750.12 ms`

Arguments:

```json
{
  "quote_uuid": "c1b3fd73-a2bc-466a-bf5e-ab48577d1b99",
  "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
  "interval_num": 3,
  "total_pay_period": 6,
  "payment_method": "bank_transfer"
}
```

Output:

```json
{
  "installments": [
    {
      "quote_uuid": "c1b3fd73-a2bc-466a-bf5e-ab48577d1b99",
      "installment_uuid": "c8d96aa8-f76b-4536-91bf-2b9216f081d9",
      "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 1500.0,
      "installment_ratio": 33.33333333333333,
      "salesorder_no": null,
      "scheduled_date": "2026-08-15T05:57:26",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-24T05:57:28.239747",
      "updated_at": "2026-06-24T05:57:28.239747",
      "quote": null
    },
    {
      "quote_uuid": "c1b3fd73-a2bc-466a-bf5e-ab48577d1b99",
      "installment_uuid": "37bc2814-e71f-46fc-9bec-2c7a9bc6032c",
      "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
      "priority": 1,
      "partition_key": "gpt#nestaging",
      "installment_amount": 1500.0,
      "installment_ratio": 33.33333333333333,
      "salesorder_no": null,
      "scheduled_date": "2026-10-15T05:57:26",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-24T05:57:30.501254",
      "updated_at": "2026-06-24T05:57:30.501254",
      "quote": null
    },
    {
      "quote_uuid": "c1b3fd73-a2bc-466a-bf5e-ab48577d1b99",
      "installment_uuid": "c06567be-438d-4868-86f0-b3427d375ec9",
      "request_uuid": "2a861a63-974e-4a91-a79c-87961589cd1a",
      "priority": 2,
      "partition_key": "gpt#nestaging",
      "installment_amount": 1500.0,
      "installment_ratio": 33.33333333333333,
      "salesorder_no": null,
      "scheduled_date": "2026-12-15T05:57:26",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-24T05:57:32.788869",
      "updated_at": "2026-06-24T05:57:32.788869",
      "quote": null
    }
  ],
  "total_created": 3,
  "installment_amount_per": 1500.0,
  "total_installment_amount": 4500.0
}
```

### 33. installments / update_installment (uuid=21270387-bff...)

- Method: `update_installment`
- Status: `pass`
- Elapsed: `20685.86 ms`

Arguments:

```json
{
  "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
  "installment_uuid": "21270387-bffc-4d6e-afda-6684c9896aa0",
  "status": "paid"
}
```

Output:

```json
{
  "quote_uuid": "e061e71f-ff9d-4614-864c-9aaaddaca2df",
  "installment_uuid": "21270387-bffc-4d6e-afda-6684c9896aa0",
  "request_uuid": "349196b8-fb8d-43ff-8f3f-5df4fc63ec84",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 9025.0,
  "installment_ratio": 100.0,
  "salesorder_no": null,
  "scheduled_date": "2026-06-24T05:55:28",
  "payment_method": "bank_transfer",
  "status": "paid",
  "updated_by": "MCP",
  "created_at": "2026-06-24T05:55:30.772561",
  "updated_at": "2026-06-24T05:57:39.693269",
  "quote": null
}
```

### 34. files / upload_rfq_file

- Method: `upload_rfq_file`
- Status: `pass`
- Elapsed: `4540.47 ms`

Arguments:

```json
{
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
  "file_name": "http_integration_test_spec.pdf",
  "email": "zbrown@example.org"
}
```

Output:

```json
{
  "file": {
    "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
    "file_name": "http_integration_test_spec.pdf",
    "email": "zbrown@example.org",
    "partition_key": "gpt#nestaging",
    "request": null,
    "updated_by": "MCP",
    "created_at": "2026-06-24T05:57:58.057587",
    "updated_at": "2026-06-24T05:57:58.057587"
  }
}
```

### 35. files / get_rfq_files

- Method: `get_rfq_files`
- Status: `pass`
- Elapsed: `4608.11 ms`

Arguments:

```json
{
  "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 2,
  "file_list": [
    {
      "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
      "file_name": "http_integration_test_spec.pdf",
      "email": "zbrown@example.org",
      "partition_key": "gpt#nestaging",
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
        "email": "zbrown@example.org",
        "request_title": "Business trip NRT to CDG November",
        "request_description": "Business travel for 2 attendee(s) attending offsite meetings in CDG. Prefer Business or Premium Economy to allow productive flight time.",
        "billing_address": {
          "city": "Maxwellhaven",
          "name": "Keith Chen",
          "phone": "001-314-580-8409x8991",
          "state": "LA",
          "street": "079 Karen Skyway",
          "country": "US",
          "postal_code": "50014"
        },
        "shipping_address": {
          "city": "Anaton",
          "name": "John Bradford",
          "phone": "(723)810-6891",
          "state": "AR",
          "street": "95551 Vaughn Villages Apt. 446",
          "country": "US",
          "postal_code": "83528"
        },
        "items": [
          {
            "quantity": "2",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "pax_breakdown": {
              "adult": "2"
            },
            "provider_items": [
              {
                "quantity": "2",
                "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
              }
            ],
            "cabin_preference": "Business"
          }
        ],
        "notes": "Eye kitchen entire member music finish despite letter eight while little win.",
        "bundle_uuid": null,
        "status": "initial",
        "expired_at": "2026-08-18T21:14:31.376040",
        "created_at": "2026-06-22T21:14:31.410885",
        "updated_by": "prepare_requests",
        "updated_at": "2026-06-22T21:14:31.410885",
        "quotes": [
          {
            "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
            "quote_uuid": "9e8378fa-f6b3-4353-bf9a-af2ff6036ff8",
            "provider_corp_external_id": "AIRLINE-DL",
            "sales_rep_email": "terri16@example.com",
            "partition_key": "gpt#nestaging",
            "shipping_method": null,
            "shipping_amount": "0",
            "total_quote_amount": "9000",
            "total_quote_discount": "111",
            "final_total_quote_amount": "8889",
            "currency": "USD",
            "display_currency": null,
            "fx_rate": null,
            "fx_rate_locked_at": null,
            "rounds": "0",
            "notes": "Auto-completed: All installments paid",
            "status": "completed",
            "created_at": "2026-06-22 21:14:32.731930",
            "updated_by": "MCP",
            "updated_at": "2026-06-23 06:54:27.199452"
          }
        ],
        "files": [
          {
            "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
            "file_name": "http_integration_test_spec.pdf",
            "email": "zbrown@example.org",
            "partition_key": "gpt#nestaging",
            "created_at": "2026-06-24 05:57:58.057587",
            "updated_by": "MCP",
            "updated_at": "2026-06-24 05:57:58.057587"
          },
          {
            "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
            "file_name": "integration_test_spec.pdf",
            "email": "zbrown@example.org",
            "partition_key": "gpt#nestaging",
            "created_at": "2026-06-23 06:48:47.795038",
            "updated_by": "MCP",
            "updated_at": "2026-06-23 21:05:05.756244"
          }
        ],
        "bundle": null
      },
      "updated_by": "MCP",
      "created_at": "2026-06-24T05:57:58.057587",
      "updated_at": "2026-06-24T05:57:58.057587"
    },
    {
      "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
      "file_name": "integration_test_spec.pdf",
      "email": "zbrown@example.org",
      "partition_key": "gpt#nestaging",
      "request": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
        "email": "zbrown@example.org",
        "request_title": "Business trip NRT to CDG November",
        "request_description": "Business travel for 2 attendee(s) attending offsite meetings in CDG. Prefer Business or Premium Economy to allow productive flight time.",
        "billing_address": {
          "city": "Maxwellhaven",
          "name": "Keith Chen",
          "phone": "001-314-580-8409x8991",
          "state": "LA",
          "street": "079 Karen Skyway",
          "country": "US",
          "postal_code": "50014"
        },
        "shipping_address": {
          "city": "Anaton",
          "name": "John Bradford",
          "phone": "(723)810-6891",
          "state": "AR",
          "street": "95551 Vaughn Villages Apt. 446",
          "country": "US",
          "postal_code": "83528"
        },
        "items": [
          {
            "quantity": "2",
            "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
            "pax_breakdown": {
              "adult": "2"
            },
            "provider_items": [
              {
                "quantity": "2",
                "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
              }
            ],
            "cabin_preference": "Business"
          }
        ],
        "notes": "Eye kitchen entire member music finish despite letter eight while little win.",
        "bundle_uuid": null,
        "status": "initial",
        "expired_at": "2026-08-18T21:14:31.376040",
        "created_at": "2026-06-22T21:14:31.410885",
        "updated_by": "prepare_requests",
        "updated_at": "2026-06-22T21:14:31.410885",
        "quotes": [
          {
            "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
            "quote_uuid": "9e8378fa-f6b3-4353-bf9a-af2ff6036ff8",
            "provider_corp_external_id": "AIRLINE-DL",
            "sales_rep_email": "terri16@example.com",
            "partition_key": "gpt#nestaging",
            "shipping_method": null,
            "shipping_amount": "0",
            "total_quote_amount": "9000",
            "total_quote_discount": "111",
            "final_total_quote_amount": "8889",
            "currency": "USD",
            "display_currency": null,
            "fx_rate": null,
            "fx_rate_locked_at": null,
            "rounds": "0",
            "notes": "Auto-completed: All installments paid",
            "status": "completed",
            "created_at": "2026-06-22 21:14:32.731930",
            "updated_by": "MCP",
            "updated_at": "2026-06-23 06:54:27.199452"
          }
        ],
        "files": [
          {
            "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
            "file_name": "http_integration_test_spec.pdf",
            "email": "zbrown@example.org",
            "partition_key": "gpt#nestaging",
            "created_at": "2026-06-24 05:57:58.057587",
            "updated_by": "MCP",
            "updated_at": "2026-06-24 05:57:58.057587"
          },
          {
            "request_uuid": "c6e3730a-e8b5-4d18-bc54-10b0c86a1a4a",
            "file_name": "integration_test_spec.pdf",
            "email": "zbrown@example.org",
            "partition_key": "gpt#nestaging",
            "created_at": "2026-06-23 06:48:47.795038",
            "updated_by": "MCP",
            "updated_at": "2026-06-23 21:05:05.756244"
          }
        ],
        "bundle": null
      },
      "updated_by": "MCP",
      "created_at": "2026-06-23T06:48:47.795038",
      "updated_at": "2026-06-23T21:05:05.756244"
    }
  ]
}
```

### 36. segments / get_segment_contacts

- Method: `get_segment_contacts`
- Status: `pass`
- Elapsed: `4597.21 ms`

Arguments:

```json
{
  "email": "zbrown@example.org",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 1,
  "segment_contact_list": [
    {
      "partition_key": "gpt#nestaging",
      "email": "zbrown@example.org",
      "contact_uuid": null,
      "consumer_corp_external_id": "CUST-7437",
      "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
      "segment": {
        "partition_key": "gpt#nestaging",
        "endpoint_id": "gpt",
        "part_id": "nestaging",
        "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
        "provider_corp_external_id": "PROV-3980",
        "segment_name": "King Group Tier",
        "segment_description": "Visionary well-modulated moratorium",
        "created_at": "2026-06-22T21:14:24.785967",
        "updated_by": "prepare_segments_and_contacts",
        "updated_at": "2026-06-22T21:14:24.785967",
        "contacts": [
          {
            "partition_key": "gpt#nestaging",
            "email": "tmeyers@example.com",
            "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
            "contact_uuid": null,
            "consumer_corp_external_id": "CUST-5927",
            "created_at": "2026-06-22 21:14:24.897500",
            "updated_by": "prepare_segments_and_contacts",
            "updated_at": "2026-06-22 21:14:24.897500"
          },
          {
            "partition_key": "gpt#nestaging",
            "email": "zwhitaker@example.com",
            "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
            "contact_uuid": null,
            "consumer_corp_external_id": "CUST-5194",
            "created_at": "2026-06-22 21:14:24.912588",
            "updated_by": "prepare_segments_and_contacts",
            "updated_at": "2026-06-22 21:14:24.912588"
          },
          {
            "partition_key": "gpt#nestaging",
            "email": "jason58@example.com",
            "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
            "contact_uuid": null,
            "consumer_corp_external_id": "CUST-2826",
            "created_at": "2026-06-22 21:14:24.924103",
            "updated_by": "prepare_segments_and_contacts",
            "updated_at": "2026-06-22 21:14:24.924103"
          },
          {
            "partition_key": "gpt#nestaging",
            "email": "ortizjoseph@example.com",
            "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
            "contact_uuid": null,
            "consumer_corp_external_id": "CUST-9689",
            "created_at": "2026-06-22 21:14:24.935089",
            "updated_by": "prepare_segments_and_contacts",
            "updated_at": "2026-06-22 21:14:24.935089"
          },
          {
            "partition_key": "gpt#nestaging",
            "email": "zbrown@example.org",
            "segment_uuid": "5101fc1b-732a-4ade-ab8c-390eee652bbe",
            "contact_uuid": null,
            "consumer_corp_external_id": "CUST-7437",
            "created_at": "2026-06-22 21:14:24.947242",
            "updated_by": "prepare_segments_and_contacts",
            "updated_at": "2026-06-22 21:14:24.947242"
          }
        ]
      },
      "updated_by": "prepare_segments_and_contacts",
      "created_at": "2026-06-22T21:14:24.947242",
      "updated_at": "2026-06-22T21:14:24.947242"
    }
  ]
}
```

### 37. availability / check_availability

- Method: `check_availability`
- Status: `pass`
- Elapsed: `4579.06 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z",
  "batch_no": "DL4822-20260918",
  "qty": 2
}
```

Output:

```json
{
  "operation": "check",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "batch_no": "DL4822-20260918",
  "service_start_at": "2026-09-18T14:45:00+00:00",
  "service_end_at": "2026-09-18T23:28:08.831283+00:00",
  "available": true,
  "hold_token": null,
  "expires_at": null,
  "payload": {
    "reason": "available",
    "matched_batches": 1,
    "available_batches": 1,
    "total_available_qty": 3.0,
    "slow_move": false
  },
  "fetched_at": "2026-06-24T05:58:11.851815+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 38. availability / acquire_availability_hold

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `4667.77 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z",
  "qty": 2,
  "batch_no": "DL4822-20260918",
  "pax_breakdown": {
    "adult": 2
  }
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": "2026-09-18T14:45:00+00:00",
    "service_end_at": "2026-09-18T23:28:08.831283+00:00",
    "available": true,
    "hold_token": "39dddaa10db79ee3fdf2b18bd4c88d3d",
    "expires_at": "2026-06-24T06:13:16.511952+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 3.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-24T05:58:16.520994+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 39. availability / confirm_availability_hold

- Method: `confirm_availability_hold`
- Status: `pass`
- Elapsed: `4552.99 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "39dddaa10db79ee3fdf2b18bd4c88d3d",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "availability": {
    "operation": "confirm_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": null,
    "service_end_at": null,
    "available": true,
    "hold_token": "39dddaa10db79ee3fdf2b18bd4c88d3d",
    "expires_at": null,
    "payload": {
      "reason": "hold_confirmed"
    },
    "fetched_at": "2026-06-24T05:58:21.072456+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```

### 40. availability / acquire_availability_hold (for release test)

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `4528.66 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z",
  "qty": 1,
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": "2026-09-18T14:45:00+00:00",
    "service_end_at": "2026-09-18T23:28:08.831283+00:00",
    "available": true,
    "hold_token": "a7213b9e70831f451efe95e5d8df9d49",
    "expires_at": "2026-06-24T06:13:25.589129+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 1.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-24T05:58:25.600627+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 41. availability / release_availability_hold

- Method: `release_availability_hold`
- Status: `pass`
- Elapsed: `4714.68 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "a7213b9e70831f451efe95e5d8df9d49",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "availability": {
    "operation": "release_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": null,
    "service_end_at": null,
    "available": true,
    "hold_token": "a7213b9e70831f451efe95e5d8df9d49",
    "expires_at": null,
    "payload": {
      "reason": "hold_released"
    },
    "fetched_at": "2026-06-24T05:58:30.315406+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```

### 42. availability / acquire_availability_hold (for expire test)

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `4766.26 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "service_start_at": "2026-09-18T14:45:00Z",
  "service_end_at": "2026-09-18T23:28:08.831283Z",
  "qty": 1,
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": "2026-09-18T14:45:00+00:00",
    "service_end_at": "2026-09-18T23:28:08.831283+00:00",
    "available": true,
    "hold_token": "3e7774ae061dc15a4c4f4d256176e7e4",
    "expires_at": "2026-06-24T06:13:35.064008+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 1.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-24T05:58:35.079040+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 43. availability / expire_availability_hold

- Method: `expire_availability_hold`
- Status: `pass`
- Elapsed: `4829.54 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "3e7774ae061dc15a4c4f4d256176e7e4",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
  "batch_no": "DL4822-20260918"
}
```

Output:

```json
{
  "availability": {
    "operation": "expire_hold",
    "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
    "batch_no": "DL4822-20260918",
    "service_start_at": null,
    "service_end_at": null,
    "available": null,
    "hold_token": null,
    "expires_at": null,
    "payload": null,
    "fetched_at": null,
    "ttl_seconds": null,
    "error_code": "unknown_hold",
    "error_message": "Availability hold has not expired"
  }
}
```

### 44. bundles / search_bundles (itinerary type)

- Method: `search_bundles`
- Status: `pass`
- Elapsed: `4881.04 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_type": "itinerary"
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 0,
  "bundle_list": []
}
```

### 45. bundles / get_bundle (FLT-ITIN-001)

- Method: `get_bundle`
- Status: `pass`
- Elapsed: `4954.93 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
  "bundle_code": "FLT-ITIN-001",
  "bundle_name": "Flight Itinerary CDG->ORD + NRT->BOS + NRT->CDG",
  "bundle_type": "flight_itinerary",
  "description": "Multi-leg flight itinerary template composed of independently priced flight legs.",
  "extra": {
    "routes": [
      "CDG->ORD",
      "NRT->BOS",
      "NRT->CDG"
    ],
    "source": "prepare_flight_products",
    "leg_count": "3",
    "item_external_ids": [
      "FLIGHT-CDG-ORD-ECO",
      "FLIGHT-NRT-BOS-BUS",
      "FLIGHT-NRT-CDG-FIR"
    ]
  },
  "status": "active",
  "created_at": "2026-06-22T21:14:26.931029",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-22T21:14:26.931029",
  "components": [
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "1cb9800a-53ba-44c8-965d-2cc90bb71842",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 3.0,
      "extra": {
        "route": "NRT->CDG",
        "item_external_id": "FLIGHT-NRT-CDG-FIR",
        "provider_item_external_id": "DL-NRT-CDG-FIR"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.048923",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.048923"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "c8ec10e4-f0e2-48bd-aa43-dfcaac88c6c9",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "48d374c4-588d-49b9-a005-36caa41706eb",
      "provider_item_uuid": "d5c08211-7dcf-42fd-8e98-00ac75aba027",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 2.0,
      "extra": {
        "route": "NRT->BOS",
        "item_external_id": "FLIGHT-NRT-BOS-BUS",
        "provider_item_external_id": "CX-NRT-BOS-BUS"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.037290",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.037290"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "19fbf77d-5ce2-4032-b4be-a15cb64917a6",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1",
      "provider_item_uuid": "bad12922-6da1-4117-95ec-5ee0284a5d95",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 1.0,
      "extra": {
        "route": "CDG->ORD",
        "item_external_id": "FLIGHT-CDG-ORD-ECO",
        "provider_item_external_id": "SQ-CDG-ORD-ECO"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.016699",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.016699"
    }
  ]
}
```

### 46. bundles / search_bundle_components

- Method: `search_bundle_components`
- Status: `pass`
- Elapsed: `5041.92 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639"
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 3,
  "bundle_component_list": [
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "1cb9800a-53ba-44c8-965d-2cc90bb71842",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "9f965bf9-7302-4f1d-8d37-6f335f880c58",
      "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 3.0,
      "extra": {
        "route": "NRT->CDG",
        "item_external_id": "FLIGHT-NRT-CDG-FIR",
        "provider_item_external_id": "DL-NRT-CDG-FIR"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.048923",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.048923"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "c8ec10e4-f0e2-48bd-aa43-dfcaac88c6c9",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "48d374c4-588d-49b9-a005-36caa41706eb",
      "provider_item_uuid": "d5c08211-7dcf-42fd-8e98-00ac75aba027",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 2.0,
      "extra": {
        "route": "NRT->BOS",
        "item_external_id": "FLIGHT-NRT-BOS-BUS",
        "provider_item_external_id": "CX-NRT-BOS-BUS"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.037290",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.037290"
    },
    {
      "partition_key": "gpt#nestaging",
      "bundle_component_uuid": "19fbf77d-5ce2-4032-b4be-a15cb64917a6",
      "bundle_uuid": "0f19ab66-07f9-44fa-ac17-5d87434e6639",
      "item_uuid": "d6dd8e87-34f1-4741-b293-dc41992089b1",
      "provider_item_uuid": "bad12922-6da1-4117-95ec-5ee0284a5d95",
      "component_role": "flight_leg",
      "required": true,
      "default_qty": 1.0,
      "sort_order": 1.0,
      "extra": {
        "route": "CDG->ORD",
        "item_external_id": "FLIGHT-CDG-ORD-ECO",
        "provider_item_external_id": "SQ-CDG-ORD-ECO"
      },
      "status": "active",
      "created_at": "2026-06-22T21:14:27.016699",
      "updated_by": "prepare_flight_products",
      "updated_at": "2026-06-22T21:14:27.016699"
    }
  ]
}
```

### 47. cancellation / get_cancellation_policy (Business Fare)

- Method: `get_cancellation_policy`
- Status: `pass`
- Elapsed: `4765.47 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "policy_uuid": "b2ede6e5-e595-4719-b0b8-07a1f5f74baf",
  "provider_item_uuid": null,
  "label": "First Fare Cancellation",
  "description": "Job service instead mention whatever between seek chance back.",
  "tiers": {
    "tiers": [
      {
        "refund_pct": "1",
        "hours_before_departure_gte": "24"
      },
      {
        "refund_pct": "0.5",
        "hours_before_departure_gte": "2"
      },
      {
        "refund_pct": "0",
        "hours_before_departure_gte": "0"
      }
    ]
  },
  "notes_template_uuid": null,
  "status": "active",
  "created_at": "2026-06-22T21:14:26.847774",
  "updated_by": "prepare_flight_products",
  "updated_at": "2026-06-22T21:14:26.847774"
}
```

### 48. cancellation / search_cancellation_policies

- Method: `search_cancellation_policies`
- Status: `pass`
- Elapsed: `4522.52 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "24529e36-bd9c-4427-ac05-d1d545ad8963"
}
```

Output:

```json
{
  "page_size": null,
  "page_number": null,
  "total": 0,
  "cancellation_policy_list": []
}
```

### 49. catalog / inquire_catalog

- Method: `inquire_catalog`
- Status: `pass`
- Elapsed: `7506.08 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "query_text": "Delta Air Lines NRT CDG First class flight with meal included",
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
          "score": "0.8775375485420227",
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
          "score": "0.7617291808128357",
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
          "score": "0.7401930093765259",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight itinerary bundle FLT-ITIN-002 named 'Flight Itinerary NRT->BOS + DFW->CDG + NRT->CDG'. Multi-leg flight itinerary template composed of independently priced flight legs. It contains 3 flight legs:\n  - Leg 1: NRT->BOS\n  - Leg 2: DFW->CDG\n  - Leg 3: NRT->CDG"
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:50",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:50",
          "score": "0.7400851249694824",
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
          "score": "0.7254970073699951",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-24T05:59:11.585638+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```
