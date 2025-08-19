# 🚀 AI + OpenShift SecOps: NIDS, NIPS & MCP Integration

[![OpenShift AI](https://img.shields.io/badge/OpenShift%20AI-v2.x-red)](https://www.redhat.com/en/technologies/cloud-computing/openshift/ai)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Security](https://img.shields.io/badge/security-enhanced-blue)]()

---

## 📖 Overview

This repository demonstrates an **end-to-end SecOps pipeline** combining:

- **Suricata NIDS** (Network Intrusion Detection System)  
- **Egress Firewall NIPS** (Network Intrusion Prevention System)  
- **OpenShift AI Workloads (RHODS Workbench)** for training/analysis  
- **MCP (Model Control Plane / Tool Server)** for policy automation  

> 🛡️ The goal is to **detect suspicious traffic, prevent malicious egress, analyze activity using AI**, and automatically **push new policies back** to the NIDS/NIPS edge.

---

## 🏗️ High-Level Architecture

```mermaid
flowchart LR
  subgraph EXT[External Traffic]
    U[User / Client]
  end

  subgraph SEC[Security Edge]
    NIDS[Suricata NIDS]
    NIPS[EgressFirewall - NIPS]
  end

  subgraph OCP[OpenShift AI Cluster]
    G[AI Workloads / RHODS Workbench]
    MCP[MCP Tool Server]
  end

  U --> NIDS --> NIPS --> G
  G --> MCP
  MCP -->|"Query alerts / push policies"| NIDS

  classDef nids fill:#eff3c7,stroke:#f59e0b,stroke-width:2px;
  classDef nips fill:#fee2e2,stroke:#ef4444,stroke-width:2px;
  classDef ai fill:#dbeafe,stroke:#2563eb,stroke-width:2px;
  classDef mcp fill:#e0f2fe,stroke:#0284c7,stroke-width:2px;

  class NIDS nids;
  class NIPS nips;
  class G ai;
  class MCP mcp;
