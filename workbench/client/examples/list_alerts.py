from mcp_client import call
print(call("nids_latest_alerts", {"limit": 10}))
