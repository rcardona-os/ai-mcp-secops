# 🚀 OpenShift AI + MCP SecOps Lab with NIDS & NIPS (No Model Optimisation)

This lab shows how to combine **OpenShift AI (RHODS)**, a lightweight **MCP tool server**, and network security controls (**Suricata NIDS** + **EgressFirewall NIPS**) to create a practical, auditable SecOps control plane on OpenShift.

- **NIDS (Suricata)** detects suspicious traffic and writes EVE JSON logs.
- **NIPS (EgressFirewall / NetworkPolicy)** blocks/contains malicious egress.
- **MCP** provides deterministic, RBAC-scoped tools (block/unblock IPs, quarantine/release namespaces) that you can call from notebooks, scripts, or automation—*no model retraining required*.

---

## 🏗️ Architecture

```mermaid
flowchart LR
  subgraph EXT[External Traffic]
    U[User / Client]
  end

  subgraph SEC[Security Edge]
    NIDS[Suricata NIDS]
    NIPS[EgressFirewall / NIPS]
  end

  subgraph OCP[OpenShift AI Cluster]
    G[AI Workloads / RHODS Workbench]
    MCP[MCP Tool Server]
  end

  U --> NIDS --> NIPS --> G
  G --> MCP
  MCP -->|"Query alerts / push policies"| NIDS

  classDef nids fill:#fef3c7,stroke:#f59e0b,stroke-width:2px;
  classDef nips fill:#fee2e2,stroke:#ef4444,stroke-width:2px;
  classDef ai fill:#dbeafe,stroke:#2563eb,stroke-width:2px;
  classDef mcp fill:#e0f2fe,stroke:#0284c7,stroke-width:2px;

  class NIDS nids;
  class NIPS nips;
  class G ai;
  class MCP mcp;