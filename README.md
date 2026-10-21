# Orbyte Smart-Defect Tracker

A Python Streamlit workspace for logging defective deliveries, reviewing claim
letters, recording manager authorization and viewing the shared audit history.

## Run

```sh
pip install -r requirements.txt
streamlit run src/main.py
```

The Replit Run workflow uses the same Streamlit command. Server address and port
are configured in `.streamlit/config.toml` (`0.0.0.0:5000`).

## Workspace

- **Control room:** system summary and the Log an Incident shortcut.
- **Log incident:** supplier, affected quantity, raw notes and estimated loss.
- **Audit history:** all pending and authorized records, visible to operations staff.
- **Manager dashboard:** financial exposure, cash leaks and active discrepancies.
- **Review & authorize:** pending records, editable letters and manager signatures.

The existing `synthetic_db.json` is used without a data conversion or reset.
All pages read and update this same file. Writes use a file lock and atomic
replacement to prevent concurrent submissions from overwriting each other.
Back up this file before moving the workspace.

Unsaved incident inputs and review drafts persist during navigation within the
same Streamlit session. Streamlit provides the collapsible responsive sidebar.

This remains a **local demo**: letters are template-generated, authorization is
recorded locally, no supplier email is sent and no external invoice is held.
The manager menu groups are workflow separation, not authentication or access
control. The former Node server and `/api` endpoints are no longer used.

## Tests

```sh
python -m unittest discover -s tests -v
```

Tests cover calculations, validation, concurrent writes, duplicate authorization,
data preservation and the complete worker-to-manager-to-audit UI flow. They use
temporary databases and do not add claims to the workspace's real JSON file.
