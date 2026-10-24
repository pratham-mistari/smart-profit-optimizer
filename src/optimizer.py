"""
Dynamic Profit Simulator & Discount Sensitivity Engine
Simulates profit recovery, volume elasticity, and margin changes under discounting constraints.
"""

import pandas as pd
import numpy as np

def simulate_discount_policy(df: pd.DataFrame, max_discount_pct: float, elasticity: float = 0.8):
    """
    Simulates the financial impact of enforcing a maximum discount ceiling.

    Parameters:
    - df: Preprocessed Superstore DataFrame.
    - max_discount_pct: Maximum allowed discount percentage (e.g. 15 for 15%).
    - elasticity: Price sensitivity coefficient (default 0.8 represents moderate volume drop on discount cuts).

    Returns:
    - dict with summary KPIs, subcategory analysis, and simulated DataFrame.
    """
    df_sim = df.copy()
    cap = max_discount_pct / 100.0

    # Baseline metrics
    base_revenue = df["Sales"].sum()
    base_profit = df["Profit"].sum()
    base_margin = (base_profit / base_revenue * 100) if base_revenue > 0 else 0
    base_loss_count = (df["Profit"] < 0).sum()
    base_total_loss = df.loc[df["Profit"] < 0, "Profit"].sum()

    # Identify orders exceeding the cap
    excess_mask = df_sim["Discount"] > cap

    # Reconstruct original gross price (before discount)
    original_gross = df_sim["Sales"] / (1.0 - df_sim["Discount"] + 1e-6)
    cogs = df_sim["COGS"]

    # Simulated discount: capped if above threshold, else unchanged
    df_sim["Sim_Discount"] = np.where(excess_mask, cap, df_sim["Discount"])

    # Price increase factor for capped orders
    # Price ratio = (1 - cap) / (1 - original_discount)
    price_ratio = np.where(
        excess_mask,
        (1.0 - cap) / np.maximum(1.0 - df_sim["Discount"], 0.05),
        1.0
    )

    # Volume elasticity: if price increased by X%, quantity drops by elasticity * (price_ratio - 1)
    # Capped at a realistic 25% max volume drop so business retains customer base
    volume_factor = np.where(
        excess_mask,
        np.clip(1.0 - (elasticity * (price_ratio - 1.0)), 0.75, 1.0),
        1.0
    )

    # Simulated Sales = original gross * (1 - new_discount) * volume_factor
    df_sim["Sim_Sales"] = np.where(
        excess_mask,
        original_gross * (1.0 - cap) * volume_factor,
        df_sim["Sales"]
    )

    # Simulated Cost = original COGS * volume_factor
    df_sim["Sim_COGS"] = cogs * volume_factor

    # Simulated Profit = Sim_Sales - Sim_COGS
    df_sim["Sim_Profit"] = df_sim["Sim_Sales"] - df_sim["Sim_COGS"]
    df_sim["Sim_Margin %"] = np.where(df_sim["Sim_Sales"] > 0, (df_sim["Sim_Profit"] / df_sim["Sim_Sales"]) * 100, 0)
    df_sim["Profit_Delta"] = df_sim["Sim_Profit"] - df_sim["Profit"]

    # Simulated KPI summaries
    sim_revenue = df_sim["Sim_Sales"].sum()
    sim_profit = df_sim["Sim_Profit"].sum()
    sim_margin = (sim_profit / sim_revenue * 100) if sim_revenue > 0 else 0
    sim_loss_count = (df_sim["Sim_Profit"] < 0).sum()
    sim_total_loss = df_sim.loc[df_sim["Sim_Profit"] < 0, "Sim_Profit"].sum()

    rescued_orders = base_loss_count - sim_loss_count
    profit_gained = sim_profit - base_profit

    # Subcategory breakdown of profit recovery
    subcat_summary = df_sim.groupby("Sub-Category").agg(
        Base_Profit=("Profit", "sum"),
        Sim_Profit=("Sim_Profit", "sum"),
        Base_Sales=("Sales", "sum"),
        Sim_Sales=("Sim_Sales", "sum"),
        Orders_Impacted=("Sim_Discount", lambda s: (df_sim.loc[s.index, "Discount"] > cap).sum())
    ).reset_index()

    subcat_summary["Profit_Recovered"] = subcat_summary["Sim_Profit"] - subcat_summary["Base_Profit"]
    subcat_summary["Base_Margin_%"] = (subcat_summary["Base_Profit"] / subcat_summary["Base_Sales"] * 100).round(1)
    subcat_summary["Sim_Margin_%"] = (subcat_summary["Sim_Profit"] / subcat_summary["Sim_Sales"] * 100).round(1)
    subcat_summary = subcat_summary.sort_values(by="Profit_Recovered", ascending=False)

    return {
        "base_revenue": base_revenue,
        "base_profit": base_profit,
        "base_margin": base_margin,
        "base_loss_count": base_loss_count,
        "base_total_loss": base_total_loss,
        "sim_revenue": sim_revenue,
        "sim_profit": sim_profit,
        "sim_margin": sim_margin,
        "sim_loss_count": sim_loss_count,
        "sim_total_loss": sim_total_loss,
        "profit_gained": profit_gained,
        "rescued_orders": rescued_orders,
        "subcat_summary": subcat_summary,
        "sim_df": df_sim
    }

def get_discount_sensitivity_curve(df: pd.DataFrame):
    """
    Computes profit recovery curve across discount caps from 0% to 50% in 5% increments.
    """
    thresholds = list(range(0, 55, 5))
    records = []
    for t in thresholds:
        res = simulate_discount_policy(df, max_discount_pct=t)
        records.append({
            "Discount Cap (%)": t,
            "Simulated Profit ($)": res["sim_profit"],
            "Profit Margin (%)": res["sim_margin"],
            "Rescued Orders": res["rescued_orders"],
            "Net Profit Gained ($)": res["profit_gained"]
        })
    return pd.DataFrame(records)
