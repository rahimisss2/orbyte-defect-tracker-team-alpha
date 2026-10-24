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

This remains a **local demo**: letters start from a template with optional live
Gemini analysis and manager-controlled paragraph insertion; authorization is
recorded locally, no supplier email is sent and no external invoice is held.

## Live AI review (`feature-live-ai`)

AI work is isolated on `feature-live-ai`; do not merge or publish it to `main`
until reviewed. In **Review & authorize**, use **Generate AI Contextual Review**
on the relevant pending incident. Gemini `gemini-2.5-flash` returns a contextual
risk assessment, urgency, recommendation, and suggested claim paragraph.
**Insert AI paragraph into draft** preserves existing edits. Review the final
letter, then use the existing manager signature and authorization action.

Configure `GEMINI_API_KEY` in **Replit Secrets** (available as an environment
variable), or in Streamlit secrets under the same name. The app checks
`st.secrets["GEMINI_API_KEY"]` first and falls back to the Replit environment.
Never commit credentials; `.streamlit/secrets.toml` is ignored.

Only an explicit Generate click calls Google. The request includes the supplier
name, item, defect notes, incident loss, and aggregate exposure; it excludes
supplier email, signatures and other claims' raw notes. There is no separate
defect-type field in existing records, so notes are supplied with that limitation
made explicit. AI advice remains session-local and does not write to JSON or
authorize anything. Inserted text is saved through the existing locked
authorization workflow. Missing keys, timeouts and invalid responses leave the
draft untouched. Always verify AI advice; it is not an automatic business decision.
The manager menu groups are workflow separation, not authentication or access
control. The former Node server and `/api` endpoints are no longer used.

## Tests

```sh
python -m unittest discover -s tests -v
```

Tests cover calculations, validation, concurrent writes, duplicate authorization,
data preservation and the complete worker-to-manager-to-audit UI flow. They use
temporary databases and do not add claims to the workspace's real JSON file.
