# Retail Sales Performance Analysis

A Python (pandas) analysis of retail sales data to identify revenue and profit drivers, seasonal trends, and underperforming product categories — with data-backed recommendations.

## Business Questions
1. Which product categories and regions drive the most revenue and profit?
2. Are there seasonal patterns in sales?
3. Which customer segments are most profitable?
4. Are any categories losing money despite high sales volume?
5. How does discounting affect profitability?

## Tools
- **Python**: pandas, numpy, matplotlib, seaborn
- **Jupyter Notebook** for analysis and narrative

## Dataset
`data/retail_sales_raw.csv` — ~9,800 order-level retail transactions (2022–2024) with region, customer segment, product category/sub-category, sales, discount, and profit fields. Includes intentional data quality issues (missing values, duplicate rows, inconsistent text formatting) to demonstrate a real cleaning workflow.

> This dataset is synthetically generated to mimic realistic retail sales patterns (seasonality, category-level margin differences, discount-driven profit erosion). To adapt this project with real-world data, swap in the [Kaggle Superstore dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) — the notebook's column names and logic are compatible with minor tweaks.

## Key Findings

| Metric | Result |
|---|---|
| Total Sales | $11.4M |
| Total Profit | $940K (8.2% margin) |
| Highest revenue category | Technology ($7.18M, 11.9% margin) |
| Loss-making category | **Furniture** (-3.8% margin — every sub-category loses money) |
| Peak sales months | November & December (holiday demand) |
| Most profitable segment | Home Office (8.6% margin, despite lowest sales volume) |
| Discount impact | Margin drops from **16.3%** (no discount) to **-9.1%** (30%+ discount) |

### Recommendations
- Review Furniture's pricing/cost structure — it sells well but loses money across every sub-category.
- Cap discounts around 15–20%; margin turns negative above that threshold.
- Scale inventory and staffing ahead of the Nov–Dec demand peak.
- Prioritize retention/upsell efforts on the Home Office segment, the most profitable per dollar of sales.

## Charts
All charts are in `/charts`:
- `sales_profit_by_category.png` — revenue vs. profit by category
- `sales_by_region.png` — revenue by region
- `monthly_sales_trend.png` — sales trend over time
- `seasonality.png` — sales by calendar month
- `margin_by_segment.png` — profit margin by customer segment
- `profit_by_subcategory.png` — profit by sub-category, loss-makers highlighted
- `margin_by_discount.png` — margin erosion by discount level

## How to Run
```bash
pip install pandas numpy matplotlib seaborn jupyter
jupyter notebook analysis.ipynb
```

## Project Structure
```
retail_sales_project/
├── data/
│   └── retail_sales_raw.csv
├── charts/
│   └── *.png
├── analysis.ipynb
├── generate_data.py      # script used to generate the synthetic dataset
└── README.md
```
