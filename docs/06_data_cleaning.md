# 🧹 Data Primary Cleaning and Transformation
> Raw: **300,564 rows** → Clean: **263,930 rows**

## ⚙️ Step 1 — Library Setup

All Python libraries imported. Output folder created for charts and CSV files.

## 📂 Step 2 — Data Loading and Deduplication

Duplicates removed using drop_duplicates(). Prevents counting same contract multiple times.

## 📅 Step 3 — Date and Numeric Conversion

REGISTRATION_DATE, START_DATE, END_DATE converted to datetime using errors='coerce'.

CONTRACT_AMOUNT, ANNUAL_AMOUNT, ACTUAL_AREA, ROOMS, PARKING converted to numeric.
> ⚠️ ANNUAL_AMOUNT converted here for data preparation only. Excluded from model in Step 7 to prevent data leakage — it is a direct mathematical derivative of CONTRACT_AMOUNT.

## 🔧 Step 4 — Missing Value Imputation

- NEAREST_METRO_EN, NEAREST_MALL_EN, NEAREST_LANDMARK_EN → "Unknown"

- ROOMS, PARKING → 0 (logical for commercial properties)

- TOTAL_PROPERTIES → numeric, nulls filled with 1

## 🚫 Step 5 — Invalid Value Removal

- ACTUAL_AREA must be > 0

- CONTRACT_AMOUNT must be > 0

- ROOMS must not exceed 50

## ✅ Step 6 — Final NaN Drop

Final dropna() on six essential columns. No NaN values remain.

## 🔨 Step 7 — Feature Engineering

- **CONTRACT_DURATION_DAYS** = END_DATE - START_DATE (r=0.56)

- **START_YEAR** = extracted from START_DATE

- **START_MONTH** = extracted from START_DATE

- **PRICE_PER_AREA** = CONTRACT_AMOUNT / ACTUAL_AREA (EDA only)

Dataset filtered to START_YEAR >= 2020.

REGISTRATION_DATE excluded — 100% values are 2026, zero temporal signal.
 