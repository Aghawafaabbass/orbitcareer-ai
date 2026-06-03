<div align="center">

```
╔══════════════════════════════════════════════════════════════════════════╗
║          OrbitCareer AI — Global Autonomous Career Agent                 ║
║     Production-Grade Recruiter Intelligence Platform · v2.1 Pro          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

[![Streamlit App](https://img.shields.io/badge/%F0%9F%9A%80_Live_Demo-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=for-the-badge)](https://console.groq.com)
[![LLM](https://img.shields.io/badge/LLM-Agentic_AI-8B5CF6?style=for-the-badge)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Production-deployed AI recruiter intelligence platform — bulk resume processing, autonomous scoring, skill gap analysis, personality profiling, culture fit scoring, LinkedIn & email outreach drafting, and branded PDF export — all powered by Groq LLaMA 3.1 Agentic AI.**

*Developed by [Agha Wafa Abbas](mailto:agha.wafa@port.ac.uk) · Lecturer & ML Researcher · University of Portsmouth, UK*

---

</div>

## 📋 Table of Contents

- [What is OrbitCareer AI?](#-what-is-orbitcareer-ai)
- [Who is it for?](#-who-is-it-for--target-users)
- [Why is it Unique?](#-why-is-it-unique--vs-traditional-ats)
- [Tech Stack](#-tech-stack--architecture)
- [System Architecture Diagram](#-system-architecture)
- [AI Pipeline Flow](#-ai-pipeline-flow)
- [Features — v2.1](#-full-feature-set--v21)
- [Screenshots](#-platform-screenshots)
- [Local Setup](#-local-setup--windows-powershell)
- [Streamlit Cloud Deploy](#-deploy-on-streamlit-cloud-free)
- [Environment Variables](#-environment-variables)
- [Project Structure](#-project-structure)
- [LLM & Agentic AI Stack](#-llm--agentic-ai-design)
- [Author](#-author)
- [License](#-license)

---

## 🎯 What is OrbitCareer AI?

OrbitCareer AI is a **production-grade autonomous recruiter intelligence platform** built on top of **Groq's ultra-fast LLaMA 3.1 inference engine**. It processes resumes in bulk — PDF, DOCX, or raw pasted text — and within seconds returns a comprehensive AI-generated candidate report covering 21 distinct intelligence dimensions.

Unlike traditional ATS (Applicant Tracking Systems) which do nothing more than keyword matching, OrbitCareer AI uses **multi-prompt Agentic AI chaining** — each candidate triggers a sequence of 7 specialized LLM calls, each responsible for one analytical dimension, producing outputs no conventional ATS can generate.

> **Core thesis:** Hiring decisions should be data-driven, contextually aware, and AI-augmented — not keyword-filtered. OrbitCareer AI delivers a senior recruiter's 4-hour analysis in under 30 seconds, at zero marginal cost per candidate.

---

## 👥 Who is it for? — Target Users

| User Type | Problem Solved | Time Saved |
|---|---|---|
| 🏢 **HR Recruiters** | Screen 50 resumes manually → AI does it in 3 min | 4–6 hrs/day |
| 🔍 **Staffing Agencies** | Write personalised outreach for 100 candidates | 90% effort cut |
| 🎓 **University Career Services** | Evaluate student CVs against real industry roles | Real-time |
| 👤 **Hiring Managers** | Get shortlist with reasoning — not just ranked names | Saves days |
| 🧑‍💼 **Candidates** | Self-assess your own CV against any role | Instant insight |
| 🌍 **Remote-First Teams** | Screen international applicants across time zones | Async ready |

---

## 🆚 Why is it Unique? — vs Traditional ATS

| Capability | Workday / Greenhouse (ATS) | OrbitCareer AI |
|---|---|---|
| Resume parsing | ✅ Keyword extraction | ✅ Full semantic AI analysis |
| Fit scoring | ⚠️ Keyword match % | ✅ LLM 0–100 talent score |
| Hiring recommendation | ❌ | ✅ Strong Hire / Hire / Maybe / No Hire |
| Personality insight | ❌ | ✅ MBTI-style profiling |
| Salary estimate | ❌ | ✅ Market range per profile |
| Culture fit | ❌ | ✅ Startup alignment score 0–100 |
| Skill gap analysis | ❌ | ✅ Missing skills highlighted |
| ATS compatibility score | ❌ Meta-ironic | ✅ Score + 3 tips |
| Interview questions | ❌ | ✅ 5 role-tailored technical Qs |
| LinkedIn outreach | ❌ | ✅ Personalised, ready to send |
| Email draft | ❌ | ✅ Full email with subject line |
| Executive summary | ❌ | ✅ 3-sentence recruiter brief |
| PDF reports | ❌ | ✅ Branded, download-ready |
| Dark mode | ❌ | ✅ Full theme toggle |
| Setup cost | $$$$ /month | ✅ Free (Groq free tier) |

---

## 🛠 Tech Stack & Architecture

### Core Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit 1.28+ | Interactive web UI, dark/light mode, tabs, sidebar |
| **LLM Engine** | Groq Cloud API | Ultra-fast LLaMA 3.1-8B inference (<500ms/call) |
| **LLM Model** | LLaMA 3.1-8B Instant | Multi-prompt agentic pipeline |
| **AI Pattern** | Agentic AI / LLM Chaining | 7 sequential specialized prompts per candidate |
| **PDF Generation** | fpdf2 | Branded executive PDF reports |
| **Resume Parsing** | pypdf + python-docx | PDF & DOCX text extraction |
| **Environment** | python-dotenv | Secure API key management |
| **Database** | psycopg2 + PostgreSQL | Optional persistent candidate storage |
| **Deployment** | Streamlit Cloud | Free public URL, GitHub-connected CI |

### LLM & Agentic AI

| Component | Detail |
|---|---|
| **Provider** | Groq Cloud (groq.com) |
| **Model** | `llama-3.1-8b-instant` |
| **Pattern** | Multi-prompt Agentic Chain (7 LLM calls/candidate) |
| **JSON Mode** | Structured outputs via `response_format: json_object` |
| **RAG** | Implicit RAG — resume text injected as context window per call |
| **Temperature** | 0.0 for analytical tasks · 0.3–0.7 for creative outputs |
| **Automation** | Fully autonomous pipeline — zero human input after upload |

> **Note on RAG:** OrbitCareer AI uses **implicit Retrieval-Augmented Generation** — the full resume text is injected into each LLM prompt as a live context document, enabling the model to reason over candidate-specific data without a vector database. This is a lightweight, production-practical RAG pattern suited for per-document inference.

---

## 🏗 System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│              OrbitCareer AI — Multi-Tier System Architecture           │
├──────────────────┬─────────────────────────┬───────────────────────────┤
│     TIER 1       │        TIER 2           │         TIER 3            │
│  Input Layer     │  AI Inference Engine    │   Output & Export Layer   │
├──────────────────┼─────────────────────────┼───────────────────────────┤
│                  │                         │                           │
│ ┌──────────────┐ │  ┌───────────────────┐  │  ┌─────────────────────┐ │
│ │ PDF Upload   │ │  │  Groq API         │  │  │ Talent Score Card   │ │
│ │ DOCX Upload  │─┼─▶│  LLaMA 3.1-8B    │  │  │ Hire Recommendation │ │
│ │ Raw Text     │ │  │  Instant Inference│  │  │ Skill Gap Tags      │ │
│ └──────────────┘ │  │                   │  │  │ Interview Questions  │ │
│                  │  │  Agentic Chain:   │  │  │ LinkedIn Outreach   │ │
│ ┌──────────────┐ │  │  1. Role Detect   │─▶│  │ Email Draft         │ │
│ │ pypdf        │ │  │  2. Core Parse    │  │  │ ATS Score + Tips    │ │
│ │ python-docx  │ │  │  3. LinkedIn Msg  │  │  │ Salary Estimate     │ │
│ │ Text Extract │ │  │  4. Email Draft   │  │  │ Personality Profile │ │
│ └──────────────┘ │  │  5. ATS Score     │  │  │ Culture Fit Score   │ │
│                  │  │  6. Salary Est.   │  │  │ Executive Summary   │ │
│ ┌──────────────┐ │  │  7. Personality   │  │  └─────────────────────┘ │
│ │ .env / TOML  │ │  │  8. Culture Fit   │  │                           │
│ │ GROQ_API_KEY │ │  │  9. Exec Summary  │  │  ┌─────────────────────┐ │
│ └──────────────┘ │  │  10. Hire Rec.    │  │  │ PDF Export (fpdf2)  │ │
│                  │  └───────────────────┘  │  │ Shortlist Manager   │ │
│                  │                         │  │ PostgreSQL (opt.)   │ │
│                  │  Implicit RAG Pattern:  │  └─────────────────────┘ │
│                  │  Resume → Context →     │                           │
│                  │  LLM → JSON Output      │                           │
└──────────────────┴─────────────────────────┴───────────────────────────┘
         Streamlit UI wraps all 3 tiers — Dark/Light theme · Sidebar controls
```

---

## 🔄 AI Pipeline Flow

```
                    ┌──────────────────────────────┐
                    │   User Uploads Resume(s)      │
                    │   PDF / DOCX / Raw Text        │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │   Text Extraction Layer       │
                    │   pypdf · python-docx         │
                    │   Max 3,500 chars/candidate   │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │   PROMPT 1 — Role Detection  │
                    │   LLaMA 3.1 → Job Title      │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │   PROMPT 2 — Core Parse      │
                    │   JSON: name, skills, exp,   │
                    │   score, flags, questions,   │
                    │   missing_skills             │
                    └──────────────┬───────────────┘
                                   │
               ┌───────────────────┼───────────────────┐
               │                   │                   │
               ▼                   ▼                   ▼
   ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
   │ PROMPT 3         │ │ PROMPT 4         │ │ PROMPT 5         │
   │ LinkedIn Outreach│ │ Email Draft      │ │ ATS Score + Tips │
   └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
            │                    │                    │
            └──────────┬─────────┘                   │
                       │                             │
               ┌───────▼──────────┐      ┌──────────▼───────────┐
               │ PROMPT 6         │      │ PROMPT 7             │
               │ Salary Estimate  │      │ Personality Profile  │
               └───────┬──────────┘      └──────────┬───────────┘
                       │                             │
               ┌───────▼──────────┐      ┌──────────▼───────────┐
               │ PROMPT 8         │      │ PROMPT 9             │
               │ Culture Fit Score│      │ Executive Summary    │
               └───────┬──────────┘      └──────────┬───────────┘
                       │                             │
                       └──────────┬──────────────────┘
                                  │
                    ┌─────────────▼──────────────────┐
                    │   PROMPT 10 — Hire Rec.        │
                    │   Strong Hire / Hire /         │
                    │   Maybe / No Hire              │
                    └─────────────┬──────────────────┘
                                  │
                    ┌─────────────▼──────────────────┐
                    │   Streamlit Render Layer       │
                    │   Candidate Card · 8 Tabs ·    │
                    │   Shortlist · Compare · PDF    │
                    └────────────────────────────────┘
```

---

## ✨ Full Feature Set — v2.1

| # | Feature | Description | AI-Powered |
|---|---|---|---|
| 1 | 📁 **Bulk Resume Upload** | Up to 50 PDF/DOCX files per batch | — |
| 2 | ✍️ **Raw Text Paste** | LinkedIn profiles, bios, any career text | — |
| 3 | 🤖 **AI Role Auto-Detection** | LLM maps best-fit job title from resume | ✅ LLM |
| 4 | 🏆 **Talent Score 0–100** | Semantic fit score vs target role | ✅ LLM |
| 5 | ✅ **Hire Recommendation** | Strong Hire / Hire / Maybe / No Hire | ✅ LLM |
| 6 | 🚩 **Red Flag Analysis** | Risk flags and concerns per candidate | ✅ LLM |
| 7 | 📋 **5 Interview Questions** | Role-tailored technical interview Qs | ✅ LLM |
| 8 | 💬 **LinkedIn Outreach** | Personalised message, ready to send | ✅ LLM |
| 9 | 📧 **Email Draft** | Full recruitment email with subject line | ✅ LLM |
| 10 | ⚠️ **Skill Gap Analysis** | Missing skills highlighted in red | ✅ LLM |
| 11 | 🤖 **ATS Score Simulator** | ATS compatibility score + 3 tips | ✅ LLM |
| 12 | 💰 **Salary Range Estimator** | Market salary estimate per profile | ✅ LLM |
| 13 | 🧠 **Personality Profiling** | MBTI-style work personality type | ✅ LLM |
| 14 | 🏢 **Culture Fit Score** | Startup culture alignment 0–100 | ✅ LLM |
| 15 | 📝 **Executive Summary** | 3-sentence AI recruiter brief | ✅ LLM |
| 16 | 📌 **Recruiter Notes** | Private per-candidate notes (session) | — |
| 17 | ⭐ **Shortlist Manager** | One-click shortlist + sidebar tracker | — |
| 18 | ⚖️ **Candidate Comparison** | Side-by-side 2-candidate evaluation | — |
| 19 | 🌙 **Dark / Light Mode** | Full theme toggle — all elements | — |
| 20 | 📄 **PDF Executive Reports** | Branded PDF — all 10 dimensions | — |
| 21 | 🗄️ **PostgreSQL Export** | Optional persistent database save | — |

---

## 📸 Platform Screenshots

### Dashboard — Talent Pool Matrix & Metrics
![Dashboard](Screenshots/1779997018591_image.png)

### Candidate Card — Full AI Analysis
![Candidate Analysis](Screenshots/1780251297854_image.png)

### Dark Mode — Complete Theme
![Dark Mode](Screenshots/1780256438261_image.png)

### Bulk Upload — PDF & DOCX Processing
![Bulk Upload](Screenshots/1780422911334_image.png)

> **Live Demo:** [🚀 Launch OrbitCareer AI](https://share.streamlit.io) *(deploy to get your public URL)*

---

## ⚙️ Local Setup — Windows PowerShell

### Step 1 — Clone the repo
```powershell
git clone https://github.com/Aghawafaabbass/orbitcareer-ai.git
cd orbitcareer-ai
```

### Step 2 — Create & activate virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3 — Install all dependencies
```powershell
pip install -r requirements.txt
```

### Step 4 — Create `.env` file
Create a file named `.env` in the project root folder:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Get your **free** API key at: [https://console.groq.com](https://console.groq.com)

### Step 5 — Run the app
```powershell
streamlit run frontend.py
```
App opens at: **http://localhost:8501**

### Stop the app
```
Ctrl + C
```

---

## 🌐 Deploy on Streamlit Cloud (Free)

Get a **permanent public URL** — free forever, GitHub-connected CI/CD:

**Step 1 — Push to GitHub** *(already done)*

**Step 2 — Deploy**
1. Go to **[https://share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your GitHub account
3. Click **New app**
4. Select:
   - Repository: `Aghawafaabbass/orbitcareer-ai`
   - Branch: `main`
   - Main file: `frontend.py`
5. Click **Advanced settings → Secrets** and paste:
```toml
GROQ_API_KEY = "gsk_your_actual_groq_key_here"
```
6. Click **Deploy** → live in ~2 minutes ✅

Your app URL will be:
```
https://aghawafaabbass-orbitcareer-ai-frontend-XXXXX.streamlit.app
```

> Every `git push` to `main` **auto-redeploys** — no manual steps needed.

---

## ⚙️ Environment Variables

| Variable | Required | Description | Where to get |
|---|---|---|---|
| `GROQ_API_KEY` | ✅ **Yes** | Groq LLaMA 3.1 API key | [console.groq.com](https://console.groq.com) — free |
| `DB_HOST` | ❌ Optional | PostgreSQL host | Your DB server |
| `DB_PORT` | ❌ Optional | PostgreSQL port (default: 5432) | Your DB config |
| `DB_USER` | ❌ Optional | PostgreSQL username | Your DB config |
| `DB_PASSWORD` | ❌ Optional | PostgreSQL password | Your DB config |

---

## 📂 Project Structure

```
orbitcareer-ai/
│
├── frontend.py           ← 🧠 Main app — all 21 features, full UI
├── app.py                ← Legacy test file
├── test_ai.py            ← Unit test / Groq API test
│
├── Screenshots/          ← Platform screenshots (used in README)
│   ├── 1779997018591_image.png
│   ├── 1780251297854_image.png
│   ├── 1780256438261_image.png
│   └── 1780422911334_image.png
│
├── .env                  ← 🔒 API keys — NEVER commit (in .gitignore)
├── .gitignore            ← Excludes .env, venv/, __pycache__/
├── requirements.txt      ← All Python dependencies
└── README.md             ← This file
```

---

## 🧠 LLM & Agentic AI Design

OrbitCareer AI uses a **10-prompt Agentic AI chain** per candidate — each prompt is a specialized AI agent responsible for one analytical task:

```python
# Prompt chain per candidate (simplified)
1. call_groq(role_detection_prompt)         # → assigned_target_role
2. call_groq(core_parse_prompt, json=True)  # → name, skills, score, flags, questions, missing_skills
3. call_groq(linkedin_prompt, temp=0.7)     # → personalised outreach message
4. call_groq(email_prompt, temp=0.7)        # → full email with subject line
5. call_groq(ats_prompt, json=True)         # → ats_score, ats_tips
6. call_groq(salary_prompt, json=True)      # → salary_range
7. call_groq(personality_prompt, json=True) # → personality_type, personality_desc
8. call_groq(culture_prompt, json=True)     # → culture_score, culture_notes
9. call_groq(summary_prompt, temp=0.5)      # → 3-sentence executive summary
10. call_groq(hire_rec_prompt, json=True)   # → Strong Hire / Hire / Maybe / No Hire
```

**Why Groq?** Groq's LPU (Language Processing Unit) hardware delivers ~500 token/sec inference — 10x faster than GPT-4o API at zero cost on the free tier. For bulk batch processing of 10–15 resumes, this means full analysis in under 3 minutes total.

**Structured outputs** via `response_format: {"type": "json_object"}` ensure deterministic, parseable JSON — no hallucinated markdown, no broken parsing.

**Implicit RAG:** Each prompt injects the full resume text as a context document — lightweight, zero-infrastructure Retrieval-Augmented Generation without a vector store.

---

## 👤 Author

### Agha Wafa Abbas
**ML Scientist · Lecturer · Researcher · Full-Stack Developer**

| Institution | Role | Contact |
|---|---|---|
| University of Portsmouth, UK | Lecturer | [agha.wafa@port.ac.uk](mailto:agha.wafa@port.ac.uk) |
| Arden University, UK | Lecturer | [awabbas@arden.ac.uk](mailto:awabbas@arden.ac.uk) |
| Pearson, UK | Lecturer | — |
| IVY College, Lahore, Pakistan | Lecturer | [wafa.abbas.lhr@rootsivy.edu.pk](mailto:wafa.abbas.lhr@rootsivy.edu.pk) |

[![GitHub](https://img.shields.io/badge/GitHub-Aghawafaabbass-181717?style=flat-square&logo=github)](https://github.com/Aghawafaabbass)
[![OmniTerra](https://img.shields.io/badge/Also_See-OmniTerra_Global_M-2EA44F?style=flat-square)](https://github.com/Aghawafaabbass/OmniTerra-Global-M)

> *"AI should augment human judgment — not replace it. OrbitCareer AI gives recruiters AI-grade insight while keeping the human decision at the centre."*
> — Agha Wafa Abbas

---

## 📜 License

MIT License — Free to use, modify, and distribute with attribution.

**Copyright © 2025 — Agha Wafa Abbas. All Rights Reserved.**

---

## ⚠️ Disclaimer

> OrbitCareer AI is a research and productivity tool. AI-generated scores, recommendations, and personality profiles are **decision-support outputs — not final hiring decisions**. All candidate evaluations should be reviewed by qualified human recruiters before any employment action is taken. Salary estimates are indicative only and vary by region, company, and market conditions.

---

<div align="center">

```
© 2025 — Agha Wafa Abbas | OrbitCareer AI
Built with 🤖 Groq LLaMA 3.1 · 🚀 Streamlit · 🐍 Python · 📄 fpdf2
```

*"Turning hours of recruiter work into seconds of AI intelligence."*

</div>
