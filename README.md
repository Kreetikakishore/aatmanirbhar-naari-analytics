# 🪷 Aatmanirbhar Naari — Women Home Business Intelligence Platform

A segmentation-driven analytics dashboard designed to track, analyse, and improve
business outcomes for women micro-entrepreneurs across India's home business ecosystem.
Built to support data-driven policy decisions for the women empowerment initiative.

---

## 🚀 Live Demo
https://kreetikakishore-aatmanirbhar-naari-analytics-app-xfwhfm.streamlit.app/

---

## 📌 Executive Summary

Women micro-entrepreneurship in India remains one of the most underleveraged economic
forces, with millions of home-based businesses lacking data visibility, digital access,
and government scheme awareness.

This project analyses **2,000 women entrepreneurs** across **15 Indian states** to uncover:

- Which business categories generate the highest revenue & profit margins
- How digital adoption directly impacts business growth stage
- Where portal dropout risk is geographically concentrated
- Which government schemes produce the strongest entrepreneur outcomes
- How SHG membership and mentorship influence the path to thriving

Using **Python, Pandas, Plotly, and Streamlit**, the outcome is a fully interactive
**6-module intelligence dashboard** built to support targeted retention and empowerment strategies.

---

## 🎯 Business Questions Addressed

- Which Indian zones and states show the highest revenue performance?
- Which business categories have the highest profit margins?
- How does digital score impact monthly revenue and growth stage?
- Are rural entrepreneurs facing a compounding digital-financial gap?
- Which government loan schemes produce the most thriving entrepreneurs?
- Where is portal dropout risk concentrated, and what drives it?
- Does SHG membership and mentorship significantly improve growth outcomes?
- Which entrepreneur segments need immediate intervention?

---

## 📊 Core KPI Snapshot

| KPI Metric | Value |
|---|---|
| Total Entrepreneurs Registered | 2,000 |
| Portal Active Rate | 80.3% |
| Overall Portal Dropout Rate | 19.7% |
| Avg Monthly Revenue | ₹21,757 |
| Avg Monthly Profit | ₹9,777 |
| Avg Profit Margin | 45.0% |
| Total Annual Revenue (All) | ₹52.2 Crore |
| Highest Revenue Category | Digital Services (₹32,498/month) |
| Highest Risk Zone (Dropout) | North Zone (22.1%) |
| Best Performing Govt Scheme | State Scheme (30.3% Thriving) |
| SHG Membership Rate | 55% |
| Digitally Enabled (Score ≥ 2) | 67.0% |

---

## 🧠 Key Analytical Findings

### 1. Digital Score is the Strongest Revenue Driver
Each step up in digital score corresponds to ₹4,000–6,000 increase in monthly revenue.
Rural smartphone penetration gap vs Urban is the single biggest barrier to income growth.

### 2. West Zone Leads, Northeast Lags
West Zone entrepreneurs earn the highest average revenue (₹22,627/month) while
Northeast Zone has the lowest digital adoption (1.77/4), creating a compounding
vulnerability of low digital access + low revenue + high dropout.

### 3. Business Category Determines Financial Ceiling
Digital Services (₹32,498) and Retail & Trading (₹30,222) are top earners.
Handicraft & Artisan (₹13,955) and Agriculture & Dairy (₹16,054) need focused
revenue enhancement and market linkage programs.

### 4. SHG Membership is the Strongest Protective Factor
SHG members are **2× more likely** to reach the Thriving growth stage.
Non-SHG members show 8% higher portal dropout rates — confirming community
support networks as critical retention infrastructure.

### 5. Training Attendance Directly Reduces Dropout
Entrepreneurs with zero trainings show 24.8% dropout rate.
Those with 7 trainings show only 9.3% dropout — a **15.5 percentage point improvement**,
making skill training the single most cost-effective intervention available.

### 6. Rural Nascent Entrepreneurs Face Compounding Risk
Rural + Nascent + DigitalScore=0 is the highest-risk combination with 35–40% dropout.
These segments need priority digital onboarding before any other intervention.

### 7. State Scheme Outperforms National Schemes
State-level government schemes produce the highest Thriving rate (30.3%),
followed by Stand-Up India (28.4%). Mudra Yojana has highest uptake (446 beneficiaries)
but lower Thriving conversion — suggesting disbursement without adequate follow-up support.

---

## 📈 Strategic Recommendations

1. **Launch rural digital literacy camps** targeting smartphone adoption as the
   first step toward income growth.
2. **Expand SHG network coverage** — especially in Northeast and East zones where
   membership rates are lowest.
3. **Mandate minimum 3 training sessions** for all newly registered entrepreneurs
   to reduce early-stage dropout by ~15%.
4. **Redesign Mudra Yojana follow-up support** — high disbursement but low Thriving
   conversion suggests post-loan mentorship gap.
5. **Create dedicated Urban-Rural linkage programs** for Handicraft and Agriculture
   categories to access premium urban markets.
6. **Deploy targeted re-engagement campaigns** for Rural Nascent entrepreneurs
   with DigitalScore=0 before silent dropout occurs.

---

## 🗂️ Dataset Scope

| Variable | Description |
|---|---|
| EntrepreneurID | Unique identifier |
| State / Zone | Geographic location |
| AreaType | Rural / Semi-Urban / Urban |
| Age / AgeGroup | Entrepreneur age & band |
| Education | Education level |
| MaritalStatus | Marital status |
| Dependents | Number of dependents |
| BusinessCategory | Type of home business |
| YearsInBusiness | Business tenure |
| MonthlyRevenue | Monthly earnings (₹) |
| MonthlyExpenses | Monthly costs (₹) |
| MonthlyProfit | Net monthly profit (₹) |
| AnnualRevenue | Annual earnings (₹) |
| HasLoan | Loan access (0/1) |
| LoanAmount | Loan amount (₹) |
| LoanScheme | Government scheme name |
| HasSmartphone | Smartphone ownership (0/1) |
| UsesDigitalPayment | Digital payment usage (0/1) |
| UsesSocialMedia | Social media marketing (0/1) |
| SellsOnline | Online selling (0/1) |
| DigitalScore | Composite digital score (0–4) |
| TrainingsAttended | Number of trainings attended |
| TrainingType | Type of skill training |
| SHGMember | SHG membership (0/1) |
| HasMentor | Mentorship access (0/1) |
| GrowthStage | Nascent / Emerging / Growing / Thriving |
| PortalDropout | Portal dropout indicator (0/1) |

---

## 📊 Entrepreneur Segmentation Layers

| Dimension | Groups |
|---|---|
| Age Band | 18–25 / 26–35 / 36–45 / 46–60 |
| Revenue Segment | Low / Medium / High / Premium |
| Tenure Group | 0–2 yrs / 3–6 yrs / 7–10 yrs |
| Digital Score | 0 / 1 / 2 / 3 / 4 |
| Growth Stage | Nascent / Emerging / Growing / Thriving |
| Area Type | Rural / Semi-Urban / Urban |

---

## 🧰 Technology Stack

| Tool | Role |
|---|---|
| Python | Core analytics programming |
| Pandas | Data cleaning & KPI generation |
| NumPy | Numerical computations & synthetic data |
| Plotly | Interactive visual analytics |
| Streamlit | Live dashboard deployment |
| Kaleido | Static PNG chart export |

---

## 🖥️ Dashboard Modules

| Module | Description |
|---|---|
| 🏠 Overview | Growth stage distribution, revenue segments, demographics |
| 🗺️ Geographic | Zone revenue, state risk matrix, rural-urban radar |
| 📈 Business & Growth | Category revenue, profit margins, tenure trends, heatmap |
| 💻 Digital Adoption | Digital divide analysis, score vs revenue, online selling |
| 🎓 Training & Schemes | Training impact, SHG/mentor analysis, govt scheme analytics |
| ⚠️ Dropout Risk | Risk heatmap, funnel chart, high-risk segment table |

---

## 📁 Repository Structure

```
aatmanirbhar-naari-analytics/
│
├── data/                        ← Auto-generated (gitignored)
│   ├── naari_data.csv
│   └── naari_clean.csv
│
├── charts/                      ← Auto-generated PNG charts (gitignored)
│
├── generate_data.py             ← Synthetic dataset generator
├── eda.py                       ← Exploratory data analysis script
├── charts.py                    ← Static PNG chart generator
├── app.py                       ← Streamlit dashboard
├── requirements.txt             ← Python dependencies
└── README.md
```

---

## 🚀 How to Run Locally

### 1. Clone Repository
```bash
git clone https://github.com/Kreetikakishore/aatmanirbhar-naari-analytics.git
cd aatmanirbhar-naari-analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Dataset
```bash
python generate_data.py
```

### 4. Run EDA Analysis
```bash
python eda.py
```

### 5. Generate Static Charts (Optional)
```bash
python charts.py
```

### 6. Launch Dashboard
```bash
streamlit run app.py
```

### 7. Open Browser
```
http://localhost:8501
```

---

## 📌 Deliverables Produced

- ✅ Synthetic dataset of 2,000 entrepreneurs across 15 Indian states
- ✅ Full EDA report with KPIs, zone analysis & dropout risk factors
- ✅ 12 static PNG charts for reporting & presentation
- ✅ 6-module interactive Streamlit dashboard
- ✅ High-risk segment identification table with intervention flags
- ✅ Strategic recommendations for government policy planning

---

## ⚠️ Data Note

This project uses a **synthetic dataset** generated using realistic distributions
derived from NSSO 73rd Round (Unincorporated Sector Survey), MSME Annual Report
2022–23, and Bain & Co. Women Entrepreneurship in India Report.
No real personal data was used. Dataset covers 2,000 records × 28 features.

---

## 👤 Author

**Kreetika Kishore**
Data Analytics Portfolio Project | 2026

---

