# RHODS Setup

1) Ensure RHODS installed and enabled.
2) `oc apply -f workbench/workbench-rhoai.yaml`
3) Launch the Workbench from the RHODS UI.
4) Clone this repo into the notebook, or mount via PVC.
5) Run `workbench/client/examples/*.py` to call MCP tools.
