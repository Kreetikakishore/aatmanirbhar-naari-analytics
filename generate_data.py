# ============================================================
#  AATMANIRBHAR NAARI — SYNTHETIC DATASET GENERATOR
#  Generates 2000 realistic women entrepreneur records
#  Run: python generate_data.py
# ============================================================

import pandas as pd
import numpy as np
import os

np.random.seed(42)
N = 2000

# ── GEOGRAPHIC DISTRIBUTION ───────────────────────────────────
states = [
    "Uttar Pradesh", "Maharashtra", "Rajasthan", "Tamil Nadu",
    "West Bengal", "Karnataka", "Gujarat", "Madhya Pradesh",
    "Bihar", "Telangana", "Odisha", "Punjab", "Assam", "Kerala",
    "Jharkhand"
]
state_weights = [0.14,0.12,0.09,0.09,0.08,0.07,0.07,0.06,
                 0.05,0.05,0.04,0.04,0.04,0.03,0.03]

zones = {
    "Uttar Pradesh":"North", "Rajasthan":"North", "Punjab":"North",
    "Maharashtra":"West", "Gujarat":"West",
    "Tamil Nadu":"South", "Karnataka":"South", "Telangana":"South", "Kerala":"South",
    "West Bengal":"East", "Bihar":"East", "Odisha":"East",
    "Jharkhand":"East", "Assam":"Northeast",
    "Madhya Pradesh":"Central"
}

area_type = np.random.choice(["Rural","Semi-Urban","Urban"],
                              size=N, p=[0.50, 0.30, 0.20])

# ── ENTREPRENEUR PROFILE ──────────────────────────────────────
entrepreneur_id = [f"AN{str(i).zfill(5)}" for i in range(1, N+1)]

state_col = np.random.choice(states, size=N, p=state_weights)
zone_col  = [zones[s] for s in state_col]

age = np.random.randint(18, 61, size=N)

education = np.random.choice(
    ["No Formal Education", "Primary (1–5)", "Secondary (6–10)",
     "Higher Secondary (11–12)", "Graduate", "Post-Graduate"],
    size=N, p=[0.10, 0.15, 0.25, 0.20, 0.22, 0.08]
)

marital_status = np.random.choice(
    ["Single", "Married", "Widowed", "Divorced"],
    size=N, p=[0.20, 0.62, 0.12, 0.06]
)

dependents = np.random.choice([0,1,2,3,4,5], size=N,
                               p=[0.10,0.20,0.30,0.25,0.10,0.05])

# ── BUSINESS CATEGORY ────────────────────────────────────────
business_category = np.random.choice(
    ["Food & Beverages", "Handicraft & Artisan", "Textile & Apparel",
     "Beauty & Wellness", "Education & Tutoring", "Agriculture & Dairy",
     "Digital Services", "Retail & Trading", "Healthcare Products",
     "Home Decor & Furnishing"],
    size=N,
    p=[0.18, 0.14, 0.13, 0.11, 0.10, 0.10, 0.07, 0.07, 0.05, 0.05]
)

years_in_business = np.random.choice(range(0, 11), size=N,
    p=[0.12,0.15,0.14,0.12,0.10,0.09,0.08,0.07,0.06,0.04,0.03])

# ── FINANCIAL PROFILE ─────────────────────────────────────────
# Monthly revenue depends on business category and area
base_revenue = {
    "Food & Beverages": 18000, "Handicraft & Artisan": 12000,
    "Textile & Apparel": 22000, "Beauty & Wellness": 20000,
    "Education & Tutoring": 16000, "Agriculture & Dairy": 14000,
    "Digital Services": 28000, "Retail & Trading": 25000,
    "Healthcare Products": 21000, "Home Decor & Furnishing": 17000
}
area_multiplier = {"Rural": 0.70, "Semi-Urban": 1.00, "Urban": 1.45}

monthly_revenue = np.array([
    max(500, int(
        base_revenue[bc] * area_multiplier[at] *
        (1 + (yib * 0.05)) *
        np.random.uniform(0.6, 1.5)
    ))
    for bc, at, yib in zip(business_category, area_type, years_in_business)
])

monthly_expenses = (monthly_revenue * np.random.uniform(0.40, 0.70, N)).astype(int)
monthly_profit   = monthly_revenue - monthly_expenses
annual_revenue   = monthly_revenue * 12

# ── LOAN & GOVERNMENT SCHEMES ────────────────────────────────
has_loan = np.random.choice([0, 1], size=N, p=[0.55, 0.45])
loan_amount = np.where(
    has_loan == 1,
    np.random.randint(10000, 500001, N),
    0
)
loan_schemes = np.random.choice(
    ["None", "Mudra Yojana", "Stand-Up India", "PM SVANidhi",
     "NABARD SHG", "State Scheme"],
    size=N, p=[0.40, 0.22, 0.10, 0.12, 0.10, 0.06]
)

# ── DIGITAL ADOPTION ─────────────────────────────────────────
has_smartphone      = np.random.choice([0,1], N, p=[0.25, 0.75])
uses_digital_payment= np.where(has_smartphone==1,
                                np.random.choice([0,1],N,p=[0.30,0.70]), 0)
uses_social_media   = np.where(has_smartphone==1,
                                np.random.choice([0,1],N,p=[0.35,0.65]), 0)
sells_online        = np.where(uses_social_media==1,
                                np.random.choice([0,1],N,p=[0.45,0.55]), 0)

digital_score = (has_smartphone + uses_digital_payment +
                 uses_social_media + sells_online)

# ── SKILL TRAINING ────────────────────────────────────────────
trainings_attended = np.random.choice(range(0,8), size=N,
    p=[0.20,0.22,0.18,0.15,0.10,0.07,0.05,0.03])

training_type = np.random.choice(
    ["None", "Financial Literacy", "Digital Marketing",
     "Product Quality & Packaging", "Business Management",
     "Vocational/Craft", "Multiple"],
    size=N, p=[0.20,0.15,0.18,0.14,0.12,0.13,0.08]
)

# ── SUPPORT NETWORK ───────────────────────────────────────────
shg_member = np.random.choice([0,1], N, p=[0.45, 0.55])
has_mentor  = np.random.choice([0,1], N, p=[0.65, 0.35])

# ── TARGET VARIABLE: BUSINESS GROWTH STAGE ────────────────────
# Score-based classification
growth_score = (
    (monthly_profit / 5000).clip(0,5) +
    (years_in_business / 2).clip(0,5) +
    digital_score * 0.8 +
    (trainings_attended / 1.5).clip(0,4) +
    shg_member * 1.5 +
    has_mentor * 1.0
)

growth_stage = np.where(
    growth_score < 4,  "Nascent",
    np.where(growth_score < 7,  "Emerging",
    np.where(growth_score < 10, "Growing",
                                 "Thriving"))
)

# ── CHURN / DROPOUT (portal engagement) ──────────────────────
# Higher dropout if: low digital, no training, low revenue
dropout_prob = np.clip(
    0.35
    - (digital_score * 0.04)
    - (trainings_attended * 0.02)
    - (years_in_business * 0.01)
    + np.random.normal(0, 0.05, N),
    0.05, 0.75
)
portal_dropout = np.array([
    np.random.choice([0,1], p=[1-p, p]) for p in dropout_prob
])

# ── ASSEMBLE DATAFRAME ────────────────────────────────────────
df = pd.DataFrame({
    "EntrepreneurID"     : entrepreneur_id,
    "State"              : state_col,
    "Zone"               : zone_col,
    "AreaType"           : area_type,
    "Age"                : age,
    "Education"          : education,
    "MaritalStatus"      : marital_status,
    "Dependents"         : dependents,
    "BusinessCategory"   : business_category,
    "YearsInBusiness"    : years_in_business,
    "MonthlyRevenue"     : monthly_revenue,
    "MonthlyExpenses"    : monthly_expenses,
    "MonthlyProfit"      : monthly_profit,
    "AnnualRevenue"      : annual_revenue,
    "HasLoan"            : has_loan,
    "LoanAmount"         : loan_amount,
    "LoanScheme"         : loan_schemes,
    "HasSmartphone"      : has_smartphone,
    "UsesDigitalPayment" : uses_digital_payment,
    "UsesSocialMedia"    : uses_social_media,
    "SellsOnline"        : sells_online,
    "DigitalScore"       : digital_score,
    "TrainingsAttended"  : trainings_attended,
    "TrainingType"       : training_type,
    "SHGMember"          : shg_member,
    "HasMentor"          : has_mentor,
    "GrowthStage"        : growth_stage,
    "PortalDropout"      : portal_dropout
})

os.makedirs("data", exist_ok=True)
df.to_csv("data/naari_data.csv", index=False)

print("=" * 58)
print("  AATMANIRBHAR NAARI — DATASET GENERATED")
print("=" * 58)
print(f"  ✅ Total Records   : {N:,}")
print(f"  ✅ Features        : {df.shape[1]}")
print(f"  ✅ States Covered  : {df['State'].nunique()}")
print(f"  ✅ Business Types  : {df['BusinessCategory'].nunique()}")
print(f"\n  Growth Stage Distribution:")
print(df["GrowthStage"].value_counts().to_string())
print(f"\n  Portal Dropout Rate: {df['PortalDropout'].mean():.1%}")
print(f"\n  ✅ Saved to: data/naari_data.csv")
print("=" * 58)
print("  Now run: python eda.py")