
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# 1. Find the CSV beside this Python script
BASE_DIR = Path(__file__).resolve().parent
input_file = BASE_DIR / "coir_daily_demand.csv"

if not input_file.exists():
    raise FileNotFoundError(
        f"CSV not found: {input_file}\n"
        "Save coir_daily_demand.csv beside this script."
    )

# 2. Read and validate the data
df = pd.read_csv(input_file)

required = {"order_date", "demand_quantity"}
if not required.issubset(df.columns):
    raise ValueError(
        "CSV needs columns: order_date, demand_quantity"
    )

df["order_date"] = pd.to_datetime(
    df["order_date"], errors="coerce"
)
df["demand_quantity"] = pd.to_numeric(
    df["demand_quantity"], errors="coerce"
)
df = df.dropna(subset=["order_date", "demand_quantity"])

# Combine multiple records from the same date
series = (
    df.groupby("order_date")["demand_quantity"]
    .sum()
    .sort_index()
)

# Create daily frequency.
# Missing dates become zero; verify this is appropriate
# for your real business data.
series = series.asfreq("D", fill_value=0).astype(float)

if len(series) < 14:
    raise ValueError(
        "Use at least 14 daily observations. "
        "More history is strongly recommended."
    )

print("Historical observations:", len(series))
print("First date:", series.index.min().date())
print("Last date:", series.index.max().date())

# 3. Hold out the latest 20% of dates for evaluation
split = int(len(series) * 0.8)
train = series.iloc[:split]
test = series.iloc[split:]

# Use weekly seasonality only if training has at least
# 4 complete weekly cycles. Otherwise use trend only.
use_seasonality = len(train) >= 28

if use_seasonality:
    model = ExponentialSmoothing(
        train,
        trend="add",
        seasonal="add",
        seasonal_periods=7,
        initialization_method="estimated"
    )
else:
    model = ExponentialSmoothing(
        train,
        trend="add",
        initialization_method="estimated"
    )

fitted_model = model.fit(optimized=True)

# 4. Predict the held-out period
test_predictions = fitted_model.forecast(len(test)).clip(lower=0)
mae = mean_absolute_error(test, test_predictions)

print("\nTIME-SERIES MODEL EVALUATION")
print(f"Mean Absolute Error (MAE): {mae:.2f} units")
print("Weekly seasonality used:", use_seasonality)

# 5. Refit on all available history
if use_seasonality:
    final_model = ExponentialSmoothing(
        series,
        trend="add",
        seasonal="add",
        seasonal_periods=7,
        initialization_method="estimated"
    )
else:
    final_model = ExponentialSmoothing(
        series,
        trend="add",
        initialization_method="estimated"
    )

final_fit = final_model.fit(optimized=True)

# 6. Forecast the next 14 days
forecast_days = 14
future_dates = pd.date_range(
    start=series.index[-1] + pd.Timedelta(days=1),
    periods=forecast_days,
    freq="D"
)

forecast_values = final_fit.forecast(forecast_days).clip(lower=0)

forecast_df = pd.DataFrame({
    "forecast_date": future_dates,
    "forecast_demand": forecast_values.round(0).astype(int)
})

# Save output for Power BI
output_file = BASE_DIR / "coir_time_series_forecast.csv"
forecast_df.to_csv(output_file, index=False)

print("\nNEXT 14 DAYS FORECAST")
print(forecast_df.to_string(index=False))
print(f"\nForecast saved to: {output_file}")

# 7. Plot history and future forecast
plt.figure(figsize=(12, 6))
plt.plot(series.index, series.values, label="Historical demand")
plt.plot(
    future_dates,
    forecast_values,
    marker="o",
    label="Time-series forecast"
)
plt.axvline(
    series.index[-1],
    linestyle="--",
    label="Forecast starts"
)
plt.title("Coir Demand Forecast - Exponential Smoothing")
plt.xlabel("Date")
plt.ylabel("Demand quantity (units)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

chart_file = BASE_DIR / "coir_time_series_forecast.png"
plt.savefig(chart_file, dpi=150)
plt.show()

print(f"Chart saved to: {chart_file}")
