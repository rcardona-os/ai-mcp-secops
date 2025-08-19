import sys
from mcp_client import call
cidr = sys.argv[1] if len(sys.argv)>1 else "203.0.113.13/32"
print(call("block_ip", {"cidr": cidr, "namespace":"secops-ai"}))
