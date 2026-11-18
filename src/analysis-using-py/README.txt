# Coir Business Analytics – Forecasting Scripts

Keep these four Python files in the same folder:
- forecasting_common.py
- demand_forecasting.py
- regression_analysis.py
- time_series_forecasting.py

Also place `coir_daily_demand.csv` in the data folder. It must contain:
`order_date,demand_quantity`

Export it from SQL Server using the completed/shipped daily sales query. The scripts treat calendar dates with no completed/shipped orders as zero recorded sales.

Install dependencies:
`python -m pip install pandas numpy matplotlib scikit-learn statsmodels`

Run:
`python demand_forecasting.py`
`python regression_analysis.py`
`python time_series_forecasting.py`

CSV tables and PNG charts are saved in the `outputs` folder.

Method note:
- Demand forecast: 7-day moving-average baseline.
- Regression: linear regression using elapsed calendar day.
- Time series: Holt damped-trend exponential smoothing, without seasonality.
- Regression and Holt metrics use the same chronological 80/20 train/test split.
- The available history is short; results are exploratory and should not be described as validated long-term market-demand forecasts.
