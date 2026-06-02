# ✅ Results
## 🏆 Model Performance
| Metric | Value |
|---|---|
| R² Score | **0.9510 (95.10%)** |
| MAE | **AED 71,130** |
| Test Set Size | 52,786 contracts |
| Industry Target R² | 0.85 |
| Exceeded By | +10.1% |
All linear models failed to exceed R²=0.52, confirming fundamental non-linearity of Dubai rental pricing. Neural Network failed with R²=0.0343 due to insufficient hyperparameter tuning.
## 💡 Key Business Findings
- 📍 **Location dominates** — Al Sufouh metro station has maximum contract value exceeding AED 3 billion
- 🏢 **Building scale** — Every 14.76 additional properties = AED 2.34M increase in predicted rental value
- 🔑 **Freehold premium** — 17% structural premium confirmed (AED 71,121 vs AED 60,654)
- 📈 **Top investment area** — Al Garhoud — highest positive GROWTH_PERCENTAGE signal
- ⚠️ **Risk areas** — Island 2 (-6,061%), Mushrif (-3,971%) — overpriced relative to model predictions
## 📅 Forecasting Output
| Scenario | Predicted Price |
|---|---|
| 📆 Next Month | ~AED 193,000 |
| 📆 Next Quarter | ~AED 187,000 |
| 📆 Next Year | ~AED 269,000 |
> ⚠️ Next Year figure reflects structural composition shift toward premium contracts, not market-wide inflation. Higher uncertainty due to only 127 training records with START_YEAR=2027.
## 🎯 Business Impact
This project replaces subjective agent-driven pricing with objective, data-verified market intelligence derived from 263,930 government-registered contracts — enabling faster, more accurate, and more defensible investment decisions across Dubai's diverse property market.
> *"We successfully translated 300,000 raw government files into an automated, predictive, and prescriptive pricing engine."*