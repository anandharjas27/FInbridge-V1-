# FinBridge Credit Intelligence Platform 🏦

A professional credit scoring and loan eligibility analysis system built with Streamlit. FinBridge goes beyond traditional CIBIL scores by analyzing actual bank statement data to produce a holistic, cash-flow-driven credit score.

---

## 🚀 Features

- **Dual-Profile Support** — 3-year statements for Students/Freelancers; 5-year for Business/Salaried
- **FinBridge Proprietary Score** — 6-dimensional scoring model (300–900 scale)
- **CIBIL vs FinBridge Comparison** — Side-by-side methodology comparison with visual breakdown
- **10 Loan Purpose Categories** — Industry-matched interest rates and maximum eligible amounts
- **EMI Planner** — Full amortisation schedule, prepayment simulator, cash-flow stress test
- **Credit Intelligence Report** — Strengths, improvement areas, and score projection
- **Professional Dark Theme** — Navy + Gold colour scheme with Playfair Display typography

---

## 📁 File Structure

```
finbridge/
├── app.py              # Main Streamlit application (single-file architecture)
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .streamlit/
    └── config.toml     # Streamlit theme configuration
```

---

## 🛠️ Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/finbridge.git
cd finbridge

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New App** → Select your repo → Set `app.py` as the main file
4. Click **Deploy** — done in under 2 minutes

---

## 📊 FinBridge Scoring Model

| Dimension | Weight | What it Measures |
|---|---|---|
| Income Stability & Growth | 25% | Consistency and upward trend of income |
| Cash-Flow Consistency | 20% | Positive net cash-flow across years |
| Savings Behaviour | 18% | Savings as % of income (benchmark: 20%+) |
| Debt Service Coverage | 17% | DSCR — income relative to EMI obligations |
| Expenditure Discipline | 12% | Expense ratio relative to income |
| Account Behaviour | 8% | Bounce-free, overdraft-free account history |

**Score Range: 300 – 900**
- 750–900: Excellent
- 700–749: Good
- 650–699: Fair
- 600–649: Marginal
- 300–599: Poor

---

## 💼 Loan Categories Supported

1. Home Purchase / Construction
2. Vehicle Purchase
3. Education Loan
4. Business Expansion / Working Capital
5. Medical Emergency
6. Equipment / Machinery Purchase
7. Travel / Lifestyle
8. Debt Consolidation
9. Renovation / Home Improvement
10. Start-Up / New Venture

---

## ⚖️ Disclaimer

FinBridge is an educational and analytical tool. It is **not** a registered Credit Information Company under the Credit Information Companies (Regulation) Act, 2005. Scores generated are based on self-declared bank statement data and should not be used as a formal credit assessment.

---

## 🎨 Tech Stack

- **Frontend/App**: Streamlit
- **Visualisations**: Plotly
- **Data Processing**: Pandas, NumPy
- **Fonts**: Playfair Display + DM Sans (Google Fonts)
- **Hosting**: Streamlit Community Cloud

---

*FinBridge © 2025 | Credit Intelligence Platform*
