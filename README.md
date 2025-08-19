# OpenShift AI + MCP + NIDS/NIPS — SecOps Reference (No Models Required)

**Goal:** Give security analysts a cockpit (OpenShift AI Workbench) and a set of auditable, deterministic **tools** (MCP server) to act on **NIDS** alerts (Suricata) with **NIPS** controls (EgressFirewall & NetworkPolicy).

## Why this approach
- Keep ML out of the operational loop. **Tools > weights** for security actions.
- Add/modify capabilities by adding **new MCP methods**, not by retraining models.
- Everything is **RBAC-scoped**, YAML-backed, and easy to audit.

## Diagram
```mermaid
flowchart LR
  subgraph Analyst["RHODS (OpenShift AI) Workbench"]
    N1[Notebook: Inspect Alerts] --> N2[Decide Action]
    N2 -->|JSON-RPC| MCP[MCP Tool Server]
  end

  subgraph Cluster["OpenShift"]
    DS[Suricata NIDS DaemonSet]:::ids --> EVE[EVE JSON Logs]
    FW[EgressFirewall (NIPS)]:::nips
    Q[NetworkPolicy Quarantine]:::nips
  end

  MCP -->|nids_latest_alerts| EVE
  MCP -->|block_ip / unblock_ip| FW
  MCP -->|quarantine_namespace / release_namespace| Q

  classDef ids fill:#fff7d6,stroke:#e0b54c,stroke-width:1px;
  classDef nips fill:#ffe6e6,stroke:#ff9999,stroke-width:1px;
```

## Quick start
```bash
export REGISTRY=quay.io/<you>
export IMAGE_TAG=v1
export NS=secops-ai

# Build & push tools image
make build push REGISTRY=$REGISTRY IMAGE_TAG=$IMAGE_TAG

# Deploy everything (namespace, RBAC, MCP, Suricata, NIPS templates, Tekton)
make deploy NS=$NS

# (Optional) Create Workbench
oc apply -f workbench/workbench-rhoai.yaml

# Use the helper clients (or call JSON-RPC yourself)
python workbench/client/examples/list_alerts.py
python workbench/client/examples/block_ip.py 203.0.113.13/32
python workbench/client/examples/quarantine_namespace.py suspicious-ns
```

## What’s here
- `mcp-tools/` — MCP-like JSON-RPC server with SecOps methods + RBAC + Deployment.
- `security/` — Suricata DaemonSet (NIDS) + NIPS examples.
- `tekton/` — pipeline to ship/enrich/act on alerts.
- `workbench/` — RHODS Workbench + simple Python clients.
- `docs/` — deep dives (API, playbooks, setup, observability).

See `docs/THREAT_PLAYBOOKS.md` for incident flows.
