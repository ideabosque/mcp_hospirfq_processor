# MCP HospiRFQ Processor Live Integration Results

- Generated at: `2026-06-17T22:48:26.559464+00:00`
- Gateway: `http://localhost:8765`
- Endpoint: `gpt`
- Partition: `nestaging`
- GraphQL URL: `http://localhost:8765/gpt/nestaging/ai_rfq_graphql`
- Dependency order: `catalog_discovery, items, requests, quotes, pricing, installments`
- Passed: `26`
- Error responses: `0`
- Failed: `0`
- Total calls: `26`

## Function Results

### 1. catalog_discovery / inquire_catalog (select primary item)

- Method: `inquire_catalog`
- Status: `pass`
- Elapsed: `9215.56 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "query_text": "Air France ATL ORD Premium Economy flight with meal included",
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
            "text": "Flight product: Flight ATL->ORD Premium Economy. Premium Economy class non-stop service from Atlanta (ATL) to Chicago (ORD). Route: ATL to ORD. Cabin class: Premium Economy. Operated by: Air France (AF). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 450.0, child USD 337.5, infant USD 45.0. Scheduled flights: AF6267 departing 2026-09-12T19:00:00Z, 52 seats; AF5319 departing 2026-09-07T12:00:00Z, 37 seats. Premium Economy Fare Cancellation: 168h+: 100% refund; 24h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary DFW->SIN + ATL->ORD + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:25",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:25",
          "score": "0.8713404536247253",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight ATL->ORD Economy. Economy class non-stop service from Atlanta (ATL) to Chicago (ORD). Route: ATL to ORD. Cabin class: Economy. Operated by: Qantas (QF). Baggage allowance: 23 kg. Meal included: no. Fares: adult USD 250.0, child USD 187.5, infant USD 25.0. Scheduled flights: QF1351 departing 2026-07-09T21:45:00Z, 145 seats; QF5796 departing 2026-09-21T19:45:00Z, 169 seats. Economy Fare Cancellation: 168h+: 100% refund; 24h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:17",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:17",
          "score": "0.7910401225090027",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight CDG->JFK Business. Business class non-stop service from Paris (CDG) to New York (JFK). Route: CDG to JFK. Cabin class: Business. Operated by: Air France (AF). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 1800.0, child USD 1350.0, infant USD 180.0. Scheduled flights: AF8751 departing 2026-08-11T08:30:00Z, 30 seats; AF5020 departing 2026-06-16T08:30:00Z, 22 seats. Business Fare Cancellation: 24h+: 100% refund; 2h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary DFW->SIN + ATL->ORD + CDG->JFK, Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:1",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:1",
          "score": "0.7605815529823303",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight LAX->HKG Premium Economy. Premium Economy class non-stop service from Los Angeles (LAX) to Hong Kong (HKG). Route: LAX to HKG. Cabin class: Premium Economy. Operated by: Lufthansa (LH). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 450.0, child USD 337.5, infant USD 45.0. Scheduled flights: LH6452 departing 2026-08-01T21:15:00Z, 34 seats; LH3684 departing 2026-09-26T20:45:00Z, 41 seats. Premium Economy Fare Cancellation: 168h+: 100% refund; 24h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary ATL->ORD + LAX->HKG + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:33",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:33",
          "score": "0.733452320098877",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "Flight product: Flight DFW->SIN Business. Business class non-stop service from Dallas (DFW) to Singapore (SIN). Route: DFW to SIN. Cabin class: Business. Operated by: Singapore Airlines (SQ). Baggage allowance: 32 kg. Meal included: yes. Fares: adult USD 1800.0, child USD 1350.0, infant USD 180.0. Scheduled flights: SQ6901 departing 2026-08-12T13:45:00Z, 33 seats; SQ8511 departing 2026-09-26T19:15:00Z, 30 seats. Business Fare Cancellation: 24h+: 100% refund; 2h+: 50% refund. This flight can be used as a component in package templates: Flight Itinerary DFW->SIN + ATL->ORD + CDG->JFK."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:9",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:9",
          "score": "0.6800904273986816",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-17T22:43:09.560257+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 2. items / search_items (flight type)

- Method: `search_items`
- Status: `pass`
- Elapsed: `3332.77 ms`

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

### 3. items / get_item (Flight ATL->ORD Premium Economy)

- Method: `get_item`
- Status: `pass`
- Elapsed: `3345.31 ms`

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

### 4. items / get_provider_items (with batches)

- Method: `get_provider_items`
- Status: `pass`
- Elapsed: `6592.19 ms`

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

### 5. requests / submit_rfq_request

- Method: `submit_rfq_request`
- Status: `pass`
- Elapsed: `3736.31 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy",
  "request_description": "E2E test request via silvaengine_gateway",
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
  "notes": "Created by run_integration.py",
  "expired_at": "2026-12-31T23:59:59Z"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "48871474724327145600",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy",
  "request_description": "E2E test request via silvaengine_gateway",
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
  "notes": "Created by run_integration.py",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-17T22:43:26.117930",
  "updated_by": "MCP",
  "updated_at": "2026-06-17T22:43:26.117930",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 6. requests / get_rfq_request (seeded)

- Method: `get_rfq_request`
- Status: `pass`
- Elapsed: `3361.66 ms`

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
  "updated_at": "2026-06-17T22:40:33.114899",
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
      "updated_at": "2026-06-17 22:40:22.097433",
      "updated_by": "MCP"
    }
  ],
  "files": [
    {
      "created_at": "2026-06-17 19:11:33.981790",
      "email": "jessicacooper@example.com",
      "file_name": "integration_test_spec.pdf",
      "partition_key": "gpt#nestaging",
      "request_uuid": "96306650268729098368",
      "updated_at": "2026-06-17 22:40:36.706892",
      "updated_by": "MCP"
    }
  ],
  "bundle": null
}
```

### 7. requests / search_rfq_requests

- Method: `search_rfq_requests`
- Status: `pass`
- Elapsed: `3985.22 ms`

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
  "total": 20,
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

### 8. requests / update_rfq_request

- Method: `update_rfq_request`
- Status: `pass`
- Elapsed: `6977.33 ms`

Arguments:

```json
{
  "request_uuid": "48871474724327145600",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "notes": "Updated via run_integration.py"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "48871474724327145600",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
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
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "initial",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-17T22:43:26.117930",
  "updated_by": "MCP",
  "updated_at": "2026-06-17T22:43:40.509457",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 9. requests / add_item_to_rfq_request

- Method: `add_item_to_rfq_request`
- Status: `pass`
- Elapsed: `7150.16 ms`

Arguments:

```json
{
  "request_uuid": "48871474724327145600",
  "item": {
    "item_uuid": "52065619693805781120",
    "item_name": "Flight ATL->ORD Economy",
    "qty": 1,
    "provider_items": []
  }
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "48871474724327145600",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
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
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-17T22:43:26.117930",
  "updated_by": "MCP",
  "updated_at": "2026-06-17T22:43:47.669798",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 10. requests / remove_item_from_rfq_request

- Method: `remove_item_from_rfq_request`
- Status: `pass`
- Elapsed: `7122.82 ms`

Arguments:

```json
{
  "request_uuid": "48871474724327145600",
  "item_uuid": "52065619693805781120"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "48871474724327145600",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
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
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-17T22:43:26.117930",
  "updated_by": "MCP",
  "updated_at": "2026-06-17T22:43:54.798512",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 11. requests / assign_provider_item_to_request_item

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `10664.05 ms`

Arguments:

```json
{
  "request_uuid": "48871474724327145600",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720",
  "provider_corp_external_id": "AIRLINE-AF",
  "qty": 2,
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "48871474724327145600",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
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
          "batch_no": "AF6267-20260912",
          "qty": "2"
        }
      ],
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-17T22:43:26.117930",
  "updated_by": "MCP",
  "updated_at": "2026-06-17T22:44:05.457180",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 12. requests / remove_provider_item_from_request_item

- Method: `remove_provider_item_from_request_item`
- Status: `pass`
- Elapsed: `7127.98 ms`

Arguments:

```json
{
  "request_uuid": "48871474724327145600",
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
  "request_uuid": "48871474724327145600",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
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
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-17T22:43:26.117930",
  "updated_by": "MCP",
  "updated_at": "2026-06-17T22:44:12.573862",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 13. requests / assign_provider_item_to_request_item (for quote workflow)

- Method: `assign_provider_item_to_request_item`
- Status: `pass`
- Elapsed: `10556.54 ms`

Arguments:

```json
{
  "request_uuid": "48871474724327145600",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720",
  "provider_corp_external_id": "AIRLINE-AF",
  "qty": 2,
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "partition_key": "gpt#nestaging",
  "endpoint_id": "gpt",
  "part_id": "nestaging",
  "request_uuid": "48871474724327145600",
  "email": "jessicacooper@example.com",
  "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
  "request_description": "E2E test request via silvaengine_gateway",
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
          "batch_no": "AF6267-20260912",
          "qty": "2"
        }
      ],
      "qty": "2",
      "pax_breakdown": {
        "adult": "2"
      }
    }
  ],
  "notes": "Updated via run_integration.py",
  "bundle_uuid": null,
  "status": "in_progress",
  "expired_at": "2026-12-31T23:59:59",
  "created_at": "2026-06-17T22:43:26.117930",
  "updated_by": "MCP",
  "updated_at": "2026-06-17T22:44:23.133552",
  "quotes": [],
  "files": [],
  "bundle": null
}
```

### 14. quotes / confirm_request_and_create_quotes

- Method: `confirm_request_and_create_quotes`
- Status: `pass`
- Elapsed: `37517.7 ms`

Arguments:

```json
{
  "request_uuid": "48871474724327145600",
  "provider_corp_external_ids": [
    "AIRLINE-AF"
  ],
  "segment_uuid": "61268299727527493760",
  "batch_no": "AF6267-20260912",
  "service_start_at": "2026-09-12T19:00:00Z",
  "service_end_at": "2026-09-12T23:07:47.008532Z"
}
```

Output:

```json
{
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "48871474724327145600",
    "email": "jessicacooper@example.com",
    "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
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
            "batch_no": "AF6267-20260912",
            "qty": "2"
          }
        ],
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        }
      }
    ],
    "notes": "Updated via run_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-17T22:43:26.117930",
    "updated_by": "MCP",
    "updated_at": "2026-06-17T22:44:33.567681",
    "quotes": [],
    "files": [],
    "bundle": null
  },
  "created_quotes": [
    {
      "request_uuid": "48871474724327145600",
      "quote_uuid": "59882695090073780352",
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
        "request_uuid": "48871474724327145600",
        "email": "jessicacooper@example.com",
        "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
        "request_description": "E2E test request via silvaengine_gateway",
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
                "batch_no": "AF6267-20260912",
                "qty": "2"
              }
            ],
            "qty": "2",
            "pax_breakdown": {
              "adult": "2"
            }
          }
        ],
        "notes": "Updated via run_integration.py",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-17T22:43:26.117930",
        "updated_by": "MCP",
        "updated_at": "2026-06-17T22:44:33.567681",
        "quotes": [
          {
            "final_total_quote_amount": "900",
            "provider_corp_external_id": "AIRLINE-AF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "in_progress",
            "total_quote_amount": "900",
            "total_quote_discount": "0",
            "created_at": "2026-06-17 22:44:40.558317",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "59882695090073780352",
            "request_uuid": "48871474724327145600",
            "updated_at": "2026-06-17 22:44:56.561909",
            "updated_by": "MCP"
          }
        ],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "batch_no": "AF6267-20260912",
          "created_at": "2026-06-17 22:44:47.987825",
          "final_subtotal": "900",
          "hold_expires_at": "2026-06-17 22:59:48.315668",
          "hold_token": "5f094e9e028c695eab6475383f0f5224",
          "item_uuid": "06041993713794695296",
          "partition_key": "gpt#nestaging",
          "pax_breakdown": {
            "adult": "2"
          },
          "price_per_uom": "450",
          "provider_item_uuid": "39876487618607726720",
          "qty": "2",
          "quote_item_uuid": "93812712643569401984",
          "quote_uuid": "59882695090073780352",
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
              "snapshotted_at": "2026-06-17 22:44:48.564014"
            }
          },
          "request_uuid": "48871474724327145600",
          "subtotal": "900",
          "subtotal_discount": "0",
          "subtotal_native": "900",
          "updated_at": "2026-06-17 22:44:47.987825",
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
         
... (truncated)
```

### 15. quotes / get_quote

- Method: `get_quote`
- Status: `pass`
- Elapsed: `4012.24 ms`

Arguments:

```json
{
  "quote_uuid": "59882695090073780352",
  "request_uuid": "48871474724327145600"
}
```

Output:

```json
{
  "request_uuid": "48871474724327145600",
  "quote_uuid": "59882695090073780352",
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
    "request_uuid": "48871474724327145600",
    "email": "jessicacooper@example.com",
    "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
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
            "batch_no": "AF6267-20260912",
            "qty": "2"
          }
        ],
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        }
      }
    ],
    "notes": "Updated via run_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-17T22:43:26.117930",
    "updated_by": "MCP",
    "updated_at": "2026-06-17T22:44:33.567681",
    "quotes": [
      {
        "final_total_quote_amount": "900",
        "provider_corp_external_id": "AIRLINE-AF",
        "rounds": "0",
        "shipping_amount": "0",
        "status": "in_progress",
        "total_quote_amount": "900",
        "total_quote_discount": "0",
        "created_at": "2026-06-17 22:44:40.558317",
        "partition_key": "gpt#nestaging",
        "quote_uuid": "59882695090073780352",
        "request_uuid": "48871474724327145600",
        "updated_at": "2026-06-17 22:44:56.561909",
        "updated_by": "MCP"
      }
    ],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "batch_no": "AF6267-20260912",
      "created_at": "2026-06-17 22:44:47.987825",
      "final_subtotal": "900",
      "hold_expires_at": "2026-06-17 22:59:48.315668",
      "hold_token": "5f094e9e028c695eab6475383f0f5224",
      "item_uuid": "06041993713794695296",
      "partition_key": "gpt#nestaging",
      "pax_breakdown": {
        "adult": "2"
      },
      "price_per_uom": "450",
      "provider_item_uuid": "39876487618607726720",
      "qty": "2",
      "quote_item_uuid": "93812712643569401984",
      "quote_uuid": "59882695090073780352",
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
          "snapshotted_at": "2026-06-17 22:44:48.564014"
        }
      },
      "request_uuid": "48871474724327145600",
      "subtotal": "900",
      "subtotal_discount": "0",
      "subtotal_native": "900",
      "updated_at": "2026-06-17 22:44:47.987825",
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
  "created_at": "2026-06-17T22:44:40.558317",
  "updated_at": "2026-06-17T22:44:56.561909"
}
```

### 16. quotes / search_quotes

- Method: `search_quotes`
- Status: `pass`
- Elapsed: `3784.94 ms`

Arguments:

```json
{
  "request_uuid": "48871474724327145600",
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
      "request_uuid": "48871474724327145600",
      "quote_uuid": "59882695090073780352",
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
        "request_uuid": "48871474724327145600",
        "email": "jessicacooper@example.com",
        "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
        "request_description": "E2E test request via silvaengine_gateway",
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
                "batch_no": "AF6267-20260912",
                "qty": "2"
              }
            ],
            "qty": "2",
            "pax_breakdown": {
              "adult": "2"
            }
          }
        ],
        "notes": "Updated via run_integration.py",
        "bundle_uuid": null,
        "status": "confirmed",
        "expired_at": "2026-12-31T23:59:59",
        "created_at": "2026-06-17T22:43:26.117930",
        "updated_by": "MCP",
        "updated_at": "2026-06-17T22:44:33.567681",
        "quotes": [
          {
            "final_total_quote_amount": "900",
            "provider_corp_external_id": "AIRLINE-AF",
            "rounds": "0",
            "shipping_amount": "0",
            "status": "in_progress",
            "total_quote_amount": "900",
            "total_quote_discount": "0",
            "created_at": "2026-06-17 22:44:40.558317",
            "partition_key": "gpt#nestaging",
            "quote_uuid": "59882695090073780352",
            "request_uuid": "48871474724327145600",
            "updated_at": "2026-06-17 22:44:56.561909",
            "updated_by": "MCP"
          }
        ],
        "files": [],
        "bundle": null
      },
      "quote_items": [
        {
          "batch_no": "AF6267-20260912",
          "created_at": "2026-06-17 22:44:47.987825",
          "final_subtotal": "900",
          "hold_expires_at": "2026-06-17 22:59:48.315668",
          "hold_token": "5f094e9e028c695eab6475383f0f5224",
          "item_uuid": "06041993713794695296",
          "partition_key": "gpt#nestaging",
          "pax_breakdown": {
            "adult": "2"
          },
          "price_per_uom": "450",
          "provider_item_uuid": "39876487618607726720",
          "qty": "2",
          "quote_item_uuid": "93812712643569401984",
          "quote_uuid": "59882695090073780352",
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
              "snapshotted_at": "2026-06-17 22:44:48.564014"
            }
          },
          "request_uuid": "48871474724327145600",
          "subtotal": "900",
          "subtotal_discount": "0",
          "subtotal_native": "900",
          "updated_at": "2026-06-17 22:44:47.987825",
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
      "created_at": "2026-06-17T22:44:40.558317",
      "updated_at": "2026-06-17T22:44:56.561909"
    }
  ]
}
```

### 17. quotes / update_quote

- Method: `update_quote`
- Status: `pass`
- Elapsed: `7763.51 ms`

Arguments:

```json
{
  "request_uuid": "48871474724327145600",
  "quote_uuid": "59882695090073780352",
  "notes": "Updated via integration test",
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0
}
```

Output:

```json
{
  "request_uuid": "48871474724327145600",
  "quote_uuid": "59882695090073780352",
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
  "notes": "Updated via integration test",
  "status": "in_progress",
  "expired_at": null,
  "request": {
    "partition_key": "gpt#nestaging",
    "endpoint_id": "gpt",
    "part_id": "nestaging",
    "request_uuid": "48871474724327145600",
    "email": "jessicacooper@example.com",
    "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
    "request_description": "E2E test request via silvaengine_gateway",
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
            "batch_no": "AF6267-20260912",
            "qty": "2"
          }
        ],
        "qty": "2",
        "pax_breakdown": {
          "adult": "2"
        }
      }
    ],
    "notes": "Updated via run_integration.py",
    "bundle_uuid": null,
    "status": "confirmed",
    "expired_at": "2026-12-31T23:59:59",
    "created_at": "2026-06-17T22:43:26.117930",
    "updated_by": "MCP",
    "updated_at": "2026-06-17T22:44:33.567681",
    "quotes": [
      {
        "final_total_quote_amount": "925",
        "provider_corp_external_id": "AIRLINE-AF",
        "rounds": "0",
        "shipping_amount": "25",
        "status": "in_progress",
        "total_quote_amount": "900",
        "total_quote_discount": "0",
        "created_at": "2026-06-17 22:44:40.558317",
        "notes": "Updated via integration test",
        "partition_key": "gpt#nestaging",
        "quote_uuid": "59882695090073780352",
        "request_uuid": "48871474724327145600",
        "shipping_method": "ticket_delivery",
        "updated_at": "2026-06-17 22:45:16.040304",
        "updated_by": "MCP"
      }
    ],
    "files": [],
    "bundle": null
  },
  "quote_items": [
    {
      "batch_no": "AF6267-20260912",
      "created_at": "2026-06-17 22:44:47.987825",
      "final_subtotal": "900",
      "hold_expires_at": "2026-06-17 22:59:48.315668",
      "hold_token": "5f094e9e028c695eab6475383f0f5224",
      "item_uuid": "06041993713794695296",
      "partition_key": "gpt#nestaging",
      "pax_breakdown": {
        "adult": "2"
      },
      "price_per_uom": "450",
      "provider_item_uuid": "39876487618607726720",
      "qty": "2",
      "quote_item_uuid": "93812712643569401984",
      "quote_uuid": "59882695090073780352",
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
          "snapshotted_at": "2026-06-17 22:44:48.564014"
        }
      },
      "request_uuid": "48871474724327145600",
      "subtotal": "900",
      "subtotal_discount": "0",
      "subtotal_native": "900",
      "updated_at": "2026-06-17 22:44:47.987825",
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
  "created_at": "2026-06-17T22:44:40.558317",
  "updated_at": "2026-06-17T22:45:16.040304"
}
```

### 18. quotes / update_quote_item

- Method: `update_quote_item`
- Status: `pass`
- Elapsed: `8479.79 ms`

Arguments:

```json
{
  "quote_uuid": "59882695090073780352",
  "quote_item_uuid": "93812712643569401984",
  "request_uuid": "48871474724327145600",
  "discount_amount": 50.0,
  "notes": "Integration test discount"
}
```

Output:

```json
{
  "quote_uuid": "59882695090073780352",
  "quote_item_uuid": "93812712643569401984",
  "provider_item_uuid": "39876487618607726720",
  "item_uuid": "06041993713794695296",
  "partition_key": "gpt#nestaging",
  "batch_no": "AF6267-20260912",
  "request_uuid": "48871474724327145600",
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
  "notes": "Integration test discount",
  "hold_token": "5f094e9e028c695eab6475383f0f5224",
  "hold_expires_at": "2026-06-17T22:59:48.315668",
  "guardrail_price_per_uom": 306.69,
  "slow_move_item": false,
  "quote": {
    "request_uuid": "48871474724327145600",
    "quote_uuid": "59882695090073780352",
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
    "notes": "Updated via integration test",
    "status": "in_progress",
    "expired_at": null,
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "48871474724327145600",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
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
              "batch_no": "AF6267-20260912",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-17T22:43:26.117930",
      "updated_by": "MCP",
      "updated_at": "2026-06-17T22:44:33.567681",
      "quotes": [
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "in_progress",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-17 22:44:40.558317",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "59882695090073780352",
          "request_uuid": "48871474724327145600",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-17 22:45:23.816769",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF6267-20260912",
        "created_at": "2026-06-17 22:44:47.987825",
        "final_subtotal": "850",
        "hold_expires_at": "2026-06-17 22:59:48.315668",
        "hold_token": "5f094e9e028c695eab6475383f0f5224",
        "item_uuid": "06041993713794695296",
        "notes": "Integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "93812712643569401984",
        "quote_uuid": "59882695090073780352",
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
            "snapshotted_at": "2026-06-17 22:44:48.564014"
          }
        },
        "request_uuid": "48871474724327145600",
        "subtotal": "900",
        "subtotal_discount": "50",
        "subtotal_native": "900",
        "updated_at": "2026-06-17 22:45:23.631651",
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
    "created_at": "2026-06-17T22:44:40.558317",
    "updated_at": "2026-06-17T22:45:23.816769"
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
    "updated_at": "2026-06-01T22:19:29.788924"
  
... (truncated)
```

### 19. pricing / get_item_price_tiers

- Method: `get_item_price_tiers`
- Status: `pass`
- Elapsed: `3275.06 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "quote_items": [
    {
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720",
      "qty": 2
    }
  ]
}
```

Output:

```json
{
  "item_price_tiers": [
    {
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720",
      "item_price_tier_uuid": "10913421828051452032",
      "quantity_greater_then": 0.0,
      "quantity_less_then": null,
      "price_per_uom": 45.0,
      "margin_per_uom": null,
      "provider_item_batches": [],
      "status": "active"
    },
    {
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720",
      "item_price_tier_uuid": "23774464543545114752",
      "quantity_greater_then": 0.0,
      "quantity_less_then": null,
      "price_per_uom": 450.0,
      "margin_per_uom": null,
      "provider_item_batches": [],
      "status": "active"
    },
    {
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720",
      "item_price_tier_uuid": "76852609247750406272",
      "quantity_greater_then": 0.0,
      "quantity_less_then": null,
      "price_per_uom": 337.5,
      "margin_per_uom": null,
      "provider_item_batches": [],
      "status": "active"
    }
  ]
}
```

### 20. pricing / get_discount_prompts

- Method: `get_discount_prompts`
- Status: `pass`
- Elapsed: `3489.36 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "quote_items": [
    {
      "item_uuid": "06041993713794695296",
      "provider_item_uuid": "39876487618607726720"
    }
  ]
}
```

Output:

```json
{
  "discount_prompts": [
    {
      "discount_prompt_uuid": "29118858989597114496",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 60 days before service receive escalating discounts. (ref: PROMO-2010-MS)",
      "conditions": [
        "is_refundable == false",
        "channel == 'direct'"
      ],
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
      "priority": 10,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "39743702329131548800",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Encourage early-bird bookings: applicants who confirm at least 14 days before service receive escalating discounts. (ref: PROMO-5160-CG)",
      "conditions": [
        "season != 'peak'",
        "min_passengers >= 20",
        "loyalty_tier in ['gold', 'platinum']"
      ],
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
      "priority": 2,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "34741236891406844032",
      "scope": "global",
      "tags": [],
      "discount_prompt": "Multi-leg itinerary incentive: bundle two or more flights on the same quote to qualify for tiered savings. (ref: PROMO-8933-ZZ)",
      "conditions": [
        "min_passengers >= 20",
        "channel == 'direct'"
      ],
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
      "priority": 7,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "81566856437527756928",
      "scope": "segment",
      "tags": [
        "61268299727527493760"
      ],
      "discount_prompt": "Preferred segment 'Johnson, Riley and Lozano Tier' members receive volume discounts at lower thresholds than retail customers.",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "min_passengers >= 10",
        "is_refundable == false"
      ],
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
      "priority": 6,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "87759969798493061248",
      "scope": "item",
      "tags": [
        "06041993713794695296"
      ],
      "discount_prompt": "Featured route 'Flight ATL->ORD Premium Economy': marketing-driven discount ladder to drive demand.",
      "conditions": [
        "payment_method in ['wire_transfer', 'credit_card']",
        "channel == 'direct'"
      ],
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
      "priority": 5,
      "status": "active"
    },
    {
      "discount_prompt_uuid": "88308794075899773056",
      "scope": "provider_item",
      "tags": [
        "39876487618607726720"
      ],
      "discount_prompt": "Strategic-partner pricing for 'Air France' on this route: preferred-rate tiers when minimums are met.",
      "conditions": [
        "season != 'peak'"
      ],
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
      "priority": 2,
      "status": "active"
    }
  ]
}
```

### 21. pricing / calculate_quote_pricing

- Method: `calculate_quote_pricing`
- Status: `pass`
- Elapsed: `3358.14 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "email": "jessicacooper@example.com"
}
```

Output:

```json
{
  "request_uuid": "96306650268729098368",
  "groups": []
}
```

### 22. installments / confirm_quote_and_create_installments

- Method: `confirm_quote_and_create_installments`
- Status: `pass`
- Elapsed: `29698.23 ms`

Arguments:

```json
{
  "request_uuid": "48871474724327145600",
  "quote_uuid": "59882695090073780352",
  "create_single_installment": true,
  "payment_method": "bank_transfer"
}
```

Output:

```json
{
  "quote": {
    "request_uuid": "48871474724327145600",
    "quote_uuid": "59882695090073780352",
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
    "notes": "Updated via integration test",
    "status": "confirmed",
    "expired_at": null,
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "48871474724327145600",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
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
              "batch_no": "AF6267-20260912",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-17T22:43:26.117930",
      "updated_by": "MCP",
      "updated_at": "2026-06-17T22:44:33.567681",
      "quotes": [
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-17 22:44:40.558317",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "59882695090073780352",
          "request_uuid": "48871474724327145600",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-17 22:45:46.008050",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF6267-20260912",
        "created_at": "2026-06-17 22:44:47.987825",
        "final_subtotal": "850",
        "hold_expires_at": "2026-06-17 22:59:48.315668",
        "hold_token": "5f094e9e028c695eab6475383f0f5224",
        "item_uuid": "06041993713794695296",
        "notes": "Integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "93812712643569401984",
        "quote_uuid": "59882695090073780352",
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
            "snapshotted_at": "2026-06-17 22:44:48.564014"
          }
        },
        "request_uuid": "48871474724327145600",
        "subtotal": "900",
        "subtotal_discount": "50",
        "subtotal_native": "900",
        "updated_at": "2026-06-17 22:45:23.631651",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "875",
        "installment_ratio": "100",
        "priority": "0",
        "status": "pending",
        "created_at": "2026-06-17 22:46:00.397145",
        "installment_uuid": "28452051202817933440",
        "partition_key": "gpt#nestaging",
        "payment_method": "bank_transfer",
        "quote_uuid": "59882695090073780352",
        "request_uuid": "48871474724327145600",
        "scheduled_date": "2026-06-17 22:45:57",
        "updated_at": "2026-06-17 22:46:00.397145",
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
    "created_at": "2026-06-17T22:44:40.558317",
    "updated_at": "2026-06-17T22:45:46.008050"
  },
  "installments": [
    {
      "quote_uuid": "59882695090073780352",
      "installment_uuid": "28452051202817933440",
      "request_uuid": "48871474724327145600",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 875.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-17T22:45:57",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-17T22:46:00.397145",
      "updated_at": "2026-06-17T22:46:00.397145",
      "quote": {
        "request_uuid": "48871474724327145600",
        "quote_uuid": "59882695090073780352",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_id": "AIRLINE-AF",
        "sales_rep_em
... (truncated)
```

### 23. installments / get_installments

- Method: `get_installments`
- Status: `pass`
- Elapsed: `3810.8 ms`

Arguments:

```json
{
  "quote_uuid": "59882695090073780352",
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
      "quote_uuid": "59882695090073780352",
      "installment_uuid": "28452051202817933440",
      "request_uuid": "48871474724327145600",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 875.0,
      "installment_ratio": 100.0,
      "salesorder_no": null,
      "scheduled_date": "2026-06-17T22:45:57",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-17T22:46:00.397145",
      "updated_at": "2026-06-17T22:46:00.397145",
      "quote": {
        "request_uuid": "48871474724327145600",
        "quote_uuid": "59882695090073780352",
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
        "notes": "Updated via integration test",
        "status": "confirmed",
        "expired_at": null,
        "request": {
          "partition_key": "gpt#nestaging",
          "endpoint_id": "gpt",
          "part_id": "nestaging",
          "request_uuid": "48871474724327145600",
          "email": "jessicacooper@example.com",
          "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
          "request_description": "E2E test request via silvaengine_gateway",
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
                  "batch_no": "AF6267-20260912",
                  "qty": "2"
                }
              ],
              "qty": "2",
              "pax_breakdown": {
                "adult": "2"
              }
            }
          ],
          "notes": "Updated via run_integration.py",
          "bundle_uuid": null,
          "status": "confirmed",
          "expired_at": "2026-12-31T23:59:59",
          "created_at": "2026-06-17T22:43:26.117930",
          "updated_by": "MCP",
          "updated_at": "2026-06-17T22:44:33.567681",
          "quotes": [
            {
              "final_total_quote_amount": "875",
              "provider_corp_external_id": "AIRLINE-AF",
              "rounds": "0",
              "shipping_amount": "25",
              "status": "confirmed",
              "total_quote_amount": "900",
              "total_quote_discount": "50",
              "created_at": "2026-06-17 22:44:40.558317",
              "notes": "Updated via integration test",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "59882695090073780352",
              "request_uuid": "48871474724327145600",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-17 22:45:46.008050",
              "updated_by": "MCP"
            }
          ],
          "files": [],
          "bundle": null
        },
        "quote_items": [
          {
            "batch_no": "AF6267-20260912",
            "created_at": "2026-06-17 22:44:47.987825",
            "final_subtotal": "850",
            "hold_expires_at": "2026-06-17 22:59:48.315668",
            "hold_token": "5f094e9e028c695eab6475383f0f5224",
            "item_uuid": "06041993713794695296",
            "notes": "Integration test discount",
            "partition_key": "gpt#nestaging",
            "pax_breakdown": {
              "adult": "2"
            },
            "price_per_uom": "450",
            "provider_item_uuid": "39876487618607726720",
            "qty": "2",
            "quote_item_uuid": "93812712643569401984",
            "quote_uuid": "59882695090073780352",
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
                "snapshotted_at": "2026-06-17 22:44:48.564014"
              }
            },
            "request_uuid": "48871474724327145600",
            "subtotal": "900",
            "subtotal_discount": "50",
            "subtotal_native": "900",
            "updated_at": "2026-06-17 22:45:23.631651",
            "updated_by": "MCP"
          }
        ],
        "installments": [
          {
            "installment_amount": "875",
            "installment_ratio": "100",
            "priority": "0",
            "status": "pending",
            "created_at": "2026-06-17 22:46:00.397145",
            "installment_uuid": "28452051202817933440",
            "partition_key": "gpt#nestaging",
            "payment_method": "bank_transfer",
            "quote_uuid": "59882695090073780352",
            "request_uuid": "48871474724327145600",
            "scheduled_date": "2026-06-17 22:45:57",
            "updated_at": "2026-06-17 22:46:00.397145",
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
          
... (truncated)
```

### 24. installments / create_installment

- Method: `_create_installment`
- Status: `pass`
- Elapsed: `10972.85 ms`

Arguments:

```json
{
  "quote_uuid": "87693521885660725376",
  "request_uuid": "48871474724327145600",
  "installment_amount": 100.0,
  "payment_method": "credit_card"
}
```

Output:

```json
{
  "quote_uuid": "87693521885660725376",
  "installment_uuid": "90146922149578817664",
  "request_uuid": "48871474724327145600",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 100.0,
  "installment_ratio": 8.333333333333332,
  "salesorder_no": null,
  "scheduled_date": "2026-06-17T22:47:32",
  "payment_method": "credit_card",
  "status": "pending",
  "updated_by": "MCP",
  "created_at": "2026-06-17T22:47:36.111547",
  "updated_at": "2026-06-17T22:47:36.111547",
  "quote": {
    "request_uuid": "48871474724327145600",
    "quote_uuid": "87693521885660725376",
    "partition_key": "gpt#nestaging",
    "provider_corp_external_id": "AIRLINE-AF",
    "sales_rep_email": null,
    "rounds": 1,
    "shipping_method": "ticket_delivery",
    "shipping_amount": 300.0,
    "total_quote_amount": 900.0,
    "total_quote_discount": 0.0,
    "final_total_quote_amount": 1200.0,
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
      "request_uuid": "48871474724327145600",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
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
              "batch_no": "AF6267-20260912",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-17T22:43:26.117930",
      "updated_by": "MCP",
      "updated_at": "2026-06-17T22:44:33.567681",
      "quotes": [
        {
          "final_total_quote_amount": "1200",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "2",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "0",
          "created_at": "2026-06-17 22:46:53.897669",
          "notes": "Confirmed setup quote for create_installments",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "19450419734386851968",
          "request_uuid": "48871474724327145600",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-17 22:47:25.341833",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-17 22:44:40.558317",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "59882695090073780352",
          "request_uuid": "48871474724327145600",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-17 22:45:46.008050",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "1200",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "1",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "0",
          "created_at": "2026-06-17 22:46:15.398445",
          "notes": "Confirmed setup quote for create_installment",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "87693521885660725376",
          "request_uuid": "48871474724327145600",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-17 22:46:46.682841",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF6267-20260912",
        "created_at": "2026-06-17 22:46:22.751486",
        "final_subtotal": "900",
        "hold_expires_at": "2026-06-17 23:01:23.065825",
        "hold_token": "bff7e0529246956bf0b8d63c9be0d281",
        "item_uuid": "06041993713794695296",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "01595900708246274176",
        "quote_uuid": "87693521885660725376",
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
            "snapshotted_at": "2026-06-17 22:46:23.301903"
          }
        },
        "request_uuid": "48871474724327145600",
        "subtotal": "900",
        "subtotal_discount": "0",
        "subtotal_native": "900",
        "updated_at": "2026-06-17 22:46:22.751486",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "100",
        "installment_ratio": "8.333333333333332",
        "priority": "0",
        "status": "pending",
        "created_at": "2026-06-17 22:47:36.111547",
        "installment_uuid": "90146922149578817664",
        "partition_key": "gpt#nestaging",
        "payment_method": "credit_card",
        "quote_uuid": "87693521885660725376",
        "request_uuid": "48871474724327145600",
        "scheduled_date": "2026-06-17 22:47:32",
        "updated_at": "2026-06-17 22:47:36.111547",
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
          "season !
... (truncated)
```

### 25. installments / create_installments

- Method: `_create_installments`
- Status: `pass`
- Elapsed: `19137.22 ms`

Arguments:

```json
{
  "quote_uuid": "19450419734386851968",
  "request_uuid": "48871474724327145600",
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
      "quote_uuid": "19450419734386851968",
      "installment_uuid": "33044365256899444864",
      "request_uuid": "48871474724327145600",
      "priority": 0,
      "partition_key": "gpt#nestaging",
      "installment_amount": 400.0,
      "installment_ratio": 33.33333333333333,
      "salesorder_no": null,
      "scheduled_date": "2026-08-15T22:47:43",
      "payment_method": "bank_transfer",
      "status": "pending",
      "updated_by": "MCP",
      "created_at": "2026-06-17T22:47:47.173823",
      "updated_at": "2026-06-17T22:47:47.173823",
      "quote": {
        "request_uuid": "48871474724327145600",
        "quote_uuid": "19450419734386851968",
        "partition_key": "gpt#nestaging",
        "provider_corp_external_id": "AIRLINE-AF",
        "sales_rep_email": null,
        "rounds": 2,
        "shipping_method": "ticket_delivery",
        "shipping_amount": 300.0,
        "total_quote_amount": 900.0,
        "total_quote_discount": 0.0,
        "final_total_quote_amount": 1200.0,
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
          "request_uuid": "48871474724327145600",
          "email": "jessicacooper@example.com",
          "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
          "request_description": "E2E test request via silvaengine_gateway",
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
                  "batch_no": "AF6267-20260912",
                  "qty": "2"
                }
              ],
              "qty": "2",
              "pax_breakdown": {
                "adult": "2"
              }
            }
          ],
          "notes": "Updated via run_integration.py",
          "bundle_uuid": null,
          "status": "confirmed",
          "expired_at": "2026-12-31T23:59:59",
          "created_at": "2026-06-17T22:43:26.117930",
          "updated_by": "MCP",
          "updated_at": "2026-06-17T22:44:33.567681",
          "quotes": [
            {
              "final_total_quote_amount": "1200",
              "provider_corp_external_id": "AIRLINE-AF",
              "rounds": "2",
              "shipping_amount": "300",
              "status": "confirmed",
              "total_quote_amount": "900",
              "total_quote_discount": "0",
              "created_at": "2026-06-17 22:46:53.897669",
              "notes": "Confirmed setup quote for create_installments",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "19450419734386851968",
              "request_uuid": "48871474724327145600",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-17 22:47:25.341833",
              "updated_by": "MCP"
            },
            {
              "final_total_quote_amount": "875",
              "provider_corp_external_id": "AIRLINE-AF",
              "rounds": "0",
              "shipping_amount": "25",
              "status": "confirmed",
              "total_quote_amount": "900",
              "total_quote_discount": "50",
              "created_at": "2026-06-17 22:44:40.558317",
              "notes": "Updated via integration test",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "59882695090073780352",
              "request_uuid": "48871474724327145600",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-17 22:45:46.008050",
              "updated_by": "MCP"
            },
            {
              "final_total_quote_amount": "1200",
              "provider_corp_external_id": "AIRLINE-AF",
              "rounds": "1",
              "shipping_amount": "300",
              "status": "confirmed",
              "total_quote_amount": "900",
              "total_quote_discount": "0",
              "created_at": "2026-06-17 22:46:15.398445",
              "notes": "Confirmed setup quote for create_installment",
              "partition_key": "gpt#nestaging",
              "quote_uuid": "87693521885660725376",
              "request_uuid": "48871474724327145600",
              "shipping_method": "ticket_delivery",
              "updated_at": "2026-06-17 22:46:46.682841",
              "updated_by": "MCP"
            }
          ],
          "files": [],
          "bundle": null
        },
        "quote_items": [
          {
            "batch_no": "AF6267-20260912",
            "created_at": "2026-06-17 22:47:01.245445",
            "final_subtotal": "900",
            "hold_expires_at": "2026-06-17 23:02:01.577496",
            "hold_token": "585d97553fd11339aae38d97b0b230ff",
            "item_uuid": "06041993713794695296",
            "partition_key": "gpt#nestaging",
            "pax_breakdown": {
              "adult": "2"
            },
            "price_per_uom": "450",
            "provider_item_uuid": "39876487618607726720",
            "qty": "2",
            "quote_item_uuid": "46075184622484865152",
            "quote_uuid": "19450419734386851968",
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
                "snapshotted_at": "2026-06-17 22:47:01.822245"
              }
            },
            "request_uuid": "48871474724327145600",
            "subtotal": "900",
            "subtotal_discount": "0",
            "subtotal_native": "900",
            "updated_at": "2026-06-17 22:47:01.245445",
            "updated_by": "MCP"
          }
        ],
        "installments": [
          {
            "installment_amount": "400",
            "installment_ratio": "33.33333333333333",
            "priority": "0",
            "status": "pending",
            "created_at": "2026-06-17 22:47:47.173823",
            "installment_uuid": "33044365256899444864",
            "partition_key": "gpt#nestaging",
            "payment_method": "bank_transfer",
            "quote_uuid": "19450419734386851968",
            "request_uuid": "48871474724327145600",
            "scheduled_date": "2026-08-15 22:47:43",
            "updated_at": "2026-06-17 22:47:47.173823",
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
            "updated_at": "2026-06-01 22:24
... (truncated)
```

### 26. installments / update_installment (uuid=284520512028...)

- Method: `update_installment`
- Status: `pass`
- Elapsed: `30515.62 ms`

Arguments:

```json
{
  "quote_uuid": "59882695090073780352",
  "installment_uuid": "28452051202817933440",
  "status": "paid"
}
```

Output:

```json
{
  "quote_uuid": "59882695090073780352",
  "installment_uuid": "28452051202817933440",
  "request_uuid": "48871474724327145600",
  "priority": 0,
  "partition_key": "gpt#nestaging",
  "installment_amount": 875.0,
  "installment_ratio": 100.0,
  "salesorder_no": null,
  "scheduled_date": "2026-06-17T22:45:57",
  "payment_method": "bank_transfer",
  "status": "paid",
  "updated_by": "MCP",
  "created_at": "2026-06-17T22:46:00.397145",
  "updated_at": "2026-06-17T22:48:03.128710",
  "quote": {
    "request_uuid": "48871474724327145600",
    "quote_uuid": "59882695090073780352",
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
    "notes": "Updated via integration test",
    "status": "confirmed",
    "expired_at": null,
    "request": {
      "partition_key": "gpt#nestaging",
      "endpoint_id": "gpt",
      "part_id": "nestaging",
      "request_uuid": "48871474724327145600",
      "email": "jessicacooper@example.com",
      "request_title": "Integration test: Flight ATL->ORD Premium Economy (updated)",
      "request_description": "E2E test request via silvaengine_gateway",
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
              "batch_no": "AF6267-20260912",
              "qty": "2"
            }
          ],
          "qty": "2",
          "pax_breakdown": {
            "adult": "2"
          }
        }
      ],
      "notes": "Updated via run_integration.py",
      "bundle_uuid": null,
      "status": "confirmed",
      "expired_at": "2026-12-31T23:59:59",
      "created_at": "2026-06-17T22:43:26.117930",
      "updated_by": "MCP",
      "updated_at": "2026-06-17T22:44:33.567681",
      "quotes": [
        {
          "final_total_quote_amount": "1200",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "2",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "0",
          "created_at": "2026-06-17 22:46:53.897669",
          "notes": "Confirmed setup quote for create_installments",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "19450419734386851968",
          "request_uuid": "48871474724327145600",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-17 22:47:25.341833",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "875",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "0",
          "shipping_amount": "25",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "50",
          "created_at": "2026-06-17 22:44:40.558317",
          "notes": "Updated via integration test",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "59882695090073780352",
          "request_uuid": "48871474724327145600",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-17 22:45:46.008050",
          "updated_by": "MCP"
        },
        {
          "final_total_quote_amount": "1200",
          "provider_corp_external_id": "AIRLINE-AF",
          "rounds": "1",
          "shipping_amount": "300",
          "status": "confirmed",
          "total_quote_amount": "900",
          "total_quote_discount": "0",
          "created_at": "2026-06-17 22:46:15.398445",
          "notes": "Confirmed setup quote for create_installment",
          "partition_key": "gpt#nestaging",
          "quote_uuid": "87693521885660725376",
          "request_uuid": "48871474724327145600",
          "shipping_method": "ticket_delivery",
          "updated_at": "2026-06-17 22:46:46.682841",
          "updated_by": "MCP"
        }
      ],
      "files": [],
      "bundle": null
    },
    "quote_items": [
      {
        "batch_no": "AF6267-20260912",
        "created_at": "2026-06-17 22:44:47.987825",
        "final_subtotal": "850",
        "hold_expires_at": "2026-06-17 22:59:48.315668",
        "hold_token": "5f094e9e028c695eab6475383f0f5224",
        "item_uuid": "06041993713794695296",
        "notes": "Integration test discount",
        "partition_key": "gpt#nestaging",
        "pax_breakdown": {
          "adult": "2"
        },
        "price_per_uom": "450",
        "provider_item_uuid": "39876487618607726720",
        "qty": "2",
        "quote_item_uuid": "93812712643569401984",
        "quote_uuid": "59882695090073780352",
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
            "snapshotted_at": "2026-06-17 22:44:48.564014"
          }
        },
        "request_uuid": "48871474724327145600",
        "subtotal": "900",
        "subtotal_discount": "50",
        "subtotal_native": "900",
        "updated_at": "2026-06-17 22:45:23.631651",
        "updated_by": "MCP"
      }
    ],
    "installments": [
      {
        "installment_amount": "875",
        "installment_ratio": "100",
        "priority": "0",
        "status": "paid",
        "created_at": "2026-06-17 22:46:00.397145",
        "installment_uuid": "28452051202817933440",
        "partition_key": "gpt#nestaging",
        "payment_method": "bank_transfer",
        "quote_uuid": "59882695090073780352",
        "request_uuid": "48871474724327145600",
        "scheduled_date": "2026-06-17 22:45:57",
        "updated_at": "2026-06-17 22:48:03.128710",
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
          "season
... (truncated)
```
