# 📊 Data Description and Understanding
## 📖 Data Dictionary
| Column Name | Data Type | Description |
|---|---|---|
| REGISTRATION_DATE | DateTime | Date the contract was registered with DLD |
| START_DATE | DateTime | Date the rental contract officially begins |
| END_DATE | DateTime | Date the rental contract officially ends |
| AREA_EN | Categorical | Dubai district/area name |
| **CONTRACT_AMOUNT** | **Float — 🎯 TARGET** | **Total rental contract value in AED. Renamed to ACTUAL_PRICE in output file.** |
| ACTUAL_AREA | Float | Property size in square meters |
| PROP_TYPE_EN | Categorical | Property type: Unit, Villa, Building, Land, Virtual Unit |
| PROP_SUB_TYPE_EN | Categorical | Sub-type: Flat, Studio, Office, Clinic, Cinema, Villa etc. |
| ROOMS | Integer (stored as Float) | Number of bedrooms. 96.4% missing, imputed with 0. |
| USAGE_EN | Categorical | Usage: Residential, Commercial, Industrial etc. |
| IS_FREE_HOLD_EN | Categorical | Freehold or Non-Freehold |
| NEAREST_METRO_EN | Categorical | Nearest Dubai Metro station |
| PARKING | Integer (stored as Float) | Number of parking spaces. 97.9% missing, imputed with 0. |
| TOTAL_PROPERTIES | Integer | Total properties in the building |
| PROJECT_EN | Categorical | Development project name |
| CONTRACT_DURATION_DAYS | 🟢 Engineered Integer | Days between START_DATE and END_DATE. Strongest predictor r=0.56 |
| START_YEAR | 🟢 Engineered Integer | Year extracted from START_DATE. Filtered to 2020+. |
| START_MONTH | 🟢 Engineered Integer | Month (1-12) from START_DATE. Captures seasonal patterns. |
| PRICE_PER_AREA | 🟢 Engineered Float | CONTRACT_AMOUNT / ACTUAL_AREA. EDA only — excluded from model to prevent data leakage. |
> 🟢 = Engineered — not in raw dataset, created in Feature Engineering Step 7.
## ❌ Excluded Columns
| Column | Reason |
|---|---|
| NEAREST_MALL_EN | NEAREST_METRO_EN captures location premium better |
| NEAREST_LANDMARK_EN | Same reason |
| ANNUAL_AMOUNT | Data leakage — direct derivative of CONTRACT_AMOUNT |
| MASTER_PROJECT_EN | Too sparse, duplicates PROJECT_EN |
| VERSION_EN | Administrative field, no pricing relevance |
## 📈 EDA Summary
### 1️⃣ Univariate Analysis
CONTRACT_AMOUNT follows right-skewed log-normal distribution. Most contracts: AED 10,000–1,000,000. Property area has near-zero correlation with price (r~0).
### 2️⃣ Bivariate Analysis
- Contract duration: strongest predictor (r=0.56)
- Building scale: second strongest (r=0.53)
- Freehold premium: 17% (AED 71,121 vs AED 60,654)
- Dubai has 5 completely separate property markets
### 3️⃣ Multivariate Analysis
CONTRACT_DURATION_DAYS shows clearest linear trend with price. Freehold premium persists regardless of property size.