# Threat Response Playbooks

## 1) C2 Beacon
- Inspect: `nids_latest_alerts`
- Contain: `quarantine_namespace`
- Block: `block_ip` to C2 CIDR
- Observe: verify alert volume drops
- Recover: `release_namespace`; `unblock_ip` if FP

## 2) Data Exfil
- Detect: spike to unknown external CIDR
- Contain: quarantine target namespace
- Investigate: logs, pod histories, service accounts
- Block: apply deny rule; open PR to long-term blocklist

## 3) Cryptomining
- Detect: Suricata signatures or pool egress
- Block: target pools via `block_ip`
- Eradicate: scale deployment to zero (add new tool method)
