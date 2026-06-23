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
proc.endpoint_id = os.getenv("endpoint_id", "gpt")
proc.part_id = os.getenv("part_id", "nestaging")

# Test check_availability
r = proc.check_availability(
    partition_key="gpt#nestaging",
    provider_item_uuid="24529e36-bd9c-4427-ac05-d1d545ad8963",
    service_start_at="2026-09-05T21:15:00Z",
    service_end_at="2026-09-06T08:30:40.740402Z",
    batch_no="DL4000-20260905",
    qty=2,
)
print("check_availability result:")
print(json.dumps(r, default=str, indent=2))

# Also test without batch_no
r2 = proc.check_availability(
    partition_key="gpt#nestaging",
    provider_item_uuid="24529e36-bd9c-4427-ac05-d1d545ad8963",
    service_start_at="2026-09-05T21:15:00Z",
    service_end_at="2026-09-06T08:30:40.740402Z",
    qty=2,
)
print("\ncheck_availability (no batch_no) result:")
print(json.dumps(r2, default=str, indent=2))