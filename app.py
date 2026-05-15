# ============================================================
#  AATMANIRBHAR NAARI — DASHBOARD (Clean Final Version)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Aatmanirbhar Naari",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif !important; }

.stApp {
    background: linear-gradient(135deg, #f5f0ff 0%, #fff0f5 50%, #f0f5ff 100%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4a0080 0%, #8b0057 50%, #c2185b 100%) !important;
}
[data-testid="stSidebar"] * { color: #ffffff !important; }

.hero-banner {
    background: linear-gradient(135deg, #4a0080 0%, #8b0057 40%, #c2185b 70%, #e91e8c 100%);
    border-radius: 20px; padding: 36px 48px; margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(74,0,128,0.25);
}
.hero-title { font-size: 2.4rem; font-weight: 800; color: #fff; margin: 0 0 6px 0; }
.hero-sub   { font-size: 1.0rem; color: rgba(255,255,255,0.85); margin: 0 0 16px 0; }
.hero-badge {
    display: inline-block; background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.35); border-radius: 20px;
    padding: 4px 16px; font-size: 0.78rem; color: #fff; margin-right: 8px;
}
.hero-stat {
    display: inline-block; background: rgba(255,255,255,0.15);
    border-radius: 12px; padding: 10px 20px; margin: 12px 12px 0 0;
    border: 1px solid rgba(255,255,255,0.25);
}
.hero-stat-num { font-size:1.5rem; font-weight:700; color:#fff; display:block; }
.hero-stat-lbl { font-size:0.72rem; color:rgba(255,255,255,0.8); }

.kpi-card {
    background: white; border-radius: 16px; padding: 20px 24px;
    box-shadow: 0 4px 20px rgba(74,0,128,0.1); border-top: 4px solid;
    margin-bottom: 12px;
}
.kpi-value  { font-size:1.9rem; font-weight:800; color:#1a0030; display:block; line-height:1.1; }
.kpi-label  { font-size:0.78rem; color:#888; font-weight:500; text-transform:uppercase; letter-spacing:0.5px; }
.kpi-icon   { font-size:1.6rem; margin-bottom:6px; display:block; }
.kpi-delta  { font-size:0.75rem; font-weight:600; margin-top:6px; display:block; }
.delta-up   { color: #27ae60; }
.delta-down { color: #e74c3c; }

.section-header {
    display:flex; align-items:center; gap:12px;
    margin: 28px 0 16px 0; padding-bottom:10px;
    border-bottom: 2px solid #c2185b;
}
.section-title    { font-size:1.2rem; font-weight:700; color:#4a0080; margin:0; }
.section-subtitle { font-size:0.8rem; color:#999; margin:0; }

.insight-card {
    background: linear-gradient(135deg, #fff0f8, #f8f0ff);
    border-left: 5px solid #8b0057; border-radius: 12px;
    padding: 14px 18px; margin: 8px 0;
    box-shadow: 0 2px 12px rgba(139,0,87,0.08);
    font-size: 0.88rem; color: #333; line-height: 1.6;
}
.insight-card b { color: #4a0080; }

.stTabs [data-baseweb="tab-list"] {
    background: rgba(74,0,128,0.06); border-radius: 14px; padding: 6px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px; font-weight: 600; font-size: 0.85rem; color: #4a0080;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7b2d8b, #c2185b) !important;
    color: white !important;
}
div[data-testid="metric-container"] {
    background: white; border-radius: 12px;
    box-shadow: 0 2px 12px rgba(74,0,128,0.08);
}
</style>
""", unsafe_allow_html=True)
# ============================================================
#  PIECE 2/6 — Plotly Theme + Data Loader + Sidebar
# ============================================================

# ── PLOTLY THEME ──────────────────────────────────────────────
PLOT_LAYOUT = dict(
    font=dict(family="Poppins, Arial", size=13, color="#1a0030"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=50, b=40, l=40, r=30),
    title_font=dict(size=15, color="#4a0080", family="Poppins"),
)
GROWTH_COLORS = {
    "Thriving": "#27ae60",
    "Growing":  "#2980b9",
    "Emerging": "#f39c12",
    "Nascent":  "#e74c3c"
}
ZONE_COLORS = {
    "North":     "#7b2d8b",
    "South":     "#c2185b",
    "East":      "#2980b9",
    "West":      "#27ae60",
    "Central":   "#f39c12",
    "Northeast": "#e67e22"
}

# ── DATA LOADER ───────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/naari_clean.csv")
    except FileNotFoundError:
        try:
            df = pd.read_csv("data/naari_data.csv")
        except FileNotFoundError:
            st.error("❌ Dataset not found. Run python generate_data.py first.")
            st.stop()
        df["AgeGroup"] = pd.cut(
            df["Age"], bins=[17,25,35,45,60],
            labels=["18–25","26–35","36–45","46–60"])
        df["RevenueSegment"] = pd.cut(
            df["MonthlyRevenue"],
            bins=[0,10000,25000,50000,999999],
            labels=["Low (<₹10K)","Medium (₹10K–25K)",
                    "High (₹25K–50K)","Premium (>₹50K)"])
        df["ProfitMargin"] = (
            df["MonthlyProfit"] / df["MonthlyRevenue"] * 100
        ).round(1)
    return df

df = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px 0;'>
        <div style='font-size:3rem;'>🪷</div>
        <div style='font-size:1.3rem; font-weight:800; color:#ffe0f0;'>
            Aatmanirbhar Naari
        </div>
        <div style='font-size:0.88rem; color:rgba(255,255,255,0.9); margin-top:4px;'>
            Home Business Enablement Portal
        </div>
        <div style='height:2px; background:rgba(255,255,255,0.2);
                    border-radius:2px; margin:14px 0;'></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 Filters")

    zones_all = sorted(df["Zone"].unique())
    sel_zones = st.multiselect(
        "🗺️ Zone", zones_all, default=zones_all)

    area_all = sorted(df["AreaType"].unique())
    sel_area = st.multiselect(
        "🏘️ Area Type", area_all, default=area_all)

    cat_all = sorted(df["BusinessCategory"].unique())
    sel_cat = st.multiselect(
        "🏭 Business Category", cat_all, default=cat_all)

    stage_all = ["Nascent","Emerging","Growing","Thriving"]
    sel_stage = st.multiselect(
        "📈 Growth Stage", stage_all, default=stage_all)

    age_range = st.slider("🎂 Age Range", 18, 60, (18, 60))

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.88rem; color:rgba(255,255,255,0.85);
                line-height:1.8;'>
        <b style='color:#ffe0f0;'>📊 Data Coverage</b><br>
        2,000 entrepreneurs<br>
        15 Indian states<br>
        10 business categories<br>
        28 data dimensions
    </div>
    """, unsafe_allow_html=True)

# ── APPLY FILTERS ─────────────────────────────────────────────
fdf = df[
    df["Zone"].isin(sel_zones) &
    df["AreaType"].isin(sel_area) &
    df["BusinessCategory"].isin(sel_cat) &
    df["GrowthStage"].isin(sel_stage) &
    df["Age"].between(age_range[0], age_range[1])
].copy()

if len(fdf) == 0:
    st.warning("⚠️ No data matches the selected filters. Please adjust.")
    st.stop()
# ============================================================
#  PIECE 3/6 — Hero Banner + KPI Cards + Tabs
# ============================================================

# ── CALCULATIONS ──────────────────────────────────────────────
total_rev_cr = fdf["AnnualRevenue"].sum() / 1e7
thriving_pct = (fdf["GrowthStage"] == "Thriving").mean() * 100
dropout_rate = fdf["PortalDropout"].mean() * 100
avg_rev      = fdf["MonthlyRevenue"].mean()
avg_prof     = fdf["MonthlyProfit"].mean()
avg_margin   = fdf["ProfitMargin"].mean()
active_pct   = (fdf["PortalDropout"] == 0).mean() * 100
digital_pct  = (fdf["DigitalScore"] >= 2).mean() * 100
shg_pct      = fdf["SHGMember"].mean() * 100
loan_pct     = fdf["HasLoan"].mean() * 100

# ── HERO BANNER ───────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    <p style='font-size:0.95rem; color:rgba(255,255,255,0.9);
              font-weight:500; margin:0 0 8px 0;'>
    </p>
    <h1 style='font-size:2.4rem; font-weight:800; color:#ffffff;
               margin:0 0 8px 0; text-shadow:0 2px 8px rgba(0,0,0,0.2);'>
        🪷 Aatmanirbhar Naari — Women Home Business Intelligence Platform
    </h1>
    <p style='font-size:1rem; color:rgba(255,255,255,0.88);
              font-weight:400; margin:0 0 16px 0;'>
        Home Business Enablement Portal &nbsp;·&nbsp;
        Data-Driven Insights for Women Entrepreneurs across India
    </p>
    <span class="hero-badge">📅 FY 2024–25</span>
    <span class="hero-badge">🇮🇳 Pan-India Initiative</span>
    <span class="hero-badge">✅ Live Dashboard</span>
    <br>
    <div class="hero-stat">
        <span class="hero-stat-num">{len(fdf):,}</span>
        <span class="hero-stat-lbl">Entrepreneurs</span>
    </div>
    <div class="hero-stat">
        <span class="hero-stat-num">₹{total_rev_cr:.1f} Cr</span>
        <span class="hero-stat-lbl">Annual Revenue</span>
    </div>
    <div class="hero-stat">
        <span class="hero-stat-num">{thriving_pct:.1f}%</span>
        <span class="hero-stat-lbl">Thriving Stage</span>
    </div>
    <div class="hero-stat">
        <span class="hero-stat-num">{fdf['State'].nunique()}</span>
        <span class="hero-stat-lbl">States Covered</span>
    </div>
    <div class="hero-stat">
        <span class="hero-stat-num">{100 - dropout_rate:.1f}%</span>
        <span class="hero-stat-lbl">Portal Retention</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI ROW 1 ─────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
kpi_style = """
    background:white; border-radius:16px; padding:22px 24px;
    box-shadow:0 4px 20px rgba(74,0,128,0.12);
    border-top:5px solid {color}; margin-bottom:12px;
"""
for col_obj, icon, value, label, delta, delta_type, color in [
    (c1,"💰", f"₹{avg_rev:,.0f}",  "Avg Monthly Revenue",
     "Per entrepreneur",            "up",   "#7b2d8b"),
    (c2,"📈", f"₹{avg_prof:,.0f}", "Avg Monthly Profit",
     f"{avg_margin:.1f}% margin",   "up",   "#c0392b"),
    (c3,"✅", f"{active_pct:.1f}%","Portal Active Rate",
     f"{int(fdf['PortalDropout'].eq(0).sum()):,} active", "up", "#27ae60"),
    (c4,"💻", f"{digital_pct:.1f}%","Digitally Enabled",
     "Score ≥ 2 out of 4",          "up",   "#2980b9"),
]:
    col_obj.markdown(f"""
    <div style='{kpi_style.format(color=color)}'>
        <div style='font-size:1.8rem; margin-bottom:8px;'>{icon}</div>
        <div style='font-size:1.85rem; font-weight:800;
                    color:#1a0030; line-height:1.1;
                    margin-bottom:5px;'>{value}</div>
        <div style='font-size:0.82rem; color:#555; font-weight:600;
                    text-transform:uppercase;
                    letter-spacing:0.5px;'>{label}</div>
        <div style='font-size:0.78rem; font-weight:600;
                    color:{"#27ae60" if delta_type=="up" else "#e74c3c"};
                    margin-top:6px;'>
            {"↑" if delta_type=="up" else "↓"} {delta}
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:4px'></div>",
            unsafe_allow_html=True)

# ── KPI ROW 2 ─────────────────────────────────────────────────
c5, c6, c7, c8 = st.columns(4)
for col_obj, icon, value, label, delta, delta_type, color in [
    (c5,"🤝", f"{shg_pct:.1f}%",
     "SHG Members",         "Community strength",   "up",   "#e67e22"),
    (c6,"🏛️", f"{loan_pct:.1f}%",
     "Loan Access Rate",    "Inclusion gap exists", "down", "#8e44ad"),
    (c7,"🎓", f"{fdf['TrainingsAttended'].mean():.1f}",
     "Avg Trainings",       "Per entrepreneur",     "up",   "#16a085"),
    (c8,"🏆", f"{thriving_pct:.1f}%",
     "Thriving Stage",      "Highest growth tier",  "up",   "#7b2d8b"),
]:
    col_obj.markdown(f"""
    <div style='{kpi_style.format(color=color)}'>
        <div style='font-size:1.8rem; margin-bottom:8px;'>{icon}</div>
        <div style='font-size:1.85rem; font-weight:800;
                    color:#1a0030; line-height:1.1;
                    margin-bottom:5px;'>{value}</div>
        <div style='font-size:0.82rem; color:#555; font-weight:600;
                    text-transform:uppercase;
                    letter-spacing:0.5px;'>{label}</div>
        <div style='font-size:0.78rem; font-weight:600;
                    color:{"#27ae60" if delta_type=="up" else "#e74c3c"};
                    margin-top:6px;'>
            {"↑" if delta_type=="up" else "↓"} {delta}
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠  Overview",
    "🗺️  Geographic",
    "📈  Business & Growth",
    "💻  Digital Adoption",
    "🎓  Training & Schemes",
    "⚠️  Dropout Risk"
])
# ============================================================
#  PIECE 4/6 — Tab 1: Overview + Tab 2: Geographic
# ============================================================

# ══════════════════════════════════════════════════════════════
#  TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>📊</span>
        <div>
            <p class="section-title">Platform Overview</p>
            <p class="section-subtitle">Growth distribution, demographics & revenue profile</p>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.1, 1.1, 1.3])

    with col1:
        gs = fdf["GrowthStage"].value_counts().reset_index()
        gs.columns = ["Stage","Count"]
        fig = go.Figure(go.Pie(
            labels=gs["Stage"], values=gs["Count"],
            hole=0.6,
            marker_colors=[GROWTH_COLORS.get(s,"#999")
                           for s in gs["Stage"]],
            textinfo="label+percent",
            textfont=dict(size=13, color="#1a0030"),
            pull=[0.04 if s=="Thriving" else 0
                  for s in gs["Stage"]],
            hovertemplate="<b>%{label}</b><br>"
                          "Count: %{value:,}<br>"
                          "%{percent}<extra></extra>"
        ))
        fig.add_annotation(
            text=f"<b>{len(fdf):,}</b><br>"
                 f"<span style='font-size:11px'>Total</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#4a0080",
                      family="Poppins")
        )
        fig.update_layout(
            title=dict(text="Growth Stage Distribution",
                       font=dict(size=15, color="#4a0080")),
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            margin=dict(t=50,b=20,l=10,r=10),
            legend=dict(font=dict(size=12, color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)")
        )
        st.plotly_chart(fig, width='stretch')

    with col2:
        area_gs = fdf.groupby(["AreaType","GrowthStage"])\
                     .size().reset_index(name="Count")
        fig2 = px.bar(area_gs, x="AreaType", y="Count",
            color="GrowthStage",
            color_discrete_map=GROWTH_COLORS,
            barmode="stack",
            labels={"Count":"Entrepreneurs",
                    "GrowthStage":"Stage","AreaType":""},
            title="Growth by Area Type")
        fig2.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            margin=dict(t=50,b=20,l=10,r=10),
            legend=dict(font=dict(size=12, color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)")
        )
        st.plotly_chart(fig2, width='stretch')

    with col3:
        order = ["Low (<₹10K)","Medium (₹10K–25K)",
                 "High (₹25K–50K)","Premium (>₹50K)"]
        rs = fdf["RevenueSegment"].value_counts()\
                                   .reindex(order).reset_index()
        rs.columns = ["Segment","Count"]
        rs["Pct"] = (rs["Count"]/rs["Count"].sum()*100).round(1)
        fig3 = px.bar(rs, x="Count", y="Segment",
            orientation="h",
            color="Segment",
            color_discrete_sequence=["#e74c3c","#f39c12",
                                      "#2980b9","#27ae60"],
            text=rs.apply(
                lambda r: f"{r['Count']:,}  ({r['Pct']}%)",
                axis=1),
            labels={"Count":"Entrepreneurs","Segment":""},
            title="Revenue Segment Breakdown")
        fig3.update_traces(textposition="outside",
                           textfont=dict(size=12,
                                         color="#1a0030"))
        fig3.update_layout(
            height=360, showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig3, width='stretch')

    # Demographics
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>👩</span>
        <div>
            <p class="section-title">Demographic Profile</p>
            <p class="section-subtitle">Age, education & marital status</p>
        </div>
    </div>""", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        age_data = fdf["AgeGroup"].value_counts().reset_index()
        age_data.columns = ["AgeGroup","Count"]
        fig4 = px.pie(age_data,
            names="AgeGroup", values="Count", hole=0.45,
            color_discrete_sequence=["#7b2d8b","#c2185b",
                                      "#f39c12","#2980b9"],
            title="Age Group Distribution")
        fig4.update_traces(
            textinfo="label+percent",
            textfont=dict(size=12, color="#1a0030"))
        fig4.update_layout(
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            margin=dict(t=50,b=20,l=10,r=10),
            legend=dict(font=dict(size=12, color="#1a0030"))
        )
        st.plotly_chart(fig4, width='stretch')

    with col5:
        edu_order = ["No Formal Education","Primary (1–5)",
                     "Secondary (6–10)",
                     "Higher Secondary (11–12)",
                     "Graduate","Post-Graduate"]
        edu_rev = fdf.groupby("Education", observed=True)\
                     ["MonthlyRevenue"].mean()\
                     .reindex(edu_order).reset_index()
        edu_rev.columns = ["Education","AvgRevenue"]
        edu_rev["Short"] = ["None","Primary","Sec",
                            "Hgr Sec","Grad","PG"]
        fig5 = go.Figure(go.Bar(
            x=edu_rev["Short"],
            y=edu_rev["AvgRevenue"],
            marker=dict(
                color=edu_rev["AvgRevenue"],
                colorscale=[[0,"#f9c6d0"],
                             [0.5,"#c2185b"],
                             [1,"#4a0080"]],
                showscale=False
            ),
            text=[f"₹{v:,.0f}" for v in edu_rev["AvgRevenue"]],
            textposition="outside",
            textfont=dict(size=12, color="#1a0030"),
            hovertemplate="<b>%{x}</b><br>"
                          "₹%{y:,.0f}<extra></extra>"
        ))
        fig5.update_layout(
            title=dict(text="Revenue by Education",
                       font=dict(size=15, color="#4a0080")),
            yaxis_title="Avg Revenue (₹)",
            yaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            xaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig5, width='stretch')

    with col6:
        marital_rev = fdf.groupby("MaritalStatus")\
                         ["MonthlyRevenue"].mean().reset_index()
        marital_cnt = fdf["MaritalStatus"]\
                         .value_counts().reset_index()
        marital_cnt.columns = ["MaritalStatus","Count"]
        m_data = marital_rev.merge(marital_cnt,
                                    on="MaritalStatus")
        fig6 = px.scatter(m_data,
            x="MonthlyRevenue", y="Count",
            size="MonthlyRevenue", color="MaritalStatus",
            text="MaritalStatus",
            color_discrete_sequence=["#7b2d8b","#c2185b",
                                      "#f39c12","#2980b9"],
            labels={"MonthlyRevenue":"Avg Revenue (₹)",
                    "Count":"No. of Entrepreneurs"},
            title="Marital Status: Count vs Revenue")
        fig6.update_traces(
            textposition="top center",
            textfont=dict(size=12, color="#1a0030"))
        fig6.update_layout(
            height=340, showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig6, width='stretch')

    st.markdown("""
    <div class="insight-card">
        💡 <b>Graduate entrepreneurs earn 35–40% more</b> than
        those with no formal education — making education-linked
        training a top priority for the portal.
    </div>
    <div class="insight-card">
        💡 <b>The 36–45 age group dominates</b> the platform.
        The 18–25 group shows highest growth potential and
        needs targeted onboarding support.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  TAB 2 — GEOGRAPHIC
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>🗺️</span>
        <div>
            <p class="section-title">Geographic Intelligence</p>
            <p class="section-subtitle">Zone, state & rural-urban performance</p>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        zone_data = fdf.groupby("Zone").agg(
            Count=("EntrepreneurID","count"),
            AvgRevenue=("MonthlyRevenue","mean"),
            DropoutRate=("PortalDropout","mean"),
            DigitalScore=("DigitalScore","mean"),
            Thriving=("GrowthStage",
                      lambda x: (x=="Thriving").mean())
        ).reset_index()
        fig = px.bar(zone_data, x="Zone", y="AvgRevenue",
            color="Zone",
            color_discrete_map=ZONE_COLORS,
            text=[f"₹{v:,.0f}" for v in zone_data["AvgRevenue"]],
            custom_data=["Count","DropoutRate","Thriving"],
            labels={"AvgRevenue":"Avg Revenue (₹)","Zone":""},
            title="Zone-wise Avg Monthly Revenue")
        fig.update_traces(
            textposition="outside",
            textfont=dict(size=12, color="#1a0030"),
            hovertemplate="<b>%{x}</b><br>"
                          "Revenue: ₹%{y:,.0f}<br>"
                          "Count: %{customdata[0]:,}<br>"
                          "Dropout: %{customdata[1]:.1%}<br>"
                          "Thriving: %{customdata[2]:.1%}"
                          "<extra></extra>"
        )
        fig.update_layout(
            showlegend=False, height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            margin=dict(t=50,b=20,l=10,r=10),
            yaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            xaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030"))
        )
        st.plotly_chart(fig, width='stretch')

    with col2:
        fig2 = px.scatter(zone_data,
            x="DigitalScore", y="AvgRevenue",
            size="Count", color="Zone", text="Zone",
            color_discrete_map=ZONE_COLORS, size_max=55,
            labels={"DigitalScore":"Avg Digital Score",
                    "AvgRevenue":"Avg Revenue (₹)"},
            title="Digital Score vs Revenue by Zone")
        fig2.update_traces(
            textposition="top center",
            textfont=dict(size=12, color="#1a0030"),
            hovertemplate="<b>%{text}</b><br>"
                          "Score: %{x:.2f}<br>"
                          "Revenue: ₹%{y:,.0f}"
                          "<extra></extra>"
        )
        fig2.update_layout(
            showlegend=False, height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig2, width='stretch')

    # State level
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>📍</span>
        <div>
            <p class="section-title">State-wise Deep Dive</p>
            <p class="section-subtitle">Revenue rankings & risk matrix</p>
        </div>
    </div>""", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        state_data = fdf.groupby("State").agg(
            Count=("EntrepreneurID","count"),
            AvgRevenue=("MonthlyRevenue","mean"),
            DropoutRate=("PortalDropout","mean"),
            Thriving=("GrowthStage",
                      lambda x: (x=="Thriving").mean())
        ).reset_index().sort_values("AvgRevenue",
                                     ascending=True)
        fig3 = go.Figure(go.Bar(
            x=state_data["AvgRevenue"],
            y=state_data["State"],
            orientation="h",
            marker=dict(
                color=state_data["AvgRevenue"],
                colorscale=[[0,"#f9c6d0"],
                             [0.5,"#c2185b"],
                             [1,"#4a0080"]],
                showscale=True,
                colorbar=dict(title="₹",thickness=12,
                              tickfont=dict(size=11,
                                            color="#1a0030"))
            ),
            text=[f"₹{v:,.0f}"
                  for v in state_data["AvgRevenue"]],
            textposition="outside",
            textfont=dict(size=11, color="#1a0030"),
            customdata=state_data[["Count","DropoutRate",
                                    "Thriving"]].values,
            hovertemplate="<b>%{y}</b><br>"
                          "Revenue: ₹%{x:,.0f}<br>"
                          "Count: %{customdata[0]:,}<br>"
                          "Dropout: %{customdata[1]:.1%}<br>"
                          "Thriving: %{customdata[2]:.1%}"
                          "<extra></extra>"
        ))
        fig3.update_layout(
            title=dict(text="All States — Avg Monthly Revenue",
                       font=dict(size=15, color="#4a0080")),
            xaxis_title="Avg Revenue (₹)",
            yaxis_title="",
            xaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            height=520,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=12,
                      color="#1a0030"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig3, width='stretch')

    with col4:
        state_bubble = fdf.groupby("State").agg(
            AvgRevenue=("MonthlyRevenue","mean"),
            DropoutRate=("PortalDropout","mean"),
            Count=("EntrepreneurID","count"),
            DigitalScore=("DigitalScore","mean")
        ).reset_index()
        fig4 = px.scatter(state_bubble,
            x="DropoutRate", y="AvgRevenue",
            size="Count", color="DigitalScore",
            text="State",
            color_continuous_scale=["#f9c6d0",
                                     "#8b0057","#4a0080"],
            size_max=45,
            labels={"DropoutRate":"Dropout Rate",
                    "AvgRevenue":"Avg Revenue (₹)",
                    "DigitalScore":"Digital Score"},
            title="State Risk Matrix: Revenue vs Dropout")
        fig4.update_traces(
            textposition="top center",
            textfont=dict(size=10, color="#1a0030"),
            hovertemplate="<b>%{text}</b><br>"
                          "Dropout: %{x:.1%}<br>"
                          "Revenue: ₹%{y:,.0f}"
                          "<extra></extra>"
        )
        fig4.update_xaxes(
            tickformat=".0%",
            tickfont=dict(size=12, color="#1a0030"))
        fig4.update_yaxes(
            tickfont=dict(size=12, color="#1a0030"))
        fig4.update_layout(
            height=520,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig4, width='stretch')

    # Radar
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>🏘️</span>
        <div>
            <p class="section-title">Area Type Comparison</p>
            <p class="section-subtitle">Multi-dimension radar analysis</p>
        </div>
    </div>""", unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        area_comp = fdf.groupby("AreaType").agg(
            AvgRevenue=("MonthlyRevenue","mean"),
            DigitalScore=("DigitalScore","mean"),
            SHGMember=("SHGMember","mean"),
            LoanUptake=("HasLoan","mean"),
            TrainingsAttended=("TrainingsAttended","mean"),
            Thriving=("GrowthStage",
                      lambda x: (x=="Thriving").mean())
        ).reset_index()
        cats    = ["Revenue","Digital","SHG",
                   "Loan","Training","Thriving"]
        metrics = ["AvgRevenue","DigitalScore","SHGMember",
                   "LoanUptake","TrainingsAttended","Thriving"]
        area_colors = {"Rural":"#e74c3c",
                       "Semi-Urban":"#f39c12",
                       "Urban":"#27ae60"}
        fig5 = go.Figure()
        for _, row in area_comp.iterrows():
            raw  = [row[m] for m in metrics]
            mn   = [min(area_comp[m]) for m in metrics]
            mx   = [max(area_comp[m]) for m in metrics]
            vals = [(v-mn[i])/(mx[i]-mn[i]+1e-9)
                    for i,v in enumerate(raw)]
            vals += [vals[0]]
            fig5.add_trace(go.Scatterpolar(
                r=vals, theta=cats+[cats[0]],
                fill="toself",
                name=row["AreaType"],
                line_color=area_colors.get(
                    row["AreaType"],"gray"),
                fillcolor=area_colors.get(
                    row["AreaType"],"gray"),
                opacity=0.25
            ))
        fig5.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, range=[0,1],
                    tickfont=dict(size=11,
                                   color="#1a0030")),
                angularaxis=dict(
                    tickfont=dict(size=12,
                                   color="#1a0030"))
            ),
            title=dict(
                text="Area Type Multi-Dimension Radar",
                font=dict(size=15, color="#4a0080")),
            height=420,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            legend=dict(font=dict(size=12,
                                   color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(t=60,b=20,l=10,r=10)
        )
        st.plotly_chart(fig5, width='stretch')

    with col6:
        area_table = fdf.groupby("AreaType").agg(
            Entrepreneurs=("EntrepreneurID","count"),
            AvgRevenue=("MonthlyRevenue","mean"),
            AvgProfit=("MonthlyProfit","mean"),
            DigitalScore=("DigitalScore","mean"),
            DropoutRate=("PortalDropout","mean"),
            SHGMember=("SHGMember","mean"),
            LoanAccess=("HasLoan","mean"),
            Thriving=("GrowthStage",
                      lambda x: (x=="Thriving").mean())
        ).reset_index()
        area_table["AvgRevenue"]  = area_table["AvgRevenue"]\
            .apply(lambda x: f"₹{x:,.0f}")
        area_table["AvgProfit"]   = area_table["AvgProfit"]\
            .apply(lambda x: f"₹{x:,.0f}")
        area_table["DigitalScore"]= area_table["DigitalScore"]\
            .apply(lambda x: f"{x:.2f}/4")
        area_table["DropoutRate"] = area_table["DropoutRate"]\
            .apply(lambda x: f"{x:.1%}")
        area_table["SHGMember"]   = area_table["SHGMember"]\
            .apply(lambda x: f"{x:.1%}")
        area_table["LoanAccess"]  = area_table["LoanAccess"]\
            .apply(lambda x: f"{x:.1%}")
        area_table["Thriving"]    = area_table["Thriving"]\
            .apply(lambda x: f"{x:.1%}")
        st.markdown("#### 📋 Area-wise Summary Table")
        st.dataframe(area_table, width='stretch',
                     hide_index=True, height=340)

    st.markdown("""
    <div class="insight-card">
        💡 <b>West Zone leads</b> in avg revenue (₹22,627)
        while Northeast has the lowest digital adoption (1.77/4).
        High-dropout states also show below-average revenue —
        a compounding vulnerability needing urgent intervention.
    </div>""", unsafe_allow_html=True)
# ============================================================
#  PIECE 5/6 — Tab 3: Business & Growth + Tab 4: Digital
# ============================================================

# ══════════════════════════════════════════════════════════════
#  TAB 3 — BUSINESS & GROWTH
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>📈</span>
        <div>
            <p class="section-title">Business & Growth Analytics</p>
            <p class="section-subtitle">Category revenue, profit margins & tenure trends</p>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        biz = fdf.groupby("BusinessCategory").agg(
            AvgRevenue=("MonthlyRevenue","mean"),
            AvgProfit=("MonthlyProfit","mean"),
            Count=("EntrepreneurID","count"),
            OnlineSellers=("SellsOnline","mean")
        ).reset_index().sort_values("AvgRevenue")
        fig = go.Figure(go.Bar(
            x=biz["AvgRevenue"],
            y=biz["BusinessCategory"],
            orientation="h",
            marker=dict(
                color=biz["AvgRevenue"],
                colorscale=[[0,"#f9c6d0"],
                             [0.5,"#8b0057"],
                             [1,"#4a0080"]],
                showscale=False
            ),
            text=[f"₹{v:,.0f}" for v in biz["AvgRevenue"]],
            textposition="outside",
            textfont=dict(size=12, color="#1a0030"),
            customdata=biz[["Count","AvgProfit",
                             "OnlineSellers"]].values,
            hovertemplate="<b>%{y}</b><br>"
                          "Revenue: ₹%{x:,.0f}<br>"
                          "Profit: ₹%{customdata[1]:,.0f}<br>"
                          "Count: %{customdata[0]:,}<br>"
                          "Online: %{customdata[2]:.1%}"
                          "<extra></extra>"
        ))
        fig.update_layout(
            title=dict(text="Avg Revenue by Category",
                       font=dict(size=15, color="#4a0080")),
            xaxis_title="Avg Revenue (₹)",
            yaxis_title="",
            xaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            height=440,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=12,
                      color="#1a0030"),
            margin=dict(t=50,b=20,l=10,r=20)
        )
        st.plotly_chart(fig, width='stretch')

    with col2:
        fig2 = px.scatter(biz,
            x="AvgRevenue", y="AvgProfit",
            size="Count", color="OnlineSellers",
            text="BusinessCategory",
            color_continuous_scale=["#f9c6d0",
                                     "#8b0057","#4a0080"],
            size_max=50,
            labels={"AvgRevenue":"Avg Revenue (₹)",
                    "AvgProfit":"Avg Profit (₹)",
                    "OnlineSellers":"Online %"},
            title="Revenue vs Profit Bubble Chart")
        fig2.update_traces(
            textposition="top center",
            textfont=dict(size=9, color="#1a0030"),
            hovertemplate="<b>%{text}</b><br>"
                          "Revenue: ₹%{x:,.0f}<br>"
                          "Profit: ₹%{y:,.0f}"
                          "<extra></extra>"
        )
        fig2.update_layout(
            height=440,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig2, width='stretch')

    col3, col4 = st.columns(2)
    with col3:
        margin_data = fdf.groupby("BusinessCategory")\
                         ["ProfitMargin"].mean()\
                         .reset_index()\
                         .sort_values("ProfitMargin")
        margin_data.columns = ["Category","AvgMargin"]
        fig3 = px.bar(margin_data,
            x="AvgMargin", y="Category",
            orientation="h",
            color="AvgMargin",
            color_continuous_scale=["#f9c6d0","#27ae60"],
            text=[f"{v:.1f}%"
                  for v in margin_data["AvgMargin"]],
            labels={"AvgMargin":"Profit Margin (%)"},
            title="Profit Margin % by Category")
        fig3.update_traces(
            textposition="outside",
            textfont=dict(size=12, color="#1a0030"))
        fig3.update_layout(
            coloraxis_showscale=False,
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=12,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            yaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            xaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            margin=dict(t=50,b=20,l=10,r=20)
        )
        st.plotly_chart(fig3, width='stretch')

    with col4:
        tenure_data = fdf.groupby("YearsInBusiness").agg(
            AvgRevenue=("MonthlyRevenue","mean"),
            MedianRevenue=("MonthlyRevenue","median"),
            Count=("EntrepreneurID","count")
        ).reset_index()
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=tenure_data["YearsInBusiness"],
            y=tenure_data["Count"],
            name="Count", yaxis="y2",
            marker_color="rgba(194,24,91,0.15)",
            hovertemplate="Year %{x}: %{y} entrepreneurs"
                          "<extra></extra>"
        ))
        fig4.add_trace(go.Scatter(
            x=tenure_data["YearsInBusiness"],
            y=tenure_data["AvgRevenue"],
            mode="lines+markers",
            name="Avg Revenue",
            line=dict(color="#8b0057", width=3),
            marker=dict(size=9, color="#8b0057"),
            hovertemplate="Year %{x}: ₹%{y:,.0f}"
                          "<extra></extra>"
        ))
        fig4.add_trace(go.Scatter(
            x=tenure_data["YearsInBusiness"],
            y=tenure_data["MedianRevenue"],
            mode="lines+markers",
            name="Median Revenue",
            line=dict(color="#c2185b", width=2,
                      dash="dot"),
            marker=dict(size=7, color="#c2185b"),
            hovertemplate="Year %{x}: ₹%{y:,.0f}"
                          "<extra></extra>"
        ))
        fig4.update_layout(
            title=dict(
                text="Revenue Growth vs Years in Business",
                font=dict(size=15, color="#4a0080")),
            xaxis_title="Years in Business",
            yaxis_title="Monthly Revenue (₹)",
            yaxis2=dict(
    title=dict(
        text="Count",
        font=dict(size=12, color="#1a0030")
    ),
    overlaying="y", side="right",
    showgrid=False,
    tickfont=dict(size=11, color="#1a0030")
),
            xaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            legend=dict(orientation="h", y=1.12,
                        font=dict(size=12,
                                   color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(t=60,b=20,l=10,r=10)
        )
        st.plotly_chart(fig4, width='stretch')

    # Heatmap
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>🔥</span>
        <div>
            <p class="section-title">Revenue Heatmap</p>
            <p class="section-subtitle">Business Category × Area Type</p>
        </div>
    </div>""", unsafe_allow_html=True)

    heat = fdf.groupby(["BusinessCategory","AreaType"])\
              ["MonthlyRevenue"].mean().reset_index()
    pivot = heat.pivot(index="BusinessCategory",
                       columns="AreaType",
                       values="MonthlyRevenue")
    fig5 = px.imshow(pivot,
        color_continuous_scale=[[0,"#fff0f5"],
                                  [0.5,"#c2185b"],
                                  [1,"#4a0080"]],
        text_auto=".0f", aspect="auto",
        labels={"color":"Avg Revenue (₹)"},
        title="Avg Revenue (₹): Category × Area Type")
    fig5.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins", size=13,
                  color="#1a0030"),
        title_font=dict(size=15, color="#4a0080"),
        xaxis=dict(tickfont=dict(size=12,
                                  color="#1a0030")),
        yaxis=dict(tickfont=dict(size=11,
                                  color="#1a0030")),
        margin=dict(t=50,b=20,l=10,r=10)
    )
    st.plotly_chart(fig5, width='stretch')

    st.markdown("""
    <div class="insight-card">
        💡 <b>Digital Services (₹32,498) and Retail & Trading
        (₹30,222)</b> are top-earning categories. Urban
        entrepreneurs earn 35–45% more than Rural peers.
        Handicraft & Agriculture need focused revenue
        enhancement programs.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  TAB 4 — DIGITAL ADOPTION
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>💻</span>
        <div>
            <p class="section-title">Digital Adoption Intelligence</p>
            <p class="section-subtitle">Smartphone, payments, social media & online selling</p>
        </div>
    </div>""", unsafe_allow_html=True)
# Digital KPI cards
    d1, d2, d3, d4 = st.columns(4)
    dig_kpis = {
        "📱 Smartphone":   (fdf["HasSmartphone"].mean(),    "#7b2d8b"),
        "💳 Digital Pay":  (fdf["UsesDigitalPayment"].mean(),"#c2185b"),
        "📲 Social Media": (fdf["UsesSocialMedia"].mean(),   "#2980b9"),
        "🛒 Sells Online": (fdf["SellsOnline"].mean(),       "#27ae60"),
    }
    for col_obj, (label, (val, color)) in zip(
        [d1,d2,d3,d4], dig_kpis.items()
    ):
        col_obj.markdown(f"""
        <div style='background:white; border-radius:14px;
                    padding:20px; border-top:4px solid {color};
                    text-align:center;
                    box-shadow:0 4px 16px rgba(74,0,128,0.1);'>
            <div style='font-size:2rem;'>{label.split()[0]}</div>
            <div style='font-size:1.9rem; font-weight:800;
                        color:{color}; margin:6px 0;'>{val:.1%}</div>
            <div style='font-size:0.85rem; color:#333;
                        font-weight:600;'>
                {" ".join(label.split()[1:])}
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        dig_stage = fdf.groupby(
            ["DigitalScore","GrowthStage"])\
            .size().reset_index(name="Count")
        fig = px.bar(dig_stage,
            x="DigitalScore", y="Count",
            color="GrowthStage",
            color_discrete_map=GROWTH_COLORS,
            barmode="stack",
            labels={"DigitalScore":"Digital Score (0–4)",
                    "Count":"Entrepreneurs",
                    "GrowthStage":"Stage"},
            title="Digital Score by Growth Stage")
        fig.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13, color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            xaxis=dict(tickfont=dict(size=12, color="#1a0030")),
            yaxis=dict(tickfont=dict(size=12, color="#1a0030")),
            legend=dict(font=dict(size=12, color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig, width='stretch')

    with col2:
        dig_rev = fdf.groupby("DigitalScore").agg(
            AvgRevenue=("MonthlyRevenue","mean"),
            Count=("EntrepreneurID","count")
        ).reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=dig_rev["DigitalScore"],
            y=dig_rev["Count"],
            name="Count", yaxis="y2",
            marker_color="rgba(194,24,91,0.15)",
            hovertemplate="Score %{x}: %{y}<extra></extra>"
        ))
        fig2.add_trace(go.Scatter(
            x=dig_rev["DigitalScore"],
            y=dig_rev["AvgRevenue"],
            mode="lines+markers+text",
            name="Avg Revenue",
            text=[f"₹{v:,.0f}" for v in dig_rev["AvgRevenue"]],
            textposition="top center",
            textfont=dict(size=11, color="#1a0030"),
            line=dict(color="#8b0057", width=3),
            marker=dict(size=12, color="#8b0057"),
            hovertemplate="Score %{x}: ₹%{y:,.0f}<extra></extra>"
        ))
        fig2.update_layout(
            title=dict(text="Digital Score vs Avg Revenue",
                       font=dict(size=15, color="#4a0080")),
            xaxis_title="Digital Score",
            yaxis_title="Avg Revenue (₹)",
            yaxis2=dict(
                title=dict(text="Count",
                           font=dict(size=12, color="#1a0030")),
                overlaying="y", side="right",
                showgrid=False,
                tickfont=dict(size=11, color="#1a0030")
            ),
            xaxis=dict(tickfont=dict(size=12, color="#1a0030")),
            yaxis=dict(tickfont=dict(size=12, color="#1a0030")),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13, color="#1a0030"),
            legend=dict(orientation="h", y=1.12,
                        font=dict(size=12, color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(t=60,b=20,l=10,r=10)
        )
        st.plotly_chart(fig2, width='stretch')

    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>📡</span>
        <div>
            <p class="section-title">Digital Divide Analysis</p>
            <p class="section-subtitle">Area-wise gap & online selling by category</p>
        </div>
    </div>""", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        dig_cols = ["HasSmartphone","UsesDigitalPayment",
                    "UsesSocialMedia","SellsOnline"]
        dig_gap = fdf.groupby("AreaType")[dig_cols]\
                     .mean().reset_index()
        dig_melt = dig_gap.melt(
            id_vars="AreaType",
            var_name="Metric", value_name="Rate")
        dig_melt["Metric"] = dig_melt["Metric"].map({
            "HasSmartphone":     "Smartphone",
            "UsesDigitalPayment":"Digital Pay",
            "UsesSocialMedia":   "Social Media",
            "SellsOnline":       "Sells Online"
        })
        fig3 = px.bar(dig_melt,
            x="Metric", y="Rate", color="AreaType",
            barmode="group",
            color_discrete_map={"Rural":"#e74c3c",
                                 "Semi-Urban":"#f39c12",
                                 "Urban":"#27ae60"},
            text=dig_melt["Rate"].apply(lambda x: f"{x:.0%}"),
            labels={"Rate":"Adoption Rate","Metric":""},
            title="Digital Adoption: Rural vs Urban")
        fig3.update_traces(
            textposition="outside",
            textfont=dict(size=11, color="#1a0030"))
        fig3.update_layout(
            yaxis_tickformat=".0%", height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13, color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            xaxis=dict(tickfont=dict(size=12, color="#1a0030")),
            yaxis=dict(tickfont=dict(size=12, color="#1a0030")),
            legend=dict(font=dict(size=12, color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig3, width='stretch')

    with col4:
        online_cat = fdf.groupby("BusinessCategory")\
                        ["SellsOnline"].mean().reset_index()\
                        .sort_values("SellsOnline", ascending=True)
        online_cat.columns = ["Category","OnlineRate"]
        fig4 = go.Figure(go.Bar(
            x=online_cat["OnlineRate"],
            y=online_cat["Category"],
            orientation="h",
            marker=dict(
                color=online_cat["OnlineRate"],
                colorscale=[[0,"#f0f0ff"],[0.5,"#7b2d8b"],
                             [1,"#4a0080"]],
                showscale=False
            ),
            text=[f"{v:.1%}" for v in online_cat["OnlineRate"]],
            textposition="outside",
            textfont=dict(size=11, color="#1a0030"),
            hovertemplate="<b>%{y}</b><br>Online: %{x:.1%}<extra></extra>"
        ))
        fig4.update_layout(
            title=dict(text="Online Selling Rate by Category",
                       font=dict(size=15, color="#4a0080")),
            xaxis_title="Adoption Rate",
            xaxis_tickformat=".0%",
            yaxis_title="",
            xaxis=dict(tickfont=dict(size=11, color="#1a0030")),
            yaxis=dict(tickfont=dict(size=11, color="#1a0030")),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=12, color="#1a0030"),
            margin=dict(t=50,b=20,l=10,r=20)
        )
        st.plotly_chart(fig4, width='stretch')

    st.markdown("""
    <div class="insight-card">
        💡 <b>Urban smartphone penetration is 25–30% higher</b>
        than Rural, creating a compounding digital gap.
        Home Decor & Textile lead online selling (29–30%),
        while Agriculture & Dairy (23%) need e-commerce
        enablement support.
    </div>""", unsafe_allow_html=True)
# ============================================================
#  PIECE 6/6 — Tab 5: Training + Tab 6: Dropout + Footer
# ============================================================

# ══════════════════════════════════════════════════════════════
#  TAB 5 — TRAINING & SCHEMES
# ══════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>🎓</span>
        <div>
            <p class="section-title">Training & Government Schemes</p>
            <p class="section-subtitle">Skill training impact, SHG membership & loan schemes</p>
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        train_data = fdf.groupby("TrainingsAttended").agg(
            AvgRevenue=("MonthlyRevenue","mean"),
            Count=("EntrepreneurID","count"),
            DropoutRate=("PortalDropout","mean")
        ).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=train_data["TrainingsAttended"],
            y=train_data["Count"],
            name="Count", yaxis="y2",
            marker_color="rgba(194,24,91,0.15)",
            hovertemplate="Trainings %{x}: %{y}"
                          "<extra></extra>"
        ))
        fig.add_trace(go.Scatter(
            x=train_data["TrainingsAttended"],
            y=train_data["AvgRevenue"],
            mode="lines+markers+text",
            name="Avg Revenue",
            text=[f"₹{v:,.0f}"
                  for v in train_data["AvgRevenue"]],
            textposition="top center",
            textfont=dict(size=10, color="#1a0030"),
            line=dict(color="#8b0057", width=3),
            marker=dict(size=10, color="#8b0057"),
            hovertemplate="Trainings %{x}: ₹%{y:,.0f}"
                          "<extra></extra>"
        ))
        fig.update_layout(
            title=dict(
                text="Training Attendance → Revenue Impact",
                font=dict(size=15, color="#4a0080")),
            xaxis_title="Trainings Attended",
            yaxis_title="Avg Revenue (₹)",
            yaxis2=dict(title="Count",
                        overlaying="y", side="right",
                        showgrid=False,
                        tickfont=dict(size=11,
                                      color="#1a0030")),
            xaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            legend=dict(orientation="h", y=1.12,
                        font=dict(size=12,
                                   color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(t=60,b=20,l=10,r=10)
        )
        st.plotly_chart(fig, width='stretch')

    with col2:
        ttype = fdf.groupby("TrainingType").agg(
            AvgRevenue=("MonthlyRevenue","mean"),
            Count=("EntrepreneurID","count")
        ).reset_index().sort_values("AvgRevenue",
                                     ascending=True)
        fig2 = go.Figure(go.Bar(
            x=ttype["AvgRevenue"],
            y=ttype["TrainingType"],
            orientation="h",
            marker=dict(
                color=ttype["AvgRevenue"],
                colorscale=[[0,"#f9c6d0"],[1,"#4a0080"]],
                showscale=False
            ),
            text=[f"₹{v:,.0f}"
                  for v in ttype["AvgRevenue"]],
            textposition="outside",
            textfont=dict(size=11, color="#1a0030"),
            customdata=ttype["Count"].values,
            hovertemplate="<b>%{y}</b><br>"
                          "Revenue: ₹%{x:,.0f}<br>"
                          "Count: %{customdata:,}"
                          "<extra></extra>"
        ))
        fig2.update_layout(
            title=dict(text="Revenue by Training Type",
                       font=dict(size=15, color="#4a0080")),
            xaxis_title="Avg Revenue (₹)",
            yaxis_title="",
            xaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=12,
                      color="#1a0030"),
            margin=dict(t=50,b=20,l=10,r=20)
        )
        st.plotly_chart(fig2, width='stretch')

    # SHG & Mentor
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>🤝</span>
        <div>
            <p class="section-title">Support Network Impact</p>
            <p class="section-subtitle">SHG & mentorship effect on growth</p>
        </div>
    </div>""", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        shg = fdf.groupby(["SHGMember","GrowthStage"])\
                  .size().reset_index(name="Count")
        shg["SHGMember"] = shg["SHGMember"].map(
            {0:"❌ Non-SHG", 1:"✅ SHG Member"})
        fig3 = px.bar(shg,
            x="SHGMember", y="Count",
            color="GrowthStage",
            color_discrete_map=GROWTH_COLORS,
            barmode="stack",
            labels={"SHGMember":"",
                    "Count":"Entrepreneurs",
                    "GrowthStage":"Stage"},
            title="SHG Membership → Growth Stage")
        fig3.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            xaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            legend=dict(font=dict(size=12,
                                   color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig3, width='stretch')

    with col4:
        mentor = fdf.groupby(["HasMentor","GrowthStage"])\
                    .size().reset_index(name="Count")
        mentor["HasMentor"] = mentor["HasMentor"].map(
            {0:"❌ No Mentor", 1:"✅ Has Mentor"})
        fig4 = px.bar(mentor,
            x="HasMentor", y="Count",
            color="GrowthStage",
            color_discrete_map=GROWTH_COLORS,
            barmode="stack",
            labels={"HasMentor":"",
                    "Count":"Entrepreneurs",
                    "GrowthStage":"Stage"},
            title="Mentorship → Growth Stage")
        fig4.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            xaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            legend=dict(font=dict(size=12,
                                   color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig4, width='stretch')

    # Govt Schemes
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>🏛️</span>
        <div>
            <p class="section-title">Government Scheme Analytics</p>
            <p class="section-subtitle">Loan uptake, avg loan & thriving rate per scheme</p>
        </div>
    </div>""", unsafe_allow_html=True)

    scheme_data = fdf[fdf["LoanScheme"] != "None"]\
        .groupby("LoanScheme").agg(
            Count=("EntrepreneurID","count"),
            AvgLoan=("LoanAmount","mean"),
            AvgRevenue=("MonthlyRevenue","mean"),
            Thriving=("GrowthStage",
                      lambda x: (x=="Thriving").mean())
        ).reset_index()\
        .sort_values("AvgRevenue", ascending=False)

    col5, col6, col7 = st.columns(3)
    with col5:
        fig5 = px.bar(scheme_data,
            x="LoanScheme", y="Count",
            color="Count",
            color_continuous_scale=["#f9c6d0","#4a0080"],
            text="Count",
            title="Scheme Beneficiaries",
            labels={"LoanScheme":"","Count":"Beneficiaries"})
        fig5.update_traces(
            textposition="outside",
            textfont=dict(size=12, color="#1a0030"))
        fig5.update_layout(
            coloraxis_showscale=False,
            height=360,
            xaxis_tickangle=-20,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=12,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            xaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig5, width='stretch')

    with col6:
        fig6 = px.bar(scheme_data,
            x="LoanScheme", y="AvgRevenue",
            color="AvgRevenue",
            color_continuous_scale=["#f9c6d0","#8b0057"],
            text=[f"₹{v:,.0f}"
                  for v in scheme_data["AvgRevenue"]],
            title="Avg Revenue per Scheme",
            labels={"LoanScheme":"",
                    "AvgRevenue":"Avg Revenue (₹)"})
        fig6.update_traces(
            textposition="outside",
            textfont=dict(size=12, color="#1a0030"))
        fig6.update_layout(
            coloraxis_showscale=False,
            height=360,
            xaxis_tickangle=-20,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=12,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            xaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig6, width='stretch')

    with col7:
        fig7 = px.bar(scheme_data,
            x="LoanScheme", y="Thriving",
            color="Thriving",
            color_continuous_scale=["#f0fff0","#27ae60"],
            text=[f"{v:.1%}"
                  for v in scheme_data["Thriving"]],
            title="% Thriving by Scheme",
            labels={"LoanScheme":"",
                    "Thriving":"% Thriving"})
        fig7.update_traces(
            textposition="outside",
            textfont=dict(size=12, color="#1a0030"))
        fig7.update_layout(
            coloraxis_showscale=False,
            height=360,
            yaxis_tickformat=".0%",
            xaxis_tickangle=-20,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=12,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            xaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=11,
                                      color="#1a0030")),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig7, width='stretch')

    st.markdown("""
    <div class="insight-card">
        💡 <b>State Scheme beneficiaries show the highest
        Thriving rate (30.3%)</b>, followed by Stand-Up India
        (28.4%). SHG members are 2× more likely to reach
        Thriving stage. Entrepreneurs with 3+ trainings show
        40–60% higher revenue than untrained peers.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  TAB 6 — DROPOUT RISK
# ══════════════════════════════════════════════════════════════
with tab6:
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>⚠️</span>
        <div>
            <p class="section-title">Portal Dropout Risk Analysis</p>
            <p class="section-subtitle">High-risk segments, dropout drivers & retention intelligence</p>
        </div>
    </div>""", unsafe_allow_html=True)

    # Risk KPI cards
    r1, r2, r3, r4 = st.columns(4)
    rural_drop   = fdf[fdf["AreaType"]=="Rural"]\
                      ["PortalDropout"].mean()
    notrain_drop = fdf[fdf["TrainingsAttended"]==0]\
                      ["PortalDropout"].mean()
    nascent_drop = fdf[fdf["GrowthStage"]=="Nascent"]\
                      ["PortalDropout"].mean()

    for col_obj, label, val, color, note in zip(
        [r1,r2,r3,r4],
        ["Overall Dropout","Rural Dropout",
         "Zero Training","Nascent Stage"],
        [fdf["PortalDropout"].mean(), rural_drop,
         notrain_drop, nascent_drop],
        ["#e74c3c","#e67e22","#8e44ad","#c0392b"],
        ["Platform-wide","Area risk",
         "Training gap","Stage risk"]
    ):
        col_obj.markdown(f"""
        <div style='background:white; border-radius:14px;
                    padding:20px; border-top:4px solid {color};
                    text-align:center;
                    box-shadow:0 4px 16px rgba(74,0,128,0.1);'>
            <div style='font-size:2rem; font-weight:800;
                        color:{color};'>{val:.1%}</div>
            <div style='font-size:0.88rem; font-weight:700;
                        color:#1a0030; margin-top:6px;'>
                {label}
            </div>
            <div style='font-size:0.78rem; color:#666;
                        margin-top:4px;'>{note}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        drop_stage = fdf.groupby("GrowthStage")\
                        ["PortalDropout"].mean().reset_index()
        drop_stage.columns = ["Stage","DropoutRate"]
        drop_stage["DropoutPct"] = \
            drop_stage["DropoutRate"] * 100
        fig = px.funnel(
            drop_stage.sort_values("DropoutPct",
                                    ascending=False),
            x="DropoutPct", y="Stage",
            color="Stage",
            color_discrete_map=GROWTH_COLORS,
            title="Dropout Rate by Growth Stage",
            labels={"DropoutPct":"Dropout Rate (%)",
                    "Stage":""})
        fig.update_layout(
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            legend=dict(font=dict(size=12,
                                   color="#1a0030"),
                        bgcolor="rgba(255,255,255,0.8)"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig, width='stretch')

    with col2:
        edu_order = ["No Formal Education","Primary (1–5)",
                     "Secondary (6–10)",
                     "Higher Secondary (11–12)",
                     "Graduate","Post-Graduate"]
        drop_edu = fdf.groupby("Education", observed=True)\
                      ["PortalDropout"].mean()\
                      .reindex(edu_order).reset_index()
        drop_edu.columns = ["Education","DropoutRate"]
        drop_edu["DropoutPct"] = \
            drop_edu["DropoutRate"] * 100
        drop_edu["Short"] = ["None","Primary","Sec",
                              "Hgr Sec","Grad","PG"]
        fig2 = go.Figure(go.Bar(
            x=drop_edu["Short"],
            y=drop_edu["DropoutPct"],
            marker=dict(
                color=drop_edu["DropoutPct"],
                colorscale=[[0,"#fff0f0"],[1,"#c0392b"]],
                showscale=False
            ),
            text=[f"{v:.1f}%"
                  for v in drop_edu["DropoutPct"]],
            textposition="outside",
            textfont=dict(size=12, color="#1a0030"),
            hovertemplate="<b>%{x}</b><br>"
                          "Dropout: %{y:.1f}%"
                          "<extra></extra>"
        ))
        fig2.update_layout(
            title=dict(text="Dropout Rate by Education",
                       font=dict(size=15, color="#4a0080")),
            yaxis_title="Dropout Rate (%)",
            xaxis_title="",
            xaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig2, width='stretch')

    col3, col4 = st.columns(2)
    with col3:
        drop_heat = fdf.groupby(
            ["AreaType","GrowthStage"])\
            ["PortalDropout"].mean().reset_index()
        pivot = drop_heat.pivot(
            index="AreaType",
            columns="GrowthStage",
            values="PortalDropout")
        fig3 = px.imshow(pivot,
            color_continuous_scale=[[0,"#fff0f0"],
                                     [0.5,"#e74c3c"],
                                     [1,"#7b0000"]],
            text_auto=".1%", aspect="auto",
            title="Dropout Heatmap: Area × Growth Stage")
        fig3.update_layout(
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            title_font=dict(size=15, color="#4a0080"),
            xaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig3, width='stretch')

    with col4:
        drop_dig = fdf.groupby("DigitalScore")\
                      ["PortalDropout"].mean().reset_index()
        drop_dig.columns = ["Score","DropoutRate"]
        drop_dig["DropoutPct"] = drop_dig["DropoutRate"] * 100
        fig4 = go.Figure(go.Bar(
            x=drop_dig["Score"],
            y=drop_dig["DropoutPct"],
            marker_color=["#c0392b","#e67e22",
                           "#f39c12","#27ae60","#2980b9"],
            text=[f"{v:.1f}%"
                  for v in drop_dig["DropoutPct"]],
            textposition="outside",
            textfont=dict(size=12, color="#1a0030"),
            hovertemplate="Score %{x}: %{y:.1f}% dropout"
                          "<extra></extra>"
        ))
        fig4.update_layout(
            title=dict(text="Dropout Rate vs Digital Score",
                       font=dict(size=15, color="#4a0080")),
            xaxis_title="Digital Score (0–4)",
            yaxis_title="Dropout Rate (%)",
            xaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            yaxis=dict(tickfont=dict(size=12,
                                      color="#1a0030")),
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13,
                      color="#1a0030"),
            margin=dict(t=50,b=20,l=10,r=10)
        )
        st.plotly_chart(fig4, width='stretch')

    # Risk Table
    st.markdown("""
    <div class="section-header">
        <span style='font-size:1.6rem;'>🚨</span>
        <div>
            <p class="section-title">High-Risk Segment Table</p>
            <p class="section-subtitle">Actionable risk flags for targeted intervention</p>
        </div>
    </div>""", unsafe_allow_html=True)

    risk = fdf.groupby(["Zone","AreaType","GrowthStage"])\
              .agg(
                Count=("EntrepreneurID","count"),
                DropoutRate=("PortalDropout","mean"),
                AvgRevenue=("MonthlyRevenue","mean"),
                DigitalScore=("DigitalScore","mean"),
                AvgTrainings=("TrainingsAttended","mean")
              ).reset_index()
    risk["Risk"] = risk["DropoutRate"].apply(
        lambda x: "🔴 High"   if x > 0.30 else
                 ("🟡 Medium" if x > 0.18 else
                  "🟢 Low"))
    risk["Action"] = risk["DropoutRate"].apply(
        lambda x: "Immediate Intervention" if x > 0.30 else
                 ("Monitor Closely" if x > 0.18 else
                  "Stable"))
    risk = risk.sort_values("DropoutRate", ascending=False)
    risk["DropoutRate"]  = risk["DropoutRate"]\
        .apply(lambda x: f"{x:.1%}")
    risk["AvgRevenue"]   = risk["AvgRevenue"]\
        .apply(lambda x: f"₹{x:,.0f}")
    risk["DigitalScore"] = risk["DigitalScore"]\
        .apply(lambda x: f"{x:.2f}/4")
    risk["AvgTrainings"] = risk["AvgTrainings"]\
        .apply(lambda x: f"{x:.1f}")
    st.dataframe(risk, width='stretch',
                 hide_index=True, height=400)

    st.markdown("""
    <div class="insight-card">
        💡 <b>Rural Nascent entrepreneurs with DigitalScore = 0
        </b> show the highest dropout risk (35–40%). Each
        additional training reduces dropout by ~2.5%. SHG
        membership is the single strongest protective factor —
        reducing dropout by ~8% vs non-members.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='
    background: linear-gradient(135deg,
        #4a0080, #8b0057, #c2185b);
    border-radius: 16px;
    padding: 28px 40px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(74,0,128,0.2);
'>
    <div style='font-size:1.8rem; margin-bottom:8px;'>🪷</div>
    <div style='font-size:1.15rem; font-weight:700;
                color:#ffffff; margin-bottom:6px;'>
        Aatmanirbhar Naari — Women Home Business Intelligence Platform 
    </div>
    <div style='font-size:0.88rem; color:rgba(255,255,255,0.88);
                margin-bottom:10px;'>
        Women Entrepreneurship Analytics &nbsp;|&nbsp;
    </div>
    <div style='font-size:0.78rem; color:rgba(255,255,255,0.7);'>
        2,000 entrepreneurs · 15 Indian states ·
        10 business categories · 28 data dimensions
    </div>
</div>
""", unsafe_allow_html=True)
