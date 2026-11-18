import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from forecasting_common import (
    OUTPUT_DIR, load_daily_demand, chronological_split,
    calculate_metrics, save_metrics, save_forecast
)

FORECAST_DAYS = 14

def fit_holt_model(series):
    # No seasonal component: the available history is too short
    # to justify estimating a reliable weekly seasonal pattern.
    model = ExponentialSmoothing(
        series.astype(float),
        trend="add",
        damped_trend=True,
        seasonal=None,
        initialization_method="estimated"
    )
    return model.fit(optimized=True)

def main():
    daily = load_daily_demand()
    train, test = chronological_split(daily)

    # Evaluate on the same later chronological holdout used by regression.
    evaluation_model = fit_holt_model(train)
    test_prediction = evaluation_model.forecast(len(test)).clip(lower=0)

    metrics = calculate_metrics(test.values, test_prediction.values)
    save_metrics(
        "Holt Damped-Trend Exponential Smoothing",
        metrics,
        "time_series_metrics.csv"
    )
    print(f"Training observations: {len(train)}")
    print(f"Testing observations: {len(test)}")
    print("Seasonality: not fitted (limited historical period)")

    # Refit using all observations, then forecast 14 days.
    final_model = fit_holt_model(daily)
    future_values = final_model.forecast(FORECAST_DAYS).clip(lower=0)
    future_dates = pd.date_range(
        daily.index[-1] + pd.Timedelta(days=1),
        periods=FORECAST_DAYS,
        freq="D"
    )
    forecast = save_forecast(
        future_dates, future_values.values, "time_series_forecast_14_days.csv"
    )

    plt.figure(figsize=(11, 5))
    plt.plot(daily.index, daily.values, marker="o", label="Historical recorded sales")
    plt.plot(
        future_dates, forecast["forecast_quantity"],
        marker="o", linestyle="--", label="Holt forecast"
    )
    plt.title("Coir Daily Sales: Holt Exponential Smoothing Forecast")
    plt.xlabel("Date")
    plt.ylabel("Quantity (units)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart = OUTPUT_DIR / "time_series_forecast.png"
    plt.savefig(chart, dpi=300)
    plt.close()
    print(f"Chart saved: {chart}")

if __name__ == "__main__":
    main()
