"""
Visualizations Module for Smart E-Commerce Profit Optimizer
High-impact, interactive Plotly visualizations for Streamlit dashboard.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLOR_PRIMARY = "#2563EB"   # Royal Blue
COLOR_ACCENT = "#10B981"    # Emerald Green
COLOR_DANGER = "#EF4444"    # Crimson Red
COLOR_WARNING = "#F59E0B"   # Amber
COLOR_MUTED = "#64748B"     # Slate Gray

def plot_sensitivity_curve(df_curve: pd.DataFrame, current_cap: int):
    """
    Plots the Dynamic Profit Sensitivity Curve showing profit recovery across discount caps.
    """
    fig = go.Figure()

    # Net Profit curve
    fig.add_trace(go.Scatter(
        x=df_curve["Discount Cap (%)"],
        y=df_curve["Simulated Profit ($)"],
        mode="lines+markers",
        name="Simulated Profit ($)",
        line=dict(color=COLOR_PRIMARY, width=3),
        marker=dict(size=7, color=COLOR_PRIMARY),
        hovertemplate="<b>Discount Cap: %{x}%</b><br>Profit: $%{y:,.0f}<extra></extra>"
    ))

    # Add vertical reference line for current slider value
    current_profit_row = df_curve[df_curve["Discount Cap (%)"] == current_cap]
    if not current_profit_row.empty:
        curr_profit = current_profit_row["Simulated Profit ($)"].values[0]
        fig.add_trace(go.Scatter(
            x=[current_cap],
            y=[curr_profit],
            mode="markers",
            name="Current Setting",
            marker=dict(size=14, color=COLOR_ACCENT, symbol="diamond"),
            hovertemplate="<b>Active Cap: %{x}%</b><br>Profit: $%{y:,.0f}<extra></extra>"
        ))

    fig.add_vline(x=current_cap, line_width=2, line_dash="dash", line_color=COLOR_ACCENT)

    fig.update_layout(
        title="<b>Dynamic Profit Recovery Curve vs. Discount Threshold</b>",
        xaxis_title="Maximum Allowed Discount (%)",
        yaxis_title="Total Projected Operating Profit ($)",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_subcat_comparison(subcat_summary: pd.DataFrame):
    """
    Compares Baseline Profit vs. Simulated Profit per Sub-Category.
    """
    df_sorted = subcat_summary.sort_values(by="Profit_Recovered", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_sorted["Sub-Category"],
        x=df_sorted["Base_Profit"],
        name="Baseline Profit ($)",
        orientation="h",
        marker=dict(color="#94A3B8")
    ))
    fig.add_trace(go.Bar(
        y=df_sorted["Sub-Category"],
        x=df_sorted["Sim_Profit"],
        name="Optimized Profit ($)",
        orientation="h",
        marker=dict(color=COLOR_ACCENT)
    ))

    fig.update_layout(
        title="<b>Sub-Category Profit Impact (Baseline vs. Simulated)</b>",
        xaxis_title="Operating Profit ($)",
        yaxis_title="Sub-Category",
        barmode="group",
        template="plotly_white",
        height=520,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_discount_vs_margin(df: pd.DataFrame):
    """
    Scatter plot revealing the 'Discount Leakage Cliff' where margins crash below 0.
    """
    # Sample 1000 points if large for performance
    df_sample = df.sample(min(1200, len(df)), random_state=42)

    fig = px.scatter(
        df_sample,
        x="Discount",
        y="Profit Margin %",
        color="Category",
        color_discrete_map={
            "Furniture": "#F97316",
            "Technology": "#2563EB",
            "Office Supplies": "#10B981"
        },
        hover_data=["Sub-Category", "Sales", "Profit", "State"],
        title="<b>Discount Leakage Cliff: Margin Degradation vs Discount %</b>"
    )

    # Reference zero margin line
    fig.add_hline(y=0, line_width=2, line_dash="solid", line_color=COLOR_DANGER)
    fig.add_annotation(
        x=0.45, y=-15,
        text="⚠️ Negative Profit Margin Zone",
        showarrow=False,
        font=dict(color=COLOR_DANGER, size=12, family="sans-serif")
    )

    fig.update_layout(
        xaxis_title="Discount Applied (Ratio: 0.0 - 0.7)",
        yaxis_title="Profit Margin (%)",
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig

def plot_state_profitability(df: pd.DataFrame):
    """
    State-level aggregation showing top profit drivers and top loss-making states.
    """
    state_agg = df.groupby("State").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Avg_Discount=("Discount", "mean"),
        Loss_Orders=("Is Loss Maker", "sum")
    ).reset_index()

    state_agg = state_agg.sort_values(by="Total_Profit", ascending=False)
    
    # Color states: positive green/blue, negative red
    state_agg["Color"] = state_agg["Total_Profit"].apply(lambda x: COLOR_ACCENT if x >= 0 else COLOR_DANGER)

    fig = go.Figure(go.Bar(
        x=state_agg["State"],
        y=state_agg["Total_Profit"],
        marker_color=state_agg["Color"],
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>"
    ))

    fig.update_layout(
        title="<b>Geographic Profitability by State (Green = Profitable, Red = Net Loss)</b>",
        xaxis_title="State",
        yaxis_title="Net Cumulative Profit ($)",
        xaxis_tickangle=-45,
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig
