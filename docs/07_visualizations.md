# 📈 Data Visualization and Insights

All charts generated using Python with seaborn and matplotlib.

## 1️⃣ Univariate Analysis

**Figure 1 — CONTRACT_AMOUNT Distribution (Log Scale)**

Right-skewed log-normal distribution. Mass market: AED 10,000–1,000,000. Confirms need for tree-based models.

**Figure 2 — ACTUAL_AREA Distribution (Log Scale)**

Property size has near-zero correlation with price (r~0). Location dominates over size.

**Figure 3 — Count of Properties by Type**

Units dominate at ~88%. Residential: ~73%, Commercial: ~27%.

## 2️⃣ Bivariate Analysis

**Figure 4 — Actual Area vs Contract Amount (Log-Log Scatter)**

Five distinct market segments visible. 1,000x price variation confirms size-based benchmarks are unreliable.

**Figure 5 — Rooms vs Contract Amount (Box Plot)**

Staircase pricing pattern for Villa segment only (9,537 records). ROOMS has 96.4% null rate.

**Figure 6 — Freehold vs Contract Amount**

Freehold: AED 71,121 vs Non-Freehold: AED 60,654 — 17% premium.

**Figure 7 — Average Contract Amount by Start Year (2020+)**

Commercial market drives volatility. Residential prices remain consistent.

## 3️⃣ Multivariate Analysis

**Figure 8 — Correlation Matrix**

CONTRACT_DURATION_DAYS: r=0.56. TOTAL_PROPERTIES: r=0.53. ACTUAL_AREA: r~0.

**Figure 9 — Area vs Price by Freehold Status**

Freehold premium persists at all property sizes.

**Figure 10 — Pairplot of Key Numeric Features**

CONTRACT_DURATION_DAYS vs CONTRACT_AMOUNT shows clearest linear trend.

**Figure 11 — Contract Amount by Property Type**

Buildings: AED 1,500,000 median. Villas: AED 173,644. Units: AED 65,000.

**Figure 12 — Property Area vs Contract Amount by Property Type**

Property type mediates the area-price relationship.
 