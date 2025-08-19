import sys
from mcp_client import call
target = sys.argv[1] if len(sys.argv)>1 else "default"
print(call("quarantine_namespace", {"target_namespace": target, "allow_namespace":"secops-ai"}))
