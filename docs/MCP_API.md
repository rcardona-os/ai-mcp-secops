# MCP Tool API

## Methods
- `ping()` → `{ "pong": true }`
- `nids_latest_alerts({ eve_json='/var/log/suricata/eve.json', limit=20 })`
- `block_ip({ cidr, namespace='secops-ai' })`
- `unblock_ip({ cidr, namespace='secops-ai' })`
- `quarantine_namespace({ target_namespace, allow_namespace='secops-ai' })`
- `release_namespace({ target_namespace })`
- `trigger_pipeline({ namespace='secops-ai', pipelinerun_yaml='tekton/pipelinerun.example.yaml' })`
