from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DATA_DIR = REPO_ROOT / "data"
OUTPUT_DIR = REPO_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_FILE = DATA_DIR / "coir_daily_demand.csv"

def load_daily_demand():
    """Load SQL-exported daily completed/shipped sales and create a calendar-day series."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Missing {DATA_FILE.name}. Export the SQL query result to this file "
            "and place it beside the Python scripts."
        )

    raw = pd.read_csv(DATA_FILE)
    required = {"order_date", "demand_quantity"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

    raw["order_date"] = pd.to_datetime(raw["order_date"], errors="coerce")
    raw["demand_quantity"] = pd.to_numeric(raw["demand_quantity"], errors="coerce")
    raw = raw.dropna(subset=["order_date", "demand_quantity"])

    if raw.empty:
        raise ValueError("The CSV contains no valid dated demand observations.")
    if (raw["demand_quantity"] < 0).any():
        raise ValueError("Demand quantities cannot be negative.")

    daily = (
        raw.groupby("order_date")["demand_quantity"]
        .sum()
        .sort_index()
        .asfreq("D", fill_value=0)
        .astype(float)
    )

    if len(daily) < 20:
        raise ValueError(
            f"Only {len(daily)} calendar days are available. "
            "At least 20 calendar days are required for this project's basic "
            "chronological train/test evaluation."
        )

    print(f"Source file: {DATA_FILE.name}")
    print(f"Date range: {daily.index.min().date()} to {daily.index.max().date()}")
    print(f"Calendar days: {len(daily)}")
    print(f"Days with recorded sales: {(daily > 0).sum()}")
    print(f"Days with zero recorded sales: {(daily == 0).sum()}")
    print(
        "Note: missing dates are treated as zero completed/shipped sales. "
        "This represents recorded sales, not necessarily unmet market demand."
    )
    return daily

def chronological_split(series, test_fraction=0.20):
    split = int(len(series) * (1 - test_fraction))
    if split < 10 or len(series) - split < 3:
        raise ValueError("Not enough observations for a meaningful chronological split.")
    return series.iloc[:split], series.iloc[split:]

def calculate_metrics(actual, predicted):
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    return {
        "MAE": float(mean_absolute_error(actual, predicted)),
        "RMSE": float(np.sqrt(mean_squared_error(actual, predicted))),
        "R-squared": float(r2_score(actual, predicted)) if len(actual) >= 2 else float("nan"),
    }

def save_metrics(model_name, metrics, filename):
    result = pd.DataFrame(
        [{"Model": model_name, **metrics}]
    )
    path = OUTPUT_DIR / filename
    result.to_csv(path, index=False)
    print("\nEvaluation metrics (chronological holdout):")
    print(result.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"Saved: {path}")
    return result

def save_forecast(future_dates, values, filename, date_column="forecast_date"):
    result = pd.DataFrame({
        date_column: future_dates,
        "forecast_quantity": np.maximum(np.asarray(values, dtype=float), 0).round(2)
    })
    path = OUTPUT_DIR / filename
    result.to_csv(path, index=False)
    print("\n14-day forecast:")
    print(result.to_string(index=False))
    print(f"Saved: {path}")
    return result
