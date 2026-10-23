# 🛡️ Orbyte Smart-Defect Tracker (Team FAIX)

An automated supply chain management application built with **Python Streamlit** for SMEs to track defective deliveries, generate claim letters, and maintain a shared audit log.

## 👥 Team Information
* **Team Name:** Team FAIX
* **Challenge Domain:** Domain 2 (Orbyte Smart SME Challenge)
* **SDG Track (1–17):** SDG 8 - Promotes SME resource productivity and prevents operational cash leakages.
                        SDG 9 - Accelerates enterprise digital adoption.
* **Team Leader:** CHE AHMAD RAHIMI BIN CHE ROZAID
* **University:** UNIVERSITI TEKNIKAL MALAYSIA MELAKA (UTeM)
* **Number of members:** 4

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
| AI / Compute | Replit Core Workspace 
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

## How We Use Replit (Required)

Our team utilized the Replit platform across multiple core engineering workflows to accelerate development and guarantee a stable, zero-config deployment:

* **Development:** Collaborative coding and live workspace environment configuration inside the Replit cloud IDE, utilizing the Replit AI Agent to structure application routines, scaffolding code structures, and rapidly resolve configuration errors.
* **Hosting:** The production Streamlit application is actively deployed using Replit Deployments (Autoscale, Asia server geography), transforming our codebase into a publicly accessible web link at the Live Demo URL provided above.
* **Secrets:** No external API keys or credentials were used in this local MVP version, ensuring zero credit drain risk, absolute security, and localized data isolation for the business workflow.

📄 **Proof of use:** [submission/SDC2026_TeamAlpha_Replit_POU.pdf](submission/SDC2026_TeamAlpha_Replit_POU.pdf)

## Challenges & Learnings

* **What challenges did you face, and how did you overcome them?**
  Our primary challenge was managing cloud deployment environment errors and Git remote synchronization conflicts (such as overlapping dependency build tracks and detached non-fast-forward push rejections) within the workspace framework. We successfully overcame this by explicitly overriding the Replit configuration scripts (`.replit` shell triggers), modularizing the production package constraints (`requirements.txt`), and initiating granular upstream cache purges (`git push --force` sync) to force clean deployments.

* **What did your team learn?**
  The team gained extensive technical insights into file-concurrency synchronization, safe database multi-user file locking practices in lightweight JSON environments, state management controls across distinct worker-to-manager interfaces in Streamlit, and modern AI-assisted engineering practices using autonomous developer agents.

## Future Improvements

* [ ] **Generative AI & Contextual Email Routing:** Transition the current deterministic template engine into a secure, fine-tuned Local Large Language Model (LLM) framework to analyze historical delivery records and dynamically generate highly contextual, urgency-weighted supplier emails.
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

