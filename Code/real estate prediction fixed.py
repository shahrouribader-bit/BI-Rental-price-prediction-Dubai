# %% [markdown]
# # Real Estate Price Prediction
#
# ## Phase 1 - Business Understanding
# **Project Objective:** Predict future real estate prices (CONTRACT_AMOUNT) in the UAE.
#
# **Main target variable:** `CONTRACT_AMOUNT`

# %%
import os
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
import joblib

def add_value_labels(ax, prefix='', suffix='', decimals=0):
   for p in ax.patches:
       value = p.get_height()
       if value > 0:
           ax.annotate(
               f'{prefix}{value:,.{decimals}f}{suffix}',
               (p.get_x() + p.get_width() / 2., value),
               ha='center', va='bottom',
               fontsize=8, fontweight='bold'
           )

warnings.filterwarnings('ignore')

# Set aesthetic style
sns.set_theme(style="whitegrid", palette="muted")

# Set global random seeds for reproducibility
np.random.seed(42)
random.seed(42)
os.environ['PYTHONHASHSEED'] = '42'

# Create output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# %% [markdown]
# ## Phase 2 - Data Preparation

# %%
print("Loading dataset...")

# Try relative path first (when run from project subfolder), then fallback to root
csv_path = os.path.join("..", "..", "rents-2026-04-07.csv")
if not os.path.exists(csv_path):
    csv_path = "rents-2026-04-07.csv"

df = pd.read_csv(csv_path)

# Drop duplicates
df.drop_duplicates(inplace=True)

# Convert dates to datetime
for col in ['REGISTRATION_DATE', 'START_DATE', 'END_DATE']:
    df[col] = pd.to_datetime(df[col], errors='coerce')

# Convert numeric fields
for col in ['CONTRACT_AMOUNT', 'ANNUAL_AMOUNT', 'ACTUAL_AREA', 'ROOMS', 'PARKING']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# %% [markdown]
# ## Phase 3 - Data Cleaning

# %%
# Fill missing proximity fields with 'Unknown' to retain rows
for col in ['NEAREST_METRO_EN', 'NEAREST_MALL_EN', 'NEAREST_LANDMARK_EN']:
    df[col] = df[col].fillna('Unknown')

# Remove physically impossible records
initial_len = len(df)
df = df[df['ACTUAL_AREA'] > 0]
df = df[df['CONTRACT_AMOUNT'] > 0]
df = df[(df['ROOMS'].isnull()) | (df['ROOMS'] <= 50)]

# Drop rows where essential columns are missing
df.dropna(
    subset=['CONTRACT_AMOUNT', 'REGISTRATION_DATE', 'START_DATE', 'END_DATE', 'ACTUAL_AREA'],
    inplace=True
)

print(f"Data cleaned. Rows remaining: {len(df)} (Original: {initial_len})")

# %% [markdown]
# ## Phase 4 - Feature Engineering & Exploratory Data Analysis

# %%
# Use START_DATE (actual contract start) for temporal features — not REGISTRATION_DATE
# REGISTRATION_DATE is clustered entirely in 2026 (administrative logging date)
# START_DATE is distributed across 2020-2030 (when contracts actually began)
df['START_YEAR']  = df['START_DATE'].dt.year
df['START_MONTH'] = df['START_DATE'].dt.month

# Filter for post-pandemic data (2020 onwards) to remove historical noise
df = df[df['START_YEAR'] >= 2020]

# Contract duration — strongest numeric predictor (r=0.56 with price)
df['CONTRACT_DURATION_DAYS'] = (df['END_DATE'] - df['START_DATE']).dt.days

# Price per area — used for EDA and outlier analysis only, not a model feature
df['PRICE_PER_AREA'] = df['CONTRACT_AMOUNT'] / df['ACTUAL_AREA']

print(f"After 2020 filter: {len(df)} rows")
print(f"START_YEAR range: {df['START_YEAR'].min()} – {df['START_YEAR'].max()}")

print("\nGenerating EDA visualizations...")

# Sample for faster scatter plots
sample_df = df.sample(min(10000, len(df)), random_state=42)

# ── 1. UNIVARIATE ANALYSIS ─────────────────────────────────────────────────────

# Distribution of Contract Amount
plt.figure(figsize=(10, 5))
sns.histplot(df['CONTRACT_AMOUNT'], bins=100, kde=True, color='blue')
plt.title('Distribution of Contract Amount')
plt.xscale('log')
plt.xlabel('Contract Amount (Log Scale)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'dist_contract_amount.png'))
plt.close()

# Distribution of Actual Area
plt.figure(figsize=(10, 5))
sns.histplot(df['ACTUAL_AREA'], bins=100, kde=True, color='green')
plt.title('Distribution of Actual Area')
plt.xscale('log')
plt.xlabel('Actual Area (Log Scale)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'dist_actual_area.png'))
plt.close()

# Property Type Count
plt.figure(figsize=(10, 5))
sns.countplot(
    y='PROP_TYPE_EN', data=df,
    order=df['PROP_TYPE_EN'].value_counts().index,
    palette='viridis'
)
plt.title('Count of Properties by Type')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'dist_property_type.png'))
plt.close()

# Median Contract Amount by Property Type - Bar Chart
plt.figure(figsize=(10, 6))
prop_median = df.groupby('PROP_TYPE_EN')['CONTRACT_AMOUNT'].median().sort_values(ascending=False).reset_index()
ax = sns.barplot(
   x='PROP_TYPE_EN',
   y='CONTRACT_AMOUNT',
   data=prop_median,
   order=prop_median['PROP_TYPE_EN'],
   palette='viridis'
)
for p in ax.patches:
   ax.annotate(
       f'AED {p.get_height():,.0f}',
       (p.get_x() + p.get_width() / 2., p.get_height()),
       ha='center', va='bottom',
       fontsize=9
   )

plt.title('Median Contract Amount by Property Type')
plt.xlabel('Property Type')
plt.ylabel('Median Contract Amount (AED)')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'dist_contract_amount_by_property_type.png'))
plt.close()

# Usage Type Count
plt.figure(figsize=(10, 5))
sns.countplot(
    y='USAGE_EN', data=df,
    order=df['USAGE_EN'].value_counts().index,
    palette='magma'
)
plt.title('Count of Properties by Usage Type')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'dist_usage_type.png'))
plt.close()

# ── 2. BIVARIATE ANALYSIS ──────────────────────────────────────────────────────

# Actual Area vs Contract Amount
plt.figure(figsize=(10, 6))
sns.scatterplot(
   x='ACTUAL_AREA',
   y='CONTRACT_AMOUNT',
   hue='PROP_TYPE_EN',
   data=sample_df,
   alpha=0.5,
   palette='tab10'
)
plt.title('Relationship: Actual Area vs Contract Amount')
plt.xlabel('Actual Area')
plt.ylabel('Contract Amount')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'rel_area_vs_price.png'))
plt.close()

# Number of Rooms vs Contract Amount
plt.figure(figsize=(10, 6))
sns.boxplot(x='ROOMS', y='CONTRACT_AMOUNT', data=df)
plt.title('Relationship: Number of Rooms vs Contract Amount')
plt.yscale('log')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'rel_rooms_vs_price.png'))
plt.close()

# Freehold Status vs Contract Amount
plt.figure(figsize=(8, 6))
freehold_avg = df.groupby('IS_FREE_HOLD_EN')['CONTRACT_AMOUNT'].median().reset_index()
ax = sns.barplot(x='IS_FREE_HOLD_EN', y='CONTRACT_AMOUNT', data=freehold_avg, palette='Set2')
add_value_labels(ax, prefix='AED')
plt.title('Median Contract Amount: Freehold vs Non-Freehold')
plt.xlabel('Freehold Status')
plt.ylabel('Median Contract Amount (AED)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'rel_freehold_vs_price.png'))
plt.close()

# Average Contract Amount by Start Year - Split by Usage Type
plt.figure(figsize=(10, 6))
yearly_usage = df.groupby(
   ['START_YEAR', 'USAGE_EN'])['CONTRACT_AMOUNT'].mean().reset_index()
sns.lineplot(
   x='START_YEAR',
   y='CONTRACT_AMOUNT',
   hue='USAGE_EN',
   data=yearly_usage,
   marker='o',
   palette='tab10'
)
plt.title('Average Contract Amount by Start Year — Split by Usage Type')
plt.xlabel('Start Year')
plt.ylabel('Average Contract Amount (AED)')
plt.legend(title='Usage Type')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'rel_year_vs_price.png'))
plt.close()

# ── 3. MULTIVARIATE ANALYSIS ───────────────────────────────────────────────────

# Correlation Heatmap
plt.figure(figsize=(12, 10))
numeric_vars = [
    'CONTRACT_AMOUNT', 'ACTUAL_AREA', 'ROOMS', 'PARKING',
    'TOTAL_PROPERTIES', 'START_YEAR', 'CONTRACT_DURATION_DAYS', 'PRICE_PER_AREA'
]
corr = df[numeric_vars].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Multivariate: Correlation Matrix of Numeric Variables')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'multi_correlation_matrix.png'))
plt.close()

# Pairplot of key numeric features
key_vars = ['CONTRACT_AMOUNT', 'ACTUAL_AREA', 'ROOMS', 'CONTRACT_DURATION_DAYS']
pairplot_sample = df[key_vars].dropna().sample(min(2000, len(df)), random_state=42)
g = sns.pairplot(pairplot_sample, diag_kind='kde')
g.fig.suptitle('Multivariate: Pairplot of Key Metrics', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'multi_pairplot.png'))
plt.close()

# Area vs Price by Freehold Status
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x='ACTUAL_AREA', y='CONTRACT_AMOUNT',
    hue='IS_FREE_HOLD_EN', data=sample_df,
    alpha=0.6, palette='Dark2'
)
plt.title('Multivariate: Area vs Price split by Freehold Status')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'multi_area_price_freehold.png'))
plt.close()

print("EDA visualizations saved.")

# %% [markdown]
# ## Phase 5 - Predictive Analysis & Phase 6 - Model Evaluation

# %%
features = [
    'AREA_EN', 'ACTUAL_AREA', 'PROP_TYPE_EN', 'PROP_SUB_TYPE_EN',
    'ROOMS', 'USAGE_EN', 'PARKING', 'IS_FREE_HOLD_EN',
    'NEAREST_METRO_EN', 'TOTAL_PROPERTIES',
    'START_YEAR', 'START_MONTH', 'CONTRACT_DURATION_DAYS'
]
target = 'CONTRACT_AMOUNT'

# Define column types
categorical_features = [
    'AREA_EN', 'PROP_TYPE_EN', 'PROP_SUB_TYPE_EN',
    'USAGE_EN', 'IS_FREE_HOLD_EN', 'NEAREST_METRO_EN'
]
numeric_features = [
    'ACTUAL_AREA', 'ROOMS', 'PARKING', 'TOTAL_PROPERTIES',
    'START_YEAR', 'START_MONTH', 'CONTRACT_DURATION_DAYS'
]

X = df[features].copy()
y = df[target].copy()

# ── BUG FIX: Fill numeric and categorical columns separately ──────────────────
# Filling numeric columns with a number, categorical columns with a string.
# The original code used X.fillna('Unknown') on the whole dataframe which crashes
# because pandas cannot store the string 'Unknown' in a float64 numeric column.

# Numeric columns: fill with 0 or 1
X['ROOMS']   = X['ROOMS'].fillna(0)
X['PARKING'] = X['PARKING'].fillna(0)
X['TOTAL_PROPERTIES'] = pd.to_numeric(X['TOTAL_PROPERTIES'], errors='coerce').fillna(1)

# Categorical columns: fill with 'Unknown' and ensure string type
for col in categorical_features:
    X[col] = X[col].fillna('Unknown').astype(str)
# ─────────────────────────────────────────────────────────────────────────────

# Train / test split — 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        # drop='first' removes the dummy variable trap for linear models
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False, drop='first'), categorical_features)
    ]
)

# Five models to evaluate
models = {
    'Linear Regression':      LinearRegression(),
    'Ridge (Linear Variant)': Ridge(),
    'Decision Tree':          DecisionTreeRegressor(random_state=42),
    'Random Forest':          RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1),
    # max_iter=200 keeps Neural Network from timing out on large datasets
    'Neural Network':         MLPRegressor(random_state=42, max_iter=200)
}

# Subsample for faster evaluation on large datasets (>50k rows)
if len(X_train) > 50000:
    print("Subsampling to 50,000 rows for model evaluation speed...")
    X_train_sub = X_train.sample(50000, random_state=42)
    y_train_sub = y_train.loc[X_train_sub.index]
else:
    X_train_sub = X_train
    y_train_sub = y_train

best_model_name = None
best_model      = None
best_r2         = -float('inf')
results         = {}

print("Evaluating models...")
for name, model in models.items():
    print(f"  Training {name}...")
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
    pipeline.fit(X_train_sub, y_train_sub)
    y_pred = pipeline.predict(X_test)

    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = r2_score(y_test, y_pred)

    results[name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
    print(f"    [{name}]  MAE: {mae:,.0f}  RMSE: {rmse:,.0f}  R2: {r2:.4f}")

    if r2 > best_r2:
        best_r2         = r2
        best_model_name = name
        best_model      = pipeline

print(f"\nBest Model: {best_model_name}  R2: {best_r2:.4f}")

# Save metrics to CSV
results_df = pd.DataFrame.from_dict(results, orient='index').reset_index()
results_df.rename(columns={'index': 'Model'}, inplace=True)
results_df.to_csv(os.path.join(output_dir, 'model_metrics.csv'), index=False)
print("model_metrics.csv saved.")

# Save the best model pipeline for the Streamlit app
print(f"Saving {best_model_name} to {output_dir}/model_artifacts.pkl...")
joblib.dump(best_model, os.path.join(output_dir, 'model_artifacts.pkl'))

# Model comparison bar chart
plt.figure(figsize=(10, 6))
model_names = list(results.keys())
r2_scores   = [results[m]['R2'] for m in model_names]
ax = sns.barplot(x=r2_scores, y=model_names, palette='viridis')
for p in ax.patches:
   ax.annotate(
       f'R²={p.get_width():.4f}',
       (p.get_width(), p.get_y() + p.get_height() / 2.),
       ha='left', va='center',
       fontsize=8, fontweight='bold'
   )
plt.title('Model Comparison - R² Score (Accuracy)')
plt.xlabel('R² Score')
plt.xlim(max(0, min(r2_scores) - 0.1), 1.0)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'model_comparison_r2.png'))
plt.close()

# Actual vs Predicted scatter for best model
test_predictions = best_model.predict(X_test)
plt.figure(figsize=(8, 8))
plt.scatter(y_test, test_predictions, alpha=0.3, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.title(f'Actual vs Predicted Prices ({best_model_name})')
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'prediction_actual_vs_predicted.png'))
plt.close()

# Save cleaned dataset
df.to_csv(os.path.join(output_dir, 'cleaned_dataset.csv'), index=False)
print("cleaned_dataset.csv saved.")

# %% [markdown]
# ## Phase 7 - Future Forecasting
#
# NOTE: The three scenarios (Next Month, Next Quarter, Next Year) are
# SNAPSHOT PRICE ESTIMATES for different property profiles — not time-trend
# forecasts. The variation across scenarios reflects the different START_YEAR
# values assigned to each scenario, which the model uses as a temporal signal.
# Next Year shows higher predicted prices because contracts with a 2027 start
# date tend to be associated with higher-value property profiles in the dataset.
# This is NOT a projection of Dubai market price growth over time.
# A genuine time-trend forecast would require multi-year historical DLD data.

# %%
print("\nGenerating future forecasts...")

future_profiles = df[[
    'AREA_EN', 'PROP_TYPE_EN', 'PROJECT_EN', 'ACTUAL_AREA', 'PROP_SUB_TYPE_EN',
    'ROOMS', 'USAGE_EN', 'PARKING', 'IS_FREE_HOLD_EN', 'NEAREST_METRO_EN',
    'TOTAL_PROPERTIES', 'CONTRACT_DURATION_DAYS'
]].drop_duplicates().head(5000)

# Base date from REGISTRATION_DATE (the latest date in the dataset)
last_date = df['REGISTRATION_DATE'].max()
print(f"Last registration date in dataset: {last_date.date()}")

scenarios = {
    'Next Month':   last_date + pd.DateOffset(months=1),
    'Next Quarter': last_date + pd.DateOffset(months=3),
    'Next Year':    last_date + pd.DateOffset(years=1)
}

forecast_dfs = []
for scenario_name, target_date in scenarios.items():
    temp_df = future_profiles.copy()
    temp_df['START_YEAR']  = target_date.year
    temp_df['START_MONTH'] = target_date.month
    temp_df['SCENARIO']    = scenario_name
    print(f"  {scenario_name}: START_YEAR={target_date.year}, START_MONTH={target_date.month}")
    forecast_dfs.append(temp_df)

forecast_data = pd.concat(forecast_dfs, ignore_index=True)

# Ensure categorical columns are strings before predicting
for col in categorical_features:
    forecast_data[col] = forecast_data[col].fillna('Unknown').astype(str)

forecast_data['PREDICTED_CONTRACT_AMOUNT'] = best_model.predict(forecast_data[features])

# Forecasting bar chart
plt.figure(figsize=(8, 6))
scenario_avg = forecast_data.groupby('SCENARIO')['PREDICTED_CONTRACT_AMOUNT'].mean().reset_index()
scenario_avg['SCENARIO'] = pd.Categorical(
    scenario_avg['SCENARIO'],
    categories=['Next Month', 'Next Quarter', 'Next Year'],
    ordered=True
)
scenario_avg = scenario_avg.sort_values('SCENARIO')
print("\nAverage predicted price per scenario:")
for _, row in scenario_avg.iterrows():
    print(f"  {row['SCENARIO']}: AED {row['PREDICTED_CONTRACT_AMOUNT']:,.0f}")

ax = sns.barplot(x='SCENARIO', y='PREDICTED_CONTRACT_AMOUNT', data=scenario_avg, palette='magma')
add_value_labels(ax, prefix='AED ')
plt.title('Forecasting: Average Projected Property Price')
plt.ylabel('Average Predicted Contract Amount (AED)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'forecast_trends.png'))
plt.close()

# %% [markdown]
# ## Phase 8 - Export Results

# %%
print("\nExporting final results...")

# Historical evaluation results
test_results = X_test.copy()
test_results['ACTUAL_PRICE']      = y_test
test_results['PREDICTED_PRICE']   = test_predictions
test_results['DIFFERENCE']        = test_results['PREDICTED_PRICE'] - test_results['ACTUAL_PRICE']
test_results['GROWTH_PERCENTAGE'] = (test_results['DIFFERENCE'] / test_results['ACTUAL_PRICE']) * 100

export_df = pd.merge(
    test_results,
    df[['PROJECT_EN']],
    left_index=True, right_index=True,
    how='left'
)
export_df['SCENARIO'] = 'Historical Evaluation'

# Align forecast columns
forecast_out = forecast_data.rename(columns={'PREDICTED_CONTRACT_AMOUNT': 'PREDICTED_PRICE'})
forecast_out['ACTUAL_PRICE']      = np.nan
forecast_out['DIFFERENCE']        = np.nan
forecast_out['GROWTH_PERCENTAGE'] = np.nan

# Master combined file for Power BI
combined_output = pd.concat([export_df, forecast_out], ignore_index=True)

export_df.to_csv(os.path.join(output_dir, 'predictions_output.csv'), index=False)
forecast_out.to_csv(os.path.join(output_dir, 'future_forecasts.csv'), index=False)
combined_output.to_csv(os.path.join(output_dir, 'combined_predictions_and_forecasts.csv'), index=False)

print(f"\npredictions_output.csv:              {len(export_df):,} rows (Historical Evaluation)")
print(f"future_forecasts.csv:                {len(forecast_out):,} rows (3 scenarios)")
print(f"combined_predictions_and_forecasts:  {len(combined_output):,} rows (master file)")
print(f"\nAll files saved to '{output_dir}/' directory.")
print("\nFinal model results summary:")
print("-" * 65)
for name, v in results.items():
    star = " ⭐" if name == best_model_name else ""
    print(f"  {name:<28}  MAE={v['MAE']:>10,.0f}  R2={v['R2']:.4f}{star}")
print("-" * 65)
