import os
import csv
import json
from collections import defaultdict
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def load_sales(path="sample_sales.csv"):
    with open(path) as f:
        return list(csv.DictReader(f))


def compute_forecast(sales, category):
    rows = [r for r in sales if r["category"] == category]
    if not rows:
        return None

    units = [int(r["units_sold"]) for r in rows]
    revenues = [float(r["revenue"]) for r in rows]
    months = [r["month"] for r in rows]

    avg_units = sum(units) / len(units)
    trend = units[-1] - units[0]
    peak_month = months[units.index(max(units))]
    low_month = months[units.index(min(units))]
    next_forecast = int(units[-1] * 1.05)  # simple 5% growth estimate

    return {
        "category": category,
        "months_analyzed": len(rows),
        "avg_monthly_units": round(avg_units, 1),
        "total_revenue": round(sum(revenues), 2),
        "trend_direction": "upward" if trend > 0 else "downward",
        "peak_month": peak_month,
        "lowest_month": low_month,
        "next_month_forecast": next_forecast,
        "last_month_units": units[-1]
    }


def explain_forecast(forecast_data):
    prompt = f"""
You are a retail business analyst. Here is the sales forecast data for a product category:

{json.dumps(forecast_data, indent=2)}

Write a clear, concise explanation (3-4 sentences) for a non-technical retail manager. Cover:
1. How the category has been performing
2. What the seasonal pattern looks like
3. What to expect next month and what action to take
"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def main():
    sales = load_sales()
    categories = list({r["category"] for r in sales})

    print("Available categories:", ", ".join(categories))
    category = input("\nEnter category to forecast: ").strip().lower()

    forecast = compute_forecast(sales, category)
    if not forecast:
        print(f"No data found for category: {category}")
        return

    print("\n--- Raw Forecast Data ---")
    for k, v in forecast.items():
        print(f"  {k}: {v}")

    print("\n--- Plain English Explanation ---")
    explanation = explain_forecast(forecast)
    print(explanation)


if __name__ == "__main__":
    main()
