import json, subprocess

def call(method, params=None, server_cmd=["python","mcp-tools/server.py"]):
    req = {"jsonrpc":"2.0","id":1,"method":method,"params":params or {}}
    p = subprocess.run(server_cmd, input=(json.dumps(req)+"\n").encode(), capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode() or "server error")
    for line in p.stdout.decode().splitlines():
        try:
            return json.loads(line)["result"]
        except Exception:
            continue
    raise RuntimeError("no result")
