# Retail Demand Forecasting Explainer

Combines a simple statistical forecasting model with Claude to generate plain-English explanations for non-technical retail managers.

## Features
- Loads monthly sales data by category
- Computes trend, peak/low months, and next-month forecast
- Claude explains the numbers in business-friendly language

## Setup
```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here
python forecaster.py
```

## Example Output
```
--- Raw Forecast Data ---
  category: jacket
  avg_monthly_units: 215.0
  trend_direction: upward
  peak_month: 2024-12
  next_month_forecast: 472

--- Plain English Explanation ---
Jacket sales show a strong seasonal pattern peaking in winter months...
```

## Tech
- Claude claude-sonnet-4-6 for natural language explanation
- Pure Python forecasting (no external ML libraries required)
