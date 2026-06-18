# MCP HospiRFQ Processor HTTP Integration Results (MCPHttpClient)

- Generated at: `2026-06-18T16:20:12.534754+00:00`
- Gateway: `http://localhost:8765`
- MCP REST URL: `http://localhost:8765/gpt/nestaging/mcp`
- Endpoint: `gpt`
- Partition: `nestaging`
- Transport: MCPHttpClient → JSON-RPC → gateway `/mcp`
- Dependency order: `requests, quotes, installments`
- Passed: `26`
- Error responses: `1`
- Failed: `0`
- Total calls: `27`

## Executive Summary

End-to-end HTTP integration testing was executed through the `mcp_http_client.MCPHttpClient` against the `silvaengine_gateway` REST/JSON-RPC MCP endpoint (`/{endpoint_id}/{part_id}/mcp`). Each tool was invoked via JSON-RPC `tools/call`, exercising the full agent → gateway → `MCPHospiRFQProcessor` stack. The gateway handles all backend dispatch internally. The run completed with 26 passing function calls, 1 error responses, and 0 failures.

## Scope

- In scope: MCP JSON-RPC transport (initialize, tools/list, tools/call), gateway MCP dispatch, MCPHospiRFQProcessor tool execution. The gateway handles backend dispatch internally.
- Out of scope: production validation, destructive cleanup, load testing, UI testing.

## Function Results

### 1. requests / submit_rfq_request

- Method: `submit_rfq_request`
- Status: `pass`
- Elapsed: `8913.23 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "items": [
    {
      "item_uuid": "06041993713794695296",
      "item_name": "Flight ATL->ORD Premium Economy",
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
  "request_uuid": "26699108493000982656",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Created by run_http_integration.py",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:12:37.490071",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:12:37.490071",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 2. requests / get_rfq_request (seeded)

- Method: `get_rfq_request`
- Status: `pass`
- Elapsed: `8801.71 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "96306650268729098368",
  "email": "jessicacooper@example.com",
  "request_title": "Honeymoon to ORD (updated by integration test)",
  "request_description": "Honeymoon trip for 2 adults. Open to splurge on the outbound in Business if pricing is reasonable.",
  "billing_address": {
    "country": "US",
    "city": "West Amy",
    "phone": "+1-287-493-0405x186",
    "street": "8532 Hernandez Ports",
    "name": "Heidi Garza",
    "state": "MA",
    "postal_code": "40901"
  },
  "shipping_address": {
    "country": "US",
    "city": "Lake Nathanside",
    "phone": "+1-494-213-4598",
    "street": "6159 Joyce Coves Suite 945",
    "name": "Mitchell Carrillo",
    "state": "WY",
    "postal_code": "72270"
  },
  "items": [
    {
      "cabin_preference": "Premium Economy",
      "quantity": "2",
      "item_uuid": "06041993713794695296",
      "provider_items": [],
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "completed",
  "expired_at": "2026-07-25T22:41:32.314663",
  "created_at": "2026-06-01T22:41:32.471123",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T15:32:54.393751",
  "quotes": [
    {
      "final_total_quote_amount": "0",
      "provider_corp_external_id": "AIRLINE-AF",
      "rounds": "0",
      "shipping_amount": "0",
      "status": "disapproved",
      "total_quote_amount": "0",
      "total_quote_discount": "0",
      "created_at": "2026-06-17 19:10:34.347670",
      "notes": "Auto-disapproved: Another quote was confirmed",
      "partition_key": "gpt#nestaging",
      "quote_uuid": "12616028676071374976",
      "request_uuid": "96306650268729098368",
      "updated_at": "2026-06-17 19:12:07.004383",
      "updated_by": "MCP"
    },
    {
      "final_total_quote_amount": "0",
      "provider_corp_external_id": "AIRLINE-LH",
      "rounds": "0",
      "shipping_amount": "0",
      "status": "disapproved",
      "total_quote_amount": "0",
      "total_quote_discount": "0",
      "created_at": "2026-06-01 22:43:00.075462",
      "currency": "USD",
      "display_currency": "CAD",
      "fx_rate": "1.335005",
      "fx_rate_locked_at": "2026-06-01 22:42:59.985871",
      "notes": "Auto-disapproved: Another quote was confirmed",
      "partition_key": "gpt#nestaging",
      "quote_uuid": "42458963099238023296",
      "request_uuid": "96306650268729098368",
      "sales_rep_email": "kimberly71@example.org",
      "updated_at": "2026-06-17 19:11:59.548180",
      "updated_by": "MCP"
    },
    {
      "final_total_quote_amount": "25",
      "provider_corp_external_id": "AIRLINE-QF",
      "rounds": "0",
      "shipping_amount": "25",
      "status": "completed",
      "total_quote_amount": "0",
      "total_quote_discount": "0",
      "created_at": "2026-06-01 22:42:59.864855",
      "currency": "USD",
      "display_currency": "CNY",
      "fx_rate": "7.081345",
      "fx_rate_locked_at": "2026-06-01 22:42:59.540604",
      "notes": "Auto-completed: All installments paid",
      "partition_key": "gpt#nestaging",
      "quote_uuid": "83893620897501692032",
      "request_uuid": "96306650268729098368",
      "sales_rep_email": "jordan99@example.net",
      "shipping_method": "ticket_delivery",
      "updated_at": "2026-06-18 15:32:43.397226",
      "updated_by": "MCP"
    }
  ],
  "files": [
    {
      "created_at": "2026-06-18 14:18:54.785362",
      "email": "jessicacooper@example.com",
      "file_name": "http_integration_test_spec.pdf",
      "partition_key": "gpt#nestaging",
      "request_uuid": "96306650268729098368",
      "updated_at": "2026-06-18 15:33:02.177621",
      "updated_by": "MCP"
    },
    {
      "created_at": "2026-06-17 19:11:33.981790",
      "email": "jessicacooper@example.com",
      "file_name": "integration_test_spec.pdf",
      "partition_key": "gpt#nestaging",
      "request_uuid": "96306650268729098368",
      "updated_at": "2026-06-18 04:40:22.620940",
      "updated_by": "MCP"
    }
  ],
  "bundle": null
}
```

### 3. requests / search_rfq_requests

- Method: `search_rfq_requests`
- Status: `pass`
- Elapsed: `8603.04 ms`

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
  "page_size": 5,
  "page_number": 1,
  "total": 27,
  "request_list": [
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "87119168162060320896",
      "email": "beannorma@example.com",
      "request_title": "Honeymoon to ORD",
      "request_description": "Honeymoon trip for 2 adults. Open to splurge on the outbound in Business if pricing is reasonable.",
      "billing_address": {
        "country": "US",
        "city": "East Cheyennemouth",
        "phone": "491-252-8236x931",
        "street": "885 Collins Avenue",
        "name": "Jason Guzman",
        "state": "NJ",
        "postal_code": "23488"
      },
      "shipping_address": {
        "country": "US",
        "city": "South Loriton",
        "phone": "266-439-8592",
        "street": "899 Morgan Lodge Apt. 070",
        "name": "Bryan King",
        "state": "MT",
        "postal_code": "87031"
      },
      "items": [
        {
          "cabin_preference": "Economy",
          "bundle_component_uuid": "80197043753719971968",
          "quantity": "2",
          "item_uuid": "52065619693805781120",
          "provider_items": [
            {
              "provider_item_uuid": "94764066649319424128",
              "quantity": "2"
            }
          ],
          "pax_breakdown": {
            "adult": "2"
          }
        },
        {
          "cabin_preference": "Economy",
          "bundle_component_uuid": "26138792054410461312",
          "quantity": "2",
          "item_uuid": "97838712287656951936",
          "provider_items": [
            {
              "provider_item_uuid": "93970690058365190272",
              "quantity": "2"
            }
          ],
          "pax_breakdown": {
            "adult": "2"
          }
        },
        {
          "cabin_preference": "Economy",
          "bundle_component_uuid": "05615016170826514560",
          "quantity": "2",
          "item_uuid": "17735923656909930624",
          "provider_items": [
            {
              "provider_item_uuid": "55349863084404523136",
              "quantity": "2",
              "batch_no": "AF5020-20260616"
            }
          ],
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Technology bar question military because away whole draw build worker star.",
      "bundle_uuid": "49956565412585947264",
      "status": "initial",
      "expired_at": "2026-07-06T22:41:32.864151",
      "created_at": "2026-06-01T22:41:33.316535",
      "updated_by": "prepare_requests",
      "updated_at": "2026-06-01T22:41:33.316535",
      "quotes": [
        {
          "final_total_quote_amount": "950",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "0",
          "shipping_amount": "0",
          "status": "initial",
          "total_quote_amount": "1000",
          "total_quote_discount": "50",
          "created_at": "2026-06-01 22:43:00.287972",
          "currency": "USD",
          "notes": "Future I industry school significant sea to month avoid serve much anyone box wall song.",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "51485446173562519680",
          "request_uuid": "87119168162060320896",
          "sales_rep_email": "williamsgary@example.net",
          "updated_at": "2026-06-17 20:17:20.488195",
          "updated_by": "prepare_quotes"
        }
      ],
      "files": [],
      "bundle": {
        "partition_key": "gpt#nestaging",
        "bundle_uuid": "49956565412585947264",
        "bundle_code": "FLT-ITIN-002",
        "bundle_name": "Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK",
        "bundle_type": "flight_itinerary",
        "description": "Multi-leg flight itinerary template composed of independently priced flight legs.",
        "extra": {
          "routes": [
            "ATL->ORD",
            "LAX->HKG",
            "CDG->JFK"
          ],
          "source": "prepare_flight_products",
          "leg_count": "3",
          "item_external_ids": [
            "FLIGHT-ATL-ORD-ECO",
            "FLIGHT-LAX-HKG-PRE",
            "FLIGHT-CDG-JFK-BUS"
          ]
        },
        "status": "active",
        "created_at": "2026-06-01T22:19:34.512270",
        "updated_by": "prepare_flight_products",
        "updated_at": "2026-06-01T22:19:34.512270",
        "components": [
          {
            "partition_key": "gpt#nestaging",
            "bundle_component_uuid": "80197043753719971968",
            "bundle_uuid": "49956565412585947264",
            "item_uuid": "52065619693805781120",
            "provider_item_uuid": "94764066649319424128",
            "component_role": "flight_leg",
            "required": true,
            "default_qty": 1.0,
            "sort_order": 1.0,
            "extra": {
              "route": "ATL->ORD",
              "item_external_id": "FLIGHT-ATL-ORD-ECO",
              "provider_item_external_id": "QF-ATL-ORD-ECO"
            },
            "status": "active",
            "created_at": "2026-06-01T22:19:34.949372",
            "updated_by": "prepare_flight_products",
            "updated_at": "2026-06-01T22:19:34.949372"
          },
          {
            "partition_key": "gpt#nestaging",
            "bundle_component_uuid": "26138792054410461312",
            "bundle_uuid": "49956565412585947264",
            "item_uuid": "97838712287656951936",
            "provider_item_uuid": "93970690058365190272",
            "component_role": "flight_leg",
            "required": true,
            "default_qty": 1.0,
            "sort_order": 2.0,
            "extra": {
              "route": "LAX->HKG",
              "item_external_id": "FLIGHT-LAX-HKG-PRE",
              "provider_item_external_id": "LH-LAX-HKG-PRE"
            },
            "status": "active",
            "created_at": "2026-06-01T22:19:35.230969",
            "updated_by": "prepare_flight_products",
            "updated_at": "2026-06-01T22:19:35.230969"
          },
          {
            "partition_key": "gpt#nestaging",
            "bundle_component_uuid": "05615016170826514560",
            "bundle_uuid": "49956565412585947264",
            "item_uuid": "17735923656909930624",
            "provider_item_uuid": "55349863084404523136",
            "component_role": "flight_leg",
            "required": true,
            "default_qty": 1.0,
            "sort_order": 3.0,
            "extra": {
              "route": "CDG->JFK",
              "item_external_id": "FLIGHT-CDG-JFK-BUS",
              "provider_item_external_id": "AF-CDG-JFK-BUS"
            },
            "status": "active",
            "created_at": "2026-06-01T22:19:35.518661",
            "updated_by": "prepare_flight_products",
            "updated_at": "2026-06-01T22:19:35.518661"
          }
        ]
      }
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "74921795627915427968",
      "email": "beannorma@example.com",
      "request_title": "Business trip LAX to HKG November",
      "request_description": "Business travel for 2 attendee(s) attending offsite meetings in HKG. Prefer Business or Premium Economy to allow productive flight time.",
      "billing_address": {
        "country": "US",
        "city": "Jamesport",
        "phone": "975.274.0279x15049",
        "street": "721 Theresa Crescent Apt. 105",
        "name": "Candace Nelson",
        "state": "AZ",
        "postal_code": "60136"
      },
      "shipping_address": {
        "country": "US",
        "city": "Port Michael",
        "phone": "700-444-5957x3273",
        "street": "392 Daniel Brook",
        "name": "Jennifer Walker",
        "state": "MP",
        "postal_code": "73736"
      },
      "items": [
        {
          "cabin_preference": "Premium Economy",
          "quantity": "2",
          "item_uuid": "97838712287656951936",
          "provider_items": [
            {
              "provider_item_uuid": "93970690058365190272",
              "quantity": "2"
            }
          ],
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Outside year industry officer wall month teacher performance site smile add beat first.",
      "bundle_uuid": null,
      "status": "initial",
      "expired_at": "2026-08-12T22:41:33.608681",
      "created_at": "2026-06-01T22:41:33.752676",
      "updated_by": "prepare_requests",
      "updated_at": "2026-06-01T22:41:33.752676",
      "quotes": [
        {
          "final_total_quote_amount": "0",
          "provider_corp_external_id": "AIRLINE-QF",
          "rounds": "0",
          "shipping_amount": "34.09",
          "status": "initial",
          "total_quote_amount": "0",
          "total_quote_discount": "0",
          "created_at": "2026-06-01 22:43:01.039803",
          "currency": "USD",
          "display_currency": "JPY",
          "fx_rate": "153.416905",
          "fx_rate_locked_at": "2026-06-01 22:43:00.600322",
          "notes": "Relationship us girl common market teacher like.",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "31038949121456095360",
          "request_uuid": "74921795627915427968",
          "sales_rep_email": "elizabeth68@example.net",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-01 22:43:01.039803",
          "updated_by": "prepare_quotes"
        },
        {
          "final_total_quote_amount": "1800",
          "provider_corp_external_id": "AIRLINE-LH",
          "rounds": "0",
          "shipping_amount": "0",
          "status": "initial",
          "total_quote_amount": "1800",
          "total_quote_discount": "0",
          "created_at": "2026-06-01 22:43:00.494956",
          "currency": "USD",
          "notes": "Try member magazine campaign among owner far return best lot today expect song source perform.",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "98513172062733877376",
          "request_uuid": "74921795627915427968",
          "sales_rep_email": "patriciareed@example.com",
          "updated_at": "2026-06-01 22:46:23.305644",
          "updated_by": "prepare_quotes"
        }
      ],
      "files": [],
      "bundle": null
    },
    {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "46915773638499123328",
      "email": "jessicacooper@example.com",
      "request_title": "Business trip ATL to ORD August",
      "request_description": "Business travel for 1 attendee(s) attending offsite meetings in ORD. Prefer Business or Premium Economy to allow productive flight time.",
      "billing_address": {
        "country": "US",
        "city": "Lake John",
        "phone": "4207609557",
        "street": "974 Janet Rue Suite 436",
        "name": "Jacqueline Burgess",
        "state": "OH",
        "postal_code": "92451"
      },
      "shipping_address": {
        "country": "US",
        "city": "Kimberlyshire",
        "phone": "3918134809",
        "street": "65959 Tony Manors",
        "name": "Christopher Swanson",
        "state": "AS",
        "postal_code": "65311"
      },
      "items": [
        {
          "cabin_preference": "Premium Economy",
          "quantity": "1",
          "item_uuid": "06041993713794695296",
          "provider_items": [
            {
              "provider_item_uuid": "39876487618607726720",
              "quantity": "1"
            }
          ],
          "pax_breakdown": {
            "adult": "1"
          }
        }
      ],
      "notes": "Leave administration well exactly she nice bed trade maintain know.",
      "bundle_uuid": null,
      "status": "initial",
      "expired_at": "2026-08-30T22:41:34.072125",
      "created_at": "2026-06-01T22:41:34.211289",
      "updated_by": "prepare_requests",
      "updated_at": "2026-06-01T22:41:34.211289",
      "
... (truncated)
```

### 4. requests / update_rfq_request

- Method: `update_rfq_request`
- Status: `pass`
- Elapsed: `12010.76 ms`

Arguments:

```json
{
  "request_uuid": "26699108493000982656",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
  "notes": "Updated via run_http_integration.py"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "26699108493000982656",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:12:37.490071",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:13:07.111607",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 5. requests / add_item_to_rfq_request

- Method: `add_item_to_rfq_request`
- Status: `pass`
- Elapsed: `12062.26 ms`

Arguments:

```json
{
  "request_uuid": "26699108493000982656",
  "item": {
    "item_uuid": "52065619693805781120",
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
  "request_uuid": "26699108493000982656",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    },
    {
      "item_name": "Flight ATL->ORD Economy",
      "item_uuid": "52065619693805781120",
      "provider_items": [],
      "qty": "1"
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:12:37.490071",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:13:19.151673",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 6. requests / remove_item_from_rfq_request

- Method: `remove_item_from_rfq_request`
- Status: `pass`
- Elapsed: `12267.98 ms`

Arguments:

```json
{
  "request_uuid": "26699108493000982656",
  "item_uuid": "52065619693805781120"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "26699108493000982656",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:12:37.490071",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:13:31.411969",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 7. requests / assign_provider_item_to_request_item

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `16117.47 ms`

Arguments:

```json
{
  "request_uuid": "26699108493000982656",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720",
  "provider_corp_external_id": "AIRLINE-AF",
  "qty": 2,
  "batch_no": "AF5319-20260907"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "26699108493000982656",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "provider_items": [
        {
          "provider_item_uuid": "39876487618607726720",
          "provider_corp_external_id": "AIRLINE-AF",
          "batch_no": "AF5319-20260907",
          "qty": "2"
        }
      ],
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:12:37.490071",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:13:47.528012",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 8. requests / remove_provider_item_from_request_item

- Method: `remove_provider_item_from_request_item`
- Status: `pass`
- Elapsed: `12287.0 ms`

Arguments:

```json
{
  "request_uuid": "26699108493000982656",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "26699108493000982656",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "provider_items": [],
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:12:37.490071",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:13:59.861080",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 9. requests / assign_provider_item_to_request_item (for quote workflow)

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `15789.68 ms`

Arguments:

```json
{
  "request_uuid": "26699108493000982656",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720",
  "provider_corp_external_id": "AIRLINE-AF",
  "qty": 2,
  "batch_no": "AF5319-20260907"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "26699108493000982656",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "provider_items": [
        {
          "provider_item_uuid": "39876487618607726720",
          "provider_corp_external_id": "AIRLINE-AF",
          "batch_no": "AF5319-20260907",
          "qty": "2"
        }
      ],
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_http_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:12:37.490071",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:14:15.629883",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 10. quotes / confirm_request_and_create_quotes

- Method: `confirm_request_and_create_quotes`
- Status: `pass`
- Elapsed: `45636.05 ms`

Arguments:

```json
{
  "request_uuid": "26699108493000982656",
  "provider_corp_external_ids": [
    "AIRLINE-AF"
  ],
  "segment_uuid": "61268299727527493760",
  "batch_no": "AF5319-20260907",
  "service_start_at": "2026-09-07T12:00:00Z",
  "service_end_at": "2026-09-07T14:37:07.381744Z"
}
```

Output:

```json
{
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "26699108493000982656",
    "email": "jessicacooper@example.com",
    "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
    "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_uuid": "06041993713794695296",
        "provider_items": [
          {
            "provider_item_uuid": "39876487618607726720",
            "provider_corp_external_id": "AIRLINE-AF",
            "batch_no": "AF5319-20260907",
            "qty": "2"
          }
        ],
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        }
      }
    ],
    "notes": "Updated via run_http_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-18T16:12:37.490071",
    "updated_by": "MCP",
    "updated_at": "2026-06-18T16:14:31.525931",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "created_quotes": [
    {
      "request_uuid": "26699108493000982656",
      "quote_uuid": "39412068575306858624",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-AF",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 900.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 900.0,
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
        "request_uuid": "26699108493000982656",
        "email": "jessicacooper@example.com",
        "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
        "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "item_name": "Flight ATL->ORD Premium Economy",
            "item_uuid": "06041993713794695296",
            "provider_items": [
              {
                "provider_item_uuid": "39876487618607726720",
                "provider_corp_external_id": "AIRLINE-AF",
                "batch_no": "AF5319-20260907",
                "qty": "2"
              }
            ],
            "qty": "2",
            "pax_breakdown": {
              "adult": "2"
            }
          }
        ],
        "notes": "Updated via run_http_integration.py",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-18T16:12:37.490071",
        "updated_by": "MCP",
        "updated_at": "2026-06-18T16:14:31.525931",
        "quotes": [
          {
            "final_total_quote_amount": "900",
            "provider_corp_external_id": "AIRLINE-AF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "in_progress",
            "total_quote_amount": "900",
            "total_quote_discount": "0",
            "created_at": "2026-06-18 16:14:39.837945",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "39412068575306858624",
            "request_uuid": "26699108493000982656",
            "updated_at": "2026-06-18 16:14:57.026095",
            "updated_by": "MCP"
          }
        ],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "batch_no": "AF5319-20260907",
          "created_at": "2026-06-18 16:14:47.683649",
          "final_subtotal": "900",
          "hold_expires_at": "2026-06-18 16:29:48.046544",
          "hold_token": "5fca8e71950450ba653bc04d6f88b99e",
          "item_uuid": "06041993713794695296",
          "partition_key": "gpt#nestaging",
          "pax_breakdown": {
            "adult": "2"
          },
          "price_per_uom": "450",
          "provider_item_uuid": "39876487618607726720",
          "qty": "2",
          "quote_item_uuid": "79136946166253502592",
          "quote_uuid": "39412068575306858624",
          "request_data": {
            "cancellation_policy_snapshot": {
              "tiers": {
                "tiers": [
                  {
                    "hours_before_departure_gte": "168",
                    "refund_pct": "1"
                  },
                  {
                    "hours_before_departure_gte": "24",
                    "refund_pct": "0.5"
                  },
                  {
                    "hours_before_departure_gte": "0",
                    "refund_pct": "0"
                  }
                ]
              },
              "notes_template_uuid": null,
              "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
              "label": "Premium Economy Fare Cancellation",
              "content_hash": "b161d765b3089e5e",
              "policy_uuid": "14167382355785826432",
              "snapshotted_at": "2026-06-18 16:14:48.324781"
            }
          },
          "request_uuid": "26699108493000982656",
          "subtotal": "900",
          "subtotal_discount": "0",
          "subtotal_native": "900",
          "updated_at": "2026-06-18 16:14:47.683649",
          "updated_by": "MCP"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "priority": "10",
          "status": "active",
          "conditions": [
            "is_refundable == false",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.614708",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
          "discount_prompt_uuid": "29118858989597114496",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "2.5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.614708",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'",
            "min_passengers >= 20",
            "loyalty_tier in ['gold', 'platinum']"
          ],
          "created_at": "2026-06-01 22:24:16.312582",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
          "discount_prompt_uuid": "39743702329131548800",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "5000"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.312582",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "7",
          "status": "active",
          "conditions": [
            "min_passengers >= 20",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.462599",
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
          "discount_prompt_uuid": "34741236891406844032",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "1000"
            },
            {
              "greater_than": "1000",
              "max_discount_percentage": "10",
              "less_than": "3500"
            },
            {
              "greater_than": "3500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.462599",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "6",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "min_passengers >= 10",
            "is_refundable == false"
          ],
          "created_at": "2026-06-01 22:24:16.923030",
          "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
          "discount_prompt_uuid": "81566856437527756928",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "500"
            },
            {
              "greater_than": "500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "segment",
          "tags": [
            "61268299727527493760"
          ],
          "updated_at": "2026-06-01 22:24:16.923030",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "5",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:18.730783",
          "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
          "discount_prompt_uuid": "87759969798493061248",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "2500"
            },
            {
              "greater_than": "2500",
              "max_discount_percentage": "10",
              "less_than": "7500"
            },
            {
              "greater_than": "7500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "item",
          "tags": [
            "06041993713794695296"
          ],
          "updated_at": "2026-06-01 22:24:18.730783",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'"
          ],
          "created_at": "2026-06-01 22:24:18.882404",
          "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
          "discount_prompt_uuid": "88308794075899773056",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5",
              "less_than": "20000"
            },
            {
              "greater_than": "20000",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scop
... (truncated)
```

### 11. quotes / get_quote

- Method: `get_quote`
- Status: `pass`
- Elapsed: `8694.7 ms`

Arguments:

```json
{
  "quote_uuid": "39412068575306858624",
  "request_uuid": "26699108493000982656"
}
```

Output:

```json
{
  "request_uuid": "26699108493000982656",
  "quote_uuid": "39412068575306858624",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-AF",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": null,
  "shipping_amount": 0.0,
  "total_quote_amount": 900.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 900.0,
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
    "request_uuid": "26699108493000982656",
    "email": "jessicacooper@example.com",
    "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
    "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_uuid": "06041993713794695296",
        "provider_items": [
          {
            "provider_item_uuid": "39876487618607726720",
            "provider_corp_external_id": "AIRLINE-AF",
            "batch_no": "AF5319-20260907",
            "qty": "2"
          }
        ],
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        }
      }
    ],
    "notes": "Updated via run_http_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-18T16:12:37.490071",
    "updated_by": "MCP",
    "updated_at": "2026-06-18T16:14:31.525931",
    "quotes": [
      {
        "final_total_quote_amount": "900",
        "provider_corp_external_id": "AIRLINE-AF",
        "rounds": "0",
        "shipping_amount": "0",
        "status": "in_progress",
        "total_quote_amount": "900",
        "total_quote_discount": "0",
        "created_at": "2026-06-18 16:14:39.837945",
        "partition_key": "gpt#nestaging",
        "quote_uuid": "39412068575306858624",
        "request_uuid": "26699108493000982656",
        "updated_at": "2026-06-18 16:14:57.026095",
        "updated_by": "MCP"
      }
    ],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "batch_no": "AF5319-20260907",
      "created_at": "2026-06-18 16:14:47.683649",
      "final_subtotal": "900",
      "hold_expires_at": "2026-06-18 16:29:48.046544",
      "hold_token": "5fca8e71950450ba653bc04d6f88b99e",
      "item_uuid": "06041993713794695296",
      "partition_key": "gpt#nestaging",
      "pax_breakdown": {
        "adult": "2"
      },
      "price_per_uom": "450",
      "provider_item_uuid": "39876487618607726720",
      "qty": "2",
      "quote_item_uuid": "79136946166253502592",
      "quote_uuid": "39412068575306858624",
      "request_data": {
        "cancellation_policy_snapshot": {
          "tiers": {
            "tiers": [
              {
                "hours_before_departure_gte": "168",
                "refund_pct": "1"
              },
              {
                "hours_before_departure_gte": "24",
                "refund_pct": "0.5"
              },
              {
                "hours_before_departure_gte": "0",
                "refund_pct": "0"
              }
            ]
          },
          "notes_template_uuid": null,
          "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
          "label": "Premium Economy Fare Cancellation",
          "content_hash": "b161d765b3089e5e",
          "policy_uuid": "14167382355785826432",
          "snapshotted_at": "2026-06-18 16:14:48.324781"
        }
      },
      "request_uuid": "26699108493000982656",
      "subtotal": "900",
      "subtotal_discount": "0",
      "subtotal_native": "900",
      "updated_at": "2026-06-18 16:14:47.683649",
      "updated_by": "MCP"
    }
  ],
  "installments": [],
  "discount_prompts": [
    {
      "priority": "10",
      "status": "active",
      "conditions": [
        "is_refundable == false",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.614708",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
      "discount_prompt_uuid": "29118858989597114496",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.614708",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'",
        "min_passengers >= 20",
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "created_at": "2026-06-01 22:24:16.312582",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
      "discount_prompt_uuid": "39743702329131548800",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "5000"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.312582",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "7",
      "status": "active",
      "conditions": [
        "min_passengers >= 20",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.462599",
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
      "discount_prompt_uuid": "34741236891406844032",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "10",
          "less_than": "3500"
        },
        {
          "greater_than": "3500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.462599",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "6",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "min_passengers >= 10",
        "is_refundable == false"
      ],
      "created_at": "2026-06-01 22:24:16.923030",
      "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
      "discount_prompt_uuid": "81566856437527756928",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "500"
        },
        {
          "greater_than": "500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "segment",
      "tags": [
        "61268299727527493760"
      ],
      "updated_at": "2026-06-01 22:24:16.923030",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "5",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:18.730783",
      "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
      "discount_prompt_uuid": "87759969798493061248",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "10",
          "less_than": "7500"
        },
        {
          "greater_than": "7500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "item",
      "tags": [
        "06041993713794695296"
      ],
      "updated_at": "2026-06-01 22:24:18.730783",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'"
      ],
      "created_at": "2026-06-01 22:24:18.882404",
      "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
      "discount_prompt_uuid": "88308794075899773056",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5",
          "less_than": "20000"
        },
        {
          "greater_than": "20000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "provider_item",
      "tags": [
        "39876487618607726720"
      ],
      "updated_at": "2026-06-01 22:24:18.882404",
      "updated_by": "prepare_discount_prompts"
    }
  ],
  "updated_by": "MCP",
  "created_at": "2026-06-18T16:14:39.837945",
  "updated_at": "2026-06-18T16:14:57.026095"
}
```

### 12. quotes / search_quotes

- Method: `search_quotes`
- Status: `pass`
- Elapsed: `8615.62 ms`

Arguments:

```json
{
  "request_uuid": "26699108493000982656",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": 10,
  "page_number": 1,
  "total": 1,
  "quote_list": [
    {
      "request_uuid": "26699108493000982656",
      "quote_uuid": "39412068575306858624",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-AF",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 900.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 900.0,
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
        "request_uuid": "26699108493000982656",
        "email": "jessicacooper@example.com",
        "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
        "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "item_name": "Flight ATL->ORD Premium Economy",
            "item_uuid": "06041993713794695296",
            "provider_items": [
              {
                "provider_item_uuid": "39876487618607726720",
                "provider_corp_external_id": "AIRLINE-AF",
                "batch_no": "AF5319-20260907",
                "qty": "2"
              }
            ],
            "qty": "2",
            "pax_breakdown": {
              "adult": "2"
            }
          }
        ],
        "notes": "Updated via run_http_integration.py",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-18T16:12:37.490071",
        "updated_by": "MCP",
        "updated_at": "2026-06-18T16:14:31.525931",
        "quotes": [
          {
            "final_total_quote_amount": "900",
            "provider_corp_external_id": "AIRLINE-AF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "in_progress",
            "total_quote_amount": "900",
            "total_quote_discount": "0",
            "created_at": "2026-06-18 16:14:39.837945",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "39412068575306858624",
            "request_uuid": "26699108493000982656",
            "updated_at": "2026-06-18 16:14:57.026095",
            "updated_by": "MCP"
          }
        ],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "batch_no": "AF5319-20260907",
          "created_at": "2026-06-18 16:14:47.683649",
          "final_subtotal": "900",
          "hold_expires_at": "2026-06-18 16:29:48.046544",
          "hold_token": "5fca8e71950450ba653bc04d6f88b99e",
          "item_uuid": "06041993713794695296",
          "partition_key": "gpt#nestaging",
          "pax_breakdown": {
            "adult": "2"
          },
          "price_per_uom": "450",
          "provider_item_uuid": "39876487618607726720",
          "qty": "2",
          "quote_item_uuid": "79136946166253502592",
          "quote_uuid": "39412068575306858624",
          "request_data": {
            "cancellation_policy_snapshot": {
              "tiers": {
                "tiers": [
                  {
                    "hours_before_departure_gte": "168",
                    "refund_pct": "1"
                  },
                  {
                    "hours_before_departure_gte": "24",
                    "refund_pct": "0.5"
                  },
                  {
                    "hours_before_departure_gte": "0",
                    "refund_pct": "0"
                  }
                ]
              },
              "notes_template_uuid": null,
              "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
              "label": "Premium Economy Fare Cancellation",
              "content_hash": "b161d765b3089e5e",
              "policy_uuid": "14167382355785826432",
              "snapshotted_at": "2026-06-18 16:14:48.324781"
            }
          },
          "request_uuid": "26699108493000982656",
          "subtotal": "900",
          "subtotal_discount": "0",
          "subtotal_native": "900",
          "updated_at": "2026-06-18 16:14:47.683649",
          "updated_by": "MCP"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "priority": "10",
          "status": "active",
          "conditions": [
            "is_refundable == false",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.614708",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
          "discount_prompt_uuid": "29118858989597114496",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "2.5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.614708",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'",
            "min_passengers >= 20",
            "loyalty_tier in ['gold', 'platinum']"
          ],
          "created_at": "2026-06-01 22:24:16.312582",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
          "discount_prompt_uuid": "39743702329131548800",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "5000"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.312582",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "7",
          "status": "active",
          "conditions": [
            "min_passengers >= 20",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.462599",
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
          "discount_prompt_uuid": "34741236891406844032",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "1000"
            },
            {
              "greater_than": "1000",
              "max_discount_percentage": "10",
              "less_than": "3500"
            },
            {
              "greater_than": "3500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.462599",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "6",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "min_passengers >= 10",
            "is_refundable == false"
          ],
          "created_at": "2026-06-01 22:24:16.923030",
          "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
          "discount_prompt_uuid": "81566856437527756928",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "500"
            },
            {
              "greater_than": "500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "segment",
          "tags": [
            "61268299727527493760"
          ],
          "updated_at": "2026-06-01 22:24:16.923030",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "5",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:18.730783",
          "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
          "discount_prompt_uuid": "87759969798493061248",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "2500"
            },
            {
              "greater_than": "2500",
              "max_discount_percentage": "10",
              "less_than": "7500"
            },
            {
              "greater_than": "7500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "item",
          "tags": [
            "06041993713794695296"
          ],
          "updated_at": "2026-06-01 22:24:18.730783",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'"
          ],
          "created_at": "2026-06-01 22:24:18.882404",
          "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
          "discount_prompt_uuid": "88308794075899773056",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5",
              "less_than": "20000"
            },
            {
              "greater_than": "20000",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "provider_item",
          "tags": [
            "39876487618607726720"
          ],
          "updated_at": "2026-06-01 22:24:18.882404",
          "updated_by": "prepare_discount_prompts"
        }
      ],
      "updated_by": "MCP",
      "created_at": "2026-06-18T16:14:39.837945",
      "updated_at": "2026-06-18T16:14:57.026095"
    }
  ]
}
```

### 13. quotes / update_quote

- Method: `update_quote`
- Status: `pass`
- Elapsed: `12819.25 ms`

Arguments:

```json
{
  "request_uuid": "26699108493000982656",
  "quote_uuid": "39412068575306858624",
  "notes": "Updated via HTTP integration test",
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0
}
```

Output:

```json
{
  "request_uuid": "26699108493000982656",
  "quote_uuid": "39412068575306858624",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-AF",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0,
  "total_quote_amount": 900.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 925.0,
  "currency": null,
  "display_currency": null,
  "fx_rate": null,
  "fx_rate_locked_at": null,
  "notes": "Updated via HTTP integration test",
  "status": "in_progress",
  "expired_at": null,
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "26699108493000982656",
    "email": "jessicacooper@example.com",
    "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
    "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_uuid": "06041993713794695296",
        "provider_items": [
          {
            "provider_item_uuid": "39876487618607726720",
            "provider_corp_external_id": "AIRLINE-AF",
            "batch_no": "AF5319-20260907",
            "qty": "2"
          }
        ],
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        }
      }
    ],
    "notes": "Updated via run_http_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-18T16:12:37.490071",
    "updated_by": "MCP",
    "updated_at": "2026-06-18T16:14:31.525931",
    "quotes": [
      {
        "final_total_quote_amount": "925",
        "provider_corp_external_id": "AIRLINE-AF",
        "rounds": "0",
        "shipping_amount": "25",
        "status": "in_progress",
        "total_quote_amount": "900",
        "total_quote_discount": "0",
        "created_at": "2026-06-18 16:14:39.837945",
        "notes": "Updated via HTTP integration test",
        "partition_key": "gpt#nestaging",
        "quote_uuid": "39412068575306858624",
        "request_uuid": "26699108493000982656",
        "shipping_method": "ticket_delivery",
        "updated_at": "2026-06-18 16:15:31.214329",
        "updated_by": "MCP"
      }
    ],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "batch_no": "AF5319-20260907",
      "created_at": "2026-06-18 16:14:47.683649",
      "final_subtotal": "900",
      "hold_expires_at": "2026-06-18 16:29:48.046544",
      "hold_token": "5fca8e71950450ba653bc04d6f88b99e",
      "item_uuid": "06041993713794695296",
      "partition_key": "gpt#nestaging",
      "pax_breakdown": {
        "adult": "2"
      },
      "price_per_uom": "450",
      "provider_item_uuid": "39876487618607726720",
      "qty": "2",
      "quote_item_uuid": "79136946166253502592",
      "quote_uuid": "39412068575306858624",
      "request_data": {
        "cancellation_policy_snapshot": {
          "tiers": {
            "tiers": [
              {
                "hours_before_departure_gte": "168",
                "refund_pct": "1"
              },
              {
                "hours_before_departure_gte": "24",
                "refund_pct": "0.5"
              },
              {
                "hours_before_departure_gte": "0",
                "refund_pct": "0"
              }
            ]
          },
          "notes_template_uuid": null,
          "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
          "label": "Premium Economy Fare Cancellation",
          "content_hash": "b161d765b3089e5e",
          "policy_uuid": "14167382355785826432",
          "snapshotted_at": "2026-06-18 16:14:48.324781"
        }
      },
      "request_uuid": "26699108493000982656",
      "subtotal": "900",
      "subtotal_discount": "0",
      "subtotal_native": "900",
      "updated_at": "2026-06-18 16:14:47.683649",
      "updated_by": "MCP"
    }
  ],
  "installments": [],
  "discount_prompts": [
    {
      "priority": "10",
      "status": "active",
      "conditions": [
        "is_refundable == false",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.614708",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
      "discount_prompt_uuid": "29118858989597114496",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.614708",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'",
        "min_passengers >= 20",
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "created_at": "2026-06-01 22:24:16.312582",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
      "discount_prompt_uuid": "39743702329131548800",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "5000"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.312582",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "7",
      "status": "active",
      "conditions": [
        "min_passengers >= 20",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.462599",
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
      "discount_prompt_uuid": "34741236891406844032",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "10",
          "less_than": "3500"
        },
        {
          "greater_than": "3500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.462599",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "6",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "min_passengers >= 10",
        "is_refundable == false"
      ],
      "created_at": "2026-06-01 22:24:16.923030",
      "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
      "discount_prompt_uuid": "81566856437527756928",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "500"
        },
        {
          "greater_than": "500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "segment",
      "tags": [
        "61268299727527493760"
      ],
      "updated_at": "2026-06-01 22:24:16.923030",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "5",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:18.730783",
      "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
      "discount_prompt_uuid": "87759969798493061248",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "10",
          "less_than": "7500"
        },
        {
          "greater_than": "7500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "item",
      "tags": [
        "06041993713794695296"
      ],
      "updated_at": "2026-06-01 22:24:18.730783",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'"
      ],
      "created_at": "2026-06-01 22:24:18.882404",
      "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
      "discount_prompt_uuid": "88308794075899773056",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5",
          "less_than": "20000"
        },
        {
          "greater_than": "20000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "provider_item",
      "tags": [
        "39876487618607726720"
      ],
      "updated_at": "2026-06-01 22:24:18.882404",
      "updated_by": "prepare_discount_prompts"
    }
  ],
  "updated_by": "MCP",
  "created_at": "2026-06-18T16:14:39.837945",
  "updated_at": "2026-06-18T16:15:31.214329"
}
```

### 14. quotes / update_quote_item

- Method: `update_quote_item`
- Status: `pass`
- Elapsed: `13132.58 ms`

Arguments:

```json
{
  "quote_uuid": "39412068575306858624",
  "quote_item_uuid": "79136946166253502592",
  "request_uuid": "26699108493000982656",
  "discount_amount": 50.0,
  "notes": "HTTP integration test discount"
}
```

Output:

```json
{
  "quote_uuid": "39412068575306858624",
  "quote_item_uuid": "79136946166253502592",
  "provider_item_uuid": "39876487618607726720",
  "item_uuid": "06041993713794695296",
  "partition_key": "gpt#nestaging",
  "batch_no": "AF5319-20260907",
  "request_uuid": "26699108493000982656",
  "qty": 2.0,
  "pax_breakdown": {
    "adult": "2"
  },
  "bundle_uuid": null,
  "bundle_label": null,
  "bundle_component_uuid": null,
  "price_per_uom": 450.0,
  "subtotal": 900.0,
  "subtotal_discount": 50.0,
  "final_subtotal": 850.0,
  "currency": null,
  "subtotal_native": 900.0,
  "notes": "HTTP integration test discount",
  "hold_token": "5fca8e71950450ba653bc04d6f88b99e",
  "hold_expires_at": "2026-06-18T16:29:48.046544",
  "guardrail_price_per_uom": 287.71,
  "slow_move_item": false,
  "quote": {
    "request_uuid": "26699108493000982656",
    "quote_uuid": "39412068575306858624",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-AF",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 900.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 875.0,
    "currency": null,
    "display_currency": null,
    "fx_rate": null,
    "fx_rate_locked_at": null,
    "notes": "Updated via HTTP integration test",
    "status": "in_progress",
    "expired_at": null,
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "26699108493000982656",
      "email": "jessicacooper@example.com",
      "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight ATL->ORD Premium Economy",
          "item_uuid": "06041993713794695296",
          "provider_items": [
            {
              "provider_item_uuid": "39876487618607726720",
              "provider_corp_external_id": "AIRLINE-AF",
              "batch_no": "AF5319-20260907",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_http_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-18T16:12:37.490071",
      "updated_by": "MCP",
      "updated_at": "2026-06-18T16:14:31.525931",
      "quotes": [
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "in_progress",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-18 16:14:39.837945",
          "notes": "Updated via HTTP integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "39412068575306858624",
          "request_uuid": "26699108493000982656",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 16:15:44.010849",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF5319-20260907",
        "created_at": "2026-06-18 16:14:47.683649",
        "final_subtotal": "850",
        "hold_expires_at": "2026-06-18 16:29:48.046544",
        "hold_token": "5fca8e71950450ba653bc04d6f88b99e",
        "item_uuid": "06041993713794695296",
        "notes": "HTTP integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "79136946166253502592",
        "quote_uuid": "39412068575306858624",
        "request_data": {
          "cancellation_policy_snapshot": {
            "tiers": {
              "tiers": [
                {
                  "hours_before_departure_gte": "168",
                  "refund_pct": "1"
                },
                {
                  "hours_before_departure_gte": "24",
                  "refund_pct": "0.5"
                },
                {
                  "hours_before_departure_gte": "0",
                  "refund_pct": "0"
                }
              ]
            },
            "notes_template_uuid": null,
            "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
            "label": "Premium Economy Fare Cancellation",
            "content_hash": "b161d765b3089e5e",
            "policy_uuid": "14167382355785826432",
            "snapshotted_at": "2026-06-18 16:14:48.324781"
          }
        },
        "request_uuid": "26699108493000982656",
        "subtotal": "900",
        "subtotal_discount": "50",
        "subtotal_native": "900",
        "updated_at": "2026-06-18 16:15:43.795845",
        "updated_by": "MCP"
      }
    ],
    "installments": [],
    "discount_prompts": [
      {
        "priority": "10",
        "status": "active",
        "conditions": [
          "is_refundable == false",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.614708",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
        "discount_prompt_uuid": "29118858989597114496",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.614708",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'",
          "min_passengers >= 20",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-01 22:24:16.312582",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
        "discount_prompt_uuid": "39743702329131548800",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "5000"
          },
          {
            "greater_than": "5000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.312582",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "7",
        "status": "active",
        "conditions": [
          "min_passengers >= 20",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.462599",
        "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
        "discount_prompt_uuid": "34741236891406844032",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "1000"
          },
          {
            "greater_than": "1000",
            "max_discount_percentage": "10",
            "less_than": "3500"
          },
          {
            "greater_than": "3500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.462599",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "6",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "min_passengers >= 10",
          "is_refundable == false"
        ],
        "created_at": "2026-06-01 22:24:16.923030",
        "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
        "discount_prompt_uuid": "81566856437527756928",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "500"
          },
          {
            "greater_than": "500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "segment",
        "tags": [
          "61268299727527493760"
        ],
        "updated_at": "2026-06-01 22:24:16.923030",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "5",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:18.730783",
        "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
        "discount_prompt_uuid": "87759969798493061248",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "item",
        "tags": [
          "06041993713794695296"
        ],
        "updated_at": "2026-06-01 22:24:18.730783",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'"
        ],
        "created_at": "2026-06-01 22:24:18.882404",
        "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
        "discount_prompt_uuid": "88308794075899773056",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5",
            "less_than": "20000"
          },
          {
            "greater_than": "20000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "provider_item",
        "tags": [
          "39876487618607726720"
        ],
        "updated_at": "2026-06-01 22:24:18.882404",
        "updated_by": "prepare_discount_prompts"
      }
    ],
    "updated_by": "MCP",
    "created_at": "2026-06-18T16:14:39.837945",
    "updated_at": "2026-06-18T16:15:44.010849"
  },
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
    
... (truncated)
```

### 15. installments / confirm_quote_and_create_installments

- Method: `confirm_quote_and_create_installments`
- Status: `pass`
- Elapsed: `36604.53 ms`

Arguments:

```json
{
  "request_uuid": "26699108493000982656",
  "quote_uuid": "39412068575306858624",
  "create_single_installment": true,
  "payment_method": "bank_transfer"
}
```

Output:

```json
{
  "quote": {
    "request_uuid": "26699108493000982656",
    "quote_uuid": "39412068575306858624",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-AF",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 900.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 875.0,
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
      "request_uuid": "26699108493000982656",
      "email": "jessicacooper@example.com",
      "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight ATL->ORD Premium Economy",
          "item_uuid": "06041993713794695296",
          "provider_items": [
            {
              "provider_item_uuid": "39876487618607726720",
              "provider_corp_external_id": "AIRLINE-AF",
              "batch_no": "AF5319-20260907",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_http_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-18T16:12:37.490071",
      "updated_by": "MCP",
      "updated_at": "2026-06-18T16:14:31.525931",
      "quotes": [
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-18 16:14:39.837945",
          "notes": "Updated via HTTP integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "39412068575306858624",
          "request_uuid": "26699108493000982656",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 16:16:00.998617",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF5319-20260907",
        "created_at": "2026-06-18 16:14:47.683649",
        "final_subtotal": "850",
        "hold_expires_at": "2026-06-18 16:29:48.046544",
        "hold_token": "5fca8e71950450ba653bc04d6f88b99e",
        "item_uuid": "06041993713794695296",
        "notes": "HTTP integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "79136946166253502592",
        "quote_uuid": "39412068575306858624",
        "request_data": {
          "cancellation_policy_snapshot": {
            "tiers": {
              "tiers": [
                {
                  "hours_before_departure_gte": "168",
                  "refund_pct": "1"
                },
                {
                  "hours_before_departure_gte": "24",
                  "refund_pct": "0.5"
                },
                {
                  "hours_before_departure_gte": "0",
                  "refund_pct": "0"
                }
              ]
            },
            "notes_template_uuid": null,
            "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
            "label": "Premium Economy Fare Cancellation",
            "content_hash": "b161d765b3089e5e",
            "policy_uuid": "14167382355785826432",
            "snapshotted_at": "2026-06-18 16:14:48.324781"
          }
        },
        "request_uuid": "26699108493000982656",
        "subtotal": "900",
        "subtotal_discount": "50",
        "subtotal_native": "900",
        "updated_at": "2026-06-18 16:15:43.795845",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "875",
        "installment_ratio": "100",
        "priority": "0",
        "status": "pending",
        "created_at": "2026-06-18 16:16:16.586931",
        "installment_uuid": "48140738447058944128",
        "partition_key": "gpt#nestaging",
        "payment_method": "bank_transfer",
        "quote_uuid": "39412068575306858624",
        "request_uuid": "26699108493000982656",
        "scheduled_date": "2026-06-18 16:16:13",
        "updated_at": "2026-06-18 16:16:16.586931",
        "updated_by": "MCP"
      }
    ],
    "discount_prompts": [
      {
        "priority": "10",
        "status": "active",
        "conditions": [
          "is_refundable == false",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.614708",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
        "discount_prompt_uuid": "29118858989597114496",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.614708",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'",
          "min_passengers >= 20",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-01 22:24:16.312582",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
        "discount_prompt_uuid": "39743702329131548800",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "5000"
          },
          {
            "greater_than": "5000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.312582",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "7",
        "status": "active",
        "conditions": [
          "min_passengers >= 20",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.462599",
        "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
        "discount_prompt_uuid": "34741236891406844032",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "1000"
          },
          {
            "greater_than": "1000",
            "max_discount_percentage": "10",
            "less_than": "3500"
          },
          {
            "greater_than": "3500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.462599",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "6",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "min_passengers >= 10",
          "is_refundable == false"
        ],
        "created_at": "2026-06-01 22:24:16.923030",
        "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
        "discount_prompt_uuid": "81566856437527756928",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "500"
          },
          {
            "greater_than": "500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "segment",
        "tags": [
          "61268299727527493760"
        ],
        "updated_at": "2026-06-01 22:24:16.923030",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "5",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:18.730783",
        "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
        "discount_prompt_uuid": "87759969798493061248",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "item",
        "tags": [
          "06041993713794695296"
        ],
        "updated_at": "2026-06-01 22:24:18.730783",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'"
        ],
        "created_at": "2026-06-01 22:24:18.882404",
        "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
        "discount_prompt_uuid": "88308794075899773056",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5",
            "less_than": "20000"
          },
          {
            "greater_than": "20000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "provider_item",
        "tags": [
          "39876487618607726720"
        ],
        "updated_at": "2026-06-01 22:24:18.882404",
        "updated_by": "prepare_discount_prompts"
      }
    ],
    "updated_by": "MCP",
    "created_at": "2026-06-18T16:14:39.837945",
    "updated_at": "2026-06-18T16:16:00.998617"
  },
  "installments": [
    {
      "quote_uuid": "39412068575306858624",
      "installment_uuid": "48140738447058944128",
      "request_uuid": "26699108493000982656",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 875.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-18T16:16:13",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-18T16:16:16.586931",
      "updated_at": "2026-06-18T16:16:16.586931",
      "quote": {
        "request_uuid": "26699108493000982656",
        "quote_uuid": "39412068575306858624",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_
... (truncated)
```

### 16. installments / get_installments

- Method: `get_installments`
- Status: `pass`
- Elapsed: `8536.9 ms`

Arguments:

```json
{
  "quote_uuid": "39412068575306858624",
  "limit": 10,
  "page_number": 1
}
```

Output:

```json
{
  "page_size": 10,
  "page_number": 1,
  "total": 1,
  "installment_list": [
    {
      "quote_uuid": "39412068575306858624",
      "installment_uuid": "48140738447058944128",
      "request_uuid": "26699108493000982656",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 875.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-18T16:16:13",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-18T16:16:16.586931",
      "updated_at": "2026-06-18T16:16:16.586931",
      "quote": {
        "request_uuid": "26699108493000982656",
        "quote_uuid": "39412068575306858624",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_id": "AIRLINE-AF",
        "sales_rep_email": null,
        "rounds": 0,
        "shipping_method": "ticket_delivery",
        "shipping_amount": 25.0,
        "total_quote_amount": 900.0,
        "total_quote_discount": 50.0,
        "final_total_quote_amount": 875.0,
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
          "request_uuid": "26699108493000982656",
          "email": "jessicacooper@example.com",
          "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
          "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
          "billing_address": null,
          "shipping_address": null,
          "items": [
            {
              "item_name": "Flight ATL->ORD Premium Economy",
              "item_uuid": "06041993713794695296",
              "provider_items": [
                {
                  "provider_item_uuid": "39876487618607726720",
                  "provider_corp_external_id": "AIRLINE-AF",
                  "batch_no": "AF5319-20260907",
                  "qty": "2"
                }
              ],
              "qty": "2",
              "pax_breakdown": {
                "adult": "2"
              }
            }
          ],
          "notes": "Updated via run_http_integration.py",
          "bundle_uuid": null,
          "status": "confirmed",
          "expired_at": "2026-12-31T23:59:59",
          "created_at": "2026-06-18T16:12:37.490071",
          "updated_by": "MCP",
          "updated_at": "2026-06-18T16:14:31.525931",
          "quotes": [
            {
              "final_total_quote_amount": "875",
              "provider_corp_external_id": "AIRLINE-AF",
              "rounds": "0",
              "shipping_amount": "25",
              "status": "confirmed",
              "total_quote_amount": "900",
              "total_quote_discount": "50",
              "created_at": "2026-06-18 16:14:39.837945",
              "notes": "Updated via HTTP integration test",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "39412068575306858624",
              "request_uuid": "26699108493000982656",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-18 16:16:00.998617",
              "updated_by": "MCP"
            }
          ],
          "files": [],
          "bundle": null
        },
        "quote_items": [
          {
            "batch_no": "AF5319-20260907",
            "created_at": "2026-06-18 16:14:47.683649",
            "final_subtotal": "850",
            "hold_expires_at": "2026-06-18 16:29:48.046544",
            "hold_token": "5fca8e71950450ba653bc04d6f88b99e",
            "item_uuid": "06041993713794695296",
            "notes": "HTTP integration test discount",
            "partition_key": "gpt#nestaging",
            "pax_breakdown": {
              "adult": "2"
            },
            "price_per_uom": "450",
            "provider_item_uuid": "39876487618607726720",
            "qty": "2",
            "quote_item_uuid": "79136946166253502592",
            "quote_uuid": "39412068575306858624",
            "request_data": {
              "cancellation_policy_snapshot": {
                "tiers": {
                  "tiers": [
                    {
                      "hours_before_departure_gte": "168",
                      "refund_pct": "1"
                    },
                    {
                      "hours_before_departure_gte": "24",
                      "refund_pct": "0.5"
                    },
                    {
                      "hours_before_departure_gte": "0",
                      "refund_pct": "0"
                    }
                  ]
                },
                "notes_template_uuid": null,
                "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
                "label": "Premium Economy Fare Cancellation",
                "content_hash": "b161d765b3089e5e",
                "policy_uuid": "14167382355785826432",
                "snapshotted_at": "2026-06-18 16:14:48.324781"
              }
            },
            "request_uuid": "26699108493000982656",
            "subtotal": "900",
            "subtotal_discount": "50",
            "subtotal_native": "900",
            "updated_at": "2026-06-18 16:15:43.795845",
            "updated_by": "MCP"
          }
        ],
        "installments": [
          {
            "installment_amount": "875",
            "installment_ratio": "100",
            "priority": "0",
            "status": "pending",
            "created_at": "2026-06-18 16:16:16.586931",
            "installment_uuid": "48140738447058944128",
            "partition_key": "gpt#nestaging",
            "payment_method": "bank_transfer",
            "quote_uuid": "39412068575306858624",
            "request_uuid": "26699108493000982656",
            "scheduled_date": "2026-06-18 16:16:13",
            "updated_at": "2026-06-18 16:16:16.586931",
            "updated_by": "MCP"
          }
        ],
        "discount_prompts": [
          {
            "priority": "10",
            "status": "active",
            "conditions": [
              "is_refundable == false",
              "channel == 'direct'"
            ],
            "created_at": "2026-06-01 22:24:16.614708",
            "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
            "discount_prompt_uuid": "29118858989597114496",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "2.5",
                "less_than": "10000"
              },
              {
                "greater_than": "10000",
                "max_discount_percentage": "7.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-01 22:24:16.614708",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "2",
            "status": "active",
            "conditions": [
              "season != 'peak'",
              "min_passengers >= 20",
              "loyalty_tier in ['gold', 'platinum']"
            ],
            "created_at": "2026-06-01 22:24:16.312582",
            "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
            "discount_prompt_uuid": "39743702329131548800",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "5",
                "less_than": "5000"
              },
              {
                "greater_than": "5000",
                "max_discount_percentage": "10"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-01 22:24:16.312582",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "7",
            "status": "active",
            "conditions": [
              "min_passengers >= 20",
              "channel == 'direct'"
            ],
            "created_at": "2026-06-01 22:24:16.462599",
            "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
            "discount_prompt_uuid": "34741236891406844032",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "7.5",
                "less_than": "1000"
              },
              {
                "greater_than": "1000",
                "max_discount_percentage": "10",
                "less_than": "3500"
              },
              {
                "greater_than": "3500",
                "max_discount_percentage": "12.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "global",
            "tags": [],
            "updated_at": "2026-06-01 22:24:16.462599",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "6",
            "status": "active",
            "conditions": [
              "payment_method in ['wire_transfer', 'credit_card']",
              "min_passengers >= 10",
              "is_refundable == false"
            ],
            "created_at": "2026-06-01 22:24:16.923030",
            "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
            "discount_prompt_uuid": "81566856437527756928",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "7.5",
                "less_than": "500"
              },
              {
                "greater_than": "500",
                "max_discount_percentage": "12.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "segment",
            "tags": [
              "61268299727527493760"
            ],
            "updated_at": "2026-06-01 22:24:16.923030",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "5",
            "status": "active",
            "conditions": [
              "payment_method in ['wire_transfer', 'credit_card']",
              "channel == 'direct'"
            ],
            "created_at": "2026-06-01 22:24:18.730783",
            "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
            "discount_prompt_uuid": "87759969798493061248",
            "discount_rules": [
              {
                "greater_than": "0",
                "max_discount_percentage": "7.5",
                "less_than": "2500"
              },
              {
                "greater_than": "2500",
                "max_discount_percentage": "10",
                "less_than": "7500"
              },
              {
                "greater_than": "7500",
                "max_discount_percentage": "12.5"
              }
            ],
            "partition_key": "gpt#nestaging",
            "scope": "item",
            "tags": [
              "06041993713794695296"
            ],
            "updated_at": "2026-06-01 22:24:18.730783",
            "updated_by": "prepare_discount_prompts"
          },
          {
            "priority": "2",
            "status": "active",
            "conditions": [
   
... (truncated)
```

### 17. installments / setup submit_rfq_request (create_installment)

- Method: `submit_rfq_request`
- Status: `pass`
- Elapsed: `8237.28 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "request_title": "HTTP installment setup (create_installment): Flight ATL->ORD Premium Economy",
  "request_description": "Setup request for standalone installment tool validation",
  "items": [
    {
      "item_uuid": "06041993713794695296",
      "item_name": "Flight ATL->ORD Premium Economy",
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
  "request_uuid": "06621945833049833600",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP installment setup (create_installment): Flight ATL->ORD Premium Economy",
  "request_description": "Setup request for standalone installment tool validation",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "qty": "1",
      "pax_breakdown": {
        "adult": "1"
      }
    }
  ],
  "notes": "Created by run_http_integration.py for create_installment",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:16:37.927649",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:16:37.927649",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 18. installments / setup assign_provider_item_to_request_item (create_installment)

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `15003.57 ms`

Arguments:

```json
{
  "request_uuid": "06621945833049833600",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720",
  "provider_corp_external_id": "AIRLINE-AF",
  "qty": 1,
  "batch_no": "AF5319-20260907"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "06621945833049833600",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP installment setup (create_installment): Flight ATL->ORD Premium Economy",
  "request_description": "Setup request for standalone installment tool validation",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "provider_items": [
        {
          "provider_item_uuid": "39876487618607726720",
          "provider_corp_external_id": "AIRLINE-AF",
          "batch_no": "AF5319-20260907",
          "qty": "1"
        }
      ],
      "qty": "1",
      "pax_breakdown": {
        "adult": "1"
      }
    }
  ],
  "notes": "Created by run_http_integration.py for create_installment",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:16:37.927649",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:16:52.944729",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 19. installments / setup confirm_request_and_create_quotes (create_installment)

- Method: `confirm_request_and_create_quotes`
- Status: `pass`
- Elapsed: `43124.42 ms`

Arguments:

```json
{
  "request_uuid": "06621945833049833600",
  "provider_corp_external_ids": [
    "AIRLINE-AF"
  ],
  "segment_uuid": "61268299727527493760",
  "batch_no": "AF5319-20260907",
  "service_start_at": "2026-09-07T12:00:00Z",
  "service_end_at": "2026-09-07T14:37:07.381744Z"
}
```

Output:

```json
{
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "06621945833049833600",
    "email": "jessicacooper@example.com",
    "request_title": "HTTP installment setup (create_installment): Flight ATL->ORD Premium Economy",
    "request_description": "Setup request for standalone installment tool validation",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_uuid": "06041993713794695296",
        "provider_items": [
          {
            "provider_item_uuid": "39876487618607726720",
            "provider_corp_external_id": "AIRLINE-AF",
            "batch_no": "AF5319-20260907",
            "qty": "1"
          }
        ],
        "qty": "1",
        "pax_breakdown": {
          "adult": "1"
        }
      }
    ],
    "notes": "Created by run_http_integration.py for create_installment",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-18T16:16:37.927649",
    "updated_by": "MCP",
    "updated_at": "2026-06-18T16:17:08.121377",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "created_quotes": [
    {
      "request_uuid": "06621945833049833600",
      "quote_uuid": "77141716998417301632",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-AF",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 450.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 450.0,
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
        "request_uuid": "06621945833049833600",
        "email": "jessicacooper@example.com",
        "request_title": "HTTP installment setup (create_installment): Flight ATL->ORD Premium Economy",
        "request_description": "Setup request for standalone installment tool validation",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "item_name": "Flight ATL->ORD Premium Economy",
            "item_uuid": "06041993713794695296",
            "provider_items": [
              {
                "provider_item_uuid": "39876487618607726720",
                "provider_corp_external_id": "AIRLINE-AF",
                "batch_no": "AF5319-20260907",
                "qty": "1"
              }
            ],
            "qty": "1",
            "pax_breakdown": {
              "adult": "1"
            }
          }
        ],
        "notes": "Created by run_http_integration.py for create_installment",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-18T16:16:37.927649",
        "updated_by": "MCP",
        "updated_at": "2026-06-18T16:17:08.121377",
        "quotes": [
          {
            "final_total_quote_amount": "450",
            "provider_corp_external_id": "AIRLINE-AF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "in_progress",
            "total_quote_amount": "450",
            "total_quote_discount": "0",
            "created_at": "2026-06-18 16:17:15.497373",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "77141716998417301632",
            "request_uuid": "06621945833049833600",
            "updated_at": "2026-06-18 16:17:32.159392",
            "updated_by": "MCP"
          }
        ],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "batch_no": "AF5319-20260907",
          "created_at": "2026-06-18 16:17:23.278755",
          "final_subtotal": "450",
          "hold_expires_at": "2026-06-18 16:32:23.627100",
          "hold_token": "5b7ed59eeaccf290103b692778960480",
          "item_uuid": "06041993713794695296",
          "partition_key": "gpt#nestaging",
          "pax_breakdown": {
            "adult": "1"
          },
          "price_per_uom": "450",
          "provider_item_uuid": "39876487618607726720",
          "qty": "1",
          "quote_item_uuid": "59084417802051797120",
          "quote_uuid": "77141716998417301632",
          "request_data": {
            "cancellation_policy_snapshot": {
              "tiers": {
                "tiers": [
                  {
                    "hours_before_departure_gte": "168",
                    "refund_pct": "1"
                  },
                  {
                    "hours_before_departure_gte": "24",
                    "refund_pct": "0.5"
                  },
                  {
                    "hours_before_departure_gte": "0",
                    "refund_pct": "0"
                  }
                ]
              },
              "notes_template_uuid": null,
              "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
              "label": "Premium Economy Fare Cancellation",
              "content_hash": "b161d765b3089e5e",
              "policy_uuid": "14167382355785826432",
              "snapshotted_at": "2026-06-18 16:17:23.869985"
            }
          },
          "request_uuid": "06621945833049833600",
          "subtotal": "450",
          "subtotal_discount": "0",
          "subtotal_native": "450",
          "updated_at": "2026-06-18 16:17:23.278755",
          "updated_by": "MCP"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "priority": "10",
          "status": "active",
          "conditions": [
            "is_refundable == false",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.614708",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
          "discount_prompt_uuid": "29118858989597114496",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "2.5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.614708",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'",
            "min_passengers >= 20",
            "loyalty_tier in ['gold', 'platinum']"
          ],
          "created_at": "2026-06-01 22:24:16.312582",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
          "discount_prompt_uuid": "39743702329131548800",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "5000"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.312582",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "7",
          "status": "active",
          "conditions": [
            "min_passengers >= 20",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.462599",
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
          "discount_prompt_uuid": "34741236891406844032",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "1000"
            },
            {
              "greater_than": "1000",
              "max_discount_percentage": "10",
              "less_than": "3500"
            },
            {
              "greater_than": "3500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.462599",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "6",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "min_passengers >= 10",
            "is_refundable == false"
          ],
          "created_at": "2026-06-01 22:24:16.923030",
          "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
          "discount_prompt_uuid": "81566856437527756928",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "500"
            },
            {
              "greater_than": "500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "segment",
          "tags": [
            "61268299727527493760"
          ],
          "updated_at": "2026-06-01 22:24:16.923030",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "5",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:18.730783",
          "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
          "discount_prompt_uuid": "87759969798493061248",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "2500"
            },
            {
              "greater_than": "2500",
              "max_discount_percentage": "10",
              "less_than": "7500"
            },
            {
              "greater_than": "7500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "item",
          "tags": [
            "06041993713794695296"
          ],
          "updated_at": "2026-06-01 22:24:18.730783",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'"
          ],
          "created_at": "2026-06-01 22:24:18.882404",
          "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
          "discount_prompt_uuid": "88308794075899773056",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5",
              "less_than": "20000"
            },
            {
              "greater_than": "20000",
              "max_discount_percentage": "10"
            }
  
... (truncated)
```

### 20. installments / setup update_quote confirmed (create_installment)

- Method: `update_quote`
- Status: `pass`
- Elapsed: `11918.58 ms`

Arguments:

```json
{
  "request_uuid": "06621945833049833600",
  "quote_uuid": "77141716998417301632",
  "status": "confirmed",
  "notes": "Confirmed setup quote for create_installment"
}
```

Output:

```json
{
  "request_uuid": "06621945833049833600",
  "quote_uuid": "77141716998417301632",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-AF",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": null,
  "shipping_amount": 0.0,
  "total_quote_amount": 450.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 450.0,
  "currency": null,
  "display_currency": null,
  "fx_rate": null,
  "fx_rate_locked_at": null,
  "notes": "Confirmed setup quote for create_installment",
  "status": "confirmed",
  "expired_at": null,
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "06621945833049833600",
    "email": "jessicacooper@example.com",
    "request_title": "HTTP installment setup (create_installment): Flight ATL->ORD Premium Economy",
    "request_description": "Setup request for standalone installment tool validation",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_uuid": "06041993713794695296",
        "provider_items": [
          {
            "provider_item_uuid": "39876487618607726720",
            "provider_corp_external_id": "AIRLINE-AF",
            "batch_no": "AF5319-20260907",
            "qty": "1"
          }
        ],
        "qty": "1",
        "pax_breakdown": {
          "adult": "1"
        }
      }
    ],
    "notes": "Created by run_http_integration.py for create_installment",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-18T16:16:37.927649",
    "updated_by": "MCP",
    "updated_at": "2026-06-18T16:17:08.121377",
    "quotes": [
      {
        "final_total_quote_amount": "450",
        "provider_corp_external_id": "AIRLINE-AF",
        "rounds": "0",
        "shipping_amount": "0",
        "status": "confirmed",
        "total_quote_amount": "450",
        "total_quote_discount": "0",
        "created_at": "2026-06-18 16:17:15.497373",
        "notes": "Confirmed setup quote for create_installment",
        "partition_key": "gpt#nestaging",
        "quote_uuid": "77141716998417301632",
        "request_uuid": "06621945833049833600",
        "updated_at": "2026-06-18 16:17:47.798727",
        "updated_by": "MCP"
      }
    ],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "batch_no": "AF5319-20260907",
      "created_at": "2026-06-18 16:17:23.278755",
      "final_subtotal": "450",
      "hold_expires_at": "2026-06-18 16:32:23.627100",
      "hold_token": "5b7ed59eeaccf290103b692778960480",
      "item_uuid": "06041993713794695296",
      "partition_key": "gpt#nestaging",
      "pax_breakdown": {
        "adult": "1"
      },
      "price_per_uom": "450",
      "provider_item_uuid": "39876487618607726720",
      "qty": "1",
      "quote_item_uuid": "59084417802051797120",
      "quote_uuid": "77141716998417301632",
      "request_data": {
        "cancellation_policy_snapshot": {
          "tiers": {
            "tiers": [
              {
                "hours_before_departure_gte": "168",
                "refund_pct": "1"
              },
              {
                "hours_before_departure_gte": "24",
                "refund_pct": "0.5"
              },
              {
                "hours_before_departure_gte": "0",
                "refund_pct": "0"
              }
            ]
          },
          "notes_template_uuid": null,
          "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
          "label": "Premium Economy Fare Cancellation",
          "content_hash": "b161d765b3089e5e",
          "policy_uuid": "14167382355785826432",
          "snapshotted_at": "2026-06-18 16:17:23.869985"
        }
      },
      "request_uuid": "06621945833049833600",
      "subtotal": "450",
      "subtotal_discount": "0",
      "subtotal_native": "450",
      "updated_at": "2026-06-18 16:17:23.278755",
      "updated_by": "MCP"
    }
  ],
  "installments": [],
  "discount_prompts": [
    {
      "priority": "10",
      "status": "active",
      "conditions": [
        "is_refundable == false",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.614708",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
      "discount_prompt_uuid": "29118858989597114496",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.614708",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'",
        "min_passengers >= 20",
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "created_at": "2026-06-01 22:24:16.312582",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
      "discount_prompt_uuid": "39743702329131548800",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "5000"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.312582",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "7",
      "status": "active",
      "conditions": [
        "min_passengers >= 20",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.462599",
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
      "discount_prompt_uuid": "34741236891406844032",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "10",
          "less_than": "3500"
        },
        {
          "greater_than": "3500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.462599",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "6",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "min_passengers >= 10",
        "is_refundable == false"
      ],
      "created_at": "2026-06-01 22:24:16.923030",
      "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
      "discount_prompt_uuid": "81566856437527756928",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "500"
        },
        {
          "greater_than": "500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "segment",
      "tags": [
        "61268299727527493760"
      ],
      "updated_at": "2026-06-01 22:24:16.923030",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "5",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:18.730783",
      "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
      "discount_prompt_uuid": "87759969798493061248",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "10",
          "less_than": "7500"
        },
        {
          "greater_than": "7500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "item",
      "tags": [
        "06041993713794695296"
      ],
      "updated_at": "2026-06-01 22:24:18.730783",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'"
      ],
      "created_at": "2026-06-01 22:24:18.882404",
      "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
      "discount_prompt_uuid": "88308794075899773056",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5",
          "less_than": "20000"
        },
        {
          "greater_than": "20000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "provider_item",
      "tags": [
        "39876487618607726720"
      ],
      "updated_at": "2026-06-01 22:24:18.882404",
      "updated_by": "prepare_discount_prompts"
    }
  ],
  "updated_by": "MCP",
  "created_at": "2026-06-18T16:17:15.497373",
  "updated_at": "2026-06-18T16:17:47.798727"
}
```

### 21. installments / create_installment

- Method: `create_installment`
- Status: `pass`
- Elapsed: `15426.27 ms`

Arguments:

```json
{
  "quote_uuid": "77141716998417301632",
  "request_uuid": "06621945833049833600",
  "installment_amount": 100.0,
  "payment_method": "credit_card"
}
```

Output:

```json
{
  "quote_uuid": "77141716998417301632",
  "installment_uuid": "30183336511305433216",
  "request_uuid": "06621945833049833600",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 100.0,
  "installment_ratio": 22.22222222222222,
  "salesorder_no": null,
  "scheduled_date": "2026-06-18T16:17:59",
  "payment_method": "credit_card",
  "status": "pending",
  "updated_by": "MCP",
  "created_at": "2026-06-18T16:18:02.972720",
  "updated_at": "2026-06-18T16:18:02.972720",
  "quote": {
    "request_uuid": "06621945833049833600",
    "quote_uuid": "77141716998417301632",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-AF",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": null,
    "shipping_amount": 0.0,
    "total_quote_amount": 450.0,
    "total_quote_discount": 0.0,
    "final_total_quote_amount": 450.0,
    "currency": null,
    "display_currency": null,
    "fx_rate": null,
    "fx_rate_locked_at": null,
    "notes": "Confirmed setup quote for create_installment",
    "status": "confirmed",
    "expired_at": null,
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "06621945833049833600",
      "email": "jessicacooper@example.com",
      "request_title": "HTTP installment setup (create_installment): Flight ATL->ORD Premium Economy",
      "request_description": "Setup request for standalone installment tool validation",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight ATL->ORD Premium Economy",
          "item_uuid": "06041993713794695296",
          "provider_items": [
            {
              "provider_item_uuid": "39876487618607726720",
              "provider_corp_external_id": "AIRLINE-AF",
              "batch_no": "AF5319-20260907",
              "qty": "1"
            }
          ],
          "qty": "1",
          "pax_breakdown": {
            "adult": "1"
          }
        }
      ],
      "notes": "Created by run_http_integration.py for create_installment",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-18T16:16:37.927649",
      "updated_by": "MCP",
      "updated_at": "2026-06-18T16:17:08.121377",
      "quotes": [
        {
          "final_total_quote_amount": "450",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "0",
          "status": "confirmed",
          "total_quote_amount": "450",
          "total_quote_discount": "0",
          "created_at": "2026-06-18 16:17:15.497373",
          "notes": "Confirmed setup quote for create_installment",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "77141716998417301632",
          "request_uuid": "06621945833049833600",
          "updated_at": "2026-06-18 16:17:47.798727",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF5319-20260907",
        "created_at": "2026-06-18 16:17:23.278755",
        "final_subtotal": "450",
        "hold_expires_at": "2026-06-18 16:32:23.627100",
        "hold_token": "5b7ed59eeaccf290103b692778960480",
        "item_uuid": "06041993713794695296",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "1"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "1",
        "quote_item_uuid": "59084417802051797120",
        "quote_uuid": "77141716998417301632",
        "request_data": {
          "cancellation_policy_snapshot": {
            "tiers": {
              "tiers": [
                {
                  "hours_before_departure_gte": "168",
                  "refund_pct": "1"
                },
                {
                  "hours_before_departure_gte": "24",
                  "refund_pct": "0.5"
                },
                {
                  "hours_before_departure_gte": "0",
                  "refund_pct": "0"
                }
              ]
            },
            "notes_template_uuid": null,
            "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
            "label": "Premium Economy Fare Cancellation",
            "content_hash": "b161d765b3089e5e",
            "policy_uuid": "14167382355785826432",
            "snapshotted_at": "2026-06-18 16:17:23.869985"
          }
        },
        "request_uuid": "06621945833049833600",
        "subtotal": "450",
        "subtotal_discount": "0",
        "subtotal_native": "450",
        "updated_at": "2026-06-18 16:17:23.278755",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "100",
        "installment_ratio": "22.22222222222222",
        "priority": "0",
        "status": "pending",
        "created_at": "2026-06-18 16:18:02.972720",
        "installment_uuid": "30183336511305433216",
        "partition_key": "gpt#nestaging",
        "payment_method": "credit_card",
        "quote_uuid": "77141716998417301632",
        "request_uuid": "06621945833049833600",
        "scheduled_date": "2026-06-18 16:17:59",
        "updated_at": "2026-06-18 16:18:02.972720",
        "updated_by": "MCP"
      }
    ],
    "discount_prompts": [
      {
        "priority": "10",
        "status": "active",
        "conditions": [
          "is_refundable == false",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.614708",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
        "discount_prompt_uuid": "29118858989597114496",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.614708",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'",
          "min_passengers >= 20",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-01 22:24:16.312582",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
        "discount_prompt_uuid": "39743702329131548800",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "5000"
          },
          {
            "greater_than": "5000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.312582",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "7",
        "status": "active",
        "conditions": [
          "min_passengers >= 20",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.462599",
        "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
        "discount_prompt_uuid": "34741236891406844032",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "1000"
          },
          {
            "greater_than": "1000",
            "max_discount_percentage": "10",
            "less_than": "3500"
          },
          {
            "greater_than": "3500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.462599",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "6",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "min_passengers >= 10",
          "is_refundable == false"
        ],
        "created_at": "2026-06-01 22:24:16.923030",
        "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
        "discount_prompt_uuid": "81566856437527756928",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "500"
          },
          {
            "greater_than": "500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "segment",
        "tags": [
          "61268299727527493760"
        ],
        "updated_at": "2026-06-01 22:24:16.923030",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "5",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:18.730783",
        "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
        "discount_prompt_uuid": "87759969798493061248",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "item",
        "tags": [
          "06041993713794695296"
        ],
        "updated_at": "2026-06-01 22:24:18.730783",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'"
        ],
        "created_at": "2026-06-01 22:24:18.882404",
        "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
        "discount_prompt_uuid": "88308794075899773056",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5",
            "less_than": "20000"
          },
          {
            "greater_than": "20000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "provider_item",
        "tags": [
          "39876487618607726720"
        ],
        "updated_at": "2026-06-01 22:24:18.882404",
        "updated_by": "prepare_discount_prompts"
      }
    ],
    "updated_by": "MCP",
    "created_at": "2026-06-18T16:17:15.497373",
    "updated_at": "2026-06-18T16:17:47.798727"
  }
}
```

### 22. installments / setup submit_rfq_request (create_installments)

- Method: `submit_rfq_request`
- Status: `pass`
- Elapsed: `7931.02 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "request_title": "HTTP installment setup (create_installments): Flight ATL->ORD Premium Economy",
  "request_description": "Setup request for standalone installment tool validation",
  "items": [
    {
      "item_uuid": "06041993713794695296",
      "item_name": "Flight ATL->ORD Premium Economy",
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
  "request_uuid": "60148758433262223488",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP installment setup (create_installments): Flight ATL->ORD Premium Economy",
  "request_description": "Setup request for standalone installment tool validation",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "qty": "1",
      "pax_breakdown": {
        "adult": "1"
      }
    }
  ],
  "notes": "Created by run_http_integration.py for create_installments",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:18:11.277177",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:18:11.277177",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 23. installments / setup assign_provider_item_to_request_item (create_installments)

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `14785.41 ms`

Arguments:

```json
{
  "request_uuid": "60148758433262223488",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720",
  "provider_corp_external_id": "AIRLINE-AF",
  "qty": 1,
  "batch_no": "AF5319-20260907"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "60148758433262223488",
  "email": "jessicacooper@example.com",
  "request_title": "HTTP installment setup (create_installments): Flight ATL->ORD Premium Economy",
  "request_description": "Setup request for standalone installment tool validation",
  "billing_address": null,
  "shipping_address": null,
  "items": [
    {
      "item_name": "Flight ATL->ORD Premium Economy",
      "item_uuid": "06041993713794695296",
      "provider_items": [
        {
          "provider_item_uuid": "39876487618607726720",
          "provider_corp_external_id": "AIRLINE-AF",
          "batch_no": "AF5319-20260907",
          "qty": "1"
        }
      ],
      "qty": "1",
      "pax_breakdown": {
        "adult": "1"
      }
    }
  ],
  "notes": "Created by run_http_integration.py for create_installments",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-18T16:18:11.277177",
  "updated_by": "MCP",
  "updated_at": "2026-06-18T16:18:26.163618",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 24. installments / setup confirm_request_and_create_quotes (create_installments)

- Method: `confirm_request_and_create_quotes`
- Status: `pass`
- Elapsed: `43824.38 ms`

Arguments:

```json
{
  "request_uuid": "60148758433262223488",
  "provider_corp_external_ids": [
    "AIRLINE-AF"
  ],
  "segment_uuid": "61268299727527493760",
  "batch_no": "AF5319-20260907",
  "service_start_at": "2026-09-07T12:00:00Z",
  "service_end_at": "2026-09-07T14:37:07.381744Z"
}
```

Output:

```json
{
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "60148758433262223488",
    "email": "jessicacooper@example.com",
    "request_title": "HTTP installment setup (create_installments): Flight ATL->ORD Premium Economy",
    "request_description": "Setup request for standalone installment tool validation",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_uuid": "06041993713794695296",
        "provider_items": [
          {
            "provider_item_uuid": "39876487618607726720",
            "provider_corp_external_id": "AIRLINE-AF",
            "batch_no": "AF5319-20260907",
            "qty": "1"
          }
        ],
        "qty": "1",
        "pax_breakdown": {
          "adult": "1"
        }
      }
    ],
    "notes": "Created by run_http_integration.py for create_installments",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-18T16:18:11.277177",
    "updated_by": "MCP",
    "updated_at": "2026-06-18T16:18:41.187185",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "created_quotes": [
    {
      "request_uuid": "60148758433262223488",
      "quote_uuid": "09264210633191080064",
      "partition_key": "gpt#nestaging",
      "provider_corp_external_id": "AIRLINE-AF",
      "sales_rep_email": null,
      "rounds": 0,
      "shipping_method": null,
      "shipping_amount": 0.0,
      "total_quote_amount": 450.0,
      "total_quote_discount": 0.0,
      "final_total_quote_amount": 450.0,
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
        "request_uuid": "60148758433262223488",
        "email": "jessicacooper@example.com",
        "request_title": "HTTP installment setup (create_installments): Flight ATL->ORD Premium Economy",
        "request_description": "Setup request for standalone installment tool validation",
        "billing_address": null,
        "shipping_address": null,
        "items": [
          {
            "item_name": "Flight ATL->ORD Premium Economy",
            "item_uuid": "06041993713794695296",
            "provider_items": [
              {
                "provider_item_uuid": "39876487618607726720",
                "provider_corp_external_id": "AIRLINE-AF",
                "batch_no": "AF5319-20260907",
                "qty": "1"
              }
            ],
            "qty": "1",
            "pax_breakdown": {
              "adult": "1"
            }
          }
        ],
        "notes": "Created by run_http_integration.py for create_installments",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-18T16:18:11.277177",
        "updated_by": "MCP",
        "updated_at": "2026-06-18T16:18:41.187185",
        "quotes": [
          {
            "final_total_quote_amount": "450",
            "provider_corp_external_id": "AIRLINE-AF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "in_progress",
            "total_quote_amount": "450",
            "total_quote_discount": "0",
            "created_at": "2026-06-18 16:18:48.400984",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "09264210633191080064",
            "request_uuid": "60148758433262223488",
            "updated_at": "2026-06-18 16:19:05.451703",
            "updated_by": "MCP"
          }
        ],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "batch_no": "AF5319-20260907",
          "created_at": "2026-06-18 16:18:55.950238",
          "final_subtotal": "450",
          "hold_expires_at": "2026-06-18 16:33:56.282116",
          "hold_token": "d5b36e4f6b608c7f3bd8460c9bb01787",
          "item_uuid": "06041993713794695296",
          "partition_key": "gpt#nestaging",
          "pax_breakdown": {
            "adult": "1"
          },
          "price_per_uom": "450",
          "provider_item_uuid": "39876487618607726720",
          "qty": "1",
          "quote_item_uuid": "10029519510784983168",
          "quote_uuid": "09264210633191080064",
          "request_data": {
            "cancellation_policy_snapshot": {
              "tiers": {
                "tiers": [
                  {
                    "hours_before_departure_gte": "168",
                    "refund_pct": "1"
                  },
                  {
                    "hours_before_departure_gte": "24",
                    "refund_pct": "0.5"
                  },
                  {
                    "hours_before_departure_gte": "0",
                    "refund_pct": "0"
                  }
                ]
              },
              "notes_template_uuid": null,
              "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
              "label": "Premium Economy Fare Cancellation",
              "content_hash": "b161d765b3089e5e",
              "policy_uuid": "14167382355785826432",
              "snapshotted_at": "2026-06-18 16:18:56.525800"
            }
          },
          "request_uuid": "60148758433262223488",
          "subtotal": "450",
          "subtotal_discount": "0",
          "subtotal_native": "450",
          "updated_at": "2026-06-18 16:18:55.950238",
          "updated_by": "MCP"
        }
      ],
      "installments": [],
      "discount_prompts": [
        {
          "priority": "10",
          "status": "active",
          "conditions": [
            "is_refundable == false",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.614708",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
          "discount_prompt_uuid": "29118858989597114496",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "2.5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.614708",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'",
            "min_passengers >= 20",
            "loyalty_tier in ['gold', 'platinum']"
          ],
          "created_at": "2026-06-01 22:24:16.312582",
          "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
          "discount_prompt_uuid": "39743702329131548800",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "5000"
            },
            {
              "greater_than": "5000",
              "max_discount_percentage": "10"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.312582",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "7",
          "status": "active",
          "conditions": [
            "min_passengers >= 20",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:16.462599",
          "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
          "discount_prompt_uuid": "34741236891406844032",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "1000"
            },
            {
              "greater_than": "1000",
              "max_discount_percentage": "10",
              "less_than": "3500"
            },
            {
              "greater_than": "3500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "global",
          "tags": [],
          "updated_at": "2026-06-01 22:24:16.462599",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "6",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "min_passengers >= 10",
            "is_refundable == false"
          ],
          "created_at": "2026-06-01 22:24:16.923030",
          "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
          "discount_prompt_uuid": "81566856437527756928",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "500"
            },
            {
              "greater_than": "500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "segment",
          "tags": [
            "61268299727527493760"
          ],
          "updated_at": "2026-06-01 22:24:16.923030",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "5",
          "status": "active",
          "conditions": [
            "payment_method in ['wire_transfer', 'credit_card']",
            "channel == 'direct'"
          ],
          "created_at": "2026-06-01 22:24:18.730783",
          "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
          "discount_prompt_uuid": "87759969798493061248",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "7.5",
              "less_than": "2500"
            },
            {
              "greater_than": "2500",
              "max_discount_percentage": "10",
              "less_than": "7500"
            },
            {
              "greater_than": "7500",
              "max_discount_percentage": "12.5"
            }
          ],
          "partition_key": "gpt#nestaging",
          "scope": "item",
          "tags": [
            "06041993713794695296"
          ],
          "updated_at": "2026-06-01 22:24:18.730783",
          "updated_by": "prepare_discount_prompts"
        },
        {
          "priority": "2",
          "status": "active",
          "conditions": [
            "season != 'peak'"
          ],
          "created_at": "2026-06-01 22:24:18.882404",
          "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
          "discount_prompt_uuid": "88308794075899773056",
          "discount_rules": [
            {
              "greater_than": "0",
              "max_discount_percentage": "5",
              "less_than": "10000"
            },
            {
              "greater_than": "10000",
              "max_discount_percentage": "7.5",
              "less_than": "20000"
            },
            {
              "greater_than": "20000",
              "max_discount_percentage": "10"
            
... (truncated)
```

### 25. installments / setup update_quote confirmed (create_installments)

- Method: `update_quote`
- Status: `pass`
- Elapsed: `13283.86 ms`

Arguments:

```json
{
  "request_uuid": "60148758433262223488",
  "quote_uuid": "09264210633191080064",
  "status": "confirmed",
  "notes": "Confirmed setup quote for create_installments"
}
```

Output:

```json
{
  "request_uuid": "60148758433262223488",
  "quote_uuid": "09264210633191080064",
  "partition_key": "gpt#nestaging",
  "provider_corp_external_id": "AIRLINE-AF",
  "sales_rep_email": null,
  "rounds": 0,
  "shipping_method": null,
  "shipping_amount": 0.0,
  "total_quote_amount": 450.0,
  "total_quote_discount": 0.0,
  "final_total_quote_amount": 450.0,
  "currency": null,
  "display_currency": null,
  "fx_rate": null,
  "fx_rate_locked_at": null,
  "notes": "Confirmed setup quote for create_installments",
  "status": "confirmed",
  "expired_at": null,
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "60148758433262223488",
    "email": "jessicacooper@example.com",
    "request_title": "HTTP installment setup (create_installments): Flight ATL->ORD Premium Economy",
    "request_description": "Setup request for standalone installment tool validation",
    "billing_address": null,
    "shipping_address": null,
    "items": [
      {
        "item_name": "Flight ATL->ORD Premium Economy",
        "item_uuid": "06041993713794695296",
        "provider_items": [
          {
            "provider_item_uuid": "39876487618607726720",
            "provider_corp_external_id": "AIRLINE-AF",
            "batch_no": "AF5319-20260907",
            "qty": "1"
          }
        ],
        "qty": "1",
        "pax_breakdown": {
          "adult": "1"
        }
      }
    ],
    "notes": "Created by run_http_integration.py for create_installments",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-18T16:18:11.277177",
    "updated_by": "MCP",
    "updated_at": "2026-06-18T16:18:41.187185",
    "quotes": [
      {
        "final_total_quote_amount": "450",
        "provider_corp_external_id": "AIRLINE-AF",
        "rounds": "0",
        "shipping_amount": "0",
        "status": "confirmed",
        "total_quote_amount": "450",
        "total_quote_discount": "0",
        "created_at": "2026-06-18 16:18:48.400984",
        "notes": "Confirmed setup quote for create_installments",
        "partition_key": "gpt#nestaging",
        "quote_uuid": "09264210633191080064",
        "request_uuid": "60148758433262223488",
        "updated_at": "2026-06-18 16:19:23.013225",
        "updated_by": "MCP"
      }
    ],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "batch_no": "AF5319-20260907",
      "created_at": "2026-06-18 16:18:55.950238",
      "final_subtotal": "450",
      "hold_expires_at": "2026-06-18 16:33:56.282116",
      "hold_token": "d5b36e4f6b608c7f3bd8460c9bb01787",
      "item_uuid": "06041993713794695296",
      "partition_key": "gpt#nestaging",
      "pax_breakdown": {
        "adult": "1"
      },
      "price_per_uom": "450",
      "provider_item_uuid": "39876487618607726720",
      "qty": "1",
      "quote_item_uuid": "10029519510784983168",
      "quote_uuid": "09264210633191080064",
      "request_data": {
        "cancellation_policy_snapshot": {
          "tiers": {
            "tiers": [
              {
                "hours_before_departure_gte": "168",
                "refund_pct": "1"
              },
              {
                "hours_before_departure_gte": "24",
                "refund_pct": "0.5"
              },
              {
                "hours_before_departure_gte": "0",
                "refund_pct": "0"
              }
            ]
          },
          "notes_template_uuid": null,
          "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
          "label": "Premium Economy Fare Cancellation",
          "content_hash": "b161d765b3089e5e",
          "policy_uuid": "14167382355785826432",
          "snapshotted_at": "2026-06-18 16:18:56.525800"
        }
      },
      "request_uuid": "60148758433262223488",
      "subtotal": "450",
      "subtotal_discount": "0",
      "subtotal_native": "450",
      "updated_at": "2026-06-18 16:18:55.950238",
      "updated_by": "MCP"
    }
  ],
  "installments": [],
  "discount_prompts": [
    {
      "priority": "10",
      "status": "active",
      "conditions": [
        "is_refundable == false",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.614708",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
      "discount_prompt_uuid": "29118858989597114496",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "2.5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.614708",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'",
        "min_passengers >= 20",
        "loyalty_tier in ['gold', 'platinum']"
      ],
      "created_at": "2026-06-01 22:24:16.312582",
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
      "discount_prompt_uuid": "39743702329131548800",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "5000"
        },
        {
          "greater_than": "5000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.312582",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "7",
      "status": "active",
      "conditions": [
        "min_passengers >= 20",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:16.462599",
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
      "discount_prompt_uuid": "34741236891406844032",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "1000"
        },
        {
          "greater_than": "1000",
          "max_discount_percentage": "10",
          "less_than": "3500"
        },
        {
          "greater_than": "3500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "global",
      "tags": [],
      "updated_at": "2026-06-01 22:24:16.462599",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "6",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "min_passengers >= 10",
        "is_refundable == false"
      ],
      "created_at": "2026-06-01 22:24:16.923030",
      "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
      "discount_prompt_uuid": "81566856437527756928",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "500"
        },
        {
          "greater_than": "500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "segment",
      "tags": [
        "61268299727527493760"
      ],
      "updated_at": "2026-06-01 22:24:16.923030",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "5",
      "status": "active",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "channel == 'direct'"
      ],
      "created_at": "2026-06-01 22:24:18.730783",
      "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
      "discount_prompt_uuid": "87759969798493061248",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "7.5",
          "less_than": "2500"
        },
        {
          "greater_than": "2500",
          "max_discount_percentage": "10",
          "less_than": "7500"
        },
        {
          "greater_than": "7500",
          "max_discount_percentage": "12.5"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "item",
      "tags": [
        "06041993713794695296"
      ],
      "updated_at": "2026-06-01 22:24:18.730783",
      "updated_by": "prepare_discount_prompts"
    },
    {
      "priority": "2",
      "status": "active",
      "conditions": [
        "season != 'peak'"
      ],
      "created_at": "2026-06-01 22:24:18.882404",
      "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
      "discount_prompt_uuid": "88308794075899773056",
      "discount_rules": [
        {
          "greater_than": "0",
          "max_discount_percentage": "5",
          "less_than": "10000"
        },
        {
          "greater_than": "10000",
          "max_discount_percentage": "7.5",
          "less_than": "20000"
        },
        {
          "greater_than": "20000",
          "max_discount_percentage": "10"
        }
      ],
      "partition_key": "gpt#nestaging",
      "scope": "provider_item",
      "tags": [
        "39876487618607726720"
      ],
      "updated_at": "2026-06-01 22:24:18.882404",
      "updated_by": "prepare_discount_prompts"
    }
  ],
  "updated_by": "MCP",
  "created_at": "2026-06-18T16:18:48.400984",
  "updated_at": "2026-06-18T16:19:23.013225"
}
```

### 26. installments / create_installments

- Method: `create_installments`
- Status: `error`
- Elapsed: `11979.28 ms`

Arguments:

```json
{
  "quote_uuid": "09264210633191080064",
  "request_uuid": "60148758433262223488",
  "interval_num": 3,
  "total_pay_period": 6,
  "payment_method": "bank_transfer"
}
```

Error:

```text
'str' object cannot be interpreted as an integer
```

Output:

```json
{
  "error": "'str' object cannot be interpreted as an integer",
  "error_code": "UNKNOWN_ERROR"
}
```

### 27. installments / update_installment (uuid=481407384470...)

- Method: `update_installment`
- Status: `pass`
- Elapsed: `36715.79 ms`

Arguments:

```json
{
  "quote_uuid": "39412068575306858624",
  "installment_uuid": "48140738447058944128",
  "status": "paid"
}
```

Output:

```json
{
  "quote_uuid": "39412068575306858624",
  "installment_uuid": "48140738447058944128",
  "request_uuid": "26699108493000982656",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 875.0,
  "installment_ratio": 100.0,
  "salesorder_no": null,
  "scheduled_date": "2026-06-18T16:16:13",
  "payment_method": "bank_transfer",
  "status": "paid",
  "updated_by": "MCP",
  "created_at": "2026-06-18T16:16:16.586931",
  "updated_at": "2026-06-18T16:19:47.825753",
  "quote": {
    "request_uuid": "26699108493000982656",
    "quote_uuid": "39412068575306858624",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-AF",
    "sales_rep_email": null,
    "rounds": 0,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 25.0,
    "total_quote_amount": 900.0,
    "total_quote_discount": 50.0,
    "final_total_quote_amount": 875.0,
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
      "request_uuid": "26699108493000982656",
      "email": "jessicacooper@example.com",
      "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via MCPHttpClient through gateway /mcp",
      "billing_address": null,
      "shipping_address": null,
      "items": [
        {
          "item_name": "Flight ATL->ORD Premium Economy",
          "item_uuid": "06041993713794695296",
          "provider_items": [
            {
              "provider_item_uuid": "39876487618607726720",
              "provider_corp_external_id": "AIRLINE-AF",
              "batch_no": "AF5319-20260907",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_http_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-18T16:12:37.490071",
      "updated_by": "MCP",
      "updated_at": "2026-06-18T16:14:31.525931",
      "quotes": [
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-18 16:14:39.837945",
          "notes": "Updated via HTTP integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "39412068575306858624",
          "request_uuid": "26699108493000982656",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-18 16:16:00.998617",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF5319-20260907",
        "created_at": "2026-06-18 16:14:47.683649",
        "final_subtotal": "850",
        "hold_expires_at": "2026-06-18 16:29:48.046544",
        "hold_token": "5fca8e71950450ba653bc04d6f88b99e",
        "item_uuid": "06041993713794695296",
        "notes": "HTTP integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "79136946166253502592",
        "quote_uuid": "39412068575306858624",
        "request_data": {
          "cancellation_policy_snapshot": {
            "tiers": {
              "tiers": [
                {
                  "hours_before_departure_gte": "168",
                  "refund_pct": "1"
                },
                {
                  "hours_before_departure_gte": "24",
                  "refund_pct": "0.5"
                },
                {
                  "hours_before_departure_gte": "0",
                  "refund_pct": "0"
                }
              ]
            },
            "notes_template_uuid": null,
            "description": "Drive smile others listen quality international stand citizen media body meeting expect material tend main.",
            "label": "Premium Economy Fare Cancellation",
            "content_hash": "b161d765b3089e5e",
            "policy_uuid": "14167382355785826432",
            "snapshotted_at": "2026-06-18 16:14:48.324781"
          }
        },
        "request_uuid": "26699108493000982656",
        "subtotal": "900",
        "subtotal_discount": "50",
        "subtotal_native": "900",
        "updated_at": "2026-06-18 16:15:43.795845",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "875",
        "installment_ratio": "100",
        "priority": "0",
        "status": "paid",
        "created_at": "2026-06-18 16:16:16.586931",
        "installment_uuid": "48140738447058944128",
        "partition_key": "gpt#nestaging",
        "payment_method": "bank_transfer",
        "quote_uuid": "39412068575306858624",
        "request_uuid": "26699108493000982656",
        "scheduled_date": "2026-06-18 16:16:13",
        "updated_at": "2026-06-18 16:19:47.825753",
        "updated_by": "MCP"
      }
    ],
    "discount_prompts": [
      {
        "priority": "10",
        "status": "active",
        "conditions": [
          "is_refundable == false",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.614708",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
        "discount_prompt_uuid": "29118858989597114496",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "2.5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.614708",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'",
          "min_passengers >= 20",
          "loyalty_tier in ['gold', 'platinum']"
        ],
        "created_at": "2026-06-01 22:24:16.312582",
        "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
        "discount_prompt_uuid": "39743702329131548800",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "5000"
          },
          {
            "greater_than": "5000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.312582",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "7",
        "status": "active",
        "conditions": [
          "min_passengers >= 20",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:16.462599",
        "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
        "discount_prompt_uuid": "34741236891406844032",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "1000"
          },
          {
            "greater_than": "1000",
            "max_discount_percentage": "10",
            "less_than": "3500"
          },
          {
            "greater_than": "3500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "global",
        "tags": [],
        "updated_at": "2026-06-01 22:24:16.462599",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "6",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "min_passengers >= 10",
          "is_refundable == false"
        ],
        "created_at": "2026-06-01 22:24:16.923030",
        "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
        "discount_prompt_uuid": "81566856437527756928",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "500"
          },
          {
            "greater_than": "500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "segment",
        "tags": [
          "61268299727527493760"
        ],
        "updated_at": "2026-06-01 22:24:16.923030",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "5",
        "status": "active",
        "conditions": [
          "payment_method in ['wire_transfer', 'credit_card']",
          "channel == 'direct'"
        ],
        "created_at": "2026-06-01 22:24:18.730783",
        "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
        "discount_prompt_uuid": "87759969798493061248",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "7.5",
            "less_than": "2500"
          },
          {
            "greater_than": "2500",
            "max_discount_percentage": "10",
            "less_than": "7500"
          },
          {
            "greater_than": "7500",
            "max_discount_percentage": "12.5"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "item",
        "tags": [
          "06041993713794695296"
        ],
        "updated_at": "2026-06-01 22:24:18.730783",
        "updated_by": "prepare_discount_prompts"
      },
      {
        "priority": "2",
        "status": "active",
        "conditions": [
          "season != 'peak'"
        ],
        "created_at": "2026-06-01 22:24:18.882404",
        "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
        "discount_prompt_uuid": "88308794075899773056",
        "discount_rules": [
          {
            "greater_than": "0",
            "max_discount_percentage": "5",
            "less_than": "10000"
          },
          {
            "greater_than": "10000",
            "max_discount_percentage": "7.5",
            "less_than": "20000"
          },
          {
            "greater_than": "20000",
            "max_discount_percentage": "10"
          }
        ],
        "partition_key": "gpt#nestaging",
        "scope": "provider_item",
        "tags": [
          "39876487618607726720"
        ],
        "updated_at": "2026-06-01 22:24:18.882404",
        "updated_by": "prepare_discount_prompts"
      }
    ],
    "updated_by": "MCP",
    "created_at": "2026-06-18T16:14:39.837945",
    "updated_at": "2026-06-18T16:16:00.998617"
  }
}
```
