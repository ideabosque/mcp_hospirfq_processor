# MCP HospiRFQ Processor Live Integration Results

- Generated at: `2026-06-17T22:35:48.875260+00:00`
- Gateway: `http://localhost:8765`
- Endpoint: `gpt`
- Partition: `nestaging`
- GraphQL URL: `http://localhost:8765/gpt/nestaging/ai_rfq_graphql`
- Dependency order: `catalog_discovery, availability`
- Passed: `8`
- Error responses: `0`
- Failed: `0`
- Total calls: `8`

## Function Results

### 1. catalog_discovery / inquire_catalog (select primary item)

- Method: `inquire_catalog`
- Status: `pass`
- Elapsed: `4393.38 ms`

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
          "score": "0.8713676929473877",
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
          "score": "0.7910864353179932",
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
          "score": "0.7605776190757751",
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
          "score": "0.7334754467010498",
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
          "score": "0.6800907850265503",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-17T22:35:25.392907+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 2. availability / check_availability

- Method: `check_availability`
- Status: `pass`
- Elapsed: `3323.93 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720",
  "service_start_at": "2026-09-12T19:00:00Z",
  "service_end_at": "2026-09-12T23:07:47.008532Z",
  "batch_no": "AF6267-20260912",
  "qty": 2
}
```

Output:

```json
{
  "operation": "check",
  "provider_item_uuid": "39876487618607726720",
  "batch_no": "AF6267-20260912",
  "service_start_at": "2026-09-12T19:00:00+00:00",
  "service_end_at": "2026-09-12T23:07:47.008532+00:00",
  "available": true,
  "hold_token": null,
  "expires_at": null,
  "payload": {
    "reason": "available",
    "matched_batches": 1,
    "available_batches": 1,
    "total_available_qty": 43.0,
    "slow_move": false
  },
  "fetched_at": "2026-06-17T22:35:28.716886+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 3. availability / acquire_availability_hold

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `3387.39 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720",
  "service_start_at": "2026-09-12T19:00:00Z",
  "service_end_at": "2026-09-12T23:07:47.008532Z",
  "qty": 2,
  "batch_no": "AF6267-20260912",
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
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
    "service_start_at": "2026-09-12T19:00:00+00:00",
    "service_end_at": "2026-09-12T23:07:47.008532+00:00",
    "available": true,
    "hold_token": "dd15f8b2d84e9807128f5617f5ec5b22",
    "expires_at": "2026-06-17T22:50:31.985646+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 43.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-17T22:35:32.105701+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 4. availability / confirm_availability_hold

- Method: `confirm_availability_hold`
- Status: `pass`
- Elapsed: `3258.22 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "dd15f8b2d84e9807128f5617f5ec5b22",
  "provider_item_uuid": "39876487618607726720",
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "availability": {
    "operation": "confirm_hold",
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
    "service_start_at": null,
    "service_end_at": null,
    "available": true,
    "hold_token": "dd15f8b2d84e9807128f5617f5ec5b22",
    "expires_at": null,
    "payload": {
      "reason": "hold_confirmed"
    },
    "fetched_at": "2026-06-17T22:35:35.362439+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```

### 5. availability / acquire_availability_hold (for release test)

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `3395.82 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720",
  "service_start_at": "2026-09-12T19:00:00Z",
  "service_end_at": "2026-09-12T23:07:47.008532Z",
  "qty": 1,
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
    "service_start_at": "2026-09-12T19:00:00+00:00",
    "service_end_at": "2026-09-12T23:07:47.008532+00:00",
    "available": true,
    "hold_token": "fe5c8228c67ec9941c5682b3bdeb4b61",
    "expires_at": "2026-06-17T22:50:38.652152+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 41.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-17T22:35:38.760278+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 6. availability / release_availability_hold

- Method: `release_availability_hold`
- Status: `pass`
- Elapsed: `3366.2 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "fe5c8228c67ec9941c5682b3bdeb4b61",
  "provider_item_uuid": "39876487618607726720",
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "availability": {
    "operation": "release_hold",
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
    "service_start_at": null,
    "service_end_at": null,
    "available": true,
    "hold_token": "fe5c8228c67ec9941c5682b3bdeb4b61",
    "expires_at": null,
    "payload": {
      "reason": "hold_released"
    },
    "fetched_at": "2026-06-17T22:35:42.124562+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```

### 7. availability / acquire_availability_hold (for expire test)

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `3491.36 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720",
  "service_start_at": "2026-09-12T19:00:00Z",
  "service_end_at": "2026-09-12T23:07:47.008532Z",
  "qty": 1,
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "availability": {
    "operation": "acquire_hold",
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
    "service_start_at": "2026-09-12T19:00:00+00:00",
    "service_end_at": "2026-09-12T23:07:47.008532+00:00",
    "available": true,
    "hold_token": "5513f0a870931db800b8f372ea0a5d32",
    "expires_at": "2026-06-17T22:50:45.505629+00:00",
    "payload": {
      "reason": "hold_acquired",
      "matched_batches": 1,
      "available_batches": 1,
      "total_available_qty": 41.0,
      "slow_move": false
    },
    "fetched_at": "2026-06-17T22:35:45.616281+00:00",
    "ttl_seconds": 900,
    "error_code": null,
    "error_message": null
  }
}
```

### 8. availability / expire_availability_hold

- Method: `expire_availability_hold`
- Status: `pass`
- Elapsed: `3254.42 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "hold_token": "5513f0a870931db800b8f372ea0a5d32",
  "provider_item_uuid": "39876487618607726720",
  "batch_no": "AF6267-20260912"
}
```

Output:

```json
{
  "availability": {
    "operation": "expire_hold",
    "provider_item_uuid": "39876487618607726720",
    "batch_no": "AF6267-20260912",
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
