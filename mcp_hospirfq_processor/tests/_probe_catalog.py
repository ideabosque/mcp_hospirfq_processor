import os, sys, json, logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)
base_dir = os.getenv("base_dir", "")
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, "silvaengine_utility"))
sys.path.insert(0, os.path.join(base_dir, "silvaengine_constants"))
sys.path.insert(0, os.path.join(base_dir, "silvaengine_dynamodb_base"))
sys.path.insert(0, os.path.join(base_dir, "rfq_engine"))
sys.path.insert(0, os.path.join(base_dir, "mcp_hospirfq_processor"))

from mcp_hospirfq_processor.mcp_hospirfq_processor import MCPHospiRFQProcessor

setting = {
    "graphql_modules": {"rfq_engine": {"class_name": "RFQEngine", "endpoint": os.getenv("RFQ_ENGINE_ENDPOINT"), "x_api_key": os.getenv("RFQ_ENGINE_X_API_KEY", "placeholder")}},
    "gateway_base_url": os.getenv("GATEWAY_BASE_URL"),
    "token_username": os.getenv("TOKEN_USERNAME"),
    "token_password": os.getenv("TOKEN_PASSWORD"),
    "sales_rep_emails": json.loads(os.getenv("SALES_REP_EMAILS", "{}")),
}
proc = MCPHospiRFQProcessor(logging.getLogger("probe"), **setting)

queries = [
    "Air France ATL ORD Premium Economy",
    "AF-ATL-ORD-PRE",
    "FLIGHT-ATL-ORD-PRE",
    "Premium Economy flight ATL ORD Air France",
    "Air France Premium Economy Atlanta Chicago",
    "Flight ATL ORD Premium Economy",
    "ATL ORD Premium Economy",
    "Air France",
]
for q in queries:
    r = proc.inquire_catalog(partition_key="gpt#nestaging", query_text=q, namespace="FLIGHTS", limit=20)
    results = ((r.get("payload") or {}).get("results") or [])
    print("\n=== query: %r -> %d results ===" % (q, len(results)))
    for hit in results[:8]:
        txt = (((hit.get("metadata") or {}).get("node") or {}).get("text") or "")[:160]
        print("  - %s" % txt)