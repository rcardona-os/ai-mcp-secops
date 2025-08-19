# OpenShift AI + MCP Security Ops

This repository demonstrates how to combine **OpenShift AI**, **Model Context Protocol (MCP)**, and traditional security controls (**NIDS/NIPS**) to build a secure, AI-augmented intrusion detection and prevention environment.

The project shows how **AI workloads** can be deployed on OpenShift AI while being monitored and protected by **network intrusion detection/prevention systems**.  
MCP serves as the extensibility layer, enabling dynamic policy enforcement, event-driven workflows, and security automation.

---

## 🔥 High-Level Architecture

```mermaid
flowchart LR
    subgraph Ext["External Traffic"]
        U[User / Client]
    end

    subgraph Sec["Security Edge"]
        NIDS[Suricata NIDS]:::nids
        NIPS[EgressFirewall (NIPS)]:::nips
    end

    subgraph OCP["OpenShift AI Cluster"]
        G[GPU Workloads / AI Pipelines]:::ai
        MCP[Model Context Protocol Server]:::mcp
    end

    U --> NIDS --> NIPS --> G
    G --> MCP
    MCP -->|"Alerts, Context, Extra Policies"| NIDS

    classDef nids fill=#fef3c7,stroke=#f59e0b,stroke-width=2px;
    classDef nips fill=#fee2e2,stroke=#ef4444,stroke-width=2px;
    classDef ai fill=#dbeafe,stroke=#2563eb,stroke-width=2px;
    classDef mcp fill=#e0f2fe,stroke=#0284c7,stroke-width=2px;