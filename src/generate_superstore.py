"""
Data Generation Script for Superstore E-Commerce Dataset
Generates authentic transactional records matching the standard Kaggle/Global Superstore schema.
Contains realistic discount, profit margin, and regional dynamics.
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# Categories and Subcategories with baseline margin benchmarks
TAXONOMY = {
    "Technology": {
        "Phones": {"base_margin": 0.28, "price_range": (120, 1100), "discount_penalty": 1.4},
        "Accessories": {"base_margin": 0.38, "price_range": (20, 180), "discount_penalty": 1.2},
        "Copiers": {"base_margin": 0.42, "price_range": (450, 2400), "discount_penalty": 1.1},
        "Machines": {"base_margin": 0.22, "price_range": (250, 1900), "discount_penalty": 1.6},
    },
    "Furniture": {
        "Chairs": {"base_margin": 0.18, "price_range": (80, 600), "discount_penalty": 1.8},
        "Tables": {"base_margin": 0.08, "price_range": (150, 950), "discount_penalty": 2.6}, # Notorious loss-maker at >15% discount
        "Bookcases": {"base_margin": 0.12, "price_range": (90, 700), "discount_penalty": 2.2}, # Margin leakage
        "Furnishings": {"base_margin": 0.25, "price_range": (15, 120), "discount_penalty": 1.5},
    },
    "Office Supplies": {
        "Storage": {"base_margin": 0.26, "price_range": (30, 320), "discount_penalty": 1.3},
        "Binders": {"base_margin": 0.35, "price_range": (5, 90), "discount_penalty": 2.4}, # Huge discounts cause losses
        "Paper": {"base_margin": 0.44, "price_range": (10, 80), "discount_penalty": 1.1},
        "Art": {"base_margin": 0.32, "price_range": (8, 65), "discount_penalty": 1.2},
        "Appliances": {"base_margin": 0.24, "price_range": (60, 480), "discount_penalty": 1.7},
        "Envelopes": {"base_margin": 0.39, "price_range": (12, 75), "discount_penalty": 1.1},
        "Labels": {"base_margin": 0.46, "price_range": (6, 45), "discount_penalty": 1.0},
        "Supplies": {"base_margin": 0.16, "price_range": (15, 140), "discount_penalty": 1.9},
        "Fasteners": {"base_margin": 0.40, "price_range": (4, 35), "discount_penalty": 1.1},
    }
}

REGIONS = {
    "West": [
        ("California", "Los Angeles", 90036),
        ("California", "San Francisco", 94102),
        ("California", "San Diego", 92101),
        ("Washington", "Seattle", 98101),
        ("Oregon", "Portland", 97201),
        ("Arizona", "Phoenix", 85001),
        ("Nevada", "Las Vegas", 89101),
        ("Colorado", "Denver", 80201),
    ],
    "East": [
        ("New York", "New York City", "10024"),
        ("Pennsylvania", "Philadelphia", "19104"),
        ("Massachusetts", "Boston", "02108"),
        ("Ohio", "Columbus", "43215"),
        ("New Jersey", "Newark", "07102"),
        ("Maryland", "Baltimore", "21201"),
        ("Delaware", "Wilmington", "19801"),
    ],
    "Central": [
        ("Texas", "Houston", 77001),
        ("Texas", "Dallas", 75201),
        ("Illinois", "Chicago", 60601),
        ("Michigan", "Detroit", 48201),
        ("Indiana", "Indianapolis", 46201),
        ("Wisconsin", "Milwaukee", 53201),
        ("Minnesota", "Minneapolis", 55401),
    ],
    "South": [
        ("Florida", "Miami", 33101),
        ("Florida", "Orlando", 32801),
        ("Georgia", "Atlanta", 30301),
        ("North Carolina", "Charlotte", 28202),
        ("Virginia", "Richmond", 23219),
        ("Tennessee", "Nashville", 37201),
        ("Kentucky", "Louisville", 40202),
    ]
}

# High discount propensity states (mimicking real Superstore phenomenon)
HIGH_DISCOUNT_STATES = {"Texas", "Illinois", "Ohio", "Pennsylvania", "North Carolina"}

SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SEGMENT_WEIGHTS = [0.52, 0.30, 0.18]

SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]
SHIP_WEIGHTS = [0.60, 0.20, 0.15, 0.05]

FIRST_NAMES = [
    "Aarav", "Claire", "Darrin", "Emma", "Liam", "Sophia", "Noah", "Olivia",
    "Prathamesh", "Rohan", "Ananya", "Marcus", "Jessica", "David", "Elena",
    "Michael", "Sarah", "Emily", "James", "Kavita", "Aditya", "Chloe", "Daniel"
]
LAST_NAMES = [
    "Gute", "Van Huff", "Smith", "Johnson", "Brown", "Taylor", "Miller", "Davis",
    "Mistari", "Sharma", "Patel", "Wilson", "Anderson", "Thomas", "Jackson",
    "White", "Harris", "Martin", "Thompson", "Verma", "Gupta", "Clark", "Lewis"
]

CUSTOMERS = []
for i in range(1, 350):
    c_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    c_id = f"CG-{10000 + i}"
    c_segment = random.choices(SEGMENTS, weights=SEGMENT_WEIGHTS)[0]
    CUSTOMERS.append((c_id, c_name, c_segment))

def generate_dataset(num_records=5000, output_path="data/raw/superstore_raw.csv"):
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range_days = (end_date - start_date).days

    rows = []
    headers = [
        "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "Customer ID", "Customer Name", "Segment", "Country", "City",
        "State", "Postal Code", "Region", "Product ID", "Category",
        "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Profit"
    ]

    for row_id in range(1, num_records + 1):
        # Order Date & Shipping
        order_days = random.randint(0, date_range_days)
        order_date = start_date + timedelta(days=order_days)
        ship_lag = random.choice([2, 3, 4, 5, 6])
        ship_date = order_date + timedelta(days=ship_lag)
        ship_mode = random.choices(SHIP_MODES, weights=SHIP_WEIGHTS)[0]

        # Customer
        c_id, c_name, c_segment = random.choice(CUSTOMERS)

        # Region & Geography
        region = random.choice(list(REGIONS.keys()))
        state, city, postal_code = random.choice(REGIONS[region])

        # Category & Subcategory
        category = random.choice(list(TAXONOMY.keys()))
        sub_cat = random.choice(list(TAXONOMY[category].keys()))
        cat_meta = TAXONOMY[category][sub_cat]

        product_id = f"{category[:3].upper()}-{sub_cat[:2].upper()}-{random.randint(1000, 9999)}"
        product_name = f"{sub_cat} Model-{random.choice(['Pro', 'Standard', 'Plus', 'Eco', 'Elite'])} Series {random.randint(100, 900)}"

        # Pricing & Economics
        base_unit_price = random.uniform(cat_meta["price_range"][0], cat_meta["price_range"][1])
        quantity = random.randint(1, 9)
        gross_sales = base_unit_price * quantity

        # Discount generation
        if state in HIGH_DISCOUNT_STATES:
            # Often high discount 20% to 70%
            discount = random.choice([0.0, 0.1, 0.2, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
        else:
            # Controlled discount 0% to 20%
            discount = random.choice([0.0, 0.0, 0.0, 0.05, 0.1, 0.15, 0.2, 0.25])

        actual_sales = round(gross_sales * (1.0 - discount), 2)

        # Cost calculation based on base margin
        cost = gross_sales * (1.0 - cat_meta["base_margin"])

        # Discount eroding profit with non-linear penalty for high discounts
        # When discount is high, profit drops negative
        net_profit = actual_sales - cost - (gross_sales * discount * (cat_meta["discount_penalty"] - 1.0) * 0.4)
        net_profit = round(net_profit, 2)

        order_id = f"CA-{order_date.year}-{random.randint(100000, 999999)}"

        rows.append([
            row_id,
            order_id,
            order_date.strftime("%Y-%m-%d"),
            ship_date.strftime("%Y-%m-%d"),
            ship_mode,
            c_id,
            c_name,
            c_segment,
            "United States",
            city,
            state,
            postal_code,
            region,
            product_id,
            category,
            sub_cat,
            product_name,
            actual_sales,
            quantity,
            round(discount, 2),
            net_profit
        ])

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Successfully generated {num_records} realistic Superstore records to {output_path}")

if __name__ == "__main__":
    generate_dataset()
