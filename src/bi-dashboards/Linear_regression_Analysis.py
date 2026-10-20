import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

base = Path(__file__).resolve().parent
df = pd.read_csv(base / "coir_daily_demand.csv")

df["order_date"] = pd.to_datetime(df["order_date"])
df["demand_quantity"] = pd.to_numeric(
    df["demand_quantity"], errors="coerce"
)
df = df.dropna(subset=["order_date", "demand_quantity"])
df = df.groupby("order_date", as_index=False)["demand_quantity"].sum()
df = df.set_index("order_date").sort_index()
daily = df["demand_quantity"].asfreq("D", fill_value=0)

if len(daily) < 10:
    raise ValueError("At least 10 daily observations are recommended.")

data = pd.DataFrame({
    "day_number": np.arange(len(daily)),
    "demand_quantity": daily.values
})

# Use earlier 80% for training and later 20% for testing
split = int(len(data) * 0.8)
train = data.iloc[:split]
test = data.iloc[split:]

model = LinearRegression()
model.fit(train[["day_number"]], train["demand_quantity"])

test_prediction = np.maximum(
    model.predict(test[["day_number"]]), 0
)

mae = mean_absolute_error(
    test["demand_quantity"], test_prediction
)
rmse = np.sqrt(mean_squared_error(
    test["demand_quantity"], test_prediction
))

print("REGRESSION ANALYSIS")
print("-------------------")
print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R-squared: {model.score(test[['day_number']], test['demand_quantity']):.3f}")

# Train on all observations before forecasting
model.fit(data[["day_number"]], data["demand_quantity"])

future_days = np.arange(len(data), len(data) + 14)
future_prediction = np.maximum(
    model.predict(pd.DataFrame({"day_number": future_days})), 0
)
future_dates = pd.date_range(
    daily.index.max() + pd.Timedelta(days=1),
    periods=14,
    freq="D"
)

forecast = pd.DataFrame({
    "order_date": future_dates,
    "forecast_demand_quantity": future_prediction
})

output = base / "outputs"
output.mkdir(exist_ok=True)
forecast.to_csv(output / "regression_forecast.csv", index=False)

plt.figure(figsize=(12, 6))
plt.plot(daily.index, daily.values, label="Recorded sales")
plt.plot(
    future_dates, future_prediction,
    marker="o", linestyle="--", label="Regression forecast"
)
plt.title("Coir Sales - Linear Regression")
plt.xlabel("Date")
plt.ylabel("Quantity sold")
plt.legend()
plt.tight_layout()
plt.savefig(output / "regression_forecast.png", dpi=300)
plt.show()

print(forecast.to_string(index=False))
