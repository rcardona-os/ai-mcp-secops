# OpenShift AI + MCP + NIDS/NIPS (No Model Optimisation)

This repository shows how to build a practical **SecOps control plane** on OpenShift using:

- **OpenShift AI (RHOAI)** – analyst workbench / notebooks.
- **MCP (Model Context Protocol)** – a lightweight, auditable tool API for operational actions.
- **NIDS** – Suricata DaemonSet generating EVE JSON alerts.
- **NIPS** – deterministic network controls (EgressFirewall + NetworkPolicy quarantine).

No model compilation or optimisation here—just actionable detection and prevention you can ship today.

---

## 🔭 High-Level Architecture

```mermaid
flowchart LR
    subgraph EXT[External Traffic]
      U[User / Client]
    end

    subgraph SEC[Security Edge]
      NIDS[Suricata NIDS]
      NIPS[EgressFirewall (NIPS)]
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
