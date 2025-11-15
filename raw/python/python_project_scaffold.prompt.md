---
mode: agent
model: GPT-5 mini (copilot)
tools: ['edit/createFile', 'edit/createDirectory', 'edit/editFiles']
---

Create a Python project scaffold with the following structure:
/src/
/src/observability/
/src/observability/logger.py
/src/observability/tracing.py
/src/observability/metrics.py
/docs/
/scripts
/tests/${input:project_name}/test/
requirements.txt
