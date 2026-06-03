import os
import json
import time
try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from fpdf import FPDF
from pypdf import PdfReader
import docx

load_dotenv()

st.set_page_config(
    page_title="OrbitCareer AI Platform",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "shortlisted" not in st.session_state:
    st.session_state.shortlisted = []
if "notes" not in st.session_state:
    st.session_state.notes = {}

def get_theme_css(dark):
    if dark:
        return """
<style>
html, body, .stApp, .stApp > div, [data-testid="stAppViewContainer"],
[data-testid="stHeader"], [data-testid="stToolbar"],
section[data-testid="stMainBlockContainer"],
.block-container {
    background-color: #0f172a !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"], [data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"] {
    background-color: #1e293b !important;
}
[data-testid="stSidebar"] *, [data-testid="stSidebarContent"] *,
[data-testid="stSidebarUserContent"] * {
    color: #e2e8f0 !important;
}
p, span, div, label, li, h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText, [data-testid="stMarkdownContainer"] {
    color: #e2e8f0 !important;
}
[data-testid="metric-container"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 10px; padding: 12px 16px;
}
[data-testid="metric-container"] * { color: #e2e8f0 !important; }
.stButton > button {
    background: #1e40af !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
}
.stDownloadButton > button {
    background: #185FA5 !important; color: white !important;
    border-radius: 8px !important; border: none !important;
    font-weight: 500 !important;
}
input, textarea, select,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
}
.stSelectbox > div > div { background: #1e293b !important; color: #e2e8f0 !important; }
.stTabs [data-baseweb="tab-list"] { background: #1e293b !important; }
.stTabs [data-baseweb="tab"] { color: #94a3b8 !important; }
.stTabs [aria-selected="true"] { color: #60a5fa !important; border-bottom-color: #60a5fa !important; }
.stExpander { background: #1e293b !important; border-color: #334155 !important; }
.streamlit-expanderHeader { color: #e2e8f0 !important; }
div[data-testid="stTable"] table { background: #1e293b !important; color: #e2e8f0 !important; }
div[data-testid="stTable"] th { background: #0f172a !important; color: #94a3b8 !important; }
div[data-testid="stTable"] td { color: #e2e8f0 !important; border-color: #334155 !important; }
[data-testid="stAlert"] { background: #1e293b !important; }
[data-testid="stInfo"] { background: #172554 !important; color: #93c5fd !important; }
[data-testid="stSuccess"] { background: #052e16 !important; color: #86efac !important; }
[data-testid="stWarning"] { background: #1c1917 !important; color: #fcd34d !important; }
[data-testid="stError"] { background: #450a0a !important; color: #fca5a5 !important; }
.stRadio label, .stCheckbox label, .stToggle label { color: #e2e8f0 !important; }
.stSlider [data-testid="stSlider"] * { color: #e2e8f0 !important; }
</style>"""
    else:
        return """
<style>
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
[data-testid="metric-container"] {
    background: #f8f9fa; border: 1px solid #e9ecef;
    border-radius: 10px; padding: 12px 16px;
}
section[data-testid="stSidebar"] { background: #f0f4f8; }
.stDownloadButton > button {
    background: #185FA5 !important; color: white !important;
    border-radius: 8px !important; border: none !important;
    font-weight: 500 !important;
}
</style>"""

st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

st.markdown("""
<style>
.score-pill { display:inline-block; padding:3px 13px; border-radius:99px; font-size:12px; font-weight:600; }
.score-high { background:#d1fae5; color:#065f46; }
.score-mid  { background:#fef3c7; color:#92400e; }
.score-low  { background:#fee2e2; color:#991b1b; }
.skill-tag  { display:inline-block; background:#e0f2fe; color:#0369a1; border-radius:5px; padding:2px 9px; font-size:11px; margin:2px 2px; }
.skill-gap-tag { display:inline-block; background:#fee2e2; color:#991b1b; border-radius:5px; padding:2px 9px; font-size:11px; margin:2px 2px; }
.orbit-footer { margin-top:3rem; padding:18px 0 6px; border-top:1px solid #e2e8f0; text-align:center; font-size:13px; }
.paste-hint { background:#f0f9ff; border-left:4px solid #0ea5e9; border-radius:6px; padding:10px 14px; font-size:13px; color:#0369a1; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def save_to_database(name, skills, experience, raw_text, score, target_role, red_flags):
    if not PSYCOPG2_AVAILABLE:
        return False
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST","localhost"),
            port=os.environ.get("DB_PORT","5432"),
            user=os.environ.get("DB_USER","postgres"),
            password=os.environ.get("DB_PASSWORD"),
            dbname="postgres",
        )
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS enterprise_compliance_resumes (
            id SERIAL PRIMARY KEY, candidate_name VARCHAR(255), skills TEXT[],
            experience_years NUMERIC, raw_text TEXT, talent_score NUMERIC,
            target_designation TEXT, compliance_notes TEXT);""")
        cur.execute("""INSERT INTO enterprise_compliance_resumes
            (candidate_name,skills,experience_years,raw_text,talent_score,target_designation,compliance_notes)
            VALUES (%s,%s,%s,%s,%s,%s,%s);""",
            (name,skills,experience,raw_text,score,target_role,str(red_flags)))
        conn.commit(); cur.close(); conn.close()
        return True
    except: return False


def generate_pdf_report(name, exp, skills, message, score, role, flags, questions,
                        salary_est="N/A", ats_score="N/A", personality="N/A",
                        culture="N/A", summary="", notes=""):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(24,95,165)
        pdf.rect(0,0,210,32,"F")
        pdf.set_text_color(255,255,255)
        pdf.set_font("Helvetica","B",17)
        pdf.set_xy(10,7)
        pdf.cell(0,10,"OrbitCareer AI -- Executive Report", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica","",9)
        pdf.set_xy(10,20)
        pdf.cell(0,6,"Developed by Agha Wafa Abbas  |  Confidential", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0,0,0)
        pdf.set_xy(10,40)
        pdf.set_font("Helvetica","B",13)
        pdf.cell(0,8,f"Candidate: {str(name)}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica","",11)
        pdf.cell(0,7,f"Target Role: {str(role)}  |  Talent Score: {str(score)}/100", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0,7,f"Experience: {str(exp)} Yrs  |  ATS: {str(ats_score)}/100  |  Salary: {str(salary_est)}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0,7,f"Personality: {str(personality)}  |  Culture Fit: {str(culture)}/100", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        if summary:
            pdf.set_font("Helvetica","B",11)
            pdf.set_fill_color(235,241,251)
            pdf.cell(0,7,"Executive Summary", fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica","",10)
            pdf.multi_cell(0,6,str(summary).encode("latin-1","ignore").decode("latin-1"))
            pdf.ln(2)
        if notes:
            pdf.set_font("Helvetica","B",11)
            pdf.set_fill_color(255,249,219)
            pdf.cell(0,7,"Recruiter Notes", fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica","",10)
            pdf.multi_cell(0,6,str(notes).encode("latin-1","ignore").decode("latin-1"))
            pdf.ln(2)
        for heading, body in [
            ("Risk Assessment & Red Flags", str(flags)),
            ("Technical Interview Matrix", str(questions)),
            ("LinkedIn Outreach Draft", str(message)),
        ]:
            pdf.set_font("Helvetica","B",11)
            pdf.set_fill_color(235,241,251)
            pdf.cell(0,7,heading, fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica","",10)
            pdf.multi_cell(0,6,body.encode("latin-1","ignore").decode("latin-1"))
            pdf.ln(2)
        pdf.set_y(-18)
        pdf.set_font("Helvetica","I",8)
        pdf.set_text_color(120,120,120)
        pdf.cell(0,6,"OrbitCareer AI Platform -- Developed by Agha Wafa Abbas -- Confidential",align="C")
        return bytes(pdf.output())
    except: return b""


def render_skill_tags(skills, gap_skills=None):
    html = "".join(f'<span class="skill-tag">{s}</span>' for s in skills)
    if gap_skills:
        html += "".join(f'<span class="skill-gap-tag">&#9888; {s}</span>' for s in gap_skills)
    return html


def call_groq(client, prompt, json_mode=False, temperature=0.0):
    kwargs = dict(
        messages=[{"role":"user","content":prompt}],
        model="llama-3.1-8b-instant",
        temperature=temperature,
    )
    if json_mode:
        kwargs["response_format"] = {"type":"json_object"}
    res = client.chat.completions.create(**kwargs)
    return res.choices[0].message.content.strip()


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Theme toggle
    dark_label = "Switch to Light Mode" if st.session_state.dark_mode else "Switch to Dark Mode"
    dark_icon  = "☀️" if st.session_state.dark_mode else "🌙"
    if st.button(f"{dark_icon}  {dark_label}", use_container_width=True, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown("---")
    st.markdown("### ⚙️ Configuration")

    st.markdown("**Role Mapping**")
    role_mode = st.radio(
        "Detection Mode:",
        ["Auto-Scan (AI Mode)", "Manual Override"],
        key="role_mode",
        label_visibility="collapsed",
    )
    manual_role_input = ""
    if role_mode == "Manual Override":
        manual_role_input = st.text_input(
            "Target Role:", value="Senior ML Engineer", placeholder="e.g. Data Scientist"
        )

    st.markdown("---")
    st.markdown("**Feature Toggles**")
    enable_ats         = st.toggle("ATS Score Simulator",    value=True)
    enable_salary      = st.toggle("Salary Estimator",       value=True)
    enable_gap         = st.toggle("Skill Gap Analysis",     value=True)
    enable_compare     = st.toggle("Candidate Comparison",   value=True)
    enable_personality = st.toggle("Personality Profiling",  value=True)
    enable_culture     = st.toggle("Culture Fit Score",      value=True)
    enable_summary     = st.toggle("Executive Summary",      value=True)
    enable_notes       = st.toggle("Recruiter Notes",        value=True)
    enable_shortlist   = st.toggle("Shortlist Manager",      value=True)
    enable_email       = st.toggle("Email Draft",            value=True)
    enable_db          = st.toggle("Save to Database",       value=False)

    st.markdown("---")
    st.markdown("**Filter Candidates**")
    min_score_filter = st.slider("Min Talent Score", 0, 100, 0)
    exp_filter       = st.slider("Min Experience (yrs)", 0, 20, 0)

    if enable_shortlist and st.session_state.shortlisted:
        st.markdown("---")
        st.markdown("**Shortlisted Candidates**")
        for nm in st.session_state.shortlisted:
            st.markdown(f"• {nm}")
        if st.button("Clear Shortlist", use_container_width=True):
            st.session_state.shortlisted = []
            st.rerun()

    st.markdown("---")
    st.caption("OrbitCareer AI v2.1  |  Developed by Agha Wafa Abbas")


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("# 💼 OrbitCareer AI — Global Autonomous Career Agent")
st.caption("PRODUCTION BULK CONTEXT STREAM ENGINE · v2.1 Pro")
st.markdown("---")

# ── HOW IT WORKS ──────────────────────────────────────────────────────────────
with st.expander("ℹ️ How to use this platform — click to expand"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
**📁 Bulk Resume Upload mode:**
- Upload up to **50 PDF/DOCX** files at once
- Each file is parsed, scored and analysed automatically
- Practical sweet spot: **10–15 resumes per batch** (Groq rate limits)
- Supports multi-page PDFs and formatted Word documents
        """)
    with col2:
        st.markdown("""
**✍️ Paste Single Raw Text mode — what to paste:**
- LinkedIn profile text (copy from browser)
- Plain text version of a resume
- A bio or "About Me" section
- Any free-form career narrative
- Job description text (for role analysis)
- Multiple sections pasted together work fine
        """)

st.markdown("---")

# ── UPLOAD ZONE ───────────────────────────────────────────────────────────────
st.markdown("### 📥 Recruiter Inbound Upload Zone")
input_mode = st.radio(
    "Choose Sourcing Method:",
    ["📁 Bulk Resume Upload (PDF / WORD Mode)", "✍ Paste Single Raw Text (Sourcing Mode)"],
    key="input_mode_main", horizontal=True,
)

source_documents = []

if input_mode == "✍ Paste Single Raw Text (Sourcing Mode)":
    st.markdown("""
<div class="paste-hint">
<strong>💡 What to paste here:</strong> LinkedIn profile · Plain-text resume · Bio / About Me · Career summary · Any professional narrative<br>
<strong>Tip:</strong> The more detail you paste, the better the AI analysis will be.
</div>
""", unsafe_allow_html=True)
    single_text = st.text_area(
        "Paste candidate profile text below:",
        height=220,
        placeholder="""Paste any of the following:
• LinkedIn profile (copy full page text from browser)
• Plain text resume content
• Bio or career summary
• About Me section
• Professional narrative

Example:
John Smith — Senior Software Engineer
5 years experience in Python, Django, AWS...
Led team of 8 engineers, delivered 3 production ML systems...""",
        key="single_text_main",
    )
    if single_text.strip():
        source_documents.append(("Manual_Input.txt", single_text))
        st.success(f"✅ Text loaded — {len(single_text):,} characters ready for analysis.")
else:
    uploaded_files = st.file_uploader(
        "Drop Candidate Resumes (PDF / DOCX) Here — up to 50 files:",
        type=["pdf","docx"],
        accept_multiple_files=True,
        key="bulk_drop_main",
    )
    if uploaded_files:
        st.info(f"📄 {len(uploaded_files)} file(s) loaded. Maximum recommended: 15 per batch for best speed.")
        for file_asset in uploaded_files:
            file_text = ""
            try:
                if file_asset.name.endswith(".pdf"):
                    reader = PdfReader(file_asset)
                    for page in reader.pages:
                        t = page.extract_text()
                        if t: file_text += t + "\n"
                elif file_asset.name.endswith(".docx"):
                    doc = docx.Document(file_asset)
                    for para in doc.paragraphs:
                        if para.text: file_text += para.text + "\n"
                if file_text.strip():
                    source_documents.append((file_asset.name, file_text))
            except Exception as fe:
                st.error(f"Error reading {file_asset.name}: {str(fe)}")

st.markdown("---")

# ── SEARCH + LAUNCH ───────────────────────────────────────────────────────────
col_s, col_b = st.columns([4,1])
with col_s:
    search_term = st.text_input("🔍 Search by name or skill:", placeholder="e.g. Python, ML Engineer, Sara...")
with col_b:
    st.markdown("<div style='margin-top:28px'>", unsafe_allow_html=True)
    execute_workflow = st.button("🚀 Launch Pipeline", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📊 Automation Telemetry Hub")

# ── MAIN EXECUTION ────────────────────────────────────────────────────────────
if execute_workflow:
    if not source_documents:
        st.error("❌ No source documents found. Upload resumes or paste text first.")
    else:
        progress_bar       = st.progress(0)
        status_text        = st.empty()
        final_output_cards = []
        final_table_matrix = []

        try:
            groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

            for index, (filename, doc_content) in enumerate(source_documents):
                status_text.text(f"⚙️ Processing [{index+1}/{len(source_documents)}]: {filename}")
                if len(doc_content) > 3500:
                    doc_content = doc_content[:3500]

                # Role detection
                assigned_target_role = manual_role_input
                if role_mode == "Auto-Scan (AI Mode)":
                    assigned_target_role = call_groq(groq_client,
                        f"Return ONLY a standard professional job title for this resume. No extra text.\nResume: {doc_content}")

                # Core parse
                js = json.loads(call_groq(groq_client, f"""
Analyze the resume and return ONLY strict JSON (no markdown, no backticks).
Required keys:
- "name": string
- "skills": list of strings
- "experience_years": float
- "talent_score": int 0-100 (fit vs {assigned_target_role})
- "red_flags": string
- "interview_questions": string (5 numbered questions)
- "missing_skills": list of strings (skills needed for {assigned_target_role} but absent)
Resume text: {doc_content}
""", json_mode=True))

                name         = js.get("name",               f"Candidate {index+1}")
                skills       = js.get("skills",             [])
                exp          = js.get("experience_years",   0.0)
                score        = js.get("talent_score",       75)
                flags        = js.get("red_flags",          "No significant risk flags identified.")
                questions    = js.get("interview_questions","Standard queries recommended.")
                missing_skls = js.get("missing_skills",     [])

                # LinkedIn outreach
                msg = call_groq(groq_client,
                    f"Write a professional LinkedIn recruitment message to {name} for {assigned_target_role}. "
                    f"Skills to highlight: {', '.join(skills[:3])}. Max 80 words. Professional tone.",
                    temperature=0.7)

                # Email draft
                email_draft = ""
                if enable_email:
                    email_draft = call_groq(groq_client,
                        f"Write a professional recruitment EMAIL to {name} for {assigned_target_role}. "
                        f"Include subject line starting with 'Subject:'. Max 150 words. Formal, warm tone. "
                        f"Skills to reference: {', '.join(skills[:3])}.",
                        temperature=0.7)

                # ATS score
                ats_score = "N/A"; ats_tips = ""
                if enable_ats:
                    ats_js = json.loads(call_groq(groq_client,
                        f"Return ONLY JSON with keys 'ats_score'(int 0-100) and 'ats_tips'(str, 3 bullet tips) "
                        f"for this resume vs ATS for {assigned_target_role}.\nResume: {doc_content}", json_mode=True))
                    ats_score = ats_js.get("ats_score","N/A")
                    ats_tips  = ats_js.get("ats_tips","")

                # Salary estimate
                salary_est = "N/A"
                if enable_salary:
                    sal_js = json.loads(call_groq(groq_client,
                        f"Return ONLY JSON with key 'salary_range'(string e.g. '$85k-$110k/yr') "
                        f"for {exp} yrs as {assigned_target_role}. Skills: {', '.join(skills[:4])}", json_mode=True))
                    salary_est = sal_js.get("salary_range","N/A")

                # Personality
                personality_type = "N/A"; personality_desc = ""
                if enable_personality:
                    per_js = json.loads(call_groq(groq_client,
                        f"Return ONLY JSON with keys 'personality_type'(str e.g. 'INTJ - The Architect') "
                        f"and 'personality_desc'(str, 2 sentences about work style).\nResume: {doc_content}",
                        json_mode=True, temperature=0.3))
                    personality_type = per_js.get("personality_type","N/A")
                    personality_desc = per_js.get("personality_desc","")

                # Culture fit
                culture_score = "N/A"; culture_notes = ""
                if enable_culture:
                    cul_js = json.loads(call_groq(groq_client,
                        f"Return ONLY JSON with keys 'culture_score'(int 0-100) and 'culture_notes'(str, 2 sentences) "
                        f"for fast-paced tech startup culture fit.\nResume: {doc_content}", json_mode=True))
                    culture_score = cul_js.get("culture_score","N/A")
                    culture_notes = cul_js.get("culture_notes","")

                # Executive summary
                exec_summary = ""
                if enable_summary:
                    exec_summary = call_groq(groq_client,
                        f"Write a 3-sentence executive recruiter summary for {name} applying as {assigned_target_role}. "
                        f"Strengths, concerns, and hiring recommendation. Professional tone.",
                        temperature=0.5)

                # Hiring recommendation
                hire_js = json.loads(call_groq(groq_client,
                    f"Return ONLY JSON with key 'recommendation'(string: exactly one of "
                    f"'Strong Hire', 'Hire', 'Maybe', 'No Hire') for {name} with score {score}/100 "
                    f"applying as {assigned_target_role}.", json_mode=True))
                recommendation = hire_js.get("recommendation","Maybe")

                if enable_db:
                    save_to_database(name,skills,exp,doc_content,score,assigned_target_role,flags)

                final_table_matrix.append({
                    "Candidate":       name,
                    "Role":            assigned_target_role,
                    "Exp":             f"{exp} yrs",
                    "Talent":          f"{score}/100",
                    "ATS":             f"{ats_score}/100" if enable_ats else "—",
                    "Culture":         f"{culture_score}/100" if enable_culture else "—",
                    "Salary":          salary_est if enable_salary else "—",
                    "Recommendation":  recommendation,
                })

                final_output_cards.append({
                    "name":name, "score":score, "flags":flags,
                    "questions":questions, "skills":skills, "msg":msg,
                    "exp":exp, "role":assigned_target_role, "js":js,
                    "missing":missing_skls, "ats_score":ats_score,
                    "ats_tips":ats_tips, "salary":salary_est,
                    "personality":personality_type, "personality_desc":personality_desc,
                    "culture":culture_score, "culture_notes":culture_notes,
                    "summary":exec_summary, "recommendation":recommendation,
                    "email_draft":email_draft,
                })

                progress_bar.progress((index+1)/len(source_documents))
                time.sleep(0.8)

            status_text.success("✅ All resumes processed successfully!")

            # Metrics
            scores  = [c["score"] for c in final_output_cards]
            top_cnt = sum(1 for s in scores if s >= 85)
            avg_sc  = round(sum(scores)/len(scores)) if scores else 0
            strong  = sum(1 for c in final_output_cards if c["recommendation"]=="Strong Hire")

            m1,m2,m3,m4,m5,m6 = st.columns(6)
            m1.metric("📄 Processed",    len(final_output_cards))
            m2.metric("⭐ Avg Score",     f"{avg_sc}/100")
            m3.metric("🏆 Top (85+)",    top_cnt)
            m4.metric("✅ Strong Hire",  strong)
            m5.metric("🤖 ATS On",       "✅" if enable_ats else "❌")
            m6.metric("🧠 Personality",  "✅" if enable_personality else "❌")

            st.markdown("---")
            st.markdown("### 🏆 Talent Pool Matrix")
            st.table(final_table_matrix)
            st.markdown("---")

            # Filter
            filtered_cards = [
                c for c in final_output_cards
                if c["score"] >= min_score_filter
                and float(c["exp"]) >= exp_filter
                and (not search_term
                     or search_term.lower() in c["name"].lower()
                     or any(search_term.lower() in s.lower() for s in c["skills"]))
            ]

            if not filtered_cards:
                st.info("ℹ️ No candidates match current filters.")

            # ── CANDIDATE CARDS ───────────────────────────────────────────────
            for idx, c in enumerate(filtered_cards):
                s        = c["score"]
                pill_cls = "score-high" if s >= 85 else ("score-mid" if s >= 60 else "score-low")
                rec      = c["recommendation"]
                rec_color = {"Strong Hire":"#065f46","Hire":"#0369a1",
                             "Maybe":"#92400e","No Hire":"#991b1b"}.get(rec,"#64748b")
                rec_bg    = {"Strong Hire":"#d1fae5","Hire":"#e0f2fe",
                             "Maybe":"#fef3c7","No Hire":"#fee2e2"}.get(rec,"#f1f5f9")

                bg_c  = "#1e293b" if st.session_state.dark_mode else "#ffffff"
                brd_c = "#334155" if st.session_state.dark_mode else "#e2e8f0"
                txt_c = "#e2e8f0" if st.session_state.dark_mode else "#1e293b"
                sub_c = "#94a3b8" if st.session_state.dark_mode else "#64748b"

                st.markdown(f"""
<div style="background:{bg_c};border:1px solid {brd_c};border-radius:12px;padding:16px 20px;margin-bottom:8px">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
    <div>
      <span style="font-size:17px;font-weight:600;color:{txt_c}">{c['name']}</span>
      <span style="margin-left:10px;font-size:12px;color:{sub_c}">{c['role']}</span>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
      <span style="background:{rec_bg};color:{rec_color};border-radius:6px;padding:3px 10px;font-size:11px;font-weight:600">{rec}</span>
      <span class="score-pill {pill_cls}">{s}/100</span>
    </div>
  </div>
  <div style="font-size:12px;color:{sub_c};margin-bottom:8px;display:flex;gap:12px;flex-wrap:wrap">
    <span>📅 {c['exp']} yrs</span>
    <span>🤖 ATS: {c['ats_score']}/100</span>
    <span>🏢 Culture: {c['culture']}/100</span>
    <span>🧠 {c['personality']}</span>
    <span>💰 {c['salary']}</span>
  </div>
  <div>{render_skill_tags(c['skills'], c['missing'] if enable_gap else [])}</div>
</div>
""", unsafe_allow_html=True)

                if enable_summary and c["summary"]:
                    st.info(f"📝 **Executive Summary:** {c['summary']}")

                # Shortlist button
                if enable_shortlist:
                    col_sl, col_note = st.columns([1,3])
                    with col_sl:
                        is_shortlisted = c["name"] in st.session_state.shortlisted
                        sl_label = "⭐ Shortlisted" if is_shortlisted else "☆ Shortlist"
                        if st.button(sl_label, key=f"sl_{idx}"):
                            if is_shortlisted:
                                st.session_state.shortlisted.remove(c["name"])
                            else:
                                st.session_state.shortlisted.append(c["name"])
                            st.rerun()

                # Recruiter notes
                if enable_notes:
                    note_key = f"note_{c['name']}"
                    note_val = st.text_area(
                        f"📌 Recruiter notes for {c['name']}:",
                        value=st.session_state.notes.get(note_key,""),
                        height=70,
                        key=f"note_input_{idx}",
                        placeholder="Add your private notes, interview feedback, follow-up reminders..."
                    )
                    if note_val:
                        st.session_state.notes[note_key] = note_val

                # Tabs
                tabs_list = ["🚩 Risk Flags","📋 Interview Qs","💬 LinkedIn","📧 Email",
                             "🤖 ATS Tips","🧠 Personality","🏢 Culture Fit","🔍 Raw JSON"]
                tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs(tabs_list)

                with tab1:
                    st.warning(c["flags"])

                with tab2:
                    st.info(c["questions"])

                with tab3:
                    st.success(c["msg"])
                    st.code(c["msg"], language=None)

                with tab4:
                    if enable_email and c["email_draft"]:
                        lines   = c["email_draft"].split("\n")
                        subject = next((l for l in lines if l.startswith("Subject:")), "Exciting Opportunity")
                        body    = "\n".join(l for l in lines if not l.startswith("Subject:")).strip()
                        st.markdown(f"**{subject}**")
                        st.info(body)
                        st.code(c["email_draft"], language=None)
                    else:
                        st.caption("Email draft not enabled.")

                with tab5:
                    if enable_ats and c["ats_tips"]:
                        st.info(c["ats_tips"])
                    else:
                        st.caption("ATS Simulator not enabled.")

                with tab6:
                    if enable_personality and c["personality"] != "N/A":
                        st.markdown(f"**Personality Type:** {c['personality']}")
                        st.write(c["personality_desc"])
                    else:
                        st.caption("Personality profiling not enabled.")

                with tab7:
                    if enable_culture and c["culture"] != "N/A":
                        try:
                            cs = int(str(c["culture"]).replace("/100",""))
                        except:
                            cs = 0
                        pill = "score-high" if cs >= 75 else ("score-mid" if cs >= 50 else "score-low")
                        st.markdown(f'<span class="score-pill {pill}">{cs}/100</span>', unsafe_allow_html=True)
                        st.write(c["culture_notes"])
                    else:
                        st.caption("Culture fit scoring not enabled.")

                with tab8:
                    st.json(c["js"])

                # PDF download
                note_txt = st.session_state.notes.get(f"note_{c['name']}","")
                pdf_bytes = generate_pdf_report(
                    c["name"],c["exp"],c["skills"],c["msg"],c["score"],c["role"],
                    c["flags"],c["questions"],c["salary"],c["ats_score"],
                    c["personality"],str(c["culture"]),c["summary"],note_txt,
                )
                if pdf_bytes:
                    col_dl,_ = st.columns([2,3])
                    with col_dl:
                        st.download_button(
                            label=f"📄 Download PDF — {c['name']}",
                            data=pdf_bytes,
                            file_name=f"OrbitCareer_{c['name'].replace(' ','_')}.pdf",
                            mime="application/pdf",
                            key=f"pdf_{idx}",
                        )
                st.markdown("---")

            # ── CANDIDATE COMPARISON ──────────────────────────────────────────
            if enable_compare and len(filtered_cards) >= 2:
                st.markdown("### ⚖️ Candidate Comparison Mode")
                names_list = [c["name"] for c in filtered_cards]
                cA = st.selectbox("Candidate A:", names_list, key="cmp_a")
                cB = st.selectbox("Candidate B:", names_list, index=min(1,len(names_list)-1), key="cmp_b")

                c1 = next((c for c in filtered_cards if c["name"]==cA), None)
                c2 = next((c for c in filtered_cards if c["name"]==cB), None)

                if c1 and c2 and cA != cB:
                    bg_cmp = "#1e293b" if st.session_state.dark_mode else "#f8fafc"
                    brd_cmp = "#334155" if st.session_state.dark_mode else "#e2e8f0"
                    colA, colB = st.columns(2)
                    for col, cnd in [(colA,c1),(colB,c2)]:
                        with col:
                            sc = cnd["score"]
                            st.metric(cnd["name"], f"{sc}/100",
                                delta="Strong Hire" if cnd["recommendation"]=="Strong Hire"
                                else cnd["recommendation"])
                            st.markdown(f"**Role:** {cnd['role']}")
                            st.markdown(f"**Experience:** {cnd['exp']} yrs")
                            st.markdown(f"**ATS Score:** {cnd['ats_score']}/100")
                            st.markdown(f"**Culture Fit:** {cnd['culture']}/100")
                            st.markdown(f"**Personality:** {cnd['personality']}")
                            st.markdown(f"**Salary Est.:** {cnd['salary']}")
                            st.markdown("**Skills:**")
                            st.markdown(render_skill_tags(cnd["skills"]), unsafe_allow_html=True)
                            if enable_gap and cnd["missing"]:
                                st.markdown("**Skill Gaps:**")
                                st.markdown(render_skill_tags([],cnd["missing"]), unsafe_allow_html=True)

                st.markdown("---")

            # ── SHORTLIST SUMMARY ─────────────────────────────────────────────
            if enable_shortlist and st.session_state.shortlisted:
                st.markdown("### ⭐ Shortlist Summary")
                shortlisted_cards = [c for c in filtered_cards if c["name"] in st.session_state.shortlisted]
                if shortlisted_cards:
                    sl_table = [{
                        "Name": c["name"], "Role": c["role"],
                        "Score": f"{c['score']}/100", "ATS": f"{c['ats_score']}/100",
                        "Recommendation": c["recommendation"]
                    } for c in shortlisted_cards]
                    st.table(sl_table)
                st.markdown("---")

        except Exception as ex:
            st.error(f"❌ Pipeline Error: {str(ex)}")
            status_text.error("Processing halted. Check your GROQ_API_KEY in .env file.")

else:
    # ── IDLE FEATURE GRID ─────────────────────────────────────────────────────
    st.info("👆 Upload resumes or paste text above, then click **🚀 Launch Pipeline**.")

    st.markdown("### ✨ Platform Features")
    features = [
        ("📄","Bulk PDF/DOCX Upload",       "Up to 50 resumes, processed in one click"),
        ("✍️","Raw Text / LinkedIn Paste",   "Paste LinkedIn, bio, or any career text"),
        ("🤖","AI Role Auto-Detection",      "LLM maps best-fit role automatically"),
        ("🏆","Talent Scoring 0–100",        "Fit score vs target role"),
        ("✅","Hiring Recommendation",       "Strong Hire / Hire / Maybe / No Hire"),
        ("🚩","Red Flag Analysis",           "Instant risk assessment per candidate"),
        ("📋","5 Interview Questions",       "Role-tailored technical questions"),
        ("💬","LinkedIn Outreach Draft",     "Personalised message, ready to send"),
        ("📧","Email Draft",                 "Full recruitment email with subject line"),
        ("⚠️","Skill Gap Analysis",          "Missing competencies in red tags"),
        ("🤖","ATS Score Simulator",         "Resume ATS compatibility + 3 tips"),
        ("💰","Salary Range Estimator",      "Market salary estimate per profile"),
        ("🧠","Personality Profiling",       "MBTI-style work personality type"),
        ("🏢","Culture Fit Score",           "Startup culture alignment score"),
        ("📝","Executive Summary",           "3-sentence recruiter summary"),
        ("📌","Recruiter Notes",             "Private per-candidate notes saved"),
        ("⭐","Shortlist Manager",           "One-click shortlist, sidebar view"),
        ("⚖️","Candidate Comparison",        "Side-by-side 2-candidate eval"),
        ("🌙","Dark / Light Mode",           "Toggle theme from sidebar"),
        ("📄","PDF Executive Reports",       "Branded PDF — all insights included"),
        ("🗄️","Database Export",             "PostgreSQL save toggle"),
    ]

    bg_f  = "#1e293b" if st.session_state.dark_mode else "#f8fafc"
    brd_f = "#334155" if st.session_state.dark_mode else "#e2e8f0"
    txt_f = "#e2e8f0" if st.session_state.dark_mode else "#1e293b"
    sub_f = "#94a3b8" if st.session_state.dark_mode else "#64748b"

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
<div style="background:{bg_f};border:1px solid {brd_f};border-radius:10px;
padding:13px 15px;margin-bottom:9px;min-height:86px">
<div style="font-size:20px;margin-bottom:3px">{icon}</div>
<div style="font-size:13px;font-weight:600;color:{txt_f}">{title}</div>
<div style="font-size:11px;color:{sub_f}">{desc}</div>
</div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
ft_brd = "#334155" if st.session_state.dark_mode else "#e2e8f0"
ft_txt = "#94a3b8" if st.session_state.dark_mode else "#64748b"
ft_str = "#e2e8f0" if st.session_state.dark_mode else "#1e293b"

st.markdown(f"""
<div style="margin-top:3rem;padding:18px 0 6px;border-top:1px solid {ft_brd};
text-align:center;color:{ft_txt};font-size:13px;line-height:2">
<strong style="color:{ft_str}">OrbitCareer AI Platform</strong>
&nbsp;·&nbsp; Global Autonomous Career Agent<br>
Developed by <strong style="color:{ft_str}">Agha Wafa Abbas</strong>
&nbsp;·&nbsp; All rights reserved &copy; 2025<br>
<span style="font-size:11px;color:#64748b">
Powered by Groq LLaMA 3.1 &nbsp;·&nbsp; Built with Streamlit
</span>
</div>
""", unsafe_allow_html=True)
