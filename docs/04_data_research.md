# 🔍 Data Research and Acquiring Effort
## Data Sources Evaluated
| Source | Decision | Reason |
|---|---|---|
| Bayut.com / PropertyFinder.ae | ❌ Rejected | Asking prices only, not actual contracts. Scraping legally restricted. |
| REIDIN UAE Database | ❌ Rejected | Paid commercial access incompatible with academic project budget. |
| Dubai Statistics Center | ❌ Rejected | Aggregate indices only. Lacks individual transaction records needed for ML. |
| **Dubai Land Department (DLD)** | ✅ **Selected** | Government-verified actual registered prices, free, open data, updated regularly. |
## ✅ Selected Dataset
| Property | Detail |
|---|---|
| **Source** | Dubai Land Department Open Data Portal |
| **URL** | https://www.dubaipulse.gov.ae/data/dld-transactions/dld_rental_contract-open |
| **File** | rents-2026-04-07.csv |
| **Raw Rows** | 300,564 |
| **Clean Rows** | 263,930 |
| **Columns** | 20 |
| **License** | Dubai Government Open Data License — free for academic use with DLD attribution |
> Every row = one legally registered rental contract filed with the Dubai Land Department.
## 📎 Secondary Reference
Dubai Statistics Center:
https://www.dsc.gov.ae/en-us/Themes/Pages/Real-Estate.aspx