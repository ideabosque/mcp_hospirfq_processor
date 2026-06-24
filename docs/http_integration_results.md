# MCP HospiRFQ Processor HTTP Integration Results (MCPHttpClient)

- Generated at: `2026-06-24T05:36:49.338439+00:00`
- Gateway: `http://localhost:8765`
- MCP REST URL: `http://localhost:8765/gpt/mcp`
- Endpoint: `gpt`
- Partition: `nestaging`
- Transport: MCPHttpClient → JSON-RPC → gateway `/mcp`
- Dependency order: `items, requests, quotes, pricing, installments, files, segments, availability, bundles, cancellation, catalog`
- Passed: `2`
- Error responses: `5`
- Failed: `31`
- Total calls: `38`

## Executive Summary

End-to-end HTTP integration testing was executed through the `mcp_http_client.MCPHttpClient` against the `silvaengine_gateway` REST/JSON-RPC MCP endpoint (`/{endpoint_id}/mcp`, with `Part-Id` sent as a request header). Each tool was invoked via JSON-RPC `tools/call`, exercising the full agent → gateway → `MCPHospiRFQProcessor` stack. The gateway handles all backend dispatch internally. The run completed with 2 passing function calls, 5 error responses, and 31 failures.

## Scope

- In scope: MCP JSON-RPC transport (initialize, tools/list, tools/call), gateway MCP dispatch, MCPHospiRFQProcessor tool execution. The gateway handles backend dispatch internally.
- Out of scope: production validation, destructive cleanup, load testing, UI testing.

## Function Results

### 1. items / search_items (flight type)

- Method: `search_items`
- Status: `fail`
- Elapsed: `15.94 ms`

Arguments:

```json
{
  "item_type": "flight",
  "limit": 10,
  "page_number": 1
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 2. items / get_item (Flight ATL->ORD Premium Economy)

- Method: `get_item`
- Status: `fail`
- Elapsed: `3.84 ms`

Arguments:

```json
{
  "item_uuid": "06041993713794695296"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 3. items / get_provider_items (with batches)

- Method: `get_provider_items`
- Status: `fail`
- Elapsed: `4.15 ms`

Arguments:

```json
{
  "item_uuid": "06041993713794695296"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 4. requests / submit_rfq_request

- Method: `submit_rfq_request`
- Status: `fail`
- Elapsed: `4.22 ms`

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

Error:

```text
MCP Error -32603: Internal error
```

### 5. requests / get_rfq_request (seeded)

- Method: `get_rfq_request`
- Status: `fail`
- Elapsed: `4.24 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 6. requests / search_rfq_requests

- Method: `search_rfq_requests`
- Status: `fail`
- Elapsed: `4.23 ms`

Arguments:

```json
{
  "limit": 5,
  "page_number": 1
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 7. requests / update_rfq_request

- Method: `update_rfq_request`
- Status: `fail`
- Elapsed: `4.35 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "request_title": "HTTP integration test: Flight ATL->ORD Premium Economy (updated)",
  "notes": "Updated via run_http_integration.py"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 8. requests / add_item_to_rfq_request

- Method: `add_item_to_rfq_request`
- Status: `fail`
- Elapsed: `3.93 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "item": {
    "item_uuid": "52065619693805781120",
    "item_name": "Flight ATL->ORD Economy",
    "qty": 1
  }
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 9. requests / remove_item_from_rfq_request

- Method: `remove_item_from_rfq_request`
- Status: `fail`
- Elapsed: `3.82 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "item_uuid": "52065619693805781120"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 10. requests / assign_provider_item_to_request_item

- Method: `assign_provider_item_to_request_item`
- Status: `fail`
- Elapsed: `3.93 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720",
  "provider_corp_external_id": "AIRLINE-AF",
  "qty": 2,
  "batch_no": "AF5319-20260907"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 11. requests / remove_provider_item_from_request_item

- Method: `remove_provider_item_from_request_item`
- Status: `fail`
- Elapsed: `5.28 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 12. requests / assign_provider_item_to_request_item (for quote workflow)

- Method: `assign_provider_item_to_request_item`
- Status: `fail`
- Elapsed: `3.72 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "item_uuid": "06041993713794695296",
  "provider_item_uuid": "39876487618607726720",
  "provider_corp_external_id": "AIRLINE-AF",
  "qty": 2,
  "batch_no": "AF5319-20260907"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 13. quotes / confirm_request_and_create_quotes

- Method: `confirm_request_and_create_quotes`
- Status: `fail`
- Elapsed: `3.72 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "provider_corp_external_ids": [
    "AIRLINE-AF"
  ],
  "segment_uuid": "61268299727527493760",
  "batch_no": "AF5319-20260907",
  "service_start_at": "2026-09-07T12:00:00Z",
  "service_end_at": "2026-09-07T14:37:07.381744Z"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 14. quotes / get_quote

- Method: `get_quote`
- Status: `fail`
- Elapsed: `4.25 ms`

Arguments:

```json
{
  "quote_uuid": "83893620897501692032",
  "request_uuid": "96306650268729098368"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 15. quotes / search_quotes

- Method: `search_quotes`
- Status: `fail`
- Elapsed: `6.19 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "limit": 10,
  "page_number": 1
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 16. quotes / update_quote

- Method: `update_quote`
- Status: `fail`
- Elapsed: `4.41 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "quote_uuid": "83893620897501692032",
  "notes": "Updated via HTTP integration test",
  "shipping_method": "ticket_delivery",
  "shipping_amount": 25.0
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 17. quotes / update_quote_item

- Method: `update_quote_item`
- Status: `fail`
- Elapsed: `22.09 ms`

Arguments:

```json
{
  "quote_uuid": "83893620897501692032",
  "quote_item_uuid": "73631515167125684352",
  "request_uuid": "96306650268729098368",
  "discount_amount": 50.0,
  "notes": "HTTP integration test discount"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 18. pricing / get_item_price_tiers

- Method: `get_item_price_tiers`
- Status: `fail`
- Elapsed: `4.68 ms`

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

Error:

```text
MCP Error -32603: Internal error
```

### 19. pricing / get_discount_prompts

- Method: `get_discount_prompts`
- Status: `fail`
- Elapsed: `3.94 ms`

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

Error:

```text
MCP Error -32603: Internal error
```

### 20. pricing / calculate_quote_pricing

- Method: `calculate_quote_pricing`
- Status: `fail`
- Elapsed: `4.1 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "email": "jessicacooper@example.com"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 21. installments / confirm_quote_and_create_installments

- Method: `confirm_quote_and_create_installments`
- Status: `fail`
- Elapsed: `3.94 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "quote_uuid": "83893620897501692032",
  "create_single_installment": true,
  "payment_method": "bank_transfer"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 22. installments / get_installments

- Method: `get_installments`
- Status: `fail`
- Elapsed: `3.79 ms`

Arguments:

```json
{
  "quote_uuid": "83893620897501692032",
  "limit": 10,
  "page_number": 1
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 23. installments / setup submit_rfq_request (create_installment)

- Method: `submit_rfq_request`
- Status: `fail`
- Elapsed: `3.8 ms`

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

Error:

```text
MCP Error -32603: Internal error
```

### 24. installments / create_installment

- Method: `create_installment`
- Status: `fail`
- Elapsed: `4.11 ms`

Arguments:

```json
{
  "quote_uuid": "83893620897501692032",
  "request_uuid": "96306650268729098368",
  "installment_amount": 100.0,
  "payment_method": "credit_card"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 25. installments / setup submit_rfq_request (create_installments)

- Method: `submit_rfq_request`
- Status: `fail`
- Elapsed: `3.96 ms`

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

Error:

```text
MCP Error -32603: Internal error
```

### 26. installments / create_installments

- Method: `create_installments`
- Status: `fail`
- Elapsed: `4.3 ms`

Arguments:

```json
{
  "quote_uuid": "83893620897501692032",
  "request_uuid": "96306650268729098368",
  "interval_num": 3,
  "total_pay_period": 6,
  "payment_method": "bank_transfer"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 27. installments / update_installment (uuid=000000000000...)

- Method: `update_installment`
- Status: `fail`
- Elapsed: `4.16 ms`

Arguments:

```json
{
  "quote_uuid": "83893620897501692032",
  "installment_uuid": "00000000000000000000",
  "status": "paid"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 28. files / upload_rfq_file

- Method: `upload_rfq_file`
- Status: `fail`
- Elapsed: `4.55 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "file_name": "http_integration_test_spec.pdf",
  "email": "jessicacooper@example.com"
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 29. files / get_rfq_files

- Method: `get_rfq_files`
- Status: `fail`
- Elapsed: `3.75 ms`

Arguments:

```json
{
  "request_uuid": "96306650268729098368",
  "limit": 10,
  "page_number": 1
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 30. segments / get_segment_contacts

- Method: `get_segment_contacts`
- Status: `fail`
- Elapsed: `4.14 ms`

Arguments:

```json
{
  "email": "jessicacooper@example.com",
  "limit": 10,
  "page_number": 1
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 31. availability / check_availability

- Method: `check_availability`
- Status: `fail`
- Elapsed: `4.36 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720",
  "service_start_at": "2026-09-07T12:00:00Z",
  "service_end_at": "2026-09-07T14:37:07.381744Z",
  "batch_no": "AF5319-20260907",
  "qty": 2
}
```

Error:

```text
MCP Error -32603: Internal error
```

### 32. availability / acquire_availability_hold

- Method: `acquire_availability_hold`
- Status: `error`
- Elapsed: `4916.62 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720",
  "service_start_at": "2026-09-07T12:00:00Z",
  "service_end_at": "2026-09-07T14:37:07.381744Z",
  "qty": 2,
  "batch_no": "AF5319-20260907",
  "pax_breakdown": {
    "adult": 2
  }
}
```

Error:

```text
GraphQL error: (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type uuid: "39876487618607726720"
LINE 4: ...RE rfq_provider_item_batches.provider_item_uuid = '398764876...
                                                             ^

[SQL: SELECT count(*) AS count_1 
FROM (SELECT rfq_provider_item_batches.provider_item_uuid AS rfq_provider_item_batches_provider_item_uuid, rfq_provider_item_batches.batch_no AS rfq_provider_item_batches_batch_no, rfq_provider_item_batches.item_uuid AS rfq_provider_item_batches_item_uuid, rfq_provider_item_batches.partition_key AS rfq_provider_item_batches_partition_key, rfq_provider_item_batches.expired_at AS rfq_provider_item_batches_expired_at, rfq_provider_item_batches.produced_at AS rfq_provider_item_batches_produced_at, rfq_provider_item_batches.service_start_at AS rfq_provider_item_batches_service_start_at, rfq_provider_item_batches.service_end_at AS rfq_provider_item_batches_service_end_at, rfq_provider_item_batches.cost_per_uom AS rfq_provider_item_batches_cost_per_uom, rfq_provider_item_batches.freight_cost_per_uom AS rfq_provider_item_batches_freight_cost_per_uom, rfq_provider_item_batches.additional_cost_per_uom AS rfq_provider_item_batches_additional_cost_per_uom, rfq_provider_item_batches.total_cost_per_uom AS rfq_provider_item_batches_total_cost_per_uom, rfq_provider_item_batches.guardrail_margin_per_uom AS rfq_provider_item_batches_guardrail_margin_per_uom, rfq_provider_item_batches.guardrail_price_per_uom AS rfq_provider_item_batches_guardrail_price_per_uom, rfq_provider_item_batches.slow_move_item AS rfq_provider_item_batches_slow_move_item, rfq_provider_item_batches.in_stock AS rfq_provider_item_batches_in_stock, rfq_provider_item_batches.availability_qty AS rfq_provider_item_batches_availability_qty, rfq_provider_item_batches.currency AS rfq_provider_item_batches_currency, rfq_provider_item_batches.cancellation_policy_uuid AS rfq_provider_item_batches_cancellation_policy_uuid, rfq_provider_item_batches.created_at AS rfq_provider_item_batches_created_at, rfq_provider_item_batches.updated_by AS rfq_provider_item_batches_updated_by, rfq_provider_item_batches.updated_at AS rfq_provider_item_batches_updated_at 
FROM rfq_provider_item_batches 
WHERE rfq_provider_item_batches.provider_item_uuid = %(provider_item_uuid_1)s::UUID AND rfq_provider_item_batches.partition_key = %(partition_key_1)s AND rfq_provider_item_batches.service_start_at < %(service_start_at_1)s AND rfq_provider_item_batches.service_end_at > %(service_end_at_1)s) AS anon_1]
[parameters: {'provider_item_uuid_1': '39876487618607726720', 'partition_key_1': 'gpt#nestaging', 'service_start_at_1': datetime.datetime(2026, 9, 7, 14, 37, 7, 381744, tzinfo=tzutc()), 'service_end_at_1': datetime.datetime(2026, 9, 7, 12, 0, tzinfo=tzutc())}]
(Background on this error at: https://sqlalche.me/e/20/9h9h)

GraphQL request:3:17
3 |                 acquireAvailabilityHold(batchNo: $batchNo, paxBreakdown: $paxBre
  |                 ^
  | akdown, providerItemUuid: $providerItemUuid, qty: $qty, serviceEndAt: $serviceEn
```

Output:

```json
{
  "error": "GraphQL error: (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type uuid: \"39876487618607726720\"\nLINE 4: ...RE rfq_provider_item_batches.provider_item_uuid = '398764876...\n                                                             ^\n\n[SQL: SELECT count(*) AS count_1 \nFROM (SELECT rfq_provider_item_batches.provider_item_uuid AS rfq_provider_item_batches_provider_item_uuid, rfq_provider_item_batches.batch_no AS rfq_provider_item_batches_batch_no, rfq_provider_item_batches.item_uuid AS rfq_provider_item_batches_item_uuid, rfq_provider_item_batches.partition_key AS rfq_provider_item_batches_partition_key, rfq_provider_item_batches.expired_at AS rfq_provider_item_batches_expired_at, rfq_provider_item_batches.produced_at AS rfq_provider_item_batches_produced_at, rfq_provider_item_batches.service_start_at AS rfq_provider_item_batches_service_start_at, rfq_provider_item_batches.service_end_at AS rfq_provider_item_batches_service_end_at, rfq_provider_item_batches.cost_per_uom AS rfq_provider_item_batches_cost_per_uom, rfq_provider_item_batches.freight_cost_per_uom AS rfq_provider_item_batches_freight_cost_per_uom, rfq_provider_item_batches.additional_cost_per_uom AS rfq_provider_item_batches_additional_cost_per_uom, rfq_provider_item_batches.total_cost_per_uom AS rfq_provider_item_batches_total_cost_per_uom, rfq_provider_item_batches.guardrail_margin_per_uom AS rfq_provider_item_batches_guardrail_margin_per_uom, rfq_provider_item_batches.guardrail_price_per_uom AS rfq_provider_item_batches_guardrail_price_per_uom, rfq_provider_item_batches.slow_move_item AS rfq_provider_item_batches_slow_move_item, rfq_provider_item_batches.in_stock AS rfq_provider_item_batches_in_stock, rfq_provider_item_batches.availability_qty AS rfq_provider_item_batches_availability_qty, rfq_provider_item_batches.currency AS rfq_provider_item_batches_currency, rfq_provider_item_batches.cancellation_policy_uuid AS rfq_provider_item_batches_cancellation_policy_uuid, rfq_provider_item_batches.created_at AS rfq_provider_item_batches_created_at, rfq_provider_item_batches.updated_by AS rfq_provider_item_batches_updated_by, rfq_provider_item_batches.updated_at AS rfq_provider_item_batches_updated_at \nFROM rfq_provider_item_batches \nWHERE rfq_provider_item_batches.provider_item_uuid = %(provider_item_uuid_1)s::UUID AND rfq_provider_item_batches.partition_key = %(partition_key_1)s AND rfq_provider_item_batches.service_start_at < %(service_start_at_1)s AND rfq_provider_item_batches.service_end_at > %(service_end_at_1)s) AS anon_1]\n[parameters: {'provider_item_uuid_1': '39876487618607726720', 'partition_key_1': 'gpt#nestaging', 'service_start_at_1': datetime.datetime(2026, 9, 7, 14, 37, 7, 381744, tzinfo=tzutc()), 'service_end_at_1': datetime.datetime(2026, 9, 7, 12, 0, tzinfo=tzutc())}]\n(Background on this error at: https://sqlalche.me/e/20/9h9h)\n\nGraphQL request:3:17\n3 |                 acquireAvailabilityHold(batchNo: $batchNo, paxBreakdown: $paxBre\n  |                 ^\n  | akdown, providerItemUuid: $providerItemUuid, qty: $qty, serviceEndAt: $serviceEn",
  "error_code": "GRAPHQL_QUERY_FAILED",
  "details": {
    "function_name": "rfq_graphql",
    "operation": "acquireAvailabilityHold"
  }
}
```

### 33. bundles / search_bundles (itinerary type)

- Method: `search_bundles`
- Status: `pass`
- Elapsed: `4590.05 ms`

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

### 34. bundles / get_bundle (FLT-ITIN-001)

- Method: `get_bundle`
- Status: `error`
- Elapsed: `4593.55 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "80092055917037633664"
}
```

Error:

```text
GraphQL error: (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type uuid: "80092055917037633664"
LINE 4: ...y = 'gpt#nestaging' AND rfq_bundles.bundle_uuid = '800920559...
                                                             ^

[SQL: SELECT count(*) AS count_1 
FROM (SELECT rfq_bundles.partition_key AS rfq_bundles_partition_key, rfq_bundles.bundle_uuid AS rfq_bundles_bundle_uuid, rfq_bundles.bundle_code AS rfq_bundles_bundle_code, rfq_bundles.bundle_name AS rfq_bundles_bundle_name, rfq_bundles.bundle_type AS rfq_bundles_bundle_type, rfq_bundles.description AS rfq_bundles_description, rfq_bundles.extra AS rfq_bundles_extra, rfq_bundles.status AS rfq_bundles_status, rfq_bundles.created_at AS rfq_bundles_created_at, rfq_bundles.updated_by AS rfq_bundles_updated_by, rfq_bundles.updated_at AS rfq_bundles_updated_at 
FROM rfq_bundles 
WHERE rfq_bundles.partition_key = %(partition_key_1)s AND rfq_bundles.bundle_uuid = %(bundle_uuid_1)s::UUID) AS anon_1]
[parameters: {'partition_key_1': 'gpt#nestaging', 'bundle_uuid_1': '80092055917037633664'}]
(Background on this error at: https://sqlalche.me/e/20/9h9h)

GraphQL request:3:17
2 |             query bundle($bundleUuid: String!) {
3 |                 bundle(bundleUuid: $bundleUuid) {
  |                 ^
4 |                     partitionKey bundleUuid bundleCode bundleName bundleType description extra status createdAt updatedBy updatedAt components { partitionKey bundleComponentUuid bundleUuid itemUuid providerItemUuid componentRole required defaultQty sortOrder extra status createdAt updatedBy updatedAt}
```

Output:

```json
{
  "error": "GraphQL error: (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type uuid: \"80092055917037633664\"\nLINE 4: ...y = 'gpt#nestaging' AND rfq_bundles.bundle_uuid = '800920559...\n                                                             ^\n\n[SQL: SELECT count(*) AS count_1 \nFROM (SELECT rfq_bundles.partition_key AS rfq_bundles_partition_key, rfq_bundles.bundle_uuid AS rfq_bundles_bundle_uuid, rfq_bundles.bundle_code AS rfq_bundles_bundle_code, rfq_bundles.bundle_name AS rfq_bundles_bundle_name, rfq_bundles.bundle_type AS rfq_bundles_bundle_type, rfq_bundles.description AS rfq_bundles_description, rfq_bundles.extra AS rfq_bundles_extra, rfq_bundles.status AS rfq_bundles_status, rfq_bundles.created_at AS rfq_bundles_created_at, rfq_bundles.updated_by AS rfq_bundles_updated_by, rfq_bundles.updated_at AS rfq_bundles_updated_at \nFROM rfq_bundles \nWHERE rfq_bundles.partition_key = %(partition_key_1)s AND rfq_bundles.bundle_uuid = %(bundle_uuid_1)s::UUID) AS anon_1]\n[parameters: {'partition_key_1': 'gpt#nestaging', 'bundle_uuid_1': '80092055917037633664'}]\n(Background on this error at: https://sqlalche.me/e/20/9h9h)\n\nGraphQL request:3:17\n2 |             query bundle($bundleUuid: String!) {\n3 |                 bundle(bundleUuid: $bundleUuid) {\n  |                 ^\n4 |                     partitionKey bundleUuid bundleCode bundleName bundleType description extra status createdAt updatedBy updatedAt components { partitionKey bundleComponentUuid bundleUuid itemUuid providerItemUuid componentRole required defaultQty sortOrder extra status createdAt updatedBy updatedAt}",
  "error_code": "GRAPHQL_QUERY_FAILED",
  "details": {
    "function_name": "rfq_graphql",
    "operation": "bundle"
  }
}
```

### 35. bundles / search_bundle_components

- Method: `search_bundle_components`
- Status: `error`
- Elapsed: `4589.01 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "bundle_uuid": "80092055917037633664"
}
```

Error:

```text
GraphQL error: (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type uuid: "80092055917037633664"
LINE 4: ...estaging' AND rfq_bundle_components.bundle_uuid = '800920559...
                                                             ^

[SQL: SELECT count(*) AS count_1 
FROM (SELECT rfq_bundle_components.partition_key AS rfq_bundle_components_partition_key, rfq_bundle_components.bundle_component_uuid AS rfq_bundle_components_bundle_component_uuid, rfq_bundle_components.bundle_uuid AS rfq_bundle_components_bundle_uuid, rfq_bundle_components.item_uuid AS rfq_bundle_components_item_uuid, rfq_bundle_components.provider_item_uuid AS rfq_bundle_components_provider_item_uuid, rfq_bundle_components.component_role AS rfq_bundle_components_component_role, rfq_bundle_components.required AS rfq_bundle_components_required, rfq_bundle_components.default_qty AS rfq_bundle_components_default_qty, rfq_bundle_components.sort_order AS rfq_bundle_components_sort_order, rfq_bundle_components.extra AS rfq_bundle_components_extra, rfq_bundle_components.status AS rfq_bundle_components_status, rfq_bundle_components.created_at AS rfq_bundle_components_created_at, rfq_bundle_components.updated_by AS rfq_bundle_components_updated_by, rfq_bundle_components.updated_at AS rfq_bundle_components_updated_at 
FROM rfq_bundle_components 
WHERE rfq_bundle_components.partition_key = %(partition_key_1)s AND rfq_bundle_components.bundle_uuid = %(bundle_uuid_1)s::UUID) AS anon_1]
[parameters: {'partition_key_1': 'gpt#nestaging', 'bundle_uuid_1': '80092055917037633664'}]
(Background on this error at: https://sqlalche.me/e/20/9h9h)

GraphQL request:3:17
3 |                 bundleComponentList(pageNumber: $pageNumber, limit: $limit, bund
  |                 ^
  | leUuid: $bundleUuid, itemUuid: $itemUuid, providerItemUuid: $providerItemUuid, c
```

Output:

```json
{
  "error": "GraphQL error: (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type uuid: \"80092055917037633664\"\nLINE 4: ...estaging' AND rfq_bundle_components.bundle_uuid = '800920559...\n                                                             ^\n\n[SQL: SELECT count(*) AS count_1 \nFROM (SELECT rfq_bundle_components.partition_key AS rfq_bundle_components_partition_key, rfq_bundle_components.bundle_component_uuid AS rfq_bundle_components_bundle_component_uuid, rfq_bundle_components.bundle_uuid AS rfq_bundle_components_bundle_uuid, rfq_bundle_components.item_uuid AS rfq_bundle_components_item_uuid, rfq_bundle_components.provider_item_uuid AS rfq_bundle_components_provider_item_uuid, rfq_bundle_components.component_role AS rfq_bundle_components_component_role, rfq_bundle_components.required AS rfq_bundle_components_required, rfq_bundle_components.default_qty AS rfq_bundle_components_default_qty, rfq_bundle_components.sort_order AS rfq_bundle_components_sort_order, rfq_bundle_components.extra AS rfq_bundle_components_extra, rfq_bundle_components.status AS rfq_bundle_components_status, rfq_bundle_components.created_at AS rfq_bundle_components_created_at, rfq_bundle_components.updated_by AS rfq_bundle_components_updated_by, rfq_bundle_components.updated_at AS rfq_bundle_components_updated_at \nFROM rfq_bundle_components \nWHERE rfq_bundle_components.partition_key = %(partition_key_1)s AND rfq_bundle_components.bundle_uuid = %(bundle_uuid_1)s::UUID) AS anon_1]\n[parameters: {'partition_key_1': 'gpt#nestaging', 'bundle_uuid_1': '80092055917037633664'}]\n(Background on this error at: https://sqlalche.me/e/20/9h9h)\n\nGraphQL request:3:17\n3 |                 bundleComponentList(pageNumber: $pageNumber, limit: $limit, bund\n  |                 ^\n  | leUuid: $bundleUuid, itemUuid: $itemUuid, providerItemUuid: $providerItemUuid, c",
  "error_code": "GRAPHQL_QUERY_FAILED",
  "details": {
    "function_name": "rfq_graphql",
    "operation": "bundleComponentList"
  }
}
```

### 36. cancellation / get_cancellation_policy (Business Fare)

- Method: `get_cancellation_policy`
- Status: `error`
- Elapsed: `4560.26 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "policy_uuid": "70591963290008567936"
}
```

Error:

```text
GraphQL error: (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type uuid: "70591963290008567936"
LINE 4: ...ging' AND rfq_cancellation_policies.policy_uuid = '705919632...
                                                             ^

[SQL: SELECT count(*) AS count_1 
FROM (SELECT rfq_cancellation_policies.partition_key AS rfq_cancellation_policies_partition_key, rfq_cancellation_policies.policy_uuid AS rfq_cancellation_policies_policy_uuid, rfq_cancellation_policies.provider_item_uuid AS rfq_cancellation_policies_provider_item_uuid, rfq_cancellation_policies.label AS rfq_cancellation_policies_label, rfq_cancellation_policies.description AS rfq_cancellation_policies_description, rfq_cancellation_policies.tiers AS rfq_cancellation_policies_tiers, rfq_cancellation_policies.notes_template_uuid AS rfq_cancellation_policies_notes_template_uuid, rfq_cancellation_policies.status AS rfq_cancellation_policies_status, rfq_cancellation_policies.created_at AS rfq_cancellation_policies_created_at, rfq_cancellation_policies.updated_by AS rfq_cancellation_policies_updated_by, rfq_cancellation_policies.updated_at AS rfq_cancellation_policies_updated_at 
FROM rfq_cancellation_policies 
WHERE rfq_cancellation_policies.partition_key = %(partition_key_1)s AND rfq_cancellation_policies.policy_uuid = %(policy_uuid_1)s::UUID) AS anon_1]
[parameters: {'partition_key_1': 'gpt#nestaging', 'policy_uuid_1': '70591963290008567936'}]
(Background on this error at: https://sqlalche.me/e/20/9h9h)

GraphQL request:3:17
2 |             query cancellationPolicy($policyUuid: String!) {
3 |                 cancellationPolicy(policyUuid: $policyUuid) {
  |                 ^
4 |                     partitionKey policyUuid providerItemUuid label description tiers notesTemplateUuid status createdAt updatedBy updatedAt
```

Output:

```json
{
  "error": "GraphQL error: (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type uuid: \"70591963290008567936\"\nLINE 4: ...ging' AND rfq_cancellation_policies.policy_uuid = '705919632...\n                                                             ^\n\n[SQL: SELECT count(*) AS count_1 \nFROM (SELECT rfq_cancellation_policies.partition_key AS rfq_cancellation_policies_partition_key, rfq_cancellation_policies.policy_uuid AS rfq_cancellation_policies_policy_uuid, rfq_cancellation_policies.provider_item_uuid AS rfq_cancellation_policies_provider_item_uuid, rfq_cancellation_policies.label AS rfq_cancellation_policies_label, rfq_cancellation_policies.description AS rfq_cancellation_policies_description, rfq_cancellation_policies.tiers AS rfq_cancellation_policies_tiers, rfq_cancellation_policies.notes_template_uuid AS rfq_cancellation_policies_notes_template_uuid, rfq_cancellation_policies.status AS rfq_cancellation_policies_status, rfq_cancellation_policies.created_at AS rfq_cancellation_policies_created_at, rfq_cancellation_policies.updated_by AS rfq_cancellation_policies_updated_by, rfq_cancellation_policies.updated_at AS rfq_cancellation_policies_updated_at \nFROM rfq_cancellation_policies \nWHERE rfq_cancellation_policies.partition_key = %(partition_key_1)s AND rfq_cancellation_policies.policy_uuid = %(policy_uuid_1)s::UUID) AS anon_1]\n[parameters: {'partition_key_1': 'gpt#nestaging', 'policy_uuid_1': '70591963290008567936'}]\n(Background on this error at: https://sqlalche.me/e/20/9h9h)\n\nGraphQL request:3:17\n2 |             query cancellationPolicy($policyUuid: String!) {\n3 |                 cancellationPolicy(policyUuid: $policyUuid) {\n  |                 ^\n4 |                     partitionKey policyUuid providerItemUuid label description tiers notesTemplateUuid status createdAt updatedBy updatedAt",
  "error_code": "GRAPHQL_QUERY_FAILED",
  "details": {
    "function_name": "rfq_graphql",
    "operation": "cancellationPolicy"
  }
}
```

### 37. cancellation / search_cancellation_policies

- Method: `search_cancellation_policies`
- Status: `error`
- Elapsed: `4683.8 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "39876487618607726720"
}
```

Error:

```text
GraphQL error: (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type uuid: "39876487618607726720"
LINE 4: ...ND rfq_cancellation_policies.provider_item_uuid = '398764876...
                                                             ^

[SQL: SELECT count(*) AS count_1 
FROM (SELECT rfq_cancellation_policies.partition_key AS rfq_cancellation_policies_partition_key, rfq_cancellation_policies.policy_uuid AS rfq_cancellation_policies_policy_uuid, rfq_cancellation_policies.provider_item_uuid AS rfq_cancellation_policies_provider_item_uuid, rfq_cancellation_policies.label AS rfq_cancellation_policies_label, rfq_cancellation_policies.description AS rfq_cancellation_policies_description, rfq_cancellation_policies.tiers AS rfq_cancellation_policies_tiers, rfq_cancellation_policies.notes_template_uuid AS rfq_cancellation_policies_notes_template_uuid, rfq_cancellation_policies.status AS rfq_cancellation_policies_status, rfq_cancellation_policies.created_at AS rfq_cancellation_policies_created_at, rfq_cancellation_policies.updated_by AS rfq_cancellation_policies_updated_by, rfq_cancellation_policies.updated_at AS rfq_cancellation_policies_updated_at 
FROM rfq_cancellation_policies 
WHERE rfq_cancellation_policies.partition_key = %(partition_key_1)s AND rfq_cancellation_policies.provider_item_uuid = %(provider_item_uuid_1)s::UUID) AS anon_1]
[parameters: {'partition_key_1': 'gpt#nestaging', 'provider_item_uuid_1': '39876487618607726720'}]
(Background on this error at: https://sqlalche.me/e/20/9h9h)

GraphQL request:3:17
3 |                 cancellationPolicyList(pageNumber: $pageNumber, limit: $limit, p
  |                 ^
  | roviderItemUuid: $providerItemUuid, status: $status) {
```

Output:

```json
{
  "error": "GraphQL error: (psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type uuid: \"39876487618607726720\"\nLINE 4: ...ND rfq_cancellation_policies.provider_item_uuid = '398764876...\n                                                             ^\n\n[SQL: SELECT count(*) AS count_1 \nFROM (SELECT rfq_cancellation_policies.partition_key AS rfq_cancellation_policies_partition_key, rfq_cancellation_policies.policy_uuid AS rfq_cancellation_policies_policy_uuid, rfq_cancellation_policies.provider_item_uuid AS rfq_cancellation_policies_provider_item_uuid, rfq_cancellation_policies.label AS rfq_cancellation_policies_label, rfq_cancellation_policies.description AS rfq_cancellation_policies_description, rfq_cancellation_policies.tiers AS rfq_cancellation_policies_tiers, rfq_cancellation_policies.notes_template_uuid AS rfq_cancellation_policies_notes_template_uuid, rfq_cancellation_policies.status AS rfq_cancellation_policies_status, rfq_cancellation_policies.created_at AS rfq_cancellation_policies_created_at, rfq_cancellation_policies.updated_by AS rfq_cancellation_policies_updated_by, rfq_cancellation_policies.updated_at AS rfq_cancellation_policies_updated_at \nFROM rfq_cancellation_policies \nWHERE rfq_cancellation_policies.partition_key = %(partition_key_1)s AND rfq_cancellation_policies.provider_item_uuid = %(provider_item_uuid_1)s::UUID) AS anon_1]\n[parameters: {'partition_key_1': 'gpt#nestaging', 'provider_item_uuid_1': '39876487618607726720'}]\n(Background on this error at: https://sqlalche.me/e/20/9h9h)\n\nGraphQL request:3:17\n3 |                 cancellationPolicyList(pageNumber: $pageNumber, limit: $limit, p\n  |                 ^\n  | roviderItemUuid: $providerItemUuid, status: $status) {",
  "error_code": "GRAPHQL_QUERY_FAILED",
  "details": {
    "function_name": "rfq_graphql",
    "operation": "cancellationPolicyList"
  }
}
```

### 38. catalog / inquire_catalog

- Method: `inquire_catalog`
- Status: `pass`
- Elapsed: `11072.45 ms`

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
            "text": "Delta Air Lines (DL) operates flight service Flight NRT->CDG First from NRT to CDG in First class. First class non-stop service from Tokyo (NRT) to Paris (CDG). Base price $4500.0 USD per seat. Baggage allowance 32kg, meal included: True. Pricing tiers:   - adult: $4500.0 USD;   - child: $3375.0 USD;   - infant: $450.0 USD. Scheduled flights:\n  - Flight DL4000 departing 2026-09-05T21:15:00Z arriving 2026-09-06T08:30:40.740402Z with 7 seats available. Cancellation policy: First Fare Cancellation.\n  - Flight DL4822 departing 2026-09-18T14:45:00Z arriving 2026-09-18T23:28:08.831283Z with 7 seats available. Cancellation policy: First Fare Cancellation.\nThis is a First class flight product offered by Delta Air Lines on the NRT->CDG route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:45",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:45",
          "score": "0.7341679930686951",
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
          "score": "0.7325248122215271",
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
          "score": "0.7050315737724304",
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
          "score": "0.7014548778533936",
          "metadata": {}
        }
      },
      {
        "content": "",
        "metadata": {
          "node": {
            "index": 0,
            "text": "British Airways (BA) operates flight service Flight ORD->BOS Business from ORD to BOS in Business class. Business class non-stop service from Chicago (ORD) to Boston (BOS). Base price $1800.0 USD per seat. Baggage allowance 32kg, meal included: True. Pricing tiers:   - adult: $1800.0 USD;   - child: $1350.0 USD;   - infant: $180.0 USD. Scheduled flights:\n  - Flight BA1430 departing 2026-07-17T21:00:00Z arriving 2026-07-18T00:24:58.762088Z with 24 seats available. Cancellation policy: Business Fare Cancellation.\n  - Flight BA7142 departing 2026-08-08T11:00:00Z arriving 2026-08-08T16:28:08.421105Z with 26 seats available. Cancellation policy: Business Fare Cancellation.\nThis is a Business class flight product offered by British Airways on the ORD->BOS route."
          },
          "node_labels": [
            "__KGBuilder__",
            "Chunk"
          ],
          "element_id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:20",
          "id": "4:3b22411f-9c6a-4eb3-afc6-101df0d460f5:20",
          "score": "0.700347900390625",
          "metadata": {}
        }
      }
    ],
    "query": null,
    "total": 5,
    "page": 1,
    "limit": 5
  },
  "fetched_at": "2026-06-24T05:36:49.318064+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```
