"""Render the observed MCP HTTP deployment and workflow evidence."""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from mcp_hospirfq_processor import MCP_CONFIGURATION


def main():
    folder = Path(__file__).resolve().parents[2] / "docs/test_results"
    calls = json.loads((folder / "banyanos_mcp_e2e_calls.json").read_text(encoding="utf-8"))
    for entry in list(calls):
        quote = entry.get("output")
        if entry["method"] == "get_quote" and isinstance(quote, dict) and quote.get("status") == "completed":
            installments = quote.get("installments") or []
            paid = sum(float(i.get("installment_amount") or 0) for i in installments if i.get("status") == "paid")
            total = float(quote.get("final_total_quote_amount") or 0)
            links_valid = all(i.get("quote_uuid") == quote["quote_uuid"] and i.get("request_uuid") == quote["request_uuid"] for i in installments)
            calls.append({"method": "financial_reconciliation", "arguments": {"quote_uuid": quote["quote_uuid"], "request_uuid": quote["request_uuid"]}, "status": "pass" if installments and abs(paid-total) <= .01 and links_valid else "fail", "output": {"paid_installments_sum": paid, "final_quote_total": total, "installment_links_valid": links_valid, "tolerance": .01}})
    tools = {t["name"] for t in MCP_CONFIGURATION["tools"]}
    attempted = {x["method"] for x in calls} & tools
    missing = sorted(tools-attempted)
    counts = Counter(x["status"] for x in calls)
    failures = [x for x in calls if x["status"] == "fail"]
    decision = "Not Ready" if failures or missing else "Ready with Conditions"
    lines = [
        "# Docker Banyanos RFQ MCP HTTP integration report", "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "Client date: 2026-10-22 (America/Los_Angeles).", "",
        f"**Certification: {decision}.** Deployment succeeded; certification is limited by the failures and coverage gaps below.", "",
        "## Scope and sequence", "",
        "Local module suite and tool registration audit → Docker RFQ read-only preflight → Git image build → gateway replacement → MCP configuration registration → MCPHttpClient initialize/tools/list → discovered reference data → fresh request → supplier assignment → pricing → quotes → installments/payment → API readback → availability lifecycle → invalid-input scenarios.",
        "The existing HTTP SOP (`docs/integration_scenarios_sop_http.md`, previously approved) was reused with the user's requested Docker target and current discovered inventory. Live writes affect uniquely labeled local test RFQs; existing business RFQs were not edited. Production, UI/load certification, infrastructure outage injection and destructive cleanup are outside this run.", "",
        "## Pre-deployment checks", "",
        "- Local pytest: 65 passed. Two obsolete catalog test fixtures were updated to the real payload.results response contract; deployed production source was not changed.",
        "- Manifest: 38 tools and 38 callable implementations.",
        "- Live direct MCP processor reads: items, requests, quotes, bundles, cancellation policies and segment contacts returned without error.",
        "- Gateway MCP registry was empty before registration.", "",
        "## Deployment and dependencies", "",
        "- Source: git@github.com:ideabosque/mcp_hospirfq_processor.git, main, commit f6a22ef6616fb8d715ab246f1f4072990a61482f (verified from installed distribution direct_url.json).",
        "- Image: banyanos-gateway:hospirfq-20261022; module 0.1.0 plus pyhumps 3.8.0 installed during image build.",
        "- BuildKit secret mount supplied the existing SSH key only during build; no private SSH key exists in the runtime container.",
        "- Registration: loadMcpConfiguration returned ok=true, 38 tools, one module and one settings record.",
        "- Transport: MCPHttpClient → http://127.0.0.1:18000/banyan/mcp → mcp_protocol_plugin → MCPHospiRFQProcessor → container loopback /banyan/rfq_graphql → rfq_engine.",
        "- Tenant partition: banyan#nestaging. Existing working user credentials were read from the Banyanos E2E secret source and configured in runtime MCP settings; no secret values are in this report.",
        "- Existing PostgreSQL, Neo4j and Redis containers were reused. Gateway health, authentication and tool discovery passed. Schema/provisioning changes were not made; full migration certification is not claimed.",
        "- [Compose overlay](deployment/docker-compose.hospirfq.yml) must be included on future compose up calls to retain the selected image. Ordinary compose up without this overlay may restore the previous image.", "",
        "## Final run statistics", "",
        f"- Tool names attempted: {len(attempted)}/38.",
        f"- Recorded checks/calls: {len(calls)}; pass={counts['pass']}, fail={counts['fail']}; tools not attempted={len(missing)}.",
        f"- Missing tools: {', '.join(missing) or 'none'}.",
        "Pass means the returned envelope matched the expected success/error condition. Empty catalog/contact results do not establish positive search coverage. Explicit request/quote IDs and terminal statuses are checked separately by reconciliation.", "",
        "| Tool | Successful calls | Failed calls |", "|---|---:|---:|",
    ]
    for name in sorted(tools):
        subset = [x for x in calls if x["method"] == name]
        lines.append(f"| {name} | {sum(x['status']=='pass' for x in subset)} | {sum(x['status']=='fail' for x in subset)} |")
    lines += ["", "## Defects, gaps and mitigation", "",
        "- Backend price tiers: open-ended quantity_less_then is null and PostgreSQL utils compares float < None. Requires a backend bounds-handling fix and regression coverage.",
        "- Missing required MCP arguments return generic -32603 Internal error. They should produce a useful validation response; recorded negative cases remain failures.",
        "- Catalog inquiry returned no results; positive knowledge-backed retrieval remains unverified. Segment lookup with the isolated test email likewise returned an empty list.",
        "- Fresh hold expiry was tested as an expected not-expired rejection. Successful TTL expiry and the scheduled expiry worker were not tested.",
        "- Unpaced calls triggered HTTP 429 on shared loopback traffic; the final functional run uses pacing and leaves rate-limit settings unchanged. Throughput/retry behavior is not certified.",
        "- The first quote attempt used an invalid default segment placeholder; the runner now uses the prepared segment UUID. Initial error evidence is retained.",
        "- Generated requests, quotes, installments and confirmed fixture holds remain in the local test partition for inspection; there was no destructive cleanup.", "",
        "## Function Results", "",
        "Exact tool arguments, outputs, elapsed times and expectations are recorded below. Deployment/discovery evidence is also retained in [banyanos_mcp_deployment.json](banyanos_mcp_deployment.json). Prior attempts: [initial](banyanos_mcp_e2e_calls_initial.json), [unpaced](banyanos_mcp_e2e_calls_unpaced.json).", "",
    ]
    for number, entry in enumerate(calls, 1):
        lines += [f"### {number}. {entry['method']}", "", f"Status: {entry['status']}; elapsed: {entry.get('elapsed_ms','n/a')} ms.", "", "Arguments:", "```json", json.dumps(entry["arguments"],indent=2,default=str), "```", "", "Output:", "```json"]
        output = json.dumps(entry["output"],indent=2,default=str,ensure_ascii=False)
        lines += [output if len(output)<10000 else output[:10000]+"\n... (truncated; full output in banyanos_mcp_e2e_calls.json)", "```", ""]
    path = folder/"banyanos_mcp_e2e_report.md"
    path.write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps({"report":str(path),"certification":decision,"counts":dict(counts),"tools_attempted":len(attempted),"missing":missing}))


if __name__ == "__main__":
    main()
