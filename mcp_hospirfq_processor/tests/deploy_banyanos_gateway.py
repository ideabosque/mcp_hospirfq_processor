"""Deploy the Git package and verify MCP HTTP discovery/read-only execution."""
import argparse
import asyncio
import json
import logging
import time
from pathlib import Path

import httpx
from dotenv import dotenv_values
from mcp_http_client import MCPHttpClient

BASE = "http://127.0.0.1:18000"
HEADERS = {"Part-Id": "nestaging"}
REPO = "git@github.com:ideabosque/mcp_hospirfq_processor.git"
OUT = Path(__file__).resolve().parents[2] / "docs/test_results/banyanos_mcp_deployment.json"


def redact(value):
    if isinstance(value, dict):
        return {k: ("<redacted>" if any(s in k.lower() for s in ("password", "token", "secret")) else redact(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


async def probe(token, records):
    async with MCPHttpClient(logging.getLogger("banyanos_deploy"), base_url=BASE + "/banyan/mcp", bearer_token=token, headers=HEADERS) as client:
        tools = await client.list_tools()
        names = [t.name for t in tools]
        records.append({"method": "MCPHttpClient.initialize/tools/list", "arguments": {}, "output": names})
        print(f"MCP discovery: {len(names)} tools")
        if "search_items" in names:
            start = time.perf_counter()
            result = await client.call_tool("search_items", {"limit": 1, "page_number": 1})
            records.append({"method": "MCPHttpClient.call_tool", "arguments": {"name": "search_items", "arguments": {"limit": 1, "page_number": 1}}, "elapsed_ms": round((time.perf_counter()-start)*1000, 2), "output": result})
            print(json.dumps(result, default=str))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inspect", "preflight", "register", "probe"])
    args = parser.parse_args()
    credentials = dotenv_values(Path(__file__).resolve().parents[4] / "banyanos/.e2e_anthropic/credentials.env")
    records = []
    def graphql(query, variables=None):
        start = time.perf_counter()
        response = httpx.post(BASE + "/banyan/mcp_daemon_graphql", headers={**HEADERS, "Authorization": "Bearer " + token}, json={"query": query, "variables": variables or {}}, timeout=360)
        response.raise_for_status()
        result = response.json()
        records.append({"method": "POST /banyan/mcp_daemon_graphql", "arguments": redact({"query": query, "variables": variables or {}}), "elapsed_ms": round((time.perf_counter()-start)*1000, 2), "output": redact(result)})
        print(json.dumps(redact(result), indent=2))
        if result.get("errors"):
            raise RuntimeError("GraphQL operation failed; see recorded response")
        return result.get("data", {})
    try:
        response = httpx.post(BASE + "/auth/token", data={"username": credentials["E2E_EMAIL"], "password": credentials["E2E_PASSWORD"]}, timeout=20)
        response.raise_for_status()
        token = response.json()["access_token"]
        if args.action == "inspect":
            graphql('{ mcpModuleList(limit:100) { mcpModuleList { moduleName packageName source } } }')
        elif args.action == "preflight":
            from mcp_hospirfq_processor import MCP_CONFIGURATION, MCPHospiRFQProcessor
            setting = {"graphql_modules": {"rfq_engine": {"class_name": "RFQEngine", "endpoint": BASE + "/{endpoint_id}/rfq_graphql", "gateway_token": token}}}
            processor = MCPHospiRFQProcessor(logging.getLogger("banyanos_preflight"), **setting)
            processor.endpoint_id, processor.part_id = "banyan", "nestaging"
            links = MCP_CONFIGURATION["module_links"]
            assert len(links) == 38 and all(callable(getattr(processor, x["function_name"], None)) for x in links)
            for name, arguments in [
                ("search_items", {"limit": 100}),
                ("search_rfq_requests", {"limit": 1}),
                ("search_quotes", {"limit": 1}),
                ("search_bundles", {"partition_key": "banyan#nestaging", "limit": 1}),
                ("search_cancellation_policies", {"partition_key": "banyan#nestaging", "limit": 1}),
                ("get_segment_contacts", {"email": credentials["E2E_EMAIL"], "limit": 1}),
            ]:
                start = time.perf_counter()
                result = getattr(processor, name)(**arguments)
                records.append({"method": name, "arguments": arguments, "elapsed_ms": round((time.perf_counter()-start)*1000,2), "output": result})
                print(name, json.dumps(result, default=str)[:1600])
        elif args.action == "register":
            variables = {"moduleName": "mcp_hospirfq_processor", "packageName": "mcp_hospirfq_processor", "updatedBy": "banyanos-mcp-deployment", "variables": {"graphql_modules": {"rfq_engine": {"class_name": "RFQEngine", "endpoint": "http://127.0.0.1:8000/{endpoint_id}/rfq_graphql", "gateway_base_url": "http://127.0.0.1:8000", "token_username": credentials["E2E_EMAIL"], "token_password": credentials["E2E_PASSWORD"]}}}}
            query = 'mutation($moduleName:String!,$packageName:String!,$updatedBy:String!,$variables:JSONCamelCase){loadMcpConfiguration(moduleName:$moduleName,packageName:$packageName,source:"local",updatedBy:$updatedBy,variables:$variables){ok message stats{tools resources prompts modules settings}}}'
            data = graphql(query, variables)
            if not data.get("loadMcpConfiguration", {}).get("ok"):
                raise RuntimeError("MCP package registration failed")
        else:
            asyncio.run(probe(token, records))
    finally:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        previous = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else []
        OUT.write_text(json.dumps(previous + records, indent=2, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
