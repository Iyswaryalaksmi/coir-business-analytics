
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# -------------------------------------------------
# 1. Find and load the CSV file
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "coir_daily_demand.csv"

if not csv_path.exists():
    raise FileNotFoundError(
        f"\nCSV file not found: {csv_path}\n"
        "Save coir_daily_demand.csv in the same folder "
        "as coir_forecasting.py."
    )

df = pd.read_csv(csv_path)

required_columns = {"order_date", "demand_quantity"}
if not required_columns.issubset(df.columns):
    raise ValueError(
        "CSV must contain columns: order_date, demand_quantity"
    )

df["order_date"] = pd.to_datetime(
    df["order_date"], errors="coerce"
)
df["demand_quantity"] = pd.to_numeric(
    df["demand_quantity"], errors="coerce"
)

df = df.dropna(
    subset=["order_date", "demand_quantity"]
)

# Combine duplicate dates
df = (
    df.groupby("order_date")["demand_quantity"]
    .sum()
    .sort_index()
)

# Daily frequency; missing dates become zero.
# Confirm that missing dates really mean zero demand
# before using this assumption with real business data.
df = df.asfreq("D", fill_value=0)

if len(df) < 10:
    raise ValueError(
        "Please provide at least 10 daily observations."
    )

print("\nHistorical demand data:")
print(df.tail())

# -------------------------------------------------
# 2. Linear regression model
# -------------------------------------------------
# Use earlier dates to train and later dates to test.
split = int(len(df) * 0.8)

if split == 0 or split >= len(df):
    raise ValueError("Not enough data for train/test split.")

day_numbers = list(range(len(df)))
X = pd.DataFrame({"day_number": day_numbers})
y = df.values

model = LinearRegression()
model.fit(X.iloc[:split], y[:split])

test_predictions = model.predict(
    X.iloc[split:]
).clip(min=0)

mae = mean_absolute_error(
    y[split:], test_predictions
)

print(f"\nRegression test MAE: {mae:.2f} units")
print(f"Estimated daily trend: {model.coef_[0]:.3f} units/day")

# -------------------------------------------------
# 3. Compare with a simple time-series baseline
# -------------------------------------------------
# Forecast each test day using the previous 7 days'
# average demand. This is a simple moving-average
# baseline, not a seasonal forecasting model.
baseline_predictions = []

for i in range(split, len(df)):
    previous_values = y[max(0, i - 7):i]
    baseline_predictions.append(previous_values.mean())

baseline_mae = mean_absolute_error(
    y[split:], baseline_predictions
)

print(
    f"7-day moving-average test MAE: "
    f"{baseline_mae:.2f} units"
)

# -------------------------------------------------
# 4. Train regression on all available data
# -------------------------------------------------
model.fit(X, y)

# -------------------------------------------------
# 5. Forecast the next 14 days
# -------------------------------------------------
forecast_days = 14

future_dates = pd.date_range(
    start=df.index[-1] + pd.Timedelta(days=1),
    periods=forecast_days,
    freq="D"
)

future_day_numbers = pd.DataFrame({
    "day_number": range(len(df), len(df) + forecast_days)
})

future_demand = model.predict(
    future_day_numbers
).clip(min=0)

forecast = pd.DataFrame({
    "forecast_date": future_dates,
    "forecast_demand": future_demand.round(0).astype(int)
})

# Save CSV for Power BI
output_path = BASE_DIR / "coir_demand_forecast.csv"

forecast.to_csv(output_path, index=False)

# -------------------------------------------------
# 6. Display the forecast
# -------------------------------------------------
print("\n14-DAY DEMAND FORECAST")
print(forecast.to_string(index=False))

print(f"\nForecast saved to: {output_path}")

# -------------------------------------------------
# 7. Plot historical demand and forecast
# -------------------------------------------------
plt.figure(figsize=(12, 6))

plt.plot(
    df.index,
    df.values,
    label="Historical demand"
)

plt.plot(
    future_dates,
    future_demand,
    marker="o",
    label="Regression forecast"
)

plt.title("Coir Demand Forecast - Next 14 Days")
plt.xlabel("Date")
plt.ylabel("Demand quantity (units)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

chart_path = BASE_DIR / "coir_demand_forecast.png"
plt.savefig(chart_path, dpi=150)

print(f"Chart saved to: {chart_path}")

plt.show()
