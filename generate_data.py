"""
Generates a synthetic retail sales dataset (Superstore-style) for the
Retail Sales Performance Analysis project.

The data includes realistic patterns (seasonality, category profit
differences, regional trends) AND intentional messiness (missing values,
duplicate rows, inconsistent text casing) so the cleaning step in the
analysis notebook has real work to do.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N = 9800  # number of orders

# ---- Reference lists ----
regions = ["East", "West", "Central", "South"]
region_weights = [0.32, 0.30, 0.22, 0.16]

segments = ["Consumer", "Corporate", "Home Office"]
segment_weights = [0.52, 0.30, 0.18]

categories = {
    "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
    "Office Supplies": ["Binders", "Paper", "Storage", "Art", "Labels", "Envelopes"],
    "Technology": ["Phones", "Machines", "Accessories", "Copiers"],
}

# base price ranges and profit margin tendencies per category
category_price_range = {
    "Furniture": (50, 1200),
    "Office Supplies": (5, 250),
    "Technology": (30, 2500),
}
# Furniture tends to run thinner (sometimes negative) margins, Technology highest
category_margin_mean = {
    "Furniture": 0.03,
    "Office Supplies": 0.22,
    "Technology": 0.18,
}
category_margin_std = {
    "Furniture": 0.18,
    "Office Supplies": 0.10,
    "Technology": 0.15,
}

customer_first = ["James", "Maria", "Wei", "Priya", "John", "Fatima", "Carlos", "Anna",
                   "David", "Sara", "Mohammed", "Linda", "Kevin", "Grace", "Tom", "Nina"]
customer_last = ["Smith", "Johnson", "Chen", "Patel", "Garcia", "Khan", "Brown", "Davis",
                  "Martinez", "Lee", "Wilson", "Clark", "Rodriguez", "Lewis", "Walker", "Young"]

start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(N):
    order_id = f"ORD-{10000 + i}"

    # seasonality: bias order dates toward Nov/Dec (holiday bump) and back-to-school (Aug/Sep)
    month_weights = np.array([0.06, 0.06, 0.07, 0.07, 0.07, 0.08,
                               0.07, 0.09, 0.09, 0.08, 0.13, 0.13])
    month_weights = month_weights / month_weights.sum()
    year = np.random.choice([2022, 2023, 2024])
    month = np.random.choice(range(1, 13), p=month_weights)
    day = np.random.randint(1, 28)
    order_date = datetime(year, month, day)
    ship_date = order_date + timedelta(days=int(np.random.choice([1, 2, 3, 4, 5, 7], p=[0.25,0.25,0.2,0.15,0.1,0.05])))

    region = np.random.choice(regions, p=region_weights)
    segment = np.random.choice(segments, p=segment_weights)
    category = np.random.choice(list(categories.keys()), p=[0.22, 0.5, 0.28])
    sub_category = np.random.choice(categories[category])

    lo, hi = category_price_range[category]
    unit_price = np.round(np.random.uniform(lo, hi), 2)
    quantity = np.random.choice([1, 2, 3, 4, 5, 6], p=[0.35, 0.25, 0.17, 0.12, 0.07, 0.04])
    discount = np.random.choice([0, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5],
                                 p=[0.35, 0.2, 0.15, 0.13, 0.09, 0.05, 0.03])

    sales = np.round(unit_price * quantity * (1 - discount), 2)

    margin = np.random.normal(category_margin_mean[category], category_margin_std[category])
    # higher discounts erode margin further
    margin -= discount * 0.6
    profit = np.round(sales * margin, 2)

    customer_name = f"{np.random.choice(customer_first)} {np.random.choice(customer_last)}"

    rows.append({
        "Order ID": order_id,
        "Order Date": order_date,
        "Ship Date": ship_date,
        "Customer Name": customer_name,
        "Segment": segment,
        "Region": region,
        "Category": category,
        "Sub-Category": sub_category,
        "Sales": sales,
        "Quantity": quantity,
        "Discount": discount,
        "Profit": profit,
    })

df = pd.DataFrame(rows)

# ---- Inject realistic messiness ----

# 1. Missing values in a few columns
missing_idx = np.random.choice(df.index, size=150, replace=False)
df.loc[missing_idx, "Customer Name"] = np.nan

missing_idx2 = np.random.choice(df.index, size=80, replace=False)
df.loc[missing_idx2, "Discount"] = np.nan

missing_idx3 = np.random.choice(df.index, size=60, replace=False)
df.loc[missing_idx3, "Ship Date"] = np.nan

# 2. Inconsistent text casing / whitespace in categorical columns
inconsistent_idx = np.random.choice(df.index, size=400, replace=False)
def mess_up_text(val):
    choice = np.random.choice(["lower", "upper", "space"])
    if choice == "lower":
        return val.lower()
    elif choice == "upper":
        return val.upper()
    else:
        return f" {val} "
df.loc[inconsistent_idx, "Region"] = df.loc[inconsistent_idx, "Region"].apply(mess_up_text)

# 3. Duplicate rows
dupes = df.sample(70, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# 4. Shuffle
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv("C:/Users/DELL/Documents/Project/retail_sales_project/data/retail_sales_raw.csv", index=False)
print("Generated:", df.shape)
print(df.head())
