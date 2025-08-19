# Architecture

- **RHODS Workbench**: analyst cockpit (notebooks calling MCP tools).
- **MCP Server**: JSON-RPC methods to operate NIDS/NIPS (no models).
- **Suricata NIDS**: DaemonSet writing EVE JSON to host logs.
- **NIPS**: EgressFirewall (block CIDR) + NetworkPolicy quarantine.
- **Tekton**: pipeline to ship/enrich/act on alerts.

All actions are RBAC-scoped and YAML-applied for auditability.
