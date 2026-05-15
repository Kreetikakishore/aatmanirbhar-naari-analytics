# ============================================================
#  AATMANIRBHAR NAARI — EDA & ANALYSIS REPORT
#  Run: python eda.py
# ============================================================

import pandas as pd
import numpy as np

print("=" * 62)
print("  AATMANIRBHAR NAARI — HOME BUSINESS ENABLEMENT ANALYTICS")
print("  Exploratory Data Analysis Report")
print("=" * 62)

df = pd.read_csv("data/naari_data.csv")
print(f"\n✅ Dataset: {df.shape[0]:,} records × {df.shape[1]} features\n")

# ── 1. DERIVED FIELDS ────────────────────────────────────────
df["AgeGroup"] = pd.cut(df["Age"],
    bins=[17,25,35,45,60],
    labels=["18–25","26–35","36–45","46–60"])

df["RevenueSegment"] = pd.cut(df["MonthlyRevenue"],
    bins=[0, 10000, 25000, 50000, 999999],
    labels=["Low (<₹10K)", "Medium (₹10K–25K)",
            "High (₹25K–50K)", "Premium (>₹50K)"])

df["ProfitMargin"] = (df["MonthlyProfit"] / df["MonthlyRevenue"] * 100).round(1)

df.to_csv("data/naari_clean.csv", index=False)
print("✅ Derived fields added. Clean data saved.\n")

sep = "-" * 62

# ── 2. PLATFORM KPIs ─────────────────────────────────────────
print(sep)
print("  PLATFORM-LEVEL KPIs")
print(sep)
print(f"  Total Entrepreneurs Registered : {len(df):,}")
print(f"  Active Users (Not Dropped Out) : {(df['PortalDropout']==0).sum():,}")
print(f"  Portal Dropout Rate            : {df['PortalDropout'].mean():.1%}")
print(f"  States Covered                 : {df['State'].nunique()}")
print(f"  Business Categories            : {df['BusinessCategory'].nunique()}")
print(f"  Avg Monthly Revenue            : ₹{df['MonthlyRevenue'].mean():,.0f}")
print(f"  Avg Monthly Profit             : ₹{df['MonthlyProfit'].mean():,.0f}")
print(f"  Avg Profit Margin              : {df['ProfitMargin'].mean():.1f}%")
print(f"  Total Annual Revenue (All)     : ₹{df['AnnualRevenue'].sum()/1e7:.1f} Crore")

# ── 3. GROWTH STAGE DISTRIBUTION ─────────────────────────────
print(f"\n{sep}")
print("  BUSINESS GROWTH STAGE DISTRIBUTION")
print(sep)
gs = df.groupby("GrowthStage").agg(
    Count=("EntrepreneurID","count"),
    AvgRevenue=("MonthlyRevenue","mean"),
    AvgProfit=("MonthlyProfit","mean"),
    AvgDigitalScore=("DigitalScore","mean"),
    DropoutRate=("PortalDropout","mean")
).reset_index()
gs["Share%"] = (gs["Count"]/len(df)*100).round(1)
gs["AvgRevenue"] = gs["AvgRevenue"].apply(lambda x: f"₹{x:,.0f}")
gs["AvgProfit"]  = gs["AvgProfit"].apply(lambda x: f"₹{x:,.0f}")
gs["DropoutRate"]= gs["DropoutRate"].apply(lambda x: f"{x:.1%}")
print(gs.to_string(index=False))

# ── 4. GEOGRAPHIC ANALYSIS ────────────────────────────────────
print(f"\n{sep}")
print("  TOP 10 STATES — ENTREPRENEUR COUNT & AVG REVENUE")
print(sep)
state_analysis = df.groupby("State").agg(
    Count=("EntrepreneurID","count"),
    AvgRevenue=("MonthlyRevenue","mean"),
    AvgProfit=("MonthlyProfit","mean"),
    DropoutRate=("PortalDropout","mean")
).reset_index().sort_values("Count", ascending=False).head(10)
state_analysis["AvgRevenue"]  = state_analysis["AvgRevenue"].apply(lambda x: f"₹{x:,.0f}")
state_analysis["DropoutRate"] = state_analysis["DropoutRate"].apply(lambda x: f"{x:.1%}")
print(state_analysis.to_string(index=False))

# ── 5. ZONE ANALYSIS ─────────────────────────────────────────
print(f"\n{sep}")
print("  ZONE-WISE PERFORMANCE")
print(sep)
zone = df.groupby("Zone").agg(
    Count=("EntrepreneurID","count"),
    AvgRevenue=("MonthlyRevenue","mean"),
    DigitalAdoption=("DigitalScore","mean"),
    DropoutRate=("PortalDropout","mean"),
    ThrivingShare=("GrowthStage", lambda x: (x=="Thriving").mean())
).reset_index()
zone["AvgRevenue"]     = zone["AvgRevenue"].apply(lambda x: f"₹{x:,.0f}")
zone["DigitalAdoption"]= zone["DigitalAdoption"].apply(lambda x: f"{x:.2f}/4")
zone["DropoutRate"]    = zone["DropoutRate"].apply(lambda x: f"{x:.1%}")
zone["ThrivingShare"]  = zone["ThrivingShare"].apply(lambda x: f"{x:.1%}")
print(zone.to_string(index=False))

# ── 6. BUSINESS CATEGORY ANALYSIS ────────────────────────────
print(f"\n{sep}")
print("  BUSINESS CATEGORY — REVENUE & GROWTH")
print(sep)
biz = df.groupby("BusinessCategory").agg(
    Count=("EntrepreneurID","count"),
    AvgRevenue=("MonthlyRevenue","mean"),
    AvgProfit=("MonthlyProfit","mean"),
    OnlineSellers=("SellsOnline","mean"),
    DropoutRate=("PortalDropout","mean")
).reset_index().sort_values("AvgRevenue", ascending=False)
biz["AvgRevenue"]   = biz["AvgRevenue"].apply(lambda x: f"₹{x:,.0f}")
biz["AvgProfit"]    = biz["AvgProfit"].apply(lambda x: f"₹{x:,.0f}")
biz["OnlineSellers"]= biz["OnlineSellers"].apply(lambda x: f"{x:.1%}")
biz["DropoutRate"]  = biz["DropoutRate"].apply(lambda x: f"{x:.1%}")
print(biz.to_string(index=False))

# ── 7. DIGITAL ADOPTION ANALYSIS ─────────────────────────────
print(f"\n{sep}")
print("  DIGITAL ADOPTION IMPACT ON REVENUE")
print(sep)
dig = df.groupby("DigitalScore")["MonthlyRevenue"].agg(
    ["mean","count"]).reset_index()
dig.columns = ["DigitalScore","AvgRevenue","Count"]
dig["AvgRevenue"] = dig["AvgRevenue"].apply(lambda x: f"₹{x:,.0f}")
print(dig.to_string(index=False))

# ── 8. TRAINING IMPACT ────────────────────────────────────────
print(f"\n{sep}")
print("  TRAINING ATTENDANCE IMPACT ON PROFIT")
print(sep)
train = df.groupby("TrainingsAttended").agg(
    Count=("EntrepreneurID","count"),
    AvgProfit=("MonthlyProfit","mean"),
    DropoutRate=("PortalDropout","mean")
).reset_index()
train["AvgProfit"]   = train["AvgProfit"].apply(lambda x: f"₹{x:,.0f}")
train["DropoutRate"] = train["DropoutRate"].apply(lambda x: f"{x:.1%}")
print(train.to_string(index=False))

# ── 9. LOAN & SCHEME UPTAKE ───────────────────────────────────
print(f"\n{sep}")
print("  GOVERNMENT SCHEME UPTAKE & IMPACT")
print(sep)
scheme = df.groupby("LoanScheme").agg(
    Count=("EntrepreneurID","count"),
    AvgLoanAmount=("LoanAmount","mean"),
    AvgRevenue=("MonthlyRevenue","mean"),
    GrowthThriving=("GrowthStage", lambda x: (x=="Thriving").mean())
).reset_index().sort_values("Count", ascending=False)
scheme["AvgLoanAmount"] = scheme["AvgLoanAmount"].apply(lambda x: f"₹{x:,.0f}")
scheme["AvgRevenue"]    = scheme["AvgRevenue"].apply(lambda x: f"₹{x:,.0f}")
scheme["GrowthThriving"]= scheme["GrowthThriving"].apply(lambda x: f"{x:.1%}")
print(scheme.to_string(index=False))

# ── 10. DROPOUT RISK ANALYSIS ────────────────────────────────
print(f"\n{sep}")
print("  PORTAL DROPOUT RISK FACTORS")
print(sep)
for col in ["AreaType","Education","AgeGroup","SHGMember","HasMentor"]:
    sub = df.groupby(col, observed=True)["PortalDropout"].mean().reset_index()
    sub.columns = [col, "DropoutRate"]
    sub["DropoutRate"] = sub["DropoutRate"].apply(lambda x: f"{x:.1%}")
    print(f"\n  By {col}:")
    print(sub.to_string(index=False))

print(f"\n{'='*62}")
print("  ✅ EDA COMPLETE — Run: streamlit run app.py")
print(f"{'='*62}")