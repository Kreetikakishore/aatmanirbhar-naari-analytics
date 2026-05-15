# ============================================================
#  AATMANIRBHAR NAARI — CHART GENERATOR
#  Saves all charts as PNG files in charts/ folder
#  Run: python charts.py
# ============================================================

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── LOAD DATA ─────────────────────────────────────────────────
df = pd.read_csv("data/naari_clean.csv")
os.makedirs("charts", exist_ok=True)

COLORS = {
    "Thriving":  "#27ae60",
    "Growing":   "#2980b9",
    "Emerging":  "#f39c12",
    "Nascent":   "#e74c3c"
}

print("=" * 55)
print("  AATMANIRBHAR NAARI — GENERATING CHARTS")
print("=" * 55)

# ── HELPER: save chart ────────────────────────────────────────
def save(fig, filename, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#2c2c2c"), x=0.5),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial", size=13),
        margin=dict(t=70, b=60, l=60, r=40)
    )
    path = f"charts/{filename}.png"
    fig.write_image(path, width=900, height=500, scale=2)
    print(f"  ✅ Saved: {path}")

# ══════════════════════════════════════════════════════════════
#  CHART 1 — Growth Stage Distribution (Donut)
# ══════════════════════════════════════════════════════════════
gs = df["GrowthStage"].value_counts().reset_index()
gs.columns = ["Stage", "Count"]

fig1 = px.pie(
    gs, names="Stage", values="Count",
    hole=0.55,
    color="Stage",
    color_discrete_map=COLORS
)
fig1.update_traces(
    textinfo="label+percent",
    textfont_size=13,
    pull=[0.03]*4
)
save(fig1, "01_growth_stage_distribution",
     "Business Growth Stage Distribution")

# ══════════════════════════════════════════════════════════════
#  CHART 2 — Avg Revenue by Business Category (Horizontal Bar)
# ══════════════════════════════════════════════════════════════
biz = df.groupby("BusinessCategory")["MonthlyRevenue"].mean()\
        .reset_index().sort_values("MonthlyRevenue")
biz.columns = ["Category", "AvgRevenue"]

fig2 = px.bar(
    biz, x="AvgRevenue", y="Category",
    orientation="h",
    color="AvgRevenue",
    color_continuous_scale="RdPu",
    text=biz["AvgRevenue"].apply(lambda x: f"₹{x:,.0f}"),
    labels={"AvgRevenue": "Avg Monthly Revenue (₹)", "Category": ""}
)
fig2.update_traces(textposition="outside")
fig2.update_layout(coloraxis_showscale=False)
save(fig2, "02_revenue_by_category",
     "Avg Monthly Revenue by Business Category")

# ══════════════════════════════════════════════════════════════
#  CHART 3 — Dropout Rate by Training Attendance (Line)
# ══════════════════════════════════════════════════════════════
train = df.groupby("TrainingsAttended")["PortalDropout"].mean()\
          .reset_index()
train.columns = ["Trainings", "DropoutRate"]
train["DropoutRate"] = train["DropoutRate"] * 100

fig3 = px.line(
    train, x="Trainings", y="DropoutRate",
    markers=True,
    color_discrete_sequence=["#e74c3c"],
    labels={"Trainings": "Trainings Attended",
            "DropoutRate": "Dropout Rate (%)"}
)
fig3.update_traces(line_width=3, marker_size=10)
fig3.update_layout(yaxis_ticksuffix="%")
save(fig3, "03_dropout_vs_training",
     "Portal Dropout Rate vs Training Attendance")

# ══════════════════════════════════════════════════════════════
#  CHART 4 — Zone-wise Avg Revenue (Bar)
# ══════════════════════════════════════════════════════════════
zone = df.groupby("Zone")["MonthlyRevenue"].mean()\
         .reset_index().sort_values("MonthlyRevenue", ascending=False)
zone.columns = ["Zone", "AvgRevenue"]

fig4 = px.bar(
    zone, x="Zone", y="AvgRevenue",
    color="Zone",
    text=zone["AvgRevenue"].apply(lambda x: f"₹{x:,.0f}"),
    labels={"AvgRevenue": "Avg Monthly Revenue (₹)", "Zone": ""}
)
fig4.update_traces(textposition="outside")
fig4.update_layout(showlegend=False)
save(fig4, "04_revenue_by_zone",
     "Avg Monthly Revenue by Zone")

# ══════════════════════════════════════════════════════════════
#  CHART 5 — Dropout Rate by Area Type (Bar)
# ══════════════════════════════════════════════════════════════
area = df.groupby("AreaType")["PortalDropout"].mean()\
         .reset_index()
area.columns = ["AreaType", "DropoutRate"]
area["DropoutRate"] = area["DropoutRate"] * 100
area["Color"] = ["#e74c3c", "#f39c12", "#27ae60"]

fig5 = px.bar(
    area, x="AreaType", y="DropoutRate",
    color="AreaType",
    color_discrete_sequence=["#e74c3c", "#f39c12", "#3498db"],
    text=area["DropoutRate"].apply(lambda x: f"{x:.1f}%"),
    labels={"DropoutRate": "Dropout Rate (%)", "AreaType": "Area Type"}
)
fig5.update_traces(textposition="outside")
fig5.update_layout(showlegend=False, yaxis_ticksuffix="%")
save(fig5, "05_dropout_by_area",
     "Portal Dropout Rate by Area Type")

# ══════════════════════════════════════════════════════════════
#  CHART 6 — Thriving % by Govt Scheme (Bar)
# ══════════════════════════════════════════════════════════════
scheme = df[df["LoanScheme"] != "None"].groupby("LoanScheme").agg(
    Thriving=("GrowthStage", lambda x: (x == "Thriving").mean())
).reset_index().sort_values("Thriving", ascending=False)
scheme["ThrivingPct"] = scheme["Thriving"] * 100

fig6 = px.bar(
    scheme, x="LoanScheme", y="ThrivingPct",
    color="ThrivingPct",
    color_continuous_scale="Greens",
    text=scheme["ThrivingPct"].apply(lambda x: f"{x:.1f}%"),
    labels={"LoanScheme": "Govt Scheme",
            "ThrivingPct": "% Thriving Entrepreneurs"}
)
fig6.update_traces(textposition="outside")
fig6.update_layout(coloraxis_showscale=False, yaxis_ticksuffix="%")
save(fig6, "06_thriving_by_scheme",
     "% Thriving Entrepreneurs by Government Scheme")

# ══════════════════════════════════════════════════════════════
#  CHART 7 — Digital Score vs Avg Revenue (Line)
# ══════════════════════════════════════════════════════════════
dig = df.groupby("DigitalScore")["MonthlyRevenue"].mean()\
        .reset_index()
dig.columns = ["DigitalScore", "AvgRevenue"]

fig7 = px.line(
    dig, x="DigitalScore", y="AvgRevenue",
    markers=True,
    color_discrete_sequence=["#8e44ad"],
    labels={"DigitalScore": "Digital Score (0–4)",
            "AvgRevenue": "Avg Monthly Revenue (₹)"}
)
fig7.update_traces(line_width=3, marker_size=10)
fig7.add_bar(
    x=dig["DigitalScore"],
    y=dig["AvgRevenue"],
    marker_color="rgba(142,68,173,0.15)",
    showlegend=False
)
save(fig7, "07_digital_score_vs_revenue",
     "Digital Adoption Score vs Avg Monthly Revenue")

# ══════════════════════════════════════════════════════════════
#  CHART 8 — Growth Stage by Area Type (Stacked Bar)
# ══════════════════════════════════════════════════════════════
area_stage = df.groupby(["AreaType", "GrowthStage"])\
               .size().reset_index(name="Count")

fig8 = px.bar(
    area_stage, x="AreaType", y="Count",
    color="GrowthStage",
    color_discrete_map=COLORS,
    barmode="stack",
    labels={"AreaType": "Area Type",
            "Count": "No. of Entrepreneurs",
            "GrowthStage": "Growth Stage"}
)
save(fig8, "08_growth_stage_by_area",
     "Growth Stage Distribution by Area Type")

# ══════════════════════════════════════════════════════════════
#  CHART 9 — Top 10 States by Avg Revenue (Horizontal Bar)
# ══════════════════════════════════════════════════════════════
states = df.groupby("State")["MonthlyRevenue"].mean()\
           .reset_index().sort_values("MonthlyRevenue",
                                       ascending=True).tail(10)
states.columns = ["State", "AvgRevenue"]

fig9 = px.bar(
    states, x="AvgRevenue", y="State",
    orientation="h",
    color="AvgRevenue",
    color_continuous_scale="Blues",
    text=states["AvgRevenue"].apply(lambda x: f"₹{x:,.0f}"),
    labels={"AvgRevenue": "Avg Monthly Revenue (₹)", "State": ""}
)
fig9.update_traces(textposition="outside")
fig9.update_layout(coloraxis_showscale=False)
save(fig9, "09_top_states_revenue",
     "Top 10 States by Avg Monthly Revenue")

# ══════════════════════════════════════════════════════════════
#  CHART 10 — SHG Member vs Non-Member Growth (Grouped Bar)
# ══════════════════════════════════════════════════════════════
shg = df.groupby(["SHGMember", "GrowthStage"])\
        .size().reset_index(name="Count")
shg["SHGMember"] = shg["SHGMember"].map({0: "Non-SHG", 1: "SHG Member"})

fig10 = px.bar(
    shg, x="GrowthStage", y="Count",
    color="SHGMember",
    barmode="group",
    color_discrete_sequence=["#e74c3c", "#27ae60"],
    labels={"GrowthStage": "Growth Stage",
            "Count": "No. of Entrepreneurs",
            "SHGMember": ""}
)
save(fig10, "10_shg_vs_growth_stage",
     "SHG Membership Impact on Business Growth Stage")

# ══════════════════════════════════════════════════════════════
#  CHART 11 — Profit Margin by Business Category (Bar)
# ══════════════════════════════════════════════════════════════
margin = df.groupby("BusinessCategory")["ProfitMargin"].mean()\
           .reset_index().sort_values("ProfitMargin", ascending=True)
margin.columns = ["Category", "AvgMargin"]

fig11 = px.bar(
    margin, x="AvgMargin", y="Category",
    orientation="h",
    color="AvgMargin",
    color_continuous_scale="Greens",
    text=margin["AvgMargin"].apply(lambda x: f"{x:.1f}%"),
    labels={"AvgMargin": "Avg Profit Margin (%)", "Category": ""}
)
fig11.update_traces(textposition="outside")
fig11.update_layout(coloraxis_showscale=False)
save(fig11, "11_profit_margin_by_category",
     "Avg Profit Margin % by Business Category")

# ══════════════════════════════════════════════════════════════
#  CHART 12 — Revenue Heatmap: Category × Area Type
# ══════════════════════════════════════════════════════════════
heat = df.groupby(["BusinessCategory", "AreaType"])\
         ["MonthlyRevenue"].mean().reset_index()
pivot = heat.pivot(index="BusinessCategory",
                   columns="AreaType",
                   values="MonthlyRevenue")

fig12 = px.imshow(
    pivot,
    color_continuous_scale="RdPu",
    text_auto=".0f",
    aspect="auto",
    labels={"color": "Avg Revenue (₹)"}
)
fig12.update_layout(margin=dict(t=70, b=80, l=200, r=40))
save(fig12, "12_revenue_heatmap_category_area",
     "Revenue Heatmap: Business Category × Area Type")

# ══════════════════════════════════════════════════════════════
#  DONE
# ══════════════════════════════════════════════════════════════
print(f"\n{'='*55}")
print(f"  ✅ All 12 charts saved in: charts/ folder")
print(f"  ✅ Now run: streamlit run app.py")
print(f"{'='*55}")