# 🚀 Project Deployment — Use Case
## Deployment Method
Scheduled batch processing. Python code re-run on new DLD CSV. Power BI dashboard refreshes automatically.
## Target Users
| User | Page Used |
|---|---|
| 💹 Investment analysts | Investment Intelligence |
| 🏢 Property managers | Executive Summary |
| 👔 Executives | Key Influencers + Forecasting |
No coding expertise required.
## Implementation Steps
**Step 1 — Download Data**
https://www.dubaipulse.gov.ae
**Step 2 — Setup Environment**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt