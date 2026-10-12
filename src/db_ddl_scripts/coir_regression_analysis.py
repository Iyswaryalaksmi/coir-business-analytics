
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Load the dataset
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "coir_daily_demand.csv"

df = pd.read_csv(file_path)

# 2. Clean the data
df["order_date"] = pd.to_datetime(
    df["order_date"], errors="coerce"
).dt.normalize()

df["demand_quantity"] = pd.to_numeric(
    df["demand_quantity"], errors="coerce"
)

df = df.dropna(
    subset=["order_date", "demand_quantity"]
)

# 3. Aggregate daily demand
daily = (
    df.groupby("order_date")["demand_quantity"]
    .sum()
    .sort_index()
)

# Fill missing dates with zero observed sales.
# Verify that missing dates really mean zero sales.
daily = daily.asfreq("D", fill_value=0)

data = pd.DataFrame({
    "order_date": daily.index,
    "demand_quantity": daily.values
})

if len(data) < 10:
    raise ValueError("Please provide at least 10 daily observations.")

# 4. Create a numerical time variable
data["day_number"] = np.arange(len(data))

X = data[["day_number"]]
y = data["demand_quantity"]

# 5. Split data chronologically (80% training, 20% testing)
split = int(len(data) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

# 6. Train the regression model
model = LinearRegression()
model.fit(X_train, y_train)

# 7. Predict test-period demand
y_pred = model.predict(X_test)

# 8. Evaluate model performance
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

r2 = (
    r2_score(y_test, y_pred)
    if len(y_test) >= 2
    else float("nan")
)

print("\n--- REGRESSION ANALYSIS RESULTS ---")
print("Total observations:", len(data))
print("Regression intercept:", round(model.intercept_, 2))
print("Daily trend slope:", round(model.coef_[0], 2))
print("Mean Absolute Error (MAE):", round(mae, 2))
print("Root Mean Squared Error (RMSE):", round(rmse, 2))
print("R-squared:", round(r2, 3))

# 9. Fit the final model using all available data
final_model = LinearRegression()
final_model.fit(X, y)

# 10. Forecast demand for the next 14 days
future_dates = pd.date_range(
    start=data["order_date"].max() + pd.Timedelta(days=1),
    periods=14,
    freq="D"
)

future = pd.DataFrame({
    "forecast_date": future_dates,
    "day_number": np.arange(len(data), len(data) + 14)
})

future["forecast_demand"] = (
    final_model.predict(future[["day_number"]])
    .clip(min=0)
    .round(2)
)

# 11. Save forecast results
future.to_csv(
    BASE_DIR / "coir_regression_forecast.csv",
    index=False
)

# 12. Plot actual data, regression trend and forecast
plt.figure(figsize=(12, 6))

plt.plot(
    data["order_date"],
    data["demand_quantity"],
    marker="o",
    label="Actual Daily Quantity"
)

plt.plot(
    data["order_date"],
    final_model.predict(X),
    label="Regression Trend"
)

plt.plot(
    future["forecast_date"],
    future["forecast_demand"],
    marker="o",
    linestyle="--",
    label="14-Day Forecast"
)

plt.title("Coir Daily Demand - Linear Regression")
plt.xlabel("Date")
plt.ylabel("Quantity Sold")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    BASE_DIR / "coir_regression_analysis.png",
    dpi=150
)

plt.show()

print("\nForecast saved: coir_regression_forecast.csv")
print("Chart saved: coir_regression_analysis.png")
