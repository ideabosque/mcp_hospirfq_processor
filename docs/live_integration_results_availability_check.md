# MCP HospiRFQ Processor Live Integration Results

- Generated at: `2026-06-17T22:33:29.547554+00:00`
- Gateway: `http://localhost:8765`
- Endpoint: `gpt`
- Partition: `nestaging`
- GraphQL URL: `http://localhost:8765/gpt/nestaging/ai_rfq_graphql`
- Dependency order: `availability`
- Passed: `2`
- Error responses: `0`
- Failed: `0`
- Total calls: `2`

## Function Results

### 1. availability / check_availability

- Method: `check_availability`
- Status: `pass`
- Elapsed: `3647.74 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "55349863084404523136",
  "service_start_at": "2026-08-11T08:30:00Z",
  "service_end_at": "2026-08-11T20:57:51.046308Z",
  "batch_no": "AF8751-20260811",
  "qty": 2
}
```

Output:

```json
{
  "operation": "check",
  "provider_item_uuid": "55349863084404523136",
  "batch_no": "AF8751-20260811",
  "service_start_at": "2026-08-11T08:30:00+00:00",
  "service_end_at": "2026-08-11T20:57:51.046308+00:00",
  "available": false,
  "hold_token": null,
  "expires_at": null,
  "payload": {
    "reason": "insufficient_availability"
  },
  "fetched_at": "2026-06-17T22:33:26.240810+00:00",
  "ttl_seconds": null,
  "error_code": null,
  "error_message": null
}
```

### 2. availability / acquire_availability_hold

- Method: `acquire_availability_hold`
- Status: `pass`
- Elapsed: `3303.13 ms`

Arguments:

```json
{
  "partition_key": "gpt#nestaging",
  "provider_item_uuid": "55349863084404523136",
  "service_start_at": "2026-08-11T08:30:00Z",
  "service_end_at": "2026-08-11T20:57:51.046308Z",
  "qty": 2,
  "batch_no": "AF8751-20260811",
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
    "provider_item_uuid": "55349863084404523136",
    "batch_no": "AF8751-20260811",
    "service_start_at": "2026-08-11T08:30:00+00:00",
    "service_end_at": "2026-08-11T20:57:51.046308+00:00",
    "available": false,
    "hold_token": null,
    "expires_at": null,
    "payload": {
      "reason": "insufficient_availability"
    },
    "fetched_at": "2026-06-17T22:33:29.543544+00:00",
    "ttl_seconds": null,
    "error_code": null,
    "error_message": null
  }
}
```
