"""Read-only RFQ connectivity probe through the real MCP processor facade."""
import argparse
import json
import logging
import os
import time
from pathlib import Path

from dotenv import dotenv_values
from mcp_hospirfq_processor import MCPHospiRFQProcessor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--credentials-file", type=Path)
    args = parser.parse_args()
    workspace = Path(__file__).resolve().parents[3]
    gateway_dir = workspace.parent / "banyanos" / "docker-banyanos-gateway"
    config = dotenv_values(gateway_dir / ".env")
    credentials = dotenv_values(args.credentials_file) if args.credentials_file else {}
    base = os.getenv("BANYANOS_GATEWAY_URL", "http://127.0.0.1:18000").rstrip("/")
    processor = MCPHospiRFQProcessor(logging.getLogger("banyanos_rfq_probe"), **{
        "graphql_modules": {"rfq_engine": {
            "class_name": "RFQEngine",
            "endpoint": base + "/{endpoint_id}/rfq_graphql",
            "gateway_base_url": base,
            "token_username": os.getenv("BANYANOS_TOKEN_USERNAME") or credentials.get("E2E_EMAIL") or config.get("ADMIN_USERNAME"),
            "token_password": os.getenv("BANYANOS_TOKEN_PASSWORD") or credentials.get("E2E_PASSWORD") or config.get("ADMIN_PASSWORD"),
            "gateway_token": os.getenv("BANYANOS_GATEWAY_TOKEN"),
        }},
    })
    processor.endpoint_id = os.getenv("BANYANOS_ENDPOINT_ID", "banyan")
    processor.part_id = os.getenv("BANYANOS_PART_ID", "nestaging")
    arguments = {"limit": 1, "page_number": 1}
    start = time.perf_counter()
    result = processor.search_items(**arguments)
    record = {
        "method": "MCPHospiRFQProcessor.search_items",
        "path": "MCP module -> docker-banyanos-gateway -> rfq_engine",
        "url": base + f"/{processor.endpoint_id}/rfq_graphql",
        "arguments": arguments,
        "elapsed_ms": round((time.perf_counter() - start) * 1000, 2),
        "output": result,
    }
    out = Path(__file__).resolve().parents[2] / "docs/test_results/banyanos_gateway_probe.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, default=str), encoding="utf-8")
    print(json.dumps(record, indent=2, default=str))
    if isinstance(result, dict) and (result.get("error") or result.get("error_code")):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
