# 🛡️ Orbyte Smart-Defect Tracker (Team FAIX)

An automated supply chain management application built with **Python Streamlit** for SMEs to track defective deliveries, generate claim letters, and maintain a shared audit log.

## 👥 Team Information
* **Team Name:** Team FAIX
* **Challenge Domain:** Domain 2 (Orbyte Smart SME Challenge)
* **SDG Track (1–17):** SDG 8 - Promotes SME resource productivity and prevents operational cash leakages.
                        SDG 9 - Accelerates enterprise digital adoption.
* **Team Leader:** CHE AHMAD RAHIMI BIN CHE ROZAID
* **University:** UNIVERSITI TEKNIKAL MALAYSIA MELAKA (UTeM)
* **Number of members:** 2

## Links
* **Github Repository:** https://github.com/rahimisss2/orbyte-defect-tracker-team-alpha
* **Replit Project:** https://replit.com/@rahimirozaid99/orbyte-defect-tracker-team-alpha
* **Live Demo URL (Prototype):** https://orbyte-defect-tracker-team-alpha.replit.app
* **Slide Deck:**
* **Demo Video:** 


---
OVERVIEW
## 💡 Problem Statement & Automated Solution

### Problem Context (SMEs):
SMEs often face financial losses from inefficient supply chain handling, manual logging of defective goods, and paper-based claim approvals.

### Team FAIX's Automated Solution:
A modular 5-step digital workflow covering a real-time control room, rapid incident logging, automated claim letter review/authorization, data concurrency guards, and an immutable audit history.

### Key Feature:
* **Control Room & Manager Dashboard:** Real-time visibility into active operational discrepancies, ongoing financial exposures, and supplier leakage metrics.
* **Automated Claims Generation & Signing:** Instant transformation of operation logs into ready-to-edit formal claim letters, complete with integrated digital signature authorization.
* **Concurrency Guard (File Locking):** A specialized data layer using atomic replacement on local JSON storage to prevent multi-user write conflicts and ensure data integrity.

---

## 🛠️ Tech Stack

| Frontend | Python (Streamlit Framework) 
| Backend | Python 3.12 
| Database | JSON (`synthetic_db.json` with File-Locking engine) 
| AI / Compute | Google Gemini (`gemini-flash-latest`) with a labelled 504 simulation fallback
| Hosting / Dev | Replit Cloud Deployment (.replit.app) 

### Repository Directory Structure:
```text
├── .streamlit/config.toml
├── src/
│   ├──main.py
│   ├── database.py
│   └── screens/
│       ├── log_incident.py
│       ├── review_authorize.py
│       └── audit_history.py
├── tests/
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
└── uv.lock
```
## Architecture

User (Staff/Manager) ➔ Streamlit Frontend (UI) ➔ Python Backend Logic (src/main.py)
                                                        │
                   ┌────────────────────────────────────┴────────────────────────────────────┐
                   ▼                                                                         ▼
      Log Incident Workflow                                                    Review & Audit Workflow
   (Captures defect data & metrics)                                          (Applies File-Locking Mechanism)
                   │                                                                         │
                   └────────────────────────────────────┬────────────────────────────────────┘
                                                        ▼
                                       Local Storage (synthetic_db.json)

---

## 🚀 Guide to Running the Application Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com.git
   cd orbyte-defect-tracker-team-alpha
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Launch the application:**
   ```bash
   streamlit run src/main.py
   ```

## Live AI review

This remains a **local demo**: letters start from a template with optional live
Gemini analysis and manually edited claim drafts; authorization is
recorded locally, no supplier email is sent and no external invoice is held.

In **Review & authorize**, use **Generate AI Contextual Review**
on the relevant pending incident. Gemini `gemini-flash-latest` returns a contextual
risk assessment, urgency, recommendation, and suggested claim paragraph.
This alias follows Google's current Flash model; its resolved version can change.
The **Suggested claim paragraph** is displayed as static text for both live and
simulated results. Read or manually copy it into the editable draft if useful.
Review the final letter, then use the existing manager signature and authorization action.

Configure `GEMINI_API_KEY` in **Replit Secrets** and restart the app. At startup,
the injected credential is merged into Streamlit's native **in-memory** secrets
store using Streamlit 1.66.1's thread-safe programmatic API. The Gemini client
reads exclusively through `st.secrets["GEMINI_API_KEY"]`; it has no environment
fallback. The bridge never writes credentials to files, logs, or session state.
Replit's injected value takes precedence over any file-based value. No
`secrets.toml` file is generated; `.streamlit/secrets.toml` is ignored defensively.

Only an explicit Generate click calls Google. The request includes the supplier
name, item, defect notes, incident loss, and aggregate exposure; it excludes
supplier email, signatures and other claims' raw notes. There is no separate
defect-type field in existing records, so notes are supplied with that limitation
made explicit. AI advice remains session-local and does not write to JSON or
authorize anything. Manually edited text is saved through the existing locked
authorization workflow. Missing keys, timeouts and invalid responses leave the
draft untouched. Always verify AI advice; it is not an automatic business decision.

The provider schema deliberately uses only object/string/enum/required constraints
for Gemini compatibility; strict length and extra-field checks still run locally.
If Google reports that a model is no longer available, do not retry it repeatedly
or silently substitute another model. Agree on the replacement first.
Requests have a 60-second deadline and no automatic retry. The review screen enables
an automatic fallback **only after a confirmed HTTP 504**. It is explicitly labelled
**SIMULATED FALLBACK**, not live Gemini. Credentials, permission failures, retired
models, invalid output, and other HTTP errors do not silently trigger simulation.
The fallback is deterministic demo assistance, not production policy: potential
safety keywords are unverified critical flags; loss of RM 500 or three incidents
with RM 250 pending exposure prompts high urgency; loss of RM 100 or three incidents
prompts medium urgency; otherwise it suggests a supplier warning. No partial
amount is invented. Every result still requires manager review and signature.
Generation leaves the existing draft and database untouched. There is no automatic
insertion button or draft mutation; managers edit the letter manually before authorization.
The manager menu groups are workflow separation, not authentication or access
control. The former Node server and `/api` endpoints are no longer used.

## How We Use Replit (Required)

Our team utilized the Replit platform across multiple core engineering workflows to accelerate development and guarantee a stable, zero-config deployment:

* **Development:** Collaborative coding and live workspace environment configuration inside the Replit cloud IDE, utilizing the Replit AI Agent to structure application routines, scaffolding code structures, and rapidly resolve configuration errors.
* **Hosting:** The production Streamlit application is actively deployed using Replit Deployments (Autoscale, Asia server geography), transforming our codebase into a publicly accessible web link at the Live Demo URL provided above.
* **Secrets:** `GEMINI_API_KEY` is configured using Replit Secrets and bridged into Streamlit's native in-memory secrets store. The Gemini client reads `st.secrets["GEMINI_API_KEY"]`; no credential file is generated and no API key is committed. Explicit live generation requests may consume Google API quota.

📄 **Proof of use:** [submission/SDC2026_TeamAlpha_Replit_POU.pdf](submission/SDC2026_TeamAlpha_Replit_POU.pdf)

## Challenges & Learnings

* **What challenges did you face, and how did you overcome them?**
  Our primary challenge was managing cloud deployment environment errors and Git remote synchronization conflicts (such as overlapping dependency build tracks and detached non-fast-forward push rejections) within the workspace framework. We successfully overcame this by explicitly overriding the Replit configuration scripts (`.replit` shell triggers), modularizing the production package constraints (`requirements.txt`), and initiating granular upstream cache purges (`git push --force` sync) to force clean deployments.

* **What did your team learn?**
  The team gained extensive technical insights into file-concurrency synchronization, safe database multi-user file locking practices in lightweight JSON environments, state management controls across distinct worker-to-manager interfaces in Streamlit, and modern AI-assisted engineering practices using autonomous developer agents.

## Future Improvements

* [ ] **Contextual Email Routing:** Extend the existing Gemini-generated, manager-reviewed claim drafts with explicit supplier-email dispatch and delivery tracking. The current application does not send email.
* [ ] **Role-Based Authentication & Third-Party API Integration:** Upgrade the user workflow separation layer into a cryptographically secured role-based authentication protocol (OAuth2/JWT) and integrate with external accounting software APIs to automatically lock claims to company digital invoices.

## Team

1) CHE AHMAD RAHIMI BIN CHE ROZAID  (TEAM LEADER) (@rahimisss2)
2) MUHAMMAD NORSHAH DANIAL BIN NORAZLAN (UI/UX DESIGNER) (@norshahdanial)

---

## 🔗 Submission Checklist

* [x] Team name, domain (Domain 2) and SDG track filled in
* [ ] Slide deck link added
* [ ] Demo video link added
* [ ] Replit used, with proof of use in `submission/`
* [ ] RunPod used, with proof of use in `submission/`
* [ ] Preliminary submission completed (`SDC2026_TeamAlpha_Preliminary.pdf`)
* [ ] Technology declaration completed (`SDC2026_TeamAlpha_TechDeclaration.pdf`)
* [ ] Submission files renamed with your team name (replace TeamName)
* [ ] "How to Run" steps verified
* [ ] No API keys or secrets committed to the repository


## 🧪 Automated Testing & SDG Alignment

Execute the test suite via:
```bash
python -m unittest discover -s tests -v
```

* **SDG 8:** Promotes SME resource productivity and prevents operational cash leakages. (Decent Work and Economic Growth)
* **SDG 9:** Accelerates enterprise digital adoption. (Industry, Innovation & Infrastructure)

---
📜 **License:** Licensed under the **Apache License 2.0**.

