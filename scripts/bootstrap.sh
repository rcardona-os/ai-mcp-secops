#!/usr/bin/env bash
set -euo pipefail
NS=${1:-secops-ai}
kubectl apply -f k8s/namespace.yaml
kubectl -n $NS apply -f mcp-tools/rbac.yaml
kubectl -n $NS apply -f mcp-tools/deployment.yaml
kubectl -n $NS apply -f security/suricata-daemonset.yaml
kubectl -n $NS apply -f security/networkpolicy-quarantine.yaml
kubectl -n $NS apply -f tekton/tasks/01-ship-eve-to-loki.yaml
kubectl -n $NS apply -f tekton/tasks/02-enrich-alerts.yaml
kubectl -n $NS apply -f tekton/tasks/03-apply-blocklist.yaml
kubectl -n $NS apply -f tekton/pipeline.yaml
echo "Bootstrap complete."
