REGISTRY ?= quay.io/youruser
IMAGE_TAG ?= latest
NS ?= secops-ai

MCP_IMG := $(REGISTRY)/mcp-tools:$(IMAGE_TAG)

.PHONY: build push deploy undeploy ids nips

build:
	docker build -t $(MCP_IMG) -f mcp-tools/Dockerfile mcp-tools

push: build
	docker push $(MCP_IMG)

deploy:
	kubectl apply -f k8s/namespace.yaml
	kubectl -n $(NS) apply -f mcp-tools/rbac.yaml
	sed 's#quay.io/youruser/mcp-tools:latest#$(MCP_IMG)#' mcp-tools/deployment.yaml | kubectl -n $(NS) apply -f -
	kubectl -n $(NS) apply -f security/suricata-daemonset.yaml
	kubectl -n $(NS) apply -f security/networkpolicy-quarantine.yaml
	kubectl -n $(NS) apply -f security/egress-firewall-example.yaml || true
	kubectl -n $(NS) apply -f tekton/tasks/01-ship-eve-to-loki.yaml
	kubectl -n $(NS) apply -f tekton/tasks/02-enrich-alerts.yaml
	kubectl -n $(NS) apply -f tekton/tasks/03-apply-blocklist.yaml
	kubectl -n $(NS) apply -f tekton/pipeline.yaml

undeploy:
	- kubectl -n $(NS) delete -f tekton/pipeline.yaml
	- kubectl -n $(NS) delete -f tekton/tasks/03-apply-blocklist.yaml
	- kubectl -n $(NS) delete -f tekton/tasks/02-enrich-alerts.yaml
	- kubectl -n $(NS) delete -f tekton/tasks/01-ship-eve-to-loki.yaml
	- kubectl -n $(NS) delete -f security/egress-firewall-example.yaml
	- kubectl -n $(NS) delete -f security/networkpolicy-quarantine.yaml
	- kubectl -n $(NS) delete -f security/suricata-daemonset.yaml
	- kubectl -n $(NS) delete -f mcp-tools/deployment.yaml
	- kubectl -n $(NS) delete -f mcp-tools/rbac.yaml
	- kubectl delete -f k8s/namespace.yaml

ids:
	kubectl -n $(NS) apply -f security/suricata-daemonset.yaml

nips:
	kubectl -n $(NS) apply -f security/egress-firewall-example.yaml || true
