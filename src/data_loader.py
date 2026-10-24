"""
Data Loader & Preprocessing Module
Handles data ingestion, feature engineering, and caching.
"""

import os
import pandas as pd
import numpy as np

RAW_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "superstore_raw.csv")
PROCESSED_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed", "superstore_clean.csv")

def clean_and_process_data(input_path=RAW_DATA_PATH, output_path=PROCESSED_DATA_PATH):
    """
    Cleans raw Superstore transactions, engineers financial KPIs,
    and saves processed dataset.
    """
    df = pd.read_csv(input_path)

    # Convert dates
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # Financial KPIs
    df["Profit Margin %"] = np.where(df["Sales"] > 0, (df["Profit"] / df["Sales"]) * 100, 0)
    df["Profit Margin %"] = df["Profit Margin %"].round(2)
    df["Is Loss Maker"] = df["Profit"] < 0
    df["Loss Amount"] = np.where(df["Profit"] < 0, df["Profit"].abs(), 0.0)

    # Discount Bins
    bins = [-0.01, 0.0, 0.10, 0.20, 0.40, 1.0]
    labels = ["0% (No Discount)", "1% - 10%", "11% - 20%", "21% - 40%", "> 40% (Aggressive)"]
    df["Discount Tier"] = pd.cut(df["Discount"], bins=bins, labels=labels)

    # Cost of Goods Sold (estimated)
    df["COGS"] = df["Sales"] - df["Profit"]

    # Save processed copy
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved: {df.shape[0]} rows, {df.shape[1]} columns -> {output_path}")
    return df

def load_superstore_data():
    """
    Loads processed data if available, otherwise runs preprocessing pipeline.
    """
    if os.path.exists(PROCESSED_DATA_PATH):
        df = pd.read_csv(PROCESSED_DATA_PATH)
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["Ship Date"] = pd.to_datetime(df["Ship Date"])
        return df
    else:
        return clean_and_process_data()

if __name__ == "__main__":
    clean_and_process_data()
