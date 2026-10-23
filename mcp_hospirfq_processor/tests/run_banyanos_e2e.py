"""Live RFQ tool workflow over MCPHttpClient, using discovered Docker data."""
import argparse
import asyncio
import json
import logging
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx
from dotenv import dotenv_values
from mcp_http_client import MCPHttpClient
from mcp_hospirfq_processor import MCP_CONFIGURATION

BASE = "http://127.0.0.1:18000"
PARTITION = "banyan#nestaging"
HERE = Path(__file__).resolve()
OUT = HERE.parents[2] / "docs/test_results"
RECORDS = []
RUN = uuid.uuid4().hex[:10]


def error(value):
    if isinstance(value, dict):
        if value.get("error") or value.get("error_code") or value.get("errorCode"):
            return True
        return any(error(v) for v in value.values())
    if isinstance(value, list):
        return any(error(v) for v in value)
    return False


async def main(discover_only=False):
    credentials = dotenv_values(HERE.parents[4] / "banyanos/.e2e_anthropic/credentials.env")
    response = httpx.post(BASE + "/auth/token", data={"username": credentials["E2E_EMAIL"], "password": credentials["E2E_PASSWORD"]}, timeout=20)
    response.raise_for_status()
    token = response.json()["access_token"]
    async with MCPHttpClient(logging.getLogger("banyanos_e2e"), base_url=BASE+"/banyan/mcp", bearer_token=token, headers={"Part-Id": "nestaging"}, timeout=120) as client:
        tools = await client.list_tools()
        assert {t.name for t in tools} >= {t["name"] for t in MCP_CONFIGURATION["tools"]}
        async def call(name, args, expected_error=False):
            # The public and loopback GraphQL calls share gateway rate limits.
            # Pace functional scenarios instead of changing those limits.
            await asyncio.sleep(4)
            start = time.perf_counter()
            try:
                content = await client.call_tool(name, args)
                text = next((x["text"] for x in content if x.get("type") == "text"), "null")
                try:
                    result = json.loads(text)
                except ValueError:
                    result = text
                failed = error(result)
                status = "pass" if failed == expected_error else "fail"
            except Exception as exc:
                result = {"exception": type(exc).__name__, "message": str(exc)}
                status = "fail"
            RECORDS.append({"method": name, "arguments": args, "status": status, "expected_error": expected_error, "elapsed_ms": round((time.perf_counter()-start)*1000,2), "output": result})
            save()
            print(f"{status.upper()} {name} {json.dumps(result,default=str,ensure_ascii=True)[:220]}", flush=True)
            return result

        items = await call("search_items", {"item_type": "flight", "limit": 100})
        candidates = items.get("item_list", [])
        chosen = provider = batch = None
        for item in candidates[:8]:
            providers = await call("get_provider_items", {"item_uuid": item["item_uuid"], "limit": 20})
            for pi in providers.get("provider_item_list", []):
                for b in pi.get("batches", []):
                    end = b.get("service_end_at") or b.get("expired_at")
                    if end and end[:10] > datetime.now(timezone.utc).date().isoformat():
                        chosen, provider, batch = item, pi, b
                        break
                if batch: break
            if batch: break
        if batch is None:
            raise RuntimeError("No prepared flight batch with a future service window found")
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT/"banyanos_e2e_selected_inventory.json").write_text(json.dumps({"item": chosen, "provider": provider, "batch": batch},indent=2,default=str),encoding="utf-8")
        print("Selected inventory saved", flush=True)
        if discover_only: return
        await workflow(call, chosen, provider, batch, candidates)


async def workflow(call, item, provider, batch, candidates):
    iid, pid = item["item_uuid"], provider["provider_item_uuid"]
    email = f"mcp-e2e-{RUN}@example.test"
    prepared = json.loads((HERE.parents[3] / "rfq_engine/rfq_engine/tests/prepare_test_data/travel/products.json").read_text(encoding="utf-8-sig"))
    segment_uuid = prepared["segmentUuid"]
    start, end = batch["service_start_at"], batch["service_end_at"]
    availability = {"partition_key": PARTITION, "provider_item_uuid": pid, "batch_no": batch["batch_no"], "service_start_at": start, "service_end_at": end, "qty": 1}
    await call("get_item", {"item_uuid": iid})
    bundles = await call("search_bundles", {"partition_key": PARTITION, "limit": 10})
    if isinstance(bundles, dict) and bundles.get("bundle_list"):
        bid = bundles["bundle_list"][0]["bundle_uuid"]
        await call("get_bundle", {"partition_key": PARTITION, "bundle_uuid": bid})
        await call("search_bundle_components", {"partition_key": PARTITION, "bundle_uuid": bid})
    policies = await call("search_cancellation_policies", {"partition_key": PARTITION})
    if isinstance(policies, dict) and policies.get("cancellation_policy_list"):
        await call("get_cancellation_policy", {"partition_key": PARTITION, "policy_uuid": policies["cancellation_policy_list"][0]["policy_uuid"]})
    await call("get_segment_contacts", {"email": email})
    await call("inquire_catalog", {"partition_key": PARTITION, "query_text": "flight", "search_mode": "graph", "namespace": "FLIGHTS", "limit": 5})

    async def setup(label, exercise=False):
        request = await call("submit_rfq_request", {"email": email, "request_title": f"MCP Docker E2E {RUN} {label}", "items": [{"item_uuid": iid, "item_name": item["item_name"], "qty": 2, "pax_breakdown": {"adult": 2}}], "notes": f"Isolated MCPHttpClient test run {RUN}", "expired_at": "2027-12-31T23:59:59Z"})
        rid = request["request_uuid"]
        if exercise:
            got = await call("get_rfq_request", {"request_uuid": rid})
            assert got["request_uuid"] == rid
            await call("search_rfq_requests", {"email": email, "limit": 10})
            await call("update_rfq_request", {"request_uuid": rid, "notes": f"Updated by MCP test {RUN}"})
            other = next(x for x in candidates if x["item_uuid"] != iid)
            await call("add_item_to_rfq_request", {"request_uuid": rid, "item": {"item_uuid": other["item_uuid"], "item_name": other["item_name"], "qty": 1}})
            await call("remove_item_from_rfq_request", {"request_uuid": rid, "item_uuid": other["item_uuid"]})
        assignment = {"request_uuid": rid, "item_uuid": iid, "provider_item_uuid": pid, "provider_corp_external_id": provider["provider_corp_external_id"], "qty": 2, "batch_no": batch["batch_no"], "service_start_at": start, "service_end_at": end}
        await call("assign_provider_item_to_request_item", assignment)
        if exercise:
            await call("remove_provider_item_from_request_item", {"request_uuid": rid, "item_uuid": iid, "provider_item_uuid": pid})
            await call("assign_provider_item_to_request_item", assignment)
            qi = [{"item_uuid": iid, "provider_item_uuid": pid, "qty": 2}]
            await call("get_item_price_tiers", {"email": email, "quote_items": qi})
            await call("get_discount_prompts", {"email": email, "quote_items": qi})
            await call("calculate_quote_pricing", {"request_uuid": rid, "email": email})
            await call("upload_rfq_file", {"request_uuid": rid, "file_name": f"mcp-e2e-{RUN}.pdf", "email": email})
            await call("get_rfq_files", {"request_uuid": rid})
        quotes = await call("confirm_request_and_create_quotes", {"request_uuid": rid, "provider_corp_external_ids": [provider["provider_corp_external_id"]], "segment_uuid": segment_uuid, "batch_no": batch["batch_no"], "service_start_at": start, "service_end_at": end})
        created = quotes.get("created_quotes", [])
        if not created:
            raise RuntimeError("Quote setup did not return a created quote")
        qid = created[0]["quote_uuid"]
        quote = await call("get_quote", {"request_uuid": rid, "quote_uuid": qid})
        if exercise:
            await call("search_quotes", {"request_uuid": rid})
            await call("update_quote", {"request_uuid": rid, "quote_uuid": qid, "notes": f"Quote test {RUN}", "shipping_amount": 25.0})
            if quote.get("quote_items"):
                await call("update_quote_item", {"request_uuid": rid, "quote_uuid": qid, "quote_item_uuid": quote["quote_items"][0]["quote_item_uuid"], "discount_amount": 10.0, "notes": f"Discount test {RUN}"})
        return rid, qid

    try:
        rid, qid = await setup("main", True)
        await call("confirm_quote_and_create_installments", {"request_uuid": rid, "quote_uuid": qid, "create_single_installment": True, "payment_method": "bank_transfer"})
        installments = await call("get_installments", {"quote_uuid": qid})
        for inst in installments.get("installment_list", []):
            await call("update_installment", {"quote_uuid": qid, "installment_uuid": inst["installment_uuid"], "status": "paid"})
        final = await call("get_quote", {"request_uuid": rid, "quote_uuid": qid})
        request = await call("get_rfq_request", {"request_uuid": rid})
        RECORDS.append({"method": "reconciliation", "arguments": {"request_uuid": rid, "quote_uuid": qid}, "status": "pass" if final.get("status") == "completed" and request.get("status") == "completed" else "fail", "output": {"quote_status": final.get("status"), "request_status": request.get("status")}})
        for label, method, extra in [("single", "create_installment", {"installment_amount": 100.0}), ("multiple", "create_installments", {"interval_num": 1, "total_pay_period": 2})]:
            srid, sqid = await setup(label)
            await call("update_quote", {"request_uuid": srid, "quote_uuid": sqid, "status": "confirmed"})
            await call(method, {"request_uuid": srid, "quote_uuid": sqid, "payment_method": "bank_transfer", **extra})
    except Exception as exc:
        RECORDS.append({"method": "workflow_dependency", "arguments": {}, "status": "fail", "output": {"message": str(exc)}})
        print("Workflow dependency failure:", str(exc), flush=True)

    before = await call("check_availability", availability)
    hold = await call("acquire_availability_hold", availability)
    held = hold.get("availability", hold) if isinstance(hold, dict) else {}
    if held.get("hold_token"):
        args = {"partition_key": PARTITION, "provider_item_uuid": pid, "batch_no": batch["batch_no"], "hold_token": held["hold_token"]}
        await call("release_availability_hold", args)
        await call("release_availability_hold", args)
    hold = await call("acquire_availability_hold", availability)
    held = hold.get("availability", hold) if isinstance(hold, dict) else {}
    if held.get("hold_token"):
        args = {"partition_key": PARTITION, "provider_item_uuid": pid, "batch_no": batch["batch_no"], "hold_token": held["hold_token"]}
        await call("expire_availability_hold", args, expected_error=True)
        await call("confirm_availability_hold", args)
    await call("check_availability", availability)
    await call("get_item", {}, expected_error=True)
    await call("submit_rfq_request", {}, expected_error=True)
    save()


def save():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"banyanos_mcp_e2e_calls.json").write_text(json.dumps(RECORDS,indent=2,default=str),encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discover-only", action="store_true")
    args = parser.parse_args()
    try:
        asyncio.run(main(args.discover_only))
    finally:
        save()
    if any(x["status"] == "fail" for x in RECORDS):
        raise SystemExit(1)
