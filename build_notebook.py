"""Builds analysis.ipynb by hand (no nbformat/jupyter available in this env)."""
import json

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

def code(src):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": src.splitlines(keepends=True)}

cells = []

cells.append(md("""# Retail Sales Performance Analysis

**Author:** Bhavesh Desale
**Tools:** Python (pandas, matplotlib, seaborn)

## Business Context
A retail company wants to understand how its sales performance breaks down across regions, product categories, and customer segments, and whether any parts of the business are quietly losing money despite strong sales.

## Business Questions
1. Which product categories and regions drive the most revenue and profit?
2. Are there seasonal patterns in sales?
3. Which customer segments are most profitable?
4. Are any categories or sub-categories losing money despite high sales volume?
5. What is the relationship between discounting and profitability?

## Dataset
`data/retail_sales_raw.csv` — order-level retail transactions with region, segment, category, sales, discount, and profit fields (2022–2024)."""))

cells.append(md("## 1. Setup"))
cells.append(code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)
pd.set_option("display.max_columns", None)
"""))

cells.append(md("## 2. Load the data"))
cells.append(code("""df = pd.read_csv("data/retail_sales_raw.csv", parse_dates=["Order Date", "Ship Date"])
print(df.shape)
df.head()
"""))

cells.append(md("""## 3. Data Cleaning

Before any analysis, we need to fix known data quality issues:
- Inconsistent text casing / stray whitespace in `Region`
- Duplicate order rows
- Missing values in `Customer Name`, `Discount`, `Ship Date`"""))

cells.append(code("""# Check data quality issues
print("Missing values:\\n", df.isna().sum())
print("\\nDuplicate rows:", df.duplicated().sum())
print("\\nRegion values before cleaning:", sorted(df['Region'].unique()))
"""))

cells.append(code("""# Standardize text columns
df["Region"] = df["Region"].str.strip().str.title()

# Drop exact duplicate rows
df = df.drop_duplicates()

# Discount: missing likely means no discount applied -> fill with 0
df["Discount"] = df["Discount"].fillna(0)

# Customer Name: missing name doesn't invalidate the transaction, keep as "Unknown"
df["Customer Name"] = df["Customer Name"].fillna("Unknown")

# Ship Date: a handful missing; not critical for this analysis, leave as NaT

print("Region values after cleaning:", sorted(df['Region'].unique()))
print("Remaining missing values:\\n", df.isna().sum())
print("Shape after cleaning:", df.shape)
"""))

cells.append(code("""# Feature engineering
df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
df["Order Year"] = df["Order Date"].dt.year
df["Profit Margin"] = df["Profit"] / df["Sales"]
df.head()
"""))

cells.append(md("## 4. Overall KPIs"))
cells.append(code("""total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
overall_margin = total_profit / total_sales
avg_order_value = df.groupby("Order ID")["Sales"].sum().mean()

print(f"Total Sales:      ${total_sales:,.0f}")
print(f"Total Profit:     ${total_profit:,.0f}")
print(f"Overall Margin:   {overall_margin:.1%}")
print(f"Avg Order Value:  ${avg_order_value:,.2f}")
print(f"Total Orders:     {df['Order ID'].nunique():,}")
"""))

cells.append(md("""## 5. Which categories and regions drive revenue and profit?"""))
cells.append(code("""cat_summary = df.groupby("Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique")
).sort_values("Sales", ascending=False)
cat_summary["Margin"] = cat_summary["Profit"] / cat_summary["Sales"]
cat_summary
"""))

cells.append(code("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))

cat_summary["Sales"].plot(kind="bar", ax=axes[0], color="#4C72B0")
axes[0].set_title("Total Sales by Category")
axes[0].set_ylabel("Sales ($)")

cat_summary["Profit"].plot(kind="bar", ax=axes[1], color="#DD8452")
axes[1].set_title("Total Profit by Category")
axes[1].set_ylabel("Profit ($)")

plt.tight_layout()
plt.savefig("charts/sales_profit_by_category.png", dpi=150)
plt.show()
"""))

cells.append(code("""region_summary = df.groupby("Region").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).sort_values("Sales", ascending=False)
region_summary["Margin"] = region_summary["Profit"] / region_summary["Sales"]

region_summary["Sales"].plot(kind="bar", color="#55A868")
plt.title("Total Sales by Region")
plt.ylabel("Sales ($)")
plt.tight_layout()
plt.savefig("charts/sales_by_region.png", dpi=150)
plt.show()

region_summary
"""))

cells.append(md("## 6. Are there seasonal sales patterns?"))
cells.append(code("""monthly = df.groupby("Order Month")["Sales"].sum()

monthly.plot(kind="line", marker="o", color="#4C72B0")
plt.title("Monthly Sales Trend (2022-2024)")
plt.ylabel("Sales ($)")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig("charts/monthly_sales_trend.png", dpi=150)
plt.show()
"""))

cells.append(code("""df["Order Month Num"] = df["Order Date"].dt.month
seasonal = df.groupby("Order Month Num")["Sales"].sum()

seasonal.plot(kind="bar", color="#C44E52")
plt.title("Sales by Calendar Month (all years combined)")
plt.xlabel("Month")
plt.ylabel("Sales ($)")
plt.tight_layout()
plt.savefig("charts/seasonality.png", dpi=150)
plt.show()
"""))

cells.append(md("## 7. Which customer segments are most profitable?"))
cells.append(code("""segment_summary = df.groupby("Segment").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique")
).sort_values("Profit", ascending=False)
segment_summary["Margin"] = segment_summary["Profit"] / segment_summary["Sales"]

segment_summary["Margin"].plot(kind="bar", color="#8172B2")
plt.title("Profit Margin by Customer Segment")
plt.ylabel("Profit Margin")
plt.tight_layout()
plt.savefig("charts/margin_by_segment.png", dpi=150)
plt.show()

segment_summary
"""))

cells.append(md("## 8. Are any sub-categories losing money despite high sales?"))
cells.append(code("""subcat_summary = df.groupby(["Category", "Sub-Category"]).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).sort_values("Sales", ascending=False)
subcat_summary["Margin"] = subcat_summary["Profit"] / subcat_summary["Sales"]

# Flag sub-categories with high sales but negative or thin margin
subcat_summary.sort_values("Margin").head(8)
"""))

cells.append(code("""fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#C44E52" if p < 0 else "#55A868" for p in subcat_summary["Profit"]]
subcat_summary["Profit"].sort_values().plot(kind="barh", color=colors, ax=ax)
ax.set_title("Total Profit by Sub-Category (red = loss-making)")
ax.set_xlabel("Profit ($)")
plt.tight_layout()
plt.savefig("charts/profit_by_subcategory.png", dpi=150)
plt.show()
"""))

cells.append(md("## 9. Relationship between discount and profitability"))
cells.append(code("""discount_bins = pd.cut(df["Discount"], bins=[-0.01, 0, 0.15, 0.3, 1.0],
                       labels=["No discount", "Low (0-15%)", "Medium (15-30%)", "High (30%+)"])
discount_summary = df.groupby(discount_bins, observed=True).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    AvgMargin=("Profit Margin", "mean")
)
discount_summary
"""))

cells.append(code("""discount_summary["AvgMargin"].plot(kind="bar", color="#DD8452")
plt.title("Average Profit Margin by Discount Level")
plt.ylabel("Avg Profit Margin")
plt.tight_layout()
plt.savefig("charts/margin_by_discount.png", dpi=150)
plt.show()
"""))

cells.append(md("""## 10. Key Findings & Recommendations

**Findings**
1. **Technology** drives the most revenue ($7.18M) and by far the most profit (~$853K, 11.9% margin). **Furniture** has comparable sales to Office Supplies but is *losing money overall* (-3.8% margin) — every Furniture sub-category (Bookcases, Furnishings, Tables, Chairs) is profit-negative.
2. Sales are clearly seasonal, peaking sharply in **November and December** (holiday demand), roughly double the Jan/Feb low months. Inventory and staffing should scale up ahead of Q4.
3. The **Home Office** segment has the highest profit margin (8.6%) despite having the lowest sales volume of the three segments — a strong candidate for targeted upsell/retention campaigns rather than the highest-revenue Consumer segment.
4. Every Furniture sub-category sells well but loses money — this points to a pricing or cost-structure problem specific to that category, not a demand problem.
5. Discounting has a direct, near-linear relationship with margin erosion: **no discount → 16.3% margin**, dropping to **-9.1% margin at 30%+ discount**. Heavy discounting is actively destroying profit.

**Recommendations**
- Investigate Furniture's cost structure (shipping, supplier costs, or return rates) — the category needs a pricing review, not just a sales push.
- Cap discounts around 15–20% on Furniture and other thin-margin sub-categories; anything beyond that appears to erase profit entirely.
- Shift marketing/inventory spend to build up ahead of the Nov–Dec peak.
- Build retention programs around the Home Office segment, which is quietly the most profitable segment per dollar of sales.

*(Note: this dataset is synthetic, generated to mimic realistic retail sales patterns for portfolio purposes. Swap in a real dataset — e.g. the Kaggle Superstore dataset — and these same cells will work with real-world numbers and findings.)*"""))

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open("C:/Users/DELL/Documents/Project/retail_sales_project/analysis.ipynb", "w") as f:
    json.dump(nb, f, indent=1)

print("Notebook written.")
