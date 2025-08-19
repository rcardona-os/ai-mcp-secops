import json, subprocess

def rpc(method, params=None):
    req = {"jsonrpc":"2.0","id":1,"method":method,"params":params or {}}
    p = subprocess.run(["python","mcp-tools/server.py"], input=(json.dumps(req)+"\n").encode(), capture_output=True)
    assert p.returncode == 0
    for line in p.stdout.decode().splitlines():
        try:
            return json.loads(line)["result"]
        except Exception:
            continue
    raise AssertionError("no result")

def test_ping():
    res = rpc("ping")
    assert res["pong"] == True
