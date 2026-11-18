import matplotlib.pyplot as plt
import pandas as pd
from forecasting_common import OUTPUT_DIR, load_daily_demand, save_forecast

FORECAST_DAYS = 14
WINDOW = 7

def main():
    daily = load_daily_demand()

    # Simple 7-calendar-day moving-average baseline.
    # The same forecast value is carried forward for each future day.
    average = float(daily.tail(WINDOW).mean())
    future_dates = pd.date_range(
        daily.index[-1] + pd.Timedelta(days=1),
        periods=FORECAST_DAYS,
        freq="D"
    )
    predictions = [average] * FORECAST_DAYS

    forecast = save_forecast(
        future_dates, predictions, "demand_forecast_14_days.csv"
    )
    print(f"\nMethod: {WINDOW}-day moving-average baseline")
    print(f"Average of latest {WINDOW} calendar days: {average:.2f} units/day")

    plt.figure(figsize=(11, 5))
    plt.plot(daily.index, daily.values, marker="o", label="Historical recorded sales")
    plt.plot(
        future_dates, forecast["forecast_quantity"],
        marker="o", linestyle="--", label="Moving-average forecast"
    )
    plt.title("Coir Daily Sales: 14-Day Moving-Average Forecast")
    plt.xlabel("Date")
    plt.ylabel("Quantity (units)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart = OUTPUT_DIR / "demand_forecast_14_days.png"
    plt.savefig(chart, dpi=300)
    plt.close()
    print(f"Chart saved: {chart}")

if __name__ == "__main__":
    main()
