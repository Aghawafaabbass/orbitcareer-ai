# 💼 OrbitCareer AI — Global Autonomous Career Agent

> **Developed by Agha Wafa Abbas**  
> AI-powered bulk resume screening, scoring, and recruiter automation platform.  
> Built with Streamlit + Groq LLaMA 3.1 · v2.1 Pro

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 🎯 What is OrbitCareer AI?

OrbitCareer AI is a production-grade recruiter intelligence platform. It processes resumes in bulk using Groq's LLaMA 3.1 AI and in seconds delivers:

- Talent scores & hiring recommendations
- Skill gap analysis with missing competencies
- ATS compatibility scores + improvement tips
- Market salary estimates
- Personality profiling (MBTI-style)
- Culture fit scores
- LinkedIn outreach + Email drafts
- Branded PDF executive reports

---

## 👥 Who is it for?

| User | Use Case |
|---|---|
| 🏢 HR Recruiters | Screen 50 resumes in minutes instead of days |
| 🔍 Staffing Agencies | Auto-generate outreach messages at scale |
| 🎓 University Career Services | Evaluate student CVs against real roles |
| 👤 Hiring Managers | Get AI-driven shortlists with reasoning |
| 🧑‍💼 Candidates | Self-evaluate your own CV against a role |

---

## ✨ Features — v2.1

| # | Feature | Description |
|---|---|---|
| 1 | 📁 Bulk Upload | Up to 50 PDF/DOCX resumes per batch |
| 2 | ✍️ Raw Text Paste | LinkedIn profiles, bios, career narratives |
| 3 | 🤖 AI Role Detection | Auto-maps best-fit job title via LLM |
| 4 | 🏆 Talent Score | 0–100 fit score vs target role |
| 5 | ✅ Hire Recommendation | Strong Hire / Hire / Maybe / No Hire |
| 6 | 🚩 Red Flag Analysis | Risk flags per candidate |
| 7 | 📋 Interview Questions | 5 role-tailored technical questions |
| 8 | 💬 LinkedIn Outreach | Personalised message ready to send |
| 9 | 📧 Email Draft | Full email with subject line |
| 10 | ⚠️ Skill Gap Analysis | Missing skills highlighted in red tags |
| 11 | 🤖 ATS Score | ATS compatibility + 3 improvement tips |
| 12 | 💰 Salary Estimator | Market salary range per profile |
| 13 | 🧠 Personality Profiling | MBTI-style work personality type |
| 14 | 🏢 Culture Fit | Startup culture alignment score 0–100 |
| 15 | 📝 Executive Summary | 3-sentence AI recruiter summary |
| 16 | 📌 Recruiter Notes | Private per-candidate notes (saved in session) |
| 17 | ⭐ Shortlist Manager | One-click shortlist + sidebar tracker |
| 18 | ⚖️ Comparison Mode | Side-by-side 2-candidate evaluation |
| 19 | 🌙 Dark / Light Mode | Sidebar theme toggle |
| 20 | 📄 PDF Reports | Branded executive PDF per candidate |
| 21 | 🗄️ DB Export | Optional PostgreSQL save toggle |

---

## 🆚 Why OrbitCareer AI vs Traditional ATS?

| Feature | Traditional ATS | OrbitCareer AI |
|---|---|---|
| Resume parsing | Keyword matching | Full AI semantic analysis |
| Personality insight | ❌ | ✅ MBTI-style profiling |
| Salary estimate | ❌ | ✅ Market range per profile |
| Culture fit | ❌ | ✅ Startup alignment score |
| Outreach messages | ❌ | ✅ LinkedIn + Email auto-draft |
| Interview questions | ❌ | ✅ 5 role-tailored Qs |
| PDF reports | ❌ | ✅ Branded executive PDF |
| Setup cost | $$$$ | Free (Groq free tier) |

---

## 🛠️ Local Setup (Windows PowerShell)

### Step 1 — Clone the repo
```powershell
git clone https://github.com/Aghawafaabbass/orbitcareer-ai.git
cd orbitcareer-ai
```

### Step 2 — Create virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3 — Install dependencies
```powershell
pip install -r requirements.txt
```

### Step 4 — Create .env file
Create a file named `.env` in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at: https://console.groq.com

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

## 🌐 Deploy on Streamlit Cloud (Free, Public URL)

1. Push code to GitHub (see commands below)
2. Go to **https://share.streamlit.io**
3. Sign in with GitHub
4. Click **New app**
5. Select your repo → branch: `main` → file: `frontend.py`
6. Click **Advanced settings → Secrets** and add:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```
7. Click **Deploy** — live public URL in ~2 minutes ✅

---

## 📂 Project Structure

```
orbitcareer-ai/
├── frontend.py          ← Main Streamlit app (all features)
├── app.py               ← (legacy / test file)
├── .env                 ← API keys — NEVER commit this
├── .gitignore           ← Excludes .env, venv, __pycache__
├── requirements.txt     ← Python dependencies
└── README.md            ← This file
```

---

## 📋 requirements.txt

```
streamlit
groq
python-dotenv
fpdf2
pypdf
python-docx
psycopg2-binary
```

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | From console.groq.com (free) |
| `DB_HOST` | ❌ Optional | PostgreSQL host (default: localhost) |
| `DB_PORT` | ❌ Optional | PostgreSQL port (default: 5432) |
| `DB_USER` | ❌ Optional | PostgreSQL user |
| `DB_PASSWORD` | ❌ Optional | PostgreSQL password |

---

## 📄 License

MIT License — Free to use, modify, and distribute.  
**Developed by Agha Wafa Abbas © 2025**

---

## 🙋 Contact

- GitHub: [github.com/Aghawafaabbass](https://github.com/Aghawafaabbass)
- Email: aghawafaabbass@gmail.com
