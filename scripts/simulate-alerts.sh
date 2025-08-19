#!/usr/bin/env bash
set -euo pipefail
FILE=${1:-/var/log/suricata/eve.json}
mkdir -p $(dirname "$FILE")
for i in $(seq 1 5); do
  cat <<EOF >> "$FILE"
{"timestamp":"$(date -Iseconds)","event_type":"alert","src_ip":"198.51.100.$i","dest_ip":"203.0.113.10","alert":{"severity":2,"signature":"DEMO Suspicious Traffic","category":"Attempted Admin"}}
EOF
done
echo "Wrote 5 demo alerts to $FILE"
