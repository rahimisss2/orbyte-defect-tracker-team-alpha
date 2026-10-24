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
* **Slide Deck:** https://canva.link/e4eyntm8w0v467u
* **Demo Video:** https://youtu.be/pyMbSz6FKJc?si=8LcM22PqPk-RyjCq


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
| AI / Compute | Google Gemini (`gemini-2.5-flash`) with a labelled simulated fallback
| Hosting / Dev | Replit Cloud Deployment (.replit.app) 

### Repository Directory Structure:

├── .streamlit/
│   └── config.toml               # Streamlit UI configuration
├── Submission/                   # Required hackathon submission documents
│   ├── SDC2026_FAIX_Preliminary.pdf
│   ├── SDC2026_FAIX_TechDeclaration.pdf
│   └── SDC2026_TeamFAIX_Replit_POU.pdf
├── src/                          # Application source code
│   ├── assets/                   # Static UI assets and images
│   └── screens/                  # Modular view interfaces
│       ├── ai_panel.py
│       ├── ai_review.py
│       ├── audit_ui.py
│       ├── database.py           # Local storage Engine (JSON File-Locking)
│       ├── main.py               # Main application entry point
│       ├── navigation.py
│       ├── page_transition.py
│       ├── runtime_secrets.py    # Bridge for st.secrets keys
│       ├── simulated_review.py   # Fault-tolerant backup engine
│       ├── theme.py
│       ├── views.py
│       └── welcome.py
├── tests/                        # Automated test suite
│   ├── test_ai_review.py
│   ├── test_audit_ui.py
│   ├── test_orbyte.py
│   ├── test_page_transition.py
│   └── test_runtime_secrets.py
├── .gitattributes
├── .gitignore
├── .replit                       # Replit cloud execution runtime triggers
├── LICENSE                       # Apache License 2.0 file
├── README.md                     # Documentation frontpage
├── pyproject.toml
├── requirements.txt              # Production dependency packages
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

## Live AI review 🧠

Our application features an AI decision layer specifically designed for SME supply chain challenges, built with Google Gemini and backed by an automated fault-tolerant simulation engine:

- **AI Decision Logic (Google Gemini):** Powered by the `gemini-2.5-flash` model via secure Replit Secrets (`st.secrets["GEMINI_API_KEY"]`). It evaluates defective delivery logs, counts historical supplier infractions, and dynamically drafts a professional, contextual supplier claim paragraph.
- **Human-in-the-Loop Workflow:** In compliance with Domain 2 rules, the manager maintains 100% control. The manager reviews the AI's risk assessment and can use the integrated "Insert simulated paragraph into draft" action to automatically populate the editable claim letter before applying a digital signature.
- **Fault-Tolerant Resilience (Labelled Fallback):** To handle real-world SME internet disruptions or external API latency (such as HTTP 504 Gateway Timeouts), the system triggers a local deterministic backup engine. This system is explicitly flagged as **SIMULATED FALLBACK** on the UI, ensuring 100% operational uptime and zero workflow crashes during judicial evaluation.


## How We Use Replit (Required)

Our team utilized the Replit platform across multiple core engineering workflows to accelerate development and guarantee a stable, zero-config deployment:

* **Development:** Collaborative coding and live workspace environment configuration inside the Replit cloud IDE, utilizing the Replit AI Agent to structure application routines, scaffolding code structures, and rapidly resolve configuration errors.
* **Hosting:** The production Streamlit application is actively deployed using Replit Deployments (Autoscale, Asia server geography), transforming our codebase into a publicly accessible web link at the Live Demo URL provided above.
* **Secrets:** `GEMINI_API_KEY` is configured using Replit Secrets and bridged into Streamlit's native in-memory secrets store. The Gemini client reads `st.secrets["GEMINI_API_KEY"]`; no credential file is generated and no API key is committed. Explicit live generation requests may consume Google API quota.

📄 **Proof of use:** (Submission/SDC2026_TeamFAIX_Replit_POU.pdf)

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

