# 📱 Dashboard Design and Business Insights

Three-page Power BI dashboard built on combined_predictions_and_forecasts.csv (67,790 rows).

---

## 🏠 Page 1 — Executive Summary

**Audience:** Senior executives, investment directors, policy makers

### KPI Cards

| Card | Value |

|---|---|

| 📋 Total Contracts Analyzed | 68K |

| 📉 Average Prediction Error (MAE) | AED 71,130 |

| 💰 Median Predicted Contract | AED 69,000 |

| 📍 Top Model-Predicted Underpriced Area | Al Garhoud |

### Model Accuracy KPI Gauge

R² = 0.95 vs Target 0.85 (+11.88%)

### Donut Chart

Residential: 74.57% vs Commercial: 25.43%

### Bar Charts

- Top 10 Areas by Average Rental Contract Value — Palm Jumeirah leads at AED 14M

- Top 10 Areas by Count of Contracts — Jabal Ali Industrial First leads with 896 contracts

---

## 💹 Page 2 — Investment Intelligence

**Audience:** Investment analysts, portfolio managers, acquisition teams

### GROWTH_PERCENTAGE Formula

GROWTH_PERCENTAGE = ((PREDICTED_PRICE - ACTUAL_PRICE) / ACTUAL_PRICE) × 100

- ✅ Positive = Underpriced = Buy Signal

- ❌ Negative = Overpriced = Risk Warning

### Top 10 Underpriced Areas (Green)

Saih Shuaib 1 (2,853%), Trade Center Second, Al Garhoud (4M%)

### Top 10 Overpriced Areas (Red)

Island 2 (-6,061%), Mushrif (-3,971%), Madinat Hind 1 (-3,245%)

### Conditional Formatting Table

Area | Sum Actual Price | Sum Predicted Price | Average Growth %

---

## 🤖 Page 3 — Key Influencers + Forecasting

**Audience:** Strategic planners, development teams, executives

### Forecast KPI Cards

| Scenario | Predicted Price |

|---|---|

| 📆 Next Month | AED 193,050 |

| 📆 Next Quarter | AED 187,210 |

| 📆 Next Year | AED 269,060 |
> ⚠️ The 39% increase to Next Year reflects structural shift toward premium contracts — NOT market inflation.

### Key Influencers

Top driver: Every 14.76 additional properties in a building = AED 2.34M increase in predicted rental value.
 