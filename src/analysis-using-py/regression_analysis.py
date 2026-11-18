import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from forecasting_common import (
    OUTPUT_DIR, load_daily_demand, chronological_split,
    calculate_metrics, save_metrics, save_forecast
)

FORECAST_DAYS = 14

def main():
    daily = load_daily_demand()
    train, test = chronological_split(daily)

    # Use elapsed calendar days as the predictor.
    x_all = np.arange(len(daily)).reshape(-1, 1)
    x_train = x_all[:len(train)]
    x_test = x_all[len(train):]
    y_train = train.values
    y_test = test.values

    model = LinearRegression()
    model.fit(x_train, y_train)
    test_prediction = np.maximum(model.predict(x_test), 0)

    metrics = calculate_metrics(y_test, test_prediction)
    save_metrics("Linear Regression", metrics, "regression_metrics.csv")
    print(f"Training observations: {len(train)}")
    print(f"Testing observations: {len(test)}")
    print(f"Estimated trend: {model.coef_[0]:.4f} units per calendar day")

    # Refit on all available observations for the future forecast.
    model.fit(x_all, daily.values)
    future_x = np.arange(len(daily), len(daily) + FORECAST_DAYS).reshape(-1, 1)
    future_dates = pd.date_range(
        daily.index[-1] + pd.Timedelta(days=1),
        periods=FORECAST_DAYS,
        freq="D"
    )
    future_prediction = np.maximum(model.predict(future_x), 0)

    forecast = save_forecast(
        future_dates, future_prediction, "regression_forecast_14_days.csv"
    )

    plt.figure(figsize=(11, 5))
    plt.plot(daily.index, daily.values, marker="o", label="Historical recorded sales")
    plt.plot(
        future_dates, forecast["forecast_quantity"],
        marker="o", linestyle="--", label="Linear regression forecast"
    )
    plt.title("Coir Daily Sales: Linear Regression Forecast")
    plt.xlabel("Date")
    plt.ylabel("Quantity (units)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart = OUTPUT_DIR / "regression_forecast.png"
    plt.savefig(chart, dpi=300)
    plt.close()
    print(f"Chart saved: {chart}")

if __name__ == "__main__":
    main()
