import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinBridge Credit Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy: #0A1628;
    --navy-mid: #112240;
    --navy-light: #1A3A5C;
    --gold: #C8960C;
    --gold-light: #F0B429;
    --gold-pale: #FFF3CD;
    --teal: #0EC4B0;
    --red-soft: #E05C5C;
    --green-soft: #3EC87A;
    --text-primary: #E8EDF5;
    --text-secondary: #8FA3BF;
    --card-bg: #112240;
    --border: #1E3A5F;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy);
    color: var(--text-primary);
}

.main { background-color: var(--navy); }
.block-container { padding: 2rem 2.5rem 3rem; max-width: 1400px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--navy-mid);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem; }

/* Headings */
h1, h2, h3 { font-family: 'Playfair Display', serif; color: var(--text-primary); }

/* Cards */
.fb-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.fb-card-gold {
    background: linear-gradient(135deg, #1A3A5C 0%, #0A1628 100%);
    border: 1px solid var(--gold);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* Score display */
.score-hero {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, var(--navy-mid) 0%, var(--navy-light) 100%);
    border-radius: 16px;
    border: 2px solid var(--gold);
}
.score-num {
    font-family: 'Playfair Display', serif;
    font-size: 5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--gold-light), var(--teal));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.score-label { font-size: 1rem; color: var(--text-secondary); margin-top: 0.5rem; }

/* Metric cards */
.metric-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem;
    text-align: center;
}
.metric-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 600;
    color: var(--gold-light);
}
.metric-lab { font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.2rem; }

/* Badge */
.badge {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-green { background: rgba(62,200,122,0.15); color: var(--green-soft); border: 1px solid var(--green-soft); }
.badge-gold  { background: rgba(240,180,41,0.15);  color: var(--gold-light);  border: 1px solid var(--gold-light); }
.badge-red   { background: rgba(224,92,92,0.15);   color: var(--red-soft);    border: 1px solid var(--red-soft); }

/* Section titles */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    color: var(--gold-light);
    border-left: 4px solid var(--gold);
    padding-left: 1rem;
    margin-bottom: 1.5rem;
}
.sub-title { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1.5rem; }

/* Comparison table */
.comp-row { display: flex; gap: 1rem; margin-bottom: 0.8rem; }
.comp-cell {
    flex: 1;
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}
.comp-cell.highlight { border-color: var(--gold); background: linear-gradient(135deg, #1A3A5C,#0A1628); }

/* Inputs */
.stNumberInput input, .stTextInput input, .stSelectbox select {
    background: var(--navy-light) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
.stSlider { accent-color: var(--gold); }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--gold), #A07009);
    color: var(--navy);
    font-weight: 600;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 2rem;
    font-family: 'DM Sans', sans-serif;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88; }

/* Divider */
.fb-divider { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }

/* Info banner */
.info-banner {
    background: rgba(14,196,176,0.08);
    border: 1px solid var(--teal);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: var(--teal);
    font-size: 0.88rem;
    margin-bottom: 1rem;
}

/* Progress bar override */
.stProgress > div > div > div { background: linear-gradient(90deg, var(--gold), var(--teal)); }

/* Expander */
.streamlit-expanderHeader {
    background: var(--card-bg) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] { background: var(--navy-mid); border-radius: 10px; padding: 0.3rem; }
.stTabs [data-baseweb="tab"] { color: var(--text-secondary); border-radius: 8px; }
.stTabs [aria-selected="true"] { background: var(--gold) !important; color: var(--navy) !important; font-weight: 600; }

/* Logo area */
.logo-area { text-align: center; padding: 1.5rem 0 1rem; }
.logo-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--gold-light), var(--teal));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.logo-sub { font-size: 0.7rem; color: var(--text-secondary); letter-spacing: 0.15em; text-transform: uppercase; }

/* Alerts */
[data-testid="stAlert"] { border-radius: 10px; }

/* Select boxes - label color */
label { color: var(--text-secondary) !important; font-size: 0.85rem !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--navy-light); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
PROFILE_TYPES = ["Student", "Freelancer", "Salaried Professional", "Self-Employed / Business"]

LOAN_PURPOSES = {
    "🏠 Home Purchase / Construction": {"rate_range": (8.5, 10.5), "max_tenure": 30, "industry": "Real Estate / Housing Finance"},
    "🚗 Vehicle Purchase (Car / Two-Wheeler)": {"rate_range": (7.5, 12.0), "max_tenure": 7, "industry": "Auto Finance"},
    "🎓 Education Loan": {"rate_range": (8.0, 13.5), "max_tenure": 15, "industry": "Education Finance"},
    "💼 Business Expansion / Working Capital": {"rate_range": (10.5, 16.0), "max_tenure": 10, "industry": "MSME / Business Finance"},
    "🏥 Medical Emergency": {"rate_range": (11.0, 14.5), "max_tenure": 5, "industry": "Healthcare Finance"},
    "⚙️ Equipment / Machinery Purchase": {"rate_range": (10.0, 15.0), "max_tenure": 7, "industry": "Asset Finance"},
    "🌏 Travel / Lifestyle": {"rate_range": (13.0, 18.0), "max_tenure": 3, "industry": "Personal Finance"},
    "🔄 Debt Consolidation": {"rate_range": (12.0, 16.5), "max_tenure": 5, "industry": "Refinancing"},
    "🏗️ Renovation / Home Improvement": {"rate_range": (9.5, 13.0), "max_tenure": 10, "industry": "Home Improvement Finance"},
    "💡 Start-Up / New Venture": {"rate_range": (12.0, 18.0), "max_tenure": 7, "industry": "Venture / Start-Up Finance"},
}

SCORE_BANDS = {
    (750, 900): ("Excellent", "badge-green", "#3EC87A"),
    (700, 749): ("Good", "badge-green", "#7CC87E"),
    (650, 699): ("Fair", "badge-gold", "#F0B429"),
    (600, 649): ("Marginal", "badge-gold", "#E08929"),
    (300, 599): ("Poor", "badge-red", "#E05C5C"),
}

# ─── HELPER FUNCTIONS ────────────────────────────────────────────────────────
def get_score_band(score):
    for (lo, hi), (label, badge, color) in SCORE_BANDS.items():
        if lo <= score <= hi:
            return label, badge, color
    return "Poor", "badge-red", "#E05C5C"

def calc_emi(principal, annual_rate, months):
    if annual_rate == 0 or months == 0:
        return principal / months if months > 0 else 0
    r = annual_rate / (12 * 100)
    emi = principal * r * ((1 + r) ** months) / (((1 + r) ** months) - 1)
    return round(emi, 2)

def compute_finbridge_score(data):
    """
    FinBridge proprietary scoring — 6 weighted dimensions:
      1. Income Stability & Growth        25%
      2. Cash-Flow Consistency            20%
      3. Savings Behaviour                18%
      4. Debt Service Coverage            17%
      5. Expenditure Discipline           12%
      6. Account Vintage & Tenure         8%
    Score mapped to 300–900 range.
    """
    profile = data.get("profile_type", "Salaried Professional")
    years = len(data.get("annual_income", []))

    incomes = np.array(data.get("annual_income", [1]), dtype=float)
    expenses = np.array(data.get("annual_expense", [0.8]), dtype=float)
    savings = np.array(data.get("annual_savings", [0.2]), dtype=float)
    emis = np.array(data.get("existing_emis", [0]), dtype=float)
    bounces = np.array(data.get("bounce_count", [0]), dtype=float)

    # Replace zeros to avoid division issues
    incomes = np.where(incomes == 0, 1, incomes)

    # ── 1. Income Stability & Growth (25 pts max)
    income_growth_rates = np.diff(incomes) / incomes[:-1] if len(incomes) > 1 else np.array([0.0])
    avg_growth = float(np.mean(income_growth_rates))
    income_cov = float(np.std(incomes) / np.mean(incomes)) if np.mean(incomes) > 0 else 1
    income_score = max(0, min(25, 25 * (0.5 * (1 - income_cov) + 0.5 * min(avg_growth / 0.15, 1))))

    # ── 2. Cash-Flow Consistency (20 pts max)
    net_flows = incomes - expenses - emis
    cf_positive_ratio = float(np.sum(net_flows > 0) / len(net_flows))
    cf_cov = float(np.std(net_flows) / (np.mean(incomes) + 1e-6))
    cf_score = max(0, min(20, 20 * (0.6 * cf_positive_ratio + 0.4 * max(0, 1 - cf_cov))))

    # ── 3. Savings Behaviour (18 pts max)
    savings_ratios = savings / incomes
    avg_savings_ratio = float(np.mean(savings_ratios))
    savings_score = max(0, min(18, 18 * min(avg_savings_ratio / 0.25, 1)))

    # ── 4. Debt Service Coverage (17 pts max)
    dscr_vals = incomes / (emis + 1)  # avoid zero
    avg_dscr = float(np.mean(dscr_vals))
    dscr_score = max(0, min(17, 17 * min((avg_dscr - 1) / 4, 1)))

    # ── 5. Expenditure Discipline (12 pts max)
    exp_ratios = expenses / incomes
    avg_exp_ratio = float(np.mean(exp_ratios))
    exp_score = max(0, min(12, 12 * max(0, 1 - avg_exp_ratio / 0.85)))

    # ── 6. Bounce/Account behaviour (8 pts max)
    total_bounces = float(np.sum(bounces))
    bounce_score = max(0, min(8, 8 * max(0, 1 - total_bounces / 10)))

    raw = income_score + cf_score + savings_score + dscr_score + exp_score + bounce_score
    # Map 0–100 → 300–900
    finbridge_score = int(300 + (raw / 100) * 600)
    finbridge_score = max(300, min(900, finbridge_score))

    components = {
        "Income Stability": round(income_score, 1),
        "Cash-Flow": round(cf_score, 1),
        "Savings Behaviour": round(savings_score, 1),
        "Debt Coverage": round(dscr_score, 1),
        "Expenditure Discipline": round(exp_score, 1),
        "Account Behaviour": round(bounce_score, 1),
    }
    return finbridge_score, components, raw

def estimate_cibil_score(data):
    """
    Simplified traditional CIBIL-like score based on same inputs.
    Primarily depends on: payment history, utilization, credit history length.
    Returns a score that is typically LESS accurate for non-salaried profiles.
    """
    incomes = np.array(data.get("annual_income", [1]), dtype=float)
    emis = np.array(data.get("existing_emis", [0]), dtype=float)
    bounces = np.array(data.get("bounce_count", [0]), dtype=float)
    avg_income = float(np.mean(incomes))
    avg_emi = float(np.mean(emis))

    # CIBIL heavily penalises any bounce
    bounce_penalty = min(float(np.sum(bounces)) * 30, 200)
    # Payment-to-income ratio
    pti = avg_emi / (avg_income + 1e-6)
    pti_score = max(0, 350 * (1 - min(pti, 0.6) / 0.6))
    cibil = int(550 + pti_score - bounce_penalty)
    cibil = max(300, min(900, cibil))
    return cibil

def max_loan_eligible(data, interest_rate, tenure_months):
    """Compute max loan based on average net monthly surplus and FOIR norms."""
    incomes = np.array(data.get("annual_income", [1]), dtype=float)
    expenses = np.array(data.get("annual_expense", [0.8]), dtype=float)
    emis = np.array(data.get("existing_emis", [0]), dtype=float)
    monthly_income = float(np.mean(incomes)) / 12
    monthly_expense = float(np.mean(expenses)) / 12
    existing_emi = float(np.mean(emis)) / 12
    # FOIR (Fixed Obligation to Income Ratio) — banks allow up to 50–65%
    foir_limit = 0.55
    disposable = monthly_income * foir_limit - existing_emi
    disposable = max(disposable, 0)
    if interest_rate == 0 or tenure_months == 0:
        return disposable * tenure_months, disposable
    r = interest_rate / (12 * 100)
    # Reverse EMI formula: P = EMI * [(1+r)^n - 1] / [r * (1+r)^n]
    max_loan = disposable * ((1 + r) ** tenure_months - 1) / (r * (1 + r) ** tenure_months)
    return round(max_loan, 0), round(disposable, 0)

def format_inr(amount):
    if amount >= 1e7:
        return f"₹{amount/1e7:.2f} Cr"
    elif amount >= 1e5:
        return f"₹{amount/1e5:.2f} L"
    else:
        return f"₹{amount:,.0f}"

def months_to_label(months):
    if months >= 12:
        y = months // 12
        m = months % 12
        return f"{y}Y {m}M" if m else f"{y} Years"
    return f"{months} Months"

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = "profile"
if "profile_data" not in st.session_state:
    st.session_state.profile_data = {}
if "stmt_data" not in st.session_state:
    st.session_state.stmt_data = {}
if "scores_computed" not in st.session_state:
    st.session_state.scores_computed = False
if "finbridge_score" not in st.session_state:
    st.session_state.finbridge_score = 0
if "cibil_score" not in st.session_state:
    st.session_state.cibil_score = 0
if "components" not in st.session_state:
    st.session_state.components = {}
if "raw_score" not in st.session_state:
    st.session_state.raw_score = 0

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-area">
        <div class="logo-text">FinBridge</div>
        <div class="logo-sub">Credit Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F;margin:0.5rem 0 1rem;'>", unsafe_allow_html=True)

    nav_options = [
        ("👤", "Profile Setup", "profile"),
        ("📊", "Bank Statement Input", "statement"),
        ("🏅", "FinBridge Score", "score"),
        ("⚖️", "CIBIL vs FinBridge", "comparison"),
        ("💰", "Loan Purpose & Eligibility", "loan"),
        ("📅", "EMI Planner", "emi"),
        ("📋", "Credit Report", "report"),
    ]

    for icon, label, key in nav_options:
        is_active = st.session_state.step == key
        btn_style = "background:linear-gradient(90deg,#1A3A5C,#112240);border-left:3px solid #F0B429;" if is_active else "background:transparent;"
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.step = key
            st.rerun()

    st.markdown("<hr style='border-color:#1E3A5F;margin:1rem 0;'>", unsafe_allow_html=True)

    if st.session_state.scores_computed:
        fb = st.session_state.finbridge_score
        label, badge, color = get_score_band(fb)
        st.markdown(f"""
        <div style='text-align:center;padding:1rem;background:#112240;border-radius:10px;border:1px solid #1E3A5F;'>
            <div style='font-size:0.7rem;color:#8FA3BF;letter-spacing:0.1em;text-transform:uppercase;'>FinBridge Score</div>
            <div style='font-family:"Playfair Display",serif;font-size:2.5rem;font-weight:700;color:#F0B429;'>{fb}</div>
            <span class='badge {badge}'>{label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='position:absolute;bottom:2rem;left:1rem;right:1rem;text-align:center;'>
        <div style='font-size:0.65rem;color:#4A6080;'>FinBridge © 2025 | Credit Intelligence<br>Not a Registered Credit Bureau</div>
    </div>
    """, unsafe_allow_html=True)

# ─── PAGE: PROFILE SETUP ─────────────────────────────────────────────────────
if st.session_state.step == "profile":
    st.markdown("<div class='section-title'>👤 Applicant Profile Setup</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Tell us about yourself so we can tailor the analysis. The statement period required varies by profile type.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
        st.markdown("**Personal Information**")
        name = st.text_input("Full Name", value=st.session_state.profile_data.get("name", ""), placeholder="e.g. Arjun Mehta")
        age = st.number_input("Age", min_value=18, max_value=80, value=st.session_state.profile_data.get("age", 28), step=1)
        profile_type = st.selectbox(
            "Profile Type",
            PROFILE_TYPES,
            index=PROFILE_TYPES.index(st.session_state.profile_data.get("profile_type", "Salaried Professional"))
        )
        occupation = st.text_input("Occupation / Industry", value=st.session_state.profile_data.get("occupation", ""), placeholder="e.g. Software Engineer, Restaurant Owner")
        city = st.text_input("City of Residence", value=st.session_state.profile_data.get("city", ""), placeholder="e.g. Mumbai")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
        st.markdown("**Financial Profile**")
        pan = st.text_input("PAN Number (optional, for reference)", value=st.session_state.profile_data.get("pan", ""), placeholder="ABCDE1234F", max_chars=10)
        credit_cards = st.number_input("Number of Active Credit Cards", min_value=0, max_value=20, value=st.session_state.profile_data.get("credit_cards", 1))
        loans_active = st.number_input("Number of Active Loans", min_value=0, max_value=10, value=st.session_state.profile_data.get("loans_active", 0))
        has_collateral = st.selectbox("Do you have collateral to offer?", ["No", "Yes – Property", "Yes – FD/Savings", "Yes – Gold", "Yes – Vehicle"], index=st.session_state.profile_data.get("collateral_idx", 0))
        employment_years = st.slider("Years in Current Occupation", 0, 40, value=st.session_state.profile_data.get("employment_years", 3))
        st.markdown("</div>", unsafe_allow_html=True)

    # Statement period info
    is_student_fl = profile_type in ["Student", "Freelancer"]
    stmt_years = 3 if is_student_fl else 5

    st.markdown(f"""
    <div class='info-banner'>
        📌 Based on your profile type <strong>({profile_type})</strong>, you are required to provide
        <strong>{stmt_years} years</strong> of bank statement data.
        {'Students and Freelancers: 3-year statement required.' if is_student_fl else 'Business / Salaried: 5-year statement required.'}
    </div>
    """, unsafe_allow_html=True)

    if st.button("Save Profile & Continue →", use_container_width=True):
        if not name.strip():
            st.error("Please enter your full name.")
        else:
            st.session_state.profile_data = {
                "name": name.strip(),
                "age": age,
                "profile_type": profile_type,
                "occupation": occupation,
                "city": city,
                "pan": pan.upper(),
                "credit_cards": credit_cards,
                "loans_active": loans_active,
                "has_collateral": has_collateral,
                "collateral_idx": ["No", "Yes – Property", "Yes – FD/Savings", "Yes – Gold", "Yes – Vehicle"].index(has_collateral),
                "employment_years": employment_years,
                "stmt_years": stmt_years,
            }
            st.session_state.step = "statement"
            st.success("Profile saved! Proceeding to bank statement input.")
            st.rerun()

# ─── PAGE: BANK STATEMENT INPUT ──────────────────────────────────────────────
elif st.session_state.step == "statement":
    prof = st.session_state.profile_data
    stmt_years = prof.get("stmt_years", 5)
    profile_type = prof.get("profile_type", "Salaried Professional")

    st.markdown("<div class='section-title'>📊 Bank Statement Data Input</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-title'>Enter your annual financial figures for the past {stmt_years} years. All amounts in Indian Rupees (₹).</div>", unsafe_allow_html=True)

    current_year = 2025
    years = [current_year - i for i in range(stmt_years - 1, -1, -1)]

    # Load existing data
    saved = st.session_state.stmt_data
    default_income    = saved.get("annual_income",    [0.0] * stmt_years)
    default_expense   = saved.get("annual_expense",   [0.0] * stmt_years)
    default_savings   = saved.get("annual_savings",   [0.0] * stmt_years)
    default_emis      = saved.get("existing_emis",    [0.0] * stmt_years)
    default_credits   = saved.get("credit_txn_count", [0]   * stmt_years)
    default_debits    = saved.get("debit_txn_count",  [0]   * stmt_years)
    default_bounces   = saved.get("bounce_count",     [0]   * stmt_years)
    default_od        = saved.get("overdraft_count",  [0]   * stmt_years)
    default_cash_in   = saved.get("cash_deposits",    [0.0] * stmt_years)

    # Pad defaults to stmt_years if needed
    def pad(lst, n, default=0.0):
        return (lst + [default] * n)[:n]

    default_income  = pad(default_income,  stmt_years)
    default_expense = pad(default_expense, stmt_years)
    default_savings = pad(default_savings, stmt_years)
    default_emis    = pad(default_emis,    stmt_years)
    default_credits = pad(default_credits, stmt_years, 0)
    default_debits  = pad(default_debits,  stmt_years, 0)
    default_bounces = pad(default_bounces, stmt_years, 0)
    default_od      = pad(default_od,      stmt_years, 0)
    default_cash_in = pad(default_cash_in, stmt_years)

    tabs = st.tabs([f"FY {y}-{str(y+1)[2:]}" for y in years])

    income_vals    = []
    expense_vals   = []
    savings_vals   = []
    emi_vals       = []
    credit_counts  = []
    debit_counts   = []
    bounce_counts  = []
    od_counts      = []
    cash_dep_vals  = []

    for i, (tab, year) in enumerate(zip(tabs, years)):
        with tab:
            c1, c2, c3 = st.columns(3, gap="medium")
            with c1:
                inc = st.number_input(f"Total Annual Income (₹)", min_value=0.0, value=float(default_income[i]),
                                      step=10000.0, key=f"inc_{year}", format="%.0f",
                                      help="Total salary, business revenue, freelance income received in this year")
                exp = st.number_input(f"Total Annual Expenses (₹)", min_value=0.0, value=float(default_expense[i]),
                                      step=10000.0, key=f"exp_{year}", format="%.0f",
                                      help="All outflows including rent, utilities, personal spending")
                sav = st.number_input(f"Net Savings / FD Created (₹)", min_value=0.0, value=float(default_savings[i]),
                                      step=5000.0, key=f"sav_{year}", format="%.0f",
                                      help="Money saved, invested, or put into FD/mutual funds")
            with c2:
                emi = st.number_input(f"Existing EMI Payments (₹/yr)", min_value=0.0, value=float(default_emis[i]),
                                      step=5000.0, key=f"emi_{year}", format="%.0f",
                                      help="Annual total of all loan EMI payments made")
                cash = st.number_input(f"Cash Deposits (₹)", min_value=0.0, value=float(default_cash_in[i]),
                                       step=5000.0, key=f"cash_{year}", format="%.0f",
                                       help="Total cash deposited into bank account this year")
                cred = st.number_input(f"No. of Credit Transactions", min_value=0, value=int(default_credits[i]),
                                       step=1, key=f"cred_{year}",
                                       help="Number of inward/credit transactions in the year")
            with c3:
                deb = st.number_input(f"No. of Debit Transactions", min_value=0, value=int(default_debits[i]),
                                      step=1, key=f"deb_{year}",
                                      help="Number of outward/debit transactions in the year")
                bnc = st.number_input(f"Cheque / ECS Bounces", min_value=0, value=int(default_bounces[i]),
                                      step=1, key=f"bnc_{year}",
                                      help="Number of bounced cheques or failed ECS debits")
                od = st.number_input(f"Overdraft / Negative Balance Days", min_value=0, value=int(default_od[i]),
                                     step=1, key=f"od_{year}",
                                     help="Number of days account went into overdraft or negative balance")

            # Auto-calc helper
            calc_sav = inc - exp - emi
            if inc > 0:
                st.markdown(f"""
                <div style='background:#0A1628;border:1px solid #1E3A5F;border-radius:8px;padding:0.8rem;margin-top:0.5rem;font-size:0.83rem;color:#8FA3BF;'>
                    📌 <b>FY {year} Summary:</b> &nbsp;
                    Income ₹{inc:,.0f} &nbsp;|&nbsp;
                    Expenses ₹{exp:,.0f} &nbsp;|&nbsp;
                    EMIs ₹{emi:,.0f} &nbsp;|&nbsp;
                    Net Cash ₹{calc_sav:,.0f} &nbsp;|&nbsp;
                    Savings Rate <b>{(sav/inc*100) if inc>0 else 0:.1f}%</b>
                </div>
                """, unsafe_allow_html=True)

            income_vals.append(inc)
            expense_vals.append(exp)
            savings_vals.append(sav)
            emi_vals.append(emi)
            credit_counts.append(cred)
            debit_counts.append(deb)
            bounce_counts.append(bnc)
            od_counts.append(od)
            cash_dep_vals.append(cash)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("**Additional Context**")
        has_gst = st.selectbox("GST Registered Business?", ["No", "Yes"], index=0 if profile_type not in ["Self-Employed / Business"] else 1)
        itr_filed = st.selectbox("ITR Filed Regularly?", ["Yes, all years", "Most years", "Occasionally", "No"], index=0)
        bank_count = st.number_input("Number of Bank Accounts", min_value=1, max_value=10, value=1)
    with col_b:
        st.markdown("**Credit History**")
        prev_defaults = st.selectbox("Any Previous Loan Default?", ["No", "Yes – resolved", "Yes – pending"], index=0)
        credit_card_util = st.slider("Average Credit Card Utilisation (%)", 0, 100, 30,
                                     help="Average % of credit card limit used. Lower is better.")
        oldest_account_yr = st.number_input("Age of Oldest Bank Account (Years)", min_value=0, max_value=50, value=5)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    if st.button("🔍 Compute FinBridge Credit Score", use_container_width=True):
        if sum(income_vals) == 0:
            st.error("Please enter income data for at least one year.")
        else:
            st.session_state.stmt_data = {
                "years": years,
                "annual_income": income_vals,
                "annual_expense": expense_vals,
                "annual_savings": savings_vals,
                "existing_emis": emi_vals,
                "credit_txn_count": credit_counts,
                "debit_txn_count": debit_counts,
                "bounce_count": bounce_counts,
                "overdraft_count": od_counts,
                "cash_deposits": cash_dep_vals,
                "has_gst": has_gst,
                "itr_filed": itr_filed,
                "bank_count": bank_count,
                "prev_defaults": prev_defaults,
                "credit_card_util": credit_card_util,
                "oldest_account_yr": oldest_account_yr,
            }

            score, comps, raw = compute_finbridge_score(st.session_state.stmt_data)
            cibil = estimate_cibil_score(st.session_state.stmt_data)

            # Adjust for ITR, defaults, credit util
            if itr_filed == "Yes, all years":
                score = min(900, score + 15)
            elif itr_filed == "Occasionally":
                score = max(300, score - 20)
            elif itr_filed == "No":
                score = max(300, score - 40)

            if prev_defaults == "Yes – pending":
                score = max(300, score - 80)
                cibil = max(300, cibil - 100)
            elif prev_defaults == "Yes – resolved":
                score = max(300, score - 30)
                cibil = max(300, cibil - 50)

            if credit_card_util > 75:
                score = max(300, score - 25)
                cibil = max(300, cibil - 30)
            elif credit_card_util < 30:
                score = min(900, score + 10)
                cibil = min(900, cibil + 15)

            if oldest_account_yr >= 10:
                score = min(900, score + 15)
                cibil = min(900, cibil + 20)

            st.session_state.finbridge_score = score
            st.session_state.cibil_score = cibil
            st.session_state.components = comps
            st.session_state.raw_score = raw
            st.session_state.scores_computed = True
            st.session_state.step = "score"
            st.success("Score computed! Redirecting to your FinBridge Score report.")
            st.rerun()

# ─── PAGE: FINBRIDGE SCORE ────────────────────────────────────────────────────
elif st.session_state.step == "score":
    if not st.session_state.scores_computed:
        st.warning("Please complete the bank statement input first.")
        if st.button("Go to Statement Input"):
            st.session_state.step = "statement"
            st.rerun()
    else:
        prof = st.session_state.profile_data
        fb   = st.session_state.finbridge_score
        comps = st.session_state.components
        stmt = st.session_state.stmt_data
        label, badge, color = get_score_band(fb)

        st.markdown("<div class='section-title'>🏅 FinBridge Credit Score</div>", unsafe_allow_html=True)

        # Score hero + gauge
        col_score, col_gauge = st.columns([1, 1.5], gap="large")

        with col_score:
            st.markdown(f"""
            <div class="score-hero">
                <div style='font-size:0.8rem;color:#8FA3BF;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;'>FinBridge Credit Score</div>
                <div class="score-num">{fb}</div>
                <div style='margin:0.8rem 0;'>
                    <span class='badge {badge}' style='font-size:0.95rem;padding:0.4rem 1.2rem;'>{label}</span>
                </div>
                <div style='font-size:0.8rem;color:#8FA3BF;'>Score Range: 300 – 900</div>
                <div style='font-size:0.8rem;color:#8FA3BF;margin-top:0.3rem;'>Assessed for: <b style="color:#E8EDF5">{prof.get("name","Applicant")}</b></div>
                <div style='font-size:0.8rem;color:#8FA3BF;'>Profile: {prof.get("profile_type","")}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Score breakdown metrics
            m1, m2 = st.columns(2)
            with m1:
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-val'>{fb}</div>
                    <div class='metric-lab'>FinBridge Score</div>
                </div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-val' style='color:#0EC4B0;'>{st.session_state.cibil_score}</div>
                    <div class='metric-lab'>Est. Traditional Score</div>
                </div>""", unsafe_allow_html=True)

        with col_gauge:
            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=fb,
                delta={"reference": st.session_state.cibil_score, "valueformat": ".0f", "prefix": "vs Traditional: "},
                title={"text": "FinBridge Score", "font": {"size": 14, "color": "#8FA3BF"}},
                number={"font": {"size": 48, "color": "#F0B429"}, "suffix": ""},
                gauge={
                    "axis": {"range": [300, 900], "tickwidth": 1, "tickcolor": "#1E3A5F",
                             "tickvals": [300, 450, 550, 650, 700, 750, 900],
                             "tickfont": {"color": "#8FA3BF", "size": 10}},
                    "bar": {"color": color, "thickness": 0.25},
                    "bgcolor": "#112240",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [300, 599], "color": "rgba(224,92,92,0.15)"},
                        {"range": [600, 649], "color": "rgba(224,137,41,0.15)"},
                        {"range": [650, 699], "color": "rgba(240,180,41,0.15)"},
                        {"range": [700, 749], "color": "rgba(124,200,126,0.15)"},
                        {"range": [750, 900], "color": "rgba(62,200,122,0.15)"},
                    ],
                    "threshold": {"line": {"color": "#F0B429", "width": 3}, "thickness": 0.75, "value": fb}
                }
            ))
            fig_gauge.update_layout(
                height=280,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#E8EDF5"},
                margin=dict(t=40, b=10, l=30, r=30),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

        # Component radar + bar
        col_r, col_b2 = st.columns([1, 1], gap="large")

        with col_r:
            st.markdown("**Score Component Breakdown**")
            cats = list(comps.keys())
            vals = list(comps.values())
            maxes = [25, 20, 18, 17, 12, 8]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=cats + [cats[0]],
                fill='toself',
                fillcolor=f"rgba(240,180,41,0.15)",
                line=dict(color="#F0B429", width=2),
                name="Your Score"
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=maxes + [maxes[0]],
                theta=cats + [cats[0]],
                fill='toself',
                fillcolor="rgba(14,196,176,0.06)",
                line=dict(color="#0EC4B0", width=1, dash="dot"),
                name="Max Possible"
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 25], gridcolor="#1E3A5F", tickfont=dict(color="#8FA3BF", size=9)),
                    angularaxis=dict(tickfont=dict(color="#E8EDF5", size=10), gridcolor="#1E3A5F"),
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                legend=dict(font=dict(color="#8FA3BF", size=10)),
                height=320,
                margin=dict(t=20, b=20, l=20, r=20),
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_b2:
            st.markdown("**Component Scores vs Maximum**")
            colors_bar = []
            for v, m in zip(vals, maxes):
                ratio = v / m if m > 0 else 0
                if ratio >= 0.75:
                    colors_bar.append("#3EC87A")
                elif ratio >= 0.5:
                    colors_bar.append("#F0B429")
                else:
                    colors_bar.append("#E05C5C")

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=cats, y=maxes,
                name="Max", marker_color="rgba(255,255,255,0.07)",
                marker_line=dict(color="#1E3A5F", width=1)
            ))
            fig_bar.add_trace(go.Bar(
                x=cats, y=vals,
                name="Your Score", marker_color=colors_bar,
                text=[f"{v:.1f}" for v in vals],
                textposition="outside",
                textfont=dict(color="#E8EDF5", size=10)
            ))
            fig_bar.update_layout(
                barmode="overlay",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8FA3BF", size=10),
                xaxis=dict(gridcolor="#1E3A5F", tickfont=dict(color="#E8EDF5", size=9)),
                yaxis=dict(gridcolor="#1E3A5F"),
                legend=dict(font=dict(color="#8FA3BF", size=10)),
                height=320,
                margin=dict(t=20, b=60, l=10, r=10),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

        # Income & Cash-flow trend
        st.markdown("**Cash-Flow Trend Analysis**")
        years = stmt.get("years", [])
        incomes = stmt.get("annual_income", [])
        expenses = stmt.get("annual_expense", [])
        savings = stmt.get("annual_savings", [])
        emis = stmt.get("existing_emis", [])
        net = [i - e - em for i, e, em in zip(incomes, expenses, emis)]

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=years, y=incomes, name="Income", line=dict(color="#3EC87A", width=2.5), mode="lines+markers", marker=dict(size=7)))
        fig_trend.add_trace(go.Scatter(x=years, y=expenses, name="Expenses", line=dict(color="#E05C5C", width=2, dash="dash"), mode="lines+markers", marker=dict(size=6)))
        fig_trend.add_trace(go.Scatter(x=years, y=emis, name="EMIs", line=dict(color="#F0B429", width=2, dash="dot"), mode="lines+markers", marker=dict(size=6)))
        fig_trend.add_trace(go.Bar(x=years, y=savings, name="Savings", marker_color="rgba(14,196,176,0.3)", marker_line=dict(color="#0EC4B0", width=1)))
        fig_trend.add_trace(go.Bar(x=years, y=net, name="Net Cash Flow", marker_color=[
            "rgba(62,200,122,0.4)" if v >= 0 else "rgba(224,92,92,0.4)" for v in net
        ], marker_line=dict(color="#1E3A5F", width=0)))

        fig_trend.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8FA3BF"),
            xaxis=dict(gridcolor="#1E3A5F", title="Financial Year"),
            yaxis=dict(gridcolor="#1E3A5F", title="Amount (₹)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#E8EDF5", size=10)),
            height=320,
            margin=dict(t=30, b=40, l=10, r=10),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # Score interpretation
        st.markdown("<br>", unsafe_allow_html=True)
        interpretation = {
            "Excellent": ("🌟 Outstanding creditworthiness. Eligible for premium loan products at best interest rates with flexible tenure.", "#3EC87A"),
            "Good": ("✅ Strong credit profile. Eligible for most loan products with competitive rates.", "#7CC87E"),
            "Fair": ("⚠️ Average creditworthiness. Eligible for standard loans; may need co-applicant for larger amounts.", "#F0B429"),
            "Marginal": ("🔶 Below average profile. Limited loan options; collateral or guarantor recommended.", "#E08929"),
            "Poor": ("🚨 Insufficient creditworthiness. Focus on improving cash-flow and reducing existing liabilities before applying.", "#E05C5C"),
        }
        msg, col = interpretation.get(label, ("", "#8FA3BF"))
        st.markdown(f"""
        <div style='background:rgba(0,0,0,0.2);border:1px solid {col};border-radius:10px;padding:1rem 1.3rem;color:{col};font-size:0.92rem;'>
            {msg}
        </div>
        """, unsafe_allow_html=True)

# ─── PAGE: COMPARISON ─────────────────────────────────────────────────────────
elif st.session_state.step == "comparison":
    if not st.session_state.scores_computed:
        st.warning("Please complete the bank statement input first.")
        st.stop()

    fb = st.session_state.finbridge_score
    ci = st.session_state.cibil_score
    prof = st.session_state.profile_data
    stmt = st.session_state.stmt_data

    label_fb, badge_fb, color_fb = get_score_band(fb)
    label_ci, badge_ci, color_ci = get_score_band(ci)

    st.markdown("<div class='section-title'>⚖️ Traditional CIBIL vs FinBridge Score</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>See how the FinBridge methodology differs from a traditional bureau score — and why it matters for your true creditworthiness.</div>", unsafe_allow_html=True)

    # Side-by-side score display
    col_ci, col_fb = st.columns(2, gap="large")
    with col_ci:
        st.markdown(f"""
        <div style='text-align:center;padding:2rem 1rem;background:#112240;border:1px solid #1E3A5F;border-radius:14px;'>
            <div style='font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#8FA3BF;margin-bottom:0.5rem;'>Traditional CIBIL Score</div>
            <div style='font-family:"Playfair Display",serif;font-size:4rem;font-weight:700;color:{color_ci};'>{ci}</div>
            <span class='badge {badge_ci}' style='font-size:0.9rem;padding:0.35rem 1rem;'>{label_ci}</span>
            <div style='font-size:0.75rem;color:#8FA3BF;margin-top:1rem;'>Bureau-based | Payment History Focused</div>
        </div>
        """, unsafe_allow_html=True)

    with col_fb:
        st.markdown(f"""
        <div style='text-align:center;padding:2rem 1rem;background:linear-gradient(135deg,#1A3A5C,#0A1628);border:2px solid #F0B429;border-radius:14px;'>
            <div style='font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#F0B429;margin-bottom:0.5rem;'>FinBridge Credit Score</div>
            <div style='font-family:"Playfair Display",serif;font-size:4rem;font-weight:700;color:{color_fb};'>{fb}</div>
            <span class='badge {badge_fb}' style='font-size:0.9rem;padding:0.35rem 1rem;'>{label_fb}</span>
            <div style='font-size:0.75rem;color:#8FA3BF;margin-top:1rem;'>Bank Statement Driven | Cash-Flow Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # Comparative bar chart
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name="Traditional Score", x=["Score"], y=[ci],
        marker_color=color_ci, width=0.25, text=[ci], textposition="outside",
        textfont=dict(color="#E8EDF5", size=14)
    ))
    fig_comp.add_trace(go.Bar(
        name="FinBridge Score", x=["Score"], y=[fb],
        marker_color=color_fb, width=0.25, text=[fb], textposition="outside",
        textfont=dict(color="#E8EDF5", size=14)
    ))
    fig_comp.add_hrect(y0=750, y1=900, fillcolor="rgba(62,200,122,0.05)", line_width=0, annotation_text="Excellent", annotation_position="right")
    fig_comp.add_hrect(y0=700, y1=749, fillcolor="rgba(62,200,122,0.03)", line_width=0, annotation_text="Good", annotation_position="right")
    fig_comp.add_hrect(y0=650, y1=699, fillcolor="rgba(240,180,41,0.05)", line_width=0, annotation_text="Fair", annotation_position="right")
    fig_comp.add_hrect(y0=600, y1=649, fillcolor="rgba(224,137,41,0.05)", line_width=0, annotation_text="Marginal", annotation_position="right")
    fig_comp.add_hrect(y0=300, y1=599, fillcolor="rgba(224,92,92,0.05)", line_width=0, annotation_text="Poor", annotation_position="right")

    fig_comp.update_layout(
        barmode="group", height=350,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(range=[300, 950], gridcolor="#1E3A5F"),
        xaxis=dict(gridcolor="#1E3A5F"),
        font=dict(color="#8FA3BF"),
        legend=dict(font=dict(color="#E8EDF5"), orientation="h", y=1.1),
        margin=dict(t=40, b=20, l=10, r=60),
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # Methodology comparison table
    st.markdown("**Methodology Comparison**")
    comp_data = [
        ("Data Source", "CIBIL Bureau / Credit Report", "Actual Bank Statements (3–5 years)"),
        ("Income Verification", "Declared income only", "Actual credited amounts verified"),
        ("Payment History", "Primary factor (35%+ weight)", "One of 6 balanced dimensions"),
        ("Cash-Flow Analysis", "Not considered", "Core scoring factor (20%)"),
        ("Savings Behaviour", "Not assessed", "Weighted at 18%"),
        ("Debt Service Coverage", "Estimated only", "Calculated from real outflows (17%)"),
        ("Informal Income", "Cannot capture", "Reflected in cash-flow patterns"),
        ("Freelancer / Gig Workers", "Often penalised (irregular income)", "Fairly assessed via income stability"),
        ("Students / First-timers", "No score (thin file)", "Scored on available history (3 yrs)"),
        ("Real-time Adjustments", "Quarterly updates only", "Instant re-assessment possible"),
        ("Manipulation Risk", "Credit card gaming possible", "Difficult to manipulate bank records"),
        ("India Relevance", "Urban / salaried bias", "Inclusive of semi-urban & rural patterns"),
    ]

    header_html = """
    <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:8px;'>
        <div style='background:#0A1628;border:1px solid #1E3A5F;border-radius:8px;padding:0.7rem 1rem;font-size:0.8rem;font-weight:600;color:#8FA3BF;text-transform:uppercase;letter-spacing:0.05em;'>Parameter</div>
        <div style='background:#0A1628;border:1px solid #1E3A5F;border-radius:8px;padding:0.7rem 1rem;font-size:0.8rem;font-weight:600;color:#8FA3BF;text-transform:uppercase;letter-spacing:0.05em;'>Traditional CIBIL</div>
        <div style='background:linear-gradient(135deg,#1A3A5C,#0A1628);border:1px solid #F0B429;border-radius:8px;padding:0.7rem 1rem;font-size:0.8rem;font-weight:600;color:#F0B429;text-transform:uppercase;letter-spacing:0.05em;'>FinBridge</div>
    </div>
    """
    rows_html = ""
    for param, trad, fb_val in comp_data:
        rows_html += f"""
        <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:6px;'>
            <div style='background:#112240;border:1px solid #1E3A5F;border-radius:6px;padding:0.6rem 0.9rem;font-size:0.82rem;color:#E8EDF5;font-weight:500;'>{param}</div>
            <div style='background:#112240;border:1px solid #1E3A5F;border-radius:6px;padding:0.6rem 0.9rem;font-size:0.82rem;color:#8FA3BF;'>{trad}</div>
            <div style='background:linear-gradient(135deg,#1A3A5C,#0A1628);border:1px solid rgba(240,180,41,0.3);border-radius:6px;padding:0.6rem 0.9rem;font-size:0.82rem;color:#E8EDF5;'>{fb_val}</div>
        </div>
        """
    st.markdown(header_html + rows_html, unsafe_allow_html=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # Who benefits more from FinBridge?
    st.markdown("**Who benefits most from FinBridge scoring?**")
    benefit_cols = st.columns(4, gap="small")
    benefits = [
        ("🧑‍🎓", "Students", "Build credit history without credit cards"),
        ("💻", "Freelancers", "Cash-flow recognized despite irregular income"),
        ("🏪", "MSMEs", "5-year business cash-flow tells the real story"),
        ("🌾", "Informal Earners", "Cash deposits and transaction patterns scored"),
    ]
    for col, (icon, title, desc) in zip(benefit_cols, benefits):
        with col:
            st.markdown(f"""
            <div class='metric-card' style='padding:1.3rem;'>
                <div style='font-size:2rem;'>{icon}</div>
                <div style='font-size:0.92rem;font-weight:600;color:#E8EDF5;margin:0.5rem 0 0.3rem;'>{title}</div>
                <div style='font-size:0.78rem;color:#8FA3BF;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ─── PAGE: LOAN PURPOSE & ELIGIBILITY ────────────────────────────────────────
elif st.session_state.step == "loan":
    if not st.session_state.scores_computed:
        st.warning("Please complete the bank statement input first.")
        st.stop()

    fb = st.session_state.finbridge_score
    prof = st.session_state.profile_data
    stmt = st.session_state.stmt_data
    label, badge, color = get_score_band(fb)

    st.markdown("<div class='section-title'>💰 Loan Purpose & Eligibility</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Select your financing need. We'll match your FinBridge score against industry lending benchmarks and compute your maximum eligible loan amount.</div>", unsafe_allow_html=True)

    col_inp, col_res = st.columns([1, 1.2], gap="large")

    with col_inp:
        st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
        st.markdown("**Select Financing Purpose**")
        purpose = st.selectbox("Why do you need financing?", list(LOAN_PURPOSES.keys()))
        purpose_data = LOAN_PURPOSES[purpose]
        rate_lo, rate_hi = purpose_data["rate_range"]
        max_tenure_yr = purpose_data["max_tenure"]
        industry = purpose_data["industry"]

        st.markdown(f"""
        <div style='background:#0A1628;border:1px solid #1E3A5F;border-radius:8px;padding:0.8rem;margin:0.8rem 0;font-size:0.82rem;'>
            <b style='color:#F0B429;'>Industry:</b> <span style='color:#E8EDF5;'>{industry}</span><br>
            <b style='color:#F0B429;'>Market Rate Range:</b> <span style='color:#E8EDF5;'>{rate_lo:.1f}% – {rate_hi:.1f}% p.a.</span><br>
            <b style='color:#F0B429;'>Max Tenure:</b> <span style='color:#E8EDF5;'>Up to {max_tenure_yr} years</span>
        </div>
        """, unsafe_allow_html=True)

        # Rate assigned based on score
        score_discount = max(0, (fb - 600) / 300)
        assigned_rate = round(rate_hi - score_discount * (rate_hi - rate_lo), 2)
        assigned_rate = max(rate_lo, min(rate_hi, assigned_rate))

        st.markdown("**Loan Parameters**")
        desired_amount = st.number_input("Desired Loan Amount (₹)", min_value=10000.0, value=1000000.0, step=50000.0, format="%.0f")
        tenure_years = st.slider("Preferred Loan Tenure (Years)", 1, max_tenure_yr, min(5, max_tenure_yr))
        tenure_months = tenure_years * 12

        st.markdown(f"""
        <div style='background:rgba(240,180,41,0.08);border:1px solid rgba(240,180,41,0.3);border-radius:8px;padding:0.8rem;margin-top:0.8rem;font-size:0.85rem;color:#F0B429;'>
            🎯 <b>Your Assigned Interest Rate: {assigned_rate:.2f}% p.a.</b><br>
            <span style='font-size:0.75rem;color:#8FA3BF;'>Determined by your FinBridge Score ({fb}) within the {rate_lo}–{rate_hi}% range</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res:
        max_eligible, disposable_emi = max_loan_eligible(stmt, assigned_rate, tenure_months)
        desired_emi = calc_emi(desired_amount, assigned_rate, tenure_months)
        max_emi = calc_emi(max_eligible, assigned_rate, tenure_months)

        can_afford = desired_emi <= disposable_emi
        eligible_pct = min(100, (max_eligible / desired_amount * 100)) if desired_amount > 0 else 0

        st.markdown("<div class='fb-card-gold'>", unsafe_allow_html=True)
        st.markdown("**Eligibility Summary**")

        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-val'>{format_inr(max_eligible)}</div>
                <div class='metric-lab'>Maximum Eligible Loan</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-val'>{format_inr(disposable_emi)}/mo</div>
                <div class='metric-lab'>Disposable for EMI (FOIR 55%)</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        m3, m4 = st.columns(2)
        with m3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-val' style='color:#0EC4B0;'>{format_inr(desired_emi)}/mo</div>
                <div class='metric-lab'>EMI on Desired Amount</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-val' style='color:#F0B429;'>{assigned_rate:.2f}%</div>
                <div class='metric-lab'>Interest Rate (p.a.)</div>
            </div>
            """, unsafe_allow_html=True)

        # Eligibility bar
        st.markdown("<br>", unsafe_allow_html=True)
        bar_color = "#3EC87A" if eligible_pct >= 90 else "#F0B429" if eligible_pct >= 60 else "#E05C5C"
        st.markdown(f"""
        <div style='margin:0.5rem 0;'>
            <div style='display:flex;justify-content:space-between;font-size:0.8rem;color:#8FA3BF;margin-bottom:0.3rem;'>
                <span>Eligibility Coverage</span><span>{eligible_pct:.1f}%</span>
            </div>
            <div style='background:#1E3A5F;border-radius:50px;height:10px;'>
                <div style='width:{min(eligible_pct,100):.1f}%;background:{bar_color};border-radius:50px;height:10px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        verdict_color = "#3EC87A" if can_afford else "#E05C5C"
        verdict_icon = "✅" if can_afford else "❌"
        verdict_msg = "Your desired loan is within your repayment capacity." if can_afford else f"Desired EMI exceeds your capacity. Max eligible: {format_inr(max_eligible)}"
        st.markdown(f"""
        <div style='background:rgba(0,0,0,0.2);border:1px solid {verdict_color};border-radius:8px;padding:0.9rem;margin-top:0.8rem;font-size:0.85rem;color:{verdict_color};'>
            {verdict_icon} {verdict_msg}
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # All purposes overview
    st.markdown("**Eligibility Across All Loan Types**")
    rows = []
    for p, pd_info in LOAN_PURPOSES.items():
        lo, hi = pd_info["rate_range"]
        sc_disc = max(0, (fb - 600) / 300)
        arate = round(hi - sc_disc * (hi - lo), 2)
        arate = max(lo, min(hi, arate))
        max_yr = pd_info["max_tenure"]
        t_months = min(60, max_yr * 12)
        mel, _ = max_loan_eligible(stmt, arate, t_months)
        rows.append({
            "Purpose": p,
            "Industry": pd_info["industry"],
            "Rate (%)": f"{arate:.2f}",
            "Max Tenure": f"{max_yr} yrs",
            "Max Eligible": format_inr(mel),
        })

    df_table = pd.DataFrame(rows)
    st.dataframe(
        df_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Purpose": st.column_config.TextColumn("Loan Purpose"),
            "Industry": st.column_config.TextColumn("Industry Segment"),
            "Rate (%)": st.column_config.TextColumn("Interest Rate"),
            "Max Tenure": st.column_config.TextColumn("Max Tenure"),
            "Max Eligible": st.column_config.TextColumn("Max Eligible Amount"),
        }
    )

# ─── PAGE: EMI PLANNER ────────────────────────────────────────────────────────
elif st.session_state.step == "emi":
    if not st.session_state.scores_computed:
        st.warning("Please complete the bank statement input first.")
        st.stop()

    fb = st.session_state.finbridge_score
    stmt = st.session_state.stmt_data
    prof = st.session_state.profile_data

    st.markdown("<div class='section-title'>📅 EMI Planner & Repayment Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Model your repayment schedule, see the true cost of borrowing, and understand how different scenarios affect your monthly cash-flow.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.markdown("<div class='fb-card'>", unsafe_allow_html=True)
        st.markdown("**Loan Inputs**")
        loan_amount = st.number_input("Loan Amount (₹)", min_value=10000.0, value=1500000.0, step=50000.0, format="%.0f")
        int_rate = st.slider("Annual Interest Rate (%)", 6.0, 24.0, 10.5, 0.25)
        tenure_yr = st.slider("Loan Tenure (Years)", 1, 30, 10)
        tenure_mo = tenure_yr * 12

        emi = calc_emi(loan_amount, int_rate, tenure_mo)
        total_payment = emi * tenure_mo
        total_interest = total_payment - loan_amount
        int_to_principal = (total_interest / loan_amount * 100) if loan_amount > 0 else 0

        st.markdown("</div>", unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-val'>{format_inr(emi)}/mo</div>
                <div class='metric-lab'>Monthly EMI</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-val' style='color:#E05C5C;'>{format_inr(total_interest)}</div>
                <div class='metric-lab'>Total Interest Paid</div>
            </div>""", unsafe_allow_html=True)
        m3, m4 = st.columns(2)
        with m3:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-val' style='color:#0EC4B0;'>{format_inr(total_payment)}</div>
                <div class='metric-lab'>Total Payable</div>
            </div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-val' style='color:#F0B429;'>{int_to_principal:.1f}%</div>
                <div class='metric-lab'>Interest-to-Principal Ratio</div>
            </div>""", unsafe_allow_html=True)

    with col2:
        # Amortisation pie
        fig_pie = go.Figure(go.Pie(
            labels=["Principal", "Total Interest"],
            values=[loan_amount, total_interest],
            hole=0.55,
            marker=dict(colors=["#0EC4B0", "#E05C5C"]),
            textinfo="label+percent",
            textfont=dict(color="#E8EDF5", size=11),
            hovertemplate="%{label}: ₹%{value:,.0f}<extra></extra>"
        ))
        fig_pie.add_annotation(text=f"Total<br>{format_inr(total_payment)}", x=0.5, y=0.5, showarrow=False,
                               font=dict(size=13, color="#E8EDF5"))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True, legend=dict(font=dict(color="#8FA3BF"), orientation="h", y=-0.1),
            height=300, margin=dict(t=20, b=30, l=10, r=10),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Amortisation schedule chart
        st.markdown("**Year-wise Amortisation Schedule**")
        balances, principals, interests_paid = [], [], []
        balance = loan_amount
        r = int_rate / (12 * 100)

        for yr in range(1, tenure_yr + 1):
            yr_interest = 0
            yr_principal = 0
            for _ in range(12):
                if balance <= 0:
                    break
                interest_portion = balance * r
                principal_portion = min(emi - interest_portion, balance)
                balance -= principal_portion
                yr_interest += interest_portion
                yr_principal += principal_portion
            principals.append(round(yr_principal, 0))
            interests_paid.append(round(yr_interest, 0))
            balances.append(max(0, round(balance, 0)))

        yrs_labels = [f"Yr {i}" for i in range(1, tenure_yr + 1)]

        fig_amort = go.Figure()
        fig_amort.add_trace(go.Bar(name="Principal", x=yrs_labels, y=principals, marker_color="#0EC4B0"))
        fig_amort.add_trace(go.Bar(name="Interest", x=yrs_labels, y=interests_paid, marker_color="#E05C5C"))
        fig_amort.add_trace(go.Scatter(name="Outstanding Balance", x=yrs_labels, y=balances,
                                       mode="lines+markers", line=dict(color="#F0B429", width=2),
                                       yaxis="y2"))
        fig_amort.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#1E3A5F"),
            yaxis=dict(gridcolor="#1E3A5F", title="Annual Payment (₹)"),
            yaxis2=dict(overlaying="y", side="right", title="Balance (₹)", gridcolor="#1E3A5F"),
            legend=dict(font=dict(color="#8FA3BF", size=9), orientation="h", y=1.1),
            font=dict(color="#8FA3BF", size=9),
            height=300, margin=dict(t=30, b=40, l=10, r=10),
        )
        st.plotly_chart(fig_amort, use_container_width=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # EMI stress test
    st.markdown("**Monthly Cash-Flow Stress Test**")
    avg_monthly_income = float(np.mean(stmt.get("annual_income", [600000]))) / 12
    avg_monthly_expense = float(np.mean(stmt.get("annual_expense", [400000]))) / 12
    existing_monthly_emi = float(np.mean(stmt.get("existing_emis", [0]))) / 12
    net_after_emi = avg_monthly_income - avg_monthly_expense - existing_monthly_emi - emi

    scenario_cols = st.columns(4, gap="small")
    scenarios = [
        ("Monthly Income", f"₹{avg_monthly_income:,.0f}", "#3EC87A"),
        ("Monthly Expenses", f"₹{avg_monthly_expense:,.0f}", "#E05C5C"),
        ("Existing EMIs", f"₹{existing_monthly_emi:,.0f}", "#E08929"),
        ("New EMI", f"₹{emi:,.0f}", "#F0B429"),
    ]
    for col, (label, val, col_color) in zip(scenario_cols, scenarios):
        with col:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-val' style='font-size:1.2rem;color:{col_color};'>{val}</div>
                <div class='metric-lab'>{label}</div>
            </div>""", unsafe_allow_html=True)

    net_color = "#3EC87A" if net_after_emi > 0 else "#E05C5C"
    net_icon = "✅" if net_after_emi > 0 else "⚠️"
    st.markdown(f"""
    <div style='background:rgba(0,0,0,0.2);border:2px solid {net_color};border-radius:10px;padding:1rem 1.3rem;margin-top:1rem;'>
        <span style='color:{net_color};font-size:1rem;font-weight:600;'>{net_icon} Net Monthly Surplus after all obligations: <span style='font-family:"Playfair Display",serif;font-size:1.4rem;'>₹{net_after_emi:,.0f}</span></span>
        <div style='font-size:0.8rem;color:#8FA3BF;margin-top:0.4rem;'>{'Comfortable repayment capacity. Loan is financially sustainable.' if net_after_emi > avg_monthly_income * 0.1 else 'Tight cash flow. Consider lower loan amount or longer tenure.' if net_after_emi > 0 else 'Loan would result in negative monthly balance. Reduce desired amount.'}</div>
    </div>
    """, unsafe_allow_html=True)

    # Prepayment analysis
    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)
    st.markdown("**Prepayment Benefit Simulator**")
    pre_col1, pre_col2 = st.columns([1, 2])
    with pre_col1:
        prepay_amount = st.number_input("Annual Prepayment Amount (₹)", min_value=0.0, value=50000.0, step=10000.0, format="%.0f")

    if prepay_amount > 0 and r > 0:
        balance_pp = loan_amount
        months_taken = 0
        int_paid_pp = 0
        for m in range(tenure_mo):
            if balance_pp <= 0:
                break
            int_p = balance_pp * r
            prin_p = min(emi - int_p, balance_pp)
            balance_pp -= prin_p
            int_paid_pp += int_p
            months_taken += 1
            if (m + 1) % 12 == 0:
                balance_pp = max(0, balance_pp - prepay_amount)
        interest_saved = total_interest - int_paid_pp
        months_saved = tenure_mo - months_taken

        with pre_col2:
            pp_cols = st.columns(3, gap="small")
            with pp_cols[0]:
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-val' style='color:#3EC87A;'>{format_inr(max(0, interest_saved))}</div>
                    <div class='metric-lab'>Interest Saved</div>
                </div>""", unsafe_allow_html=True)
            with pp_cols[1]:
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-val' style='color:#0EC4B0;'>{months_to_label(max(0, months_saved))}</div>
                    <div class='metric-lab'>Tenure Reduced</div>
                </div>""", unsafe_allow_html=True)
            with pp_cols[2]:
                new_total = int_paid_pp + loan_amount
                st.markdown(f"""<div class='metric-card'>
                    <div class='metric-val' style='color:#F0B429;'>{format_inr(new_total)}</div>
                    <div class='metric-lab'>New Total Payable</div>
                </div>""", unsafe_allow_html=True)

# ─── PAGE: CREDIT REPORT ─────────────────────────────────────────────────────
elif st.session_state.step == "report":
    if not st.session_state.scores_computed:
        st.warning("Please complete the bank statement input first.")
        st.stop()

    fb = st.session_state.finbridge_score
    ci = st.session_state.cibil_score
    prof = st.session_state.profile_data
    stmt = st.session_state.stmt_data
    comps = st.session_state.components
    label, badge, color = get_score_band(fb)

    st.markdown("<div class='section-title'>📋 FinBridge Credit Intelligence Report</div>", unsafe_allow_html=True)

    # Report header
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#1A3A5C 0%,#0A1628 100%);border:1px solid #F0B429;border-radius:14px;padding:2rem;margin-bottom:1.5rem;'>
        <div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;'>
            <div>
                <div style='font-family:"Playfair Display",serif;font-size:1.5rem;font-weight:700;color:#F0B429;'>FinBridge Credit Intelligence Report</div>
                <div style='color:#8FA3BF;font-size:0.82rem;margin-top:0.3rem;'>Confidential | Generated: April 2025</div>
            </div>
            <div style='text-align:right;'>
                <div style='font-size:0.75rem;color:#8FA3BF;'>FinBridge Score</div>
                <div style='font-family:"Playfair Display",serif;font-size:2.5rem;color:{color};font-weight:700;'>{fb}</div>
                <span class='badge {badge}'>{label}</span>
            </div>
        </div>
        <hr style='border-color:#1E3A5F;margin:1rem 0;'>
        <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;font-size:0.82rem;'>
            <div><span style='color:#8FA3BF;'>Name:</span> <span style='color:#E8EDF5;'>{prof.get("name","N/A")}</span></div>
            <div><span style='color:#8FA3BF;'>Age:</span> <span style='color:#E8EDF5;'>{prof.get("age","N/A")}</span></div>
            <div><span style='color:#8FA3BF;'>Profile:</span> <span style='color:#E8EDF5;'>{prof.get("profile_type","N/A")}</span></div>
            <div><span style='color:#8FA3BF;'>City:</span> <span style='color:#E8EDF5;'>{prof.get("city","N/A")}</span></div>
            <div><span style='color:#8FA3BF;'>Occupation:</span> <span style='color:#E8EDF5;'>{prof.get("occupation","N/A")}</span></div>
            <div><span style='color:#8FA3BF;'>Credit Cards:</span> <span style='color:#E8EDF5;'>{prof.get("credit_cards","N/A")}</span></div>
            <div><span style='color:#8FA3BF;'>Active Loans:</span> <span style='color:#E8EDF5;'>{prof.get("loans_active","N/A")}</span></div>
            <div><span style='color:#8FA3BF;'>Collateral:</span> <span style='color:#E8EDF5;'>{prof.get("has_collateral","N/A")}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Scores row
    r1, r2, r3, r4, r5 = st.columns(5, gap="small")
    incomes = stmt.get("annual_income", [1])
    avg_income = float(np.mean(incomes))
    avg_expense = float(np.mean(stmt.get("annual_expense", [0])))
    avg_savings = float(np.mean(stmt.get("annual_savings", [0])))
    total_bounces = int(sum(stmt.get("bounce_count", [0])))
    savings_rate = (avg_savings / avg_income * 100) if avg_income > 0 else 0

    metrics_report = [
        ("FinBridge Score", str(fb), color),
        ("Traditional Score", str(ci), "#0EC4B0"),
        ("Avg Annual Income", format_inr(avg_income), "#3EC87A"),
        ("Avg Savings Rate", f"{savings_rate:.1f}%", "#F0B429"),
        ("Total Bounces", str(total_bounces), "#E05C5C" if total_bounces > 2 else "#8FA3BF"),
    ]
    for col, (lbl, val, col_color) in zip([r1, r2, r3, r4, r5], metrics_report):
        with col:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-val' style='font-size:1.4rem;color:{col_color};'>{val}</div>
                <div class='metric-lab'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # Score breakdown table
    st.markdown("**Score Component Analysis**")
    maxes = {"Income Stability": 25, "Cash-Flow": 20, "Savings Behaviour": 18,
             "Debt Coverage": 17, "Expenditure Discipline": 12, "Account Behaviour": 8}

    for comp_name, score_val in comps.items():
        max_val = maxes.get(comp_name, 25)
        pct = score_val / max_val * 100 if max_val > 0 else 0
        bar_col = "#3EC87A" if pct >= 75 else "#F0B429" if pct >= 50 else "#E05C5C"
        strength = "Strong" if pct >= 75 else "Moderate" if pct >= 50 else "Weak"
        st.markdown(f"""
        <div style='display:grid;grid-template-columns:180px 1fr 80px 70px;gap:1rem;align-items:center;margin-bottom:0.6rem;'>
            <div style='font-size:0.85rem;color:#E8EDF5;'>{comp_name}</div>
            <div style='background:#1E3A5F;border-radius:50px;height:8px;'>
                <div style='width:{pct:.1f}%;background:{bar_col};border-radius:50px;height:8px;'></div>
            </div>
            <div style='font-size:0.85rem;color:{bar_col};text-align:right;'>{score_val:.1f}/{max_val}</div>
            <div><span class='badge {"badge-green" if pct>=75 else "badge-gold" if pct>=50 else "badge-red"}' style='font-size:0.68rem;'>{strength}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # Key strengths and improvement areas
    col_str, col_imp = st.columns(2, gap="large")

    with col_str:
        st.markdown("**💪 Key Strengths**")
        strengths = []
        if comps.get("Income Stability", 0) >= 18:
            strengths.append("Consistent income growth demonstrates financial stability")
        if comps.get("Savings Behaviour", 0) >= 13:
            strengths.append("Strong savings discipline — above benchmark savings rate")
        if comps.get("Cash-Flow", 0) >= 15:
            strengths.append("Positive cash-flow maintained across all years")
        if comps.get("Debt Coverage", 0) >= 12:
            strengths.append("Healthy Debt Service Coverage Ratio (DSCR)")
        if comps.get("Expenditure Discipline", 0) >= 9:
            strengths.append("Controlled expenditure relative to income")
        if comps.get("Account Behaviour", 0) >= 6:
            strengths.append("Clean account history with minimal bounces")
        if total_bounces == 0:
            strengths.append("Zero bounce record — excellent payment behaviour")
        if not strengths:
            strengths.append("Continue building financial discipline for a stronger score")
        for s in strengths:
            st.markdown(f"""<div style='background:rgba(62,200,122,0.05);border:1px solid rgba(62,200,122,0.2);border-radius:8px;padding:0.6rem 0.9rem;margin-bottom:0.5rem;font-size:0.83rem;color:#E8EDF5;'>✅ {s}</div>""", unsafe_allow_html=True)

    with col_imp:
        st.markdown("**🔧 Areas for Improvement**")
        improvements = []
        if comps.get("Savings Behaviour", 0) < 10:
            improvements.append("Increase monthly savings rate to at least 20% of income")
        if comps.get("Cash-Flow", 0) < 12:
            improvements.append("Improve cash-flow consistency — reduce unnecessary outflows")
        if comps.get("Income Stability", 0) < 15:
            improvements.append("Diversify income sources to improve stability score")
        if comps.get("Debt Coverage", 0) < 10:
            improvements.append("Reduce existing EMI obligations to improve DSCR")
        if comps.get("Account Behaviour", 0) < 6:
            improvements.append("Eliminate cheque/ECS bounces — maintain minimum balance")
        if comps.get("Expenditure Discipline", 0) < 8:
            improvements.append("Reduce discretionary spending to below 75% of income")
        if total_bounces > 2:
            improvements.append(f"Address {total_bounces} bounces recorded — serious negative signal")
        if not improvements:
            improvements.append("Excellent profile — maintain current financial discipline")
        for im in improvements:
            st.markdown(f"""<div style='background:rgba(240,180,41,0.05);border:1px solid rgba(240,180,41,0.2);border-radius:8px;padding:0.6rem 0.9rem;margin-bottom:0.5rem;font-size:0.83rem;color:#E8EDF5;'>⚠️ {im}</div>""", unsafe_allow_html=True)

    st.markdown("<hr class='fb-divider'>", unsafe_allow_html=True)

    # Score projection
    st.markdown("**📈 Score Improvement Projection**")
    months_proj = list(range(0, 25, 3))
    if savings_rate < 20 and total_bounces == 0:
        proj_scores = [min(900, fb + int(m * 2.5)) for m in months_proj]
    elif total_bounces > 0:
        proj_scores = [min(900, fb + int(m * 1.2)) for m in months_proj]
    else:
        proj_scores = [min(900, fb + int(m * 3)) for m in months_proj]

    fig_proj = go.Figure()
    fig_proj.add_trace(go.Scatter(
        x=[f"M+{m}" for m in months_proj], y=proj_scores,
        mode="lines+markers", line=dict(color="#F0B429", width=2.5),
        marker=dict(size=8, color="#F0B429"),
        fill="tozeroy", fillcolor="rgba(240,180,41,0.05)",
        name="Projected Score"
    ))
    fig_proj.add_hline(y=750, line_dash="dot", line_color="#3EC87A", annotation_text="Excellent (750)", annotation_font_color="#3EC87A")
    fig_proj.add_hline(y=700, line_dash="dot", line_color="#7CC87E", annotation_text="Good (700)", annotation_font_color="#7CC87E")
    fig_proj.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#1E3A5F"),
        yaxis=dict(gridcolor="#1E3A5F", range=[300, 950]),
        font=dict(color="#8FA3BF"),
        height=250, margin=dict(t=20, b=30, l=10, r=10),
        showlegend=False,
    )
    st.plotly_chart(fig_proj, use_container_width=True)

    st.markdown("""
    <div style='text-align:center;font-size:0.72rem;color:#4A6080;margin-top:1rem;border-top:1px solid #1E3A5F;padding-top:1rem;'>
        FinBridge Credit Intelligence Platform &nbsp;|&nbsp; This report is for informational purposes only and does not constitute a formal credit assessment.
        &nbsp;|&nbsp; FinBridge is not a registered Credit Information Company under the Credit Information Companies (Regulation) Act, 2005.
        &nbsp;|&nbsp; All scores are computed using the applicant's self-declared bank statement data.
    </div>
    """, unsafe_allow_html=True)

# ─── DEFAULT / FALLBACK ───────────────────────────────────────────────────────
else:
    st.session_state.step = "profile"
    st.rerun()
