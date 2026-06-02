# 🤖 Advanced Analytics and AI Modeling
## Problem Framing
Supervised machine learning regression. Target: CONTRACT_AMOUNT (continuous AED value).
## Preprocessing Pipeline
- scikit-learn ColumnTransformer pipeline
- StandardScaler for numeric features
- OneHotEncoder for categorical features
- 80/20 train-test split, random_state=42
## 13 Model Features
AREA_EN, ACTUAL_AREA, PROP_TYPE_EN, PROP_SUB_TYPE_EN, ROOMS, USAGE_EN, PARKING, IS_FREE_HOLD_EN, NEAREST_METRO_EN, TOTAL_PROPERTIES, START_YEAR, START_MONTH, CONTRACT_DURATION_DAYS
## Model Results
| Model | R² | MAE |
|---|---|---|
| 🟡 Linear Regression | 0.5390 | AED 526,976 |
| 🟡 Ridge Regression | 0.5410 | AED 522,355 |
| 🟢 Decision Tree | 0.9501 | AED 72,199 |
| ⭐ Random Forest | 0.9510 | AED 71,130 |
| 🔴 Neural Network | 0.0343 | AED 339,234 |
Random Forest selected. Exceeds industry R²=0.85 target by 10.1%.
## Why Random Forest Won
Dubai rental pricing is fundamentally non-linear. Linear models plateau at 52%. 43% accuracy gap confirms pricing cannot be modeled as a simple sum of parts.
## Forecasting
Applied to 5,000 property profiles across 3 scenarios:
- Next Month, Next Quarter, Next Year
Total output: 67,790 rows (52,790 historical + 15,000 forecasts)
## Limitations
1. Decision Tree vs Random Forest gap is only 0.0009 R²
2. ROOMS (96.4% missing) and PARKING (97.9% missing) — limited predictive contribution
3. Next Year based on only 127 records with START_YEAR=2027 — higher uncertainty
4. Single 80/20 split — k-fold cross-validation recommended for future work