#!/usr/bin/env python3
# JSON-RPC 2.0 over stdio (one JSON per line)
# Methods:
# - nids_latest_alerts(eve_json?: str, limit?: int)
# - block_ip(cidr: str, namespace?: str)
# - unblock_ip(cidr: str, namespace?: str)
# - quarantine_namespace(target_namespace: str, allow_namespace?: str)
# - release_namespace(target_namespace: str)
# - trigger_pipeline(namespace?: str, pipelinerun_yaml?: str)

import sys, json, subprocess, tempfile
from typing import Any, Dict, Optional

def _read() -> Optional[Dict[str, Any]]:
    line = sys.stdin.readline()
    if not line:
        return None
    try:
        return json.loads(line)
    except Exception:
        return None

def _send(id_, result=None, error=None):
    msg = {"jsonrpc":"2.0","id":id_}
    if error is not None:
        msg["error"] = {"code": -32000, "message": str(error)}
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def nids_latest_alerts(params: Dict[str, Any]):
    path = params.get("eve_json","/var/log/suricata/eve.json")
    limit = int(params.get("limit", 20))
    alerts = []
    try:
        with open(path,"r") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if obj.get("event_type") == "alert":
                        a = {
                            "timestamp": obj.get("timestamp"),
                            "src_ip": obj.get("src_ip"),
                            "dest_ip": obj.get("dest_ip"),
                        }
                        al = obj.get("alert",{})
                        a.update({
                            "severity": al.get("severity"),
                            "signature": al.get("signature"),
                            "category": al.get("category")
                        })
                        alerts.append(a)
                except Exception:
                    pass
        return {"ok": True, "alerts": alerts[-limit:]}
    except FileNotFoundError:
        return {"ok": False, "error": f"{path} not found"}

def _oc_apply(yaml: str, namespace: Optional[str]=None):
    fd = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml", mode="w")
    fd.write(yaml)
    fd.close()
    cmd = ["oc"]
    if namespace:
        cmd += ["-n", namespace]
    cmd += ["apply", "-f", fd.name]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr, yaml

def block_ip(params: Dict[str, Any]):
    cidr = params.get("cidr")
    ns = params.get("namespace","secops-ai")
    if not cidr:
        return {"ok": False, "error":"cidr required"}
    name = f"block-{cidr.replace('/','-').replace('.','-')}"
    yaml = f"""apiVersion: network.openshift.io/v1
kind: EgressFirewall
metadata:
  name: {name}
  namespace: {ns}
spec:
  egress:
  - type: Deny
    to:
      cidrSelector: {cidr}
"""
    rc, out, err, y = _oc_apply(yaml, None)
    return {"ok": rc==0, "stdout": out, "stderr": err, "yaml": y}

def unblock_ip(params: Dict[str, Any]):
    cidr = params.get("cidr")
    ns = params.get("namespace","secops-ai")
    if not cidr:
        return {"ok": False, "error":"cidr required"}
    name = f"block-{cidr.replace('/','-').replace('.','-')}"
    p = subprocess.run(["oc","-n",ns,"delete","egressfirewall",name], capture_output=True, text=True)
    return {"ok": p.returncode==0, "stdout":p.stdout, "stderr":p.stderr}

def quarantine_namespace(params: Dict[str, Any]):
    target_ns = params.get("target_namespace")
    allow_ns = params.get("allow_namespace","secops-ai")
    if not target_ns:
        return {"ok": False, "error":"target_namespace required"}
    yaml = f"""apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: quarantine
  namespace: {target_ns}
spec:
  podSelector: {{}}
  policyTypes: ["Ingress","Egress"]
  ingress:
    - from:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: {allow_ns}
  egress:
    - to:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: {allow_ns}
"""
    rc, out, err, y = _oc_apply(yaml, None)
    return {"ok": rc==0, "stdout": out, "stderr": err, "yaml": y}

def release_namespace(params: Dict[str, Any]):
    target_ns = params.get("target_namespace")
    if not target_ns:
        return {"ok": False, "error":"target_namespace required"}
    p = subprocess.run(["oc","-n",target_ns,"delete","networkpolicy","quarantine"], capture_output=True, text=True)
    return {"ok": p.returncode==0, "stdout":p.stdout, "stderr":p.stderr}

def trigger_pipeline(params: Dict[str, Any]):
    ns = params.get("namespace","secops-ai")
    pr = params.get("pipelinerun_yaml","tekton/pipelinerun.example.yaml")
    p = subprocess.run(["oc","-n",ns,"create","-f",pr], capture_output=True, text=True)
    return {"ok": p.returncode==0, "stdout":p.stdout, "stderr":p.stderr}

HANDLERS = {
    "nids_latest_alerts": nids_latest_alerts,
    "block_ip": block_ip,
    "unblock_ip": unblock_ip,
    "quarantine_namespace": quarantine_namespace,
    "release_namespace": release_namespace,
    "trigger_pipeline": trigger_pipeline,
}

def main():
    while True:
        msg = _read()
        if msg is None:
            break
        mid = msg.get("id")
        method = msg.get("method")
        params = msg.get("params",{}) or {}
        if method == "ping":
            _send(mid, {"pong":True})
        elif method in HANDLERS:
            try:
                res = HANDLERS[method](params)
                _send(mid, res)
            except Exception as e:
                _send(mid, error=str(e))
        else:
            _send(mid, error=f"unknown method {method}")
if __name__ == "__main__":
    main()
