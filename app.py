"""
Smart E-Commerce Profit Optimizer & Dynamic Pricing Simulator
Author: Prathamesh Mistari (BCA Sem 7 - SPU Guidelines)
Tech Stack: Pure Python (Streamlit + Plotly + Pandas + NumPy)
Repository: https://github.com/pratham-mistari/smart-profit-optimizer
"""

import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Smart Profit Optimizer | E-Commerce Pricing Simulator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #E2E8F0;
    }
    .highlight-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #BFDBFE;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Import local project modules
from src.data_loader import load_superstore_data
from src.optimizer import simulate_discount_policy, get_discount_sensitivity_curve
from src.visualizations import (
    plot_sensitivity_curve,
    plot_subcat_comparison,
    plot_discount_vs_margin,
    plot_state_profitability
)

# ----------------- DATA INGESTION & CACHING -----------------
@st.cache_data
def get_cached_data():
    return load_superstore_data()

try:
    df_raw = get_cached_data()
except Exception as e:
    st.error(f"Error loading transaction dataset: {e}")
    st.stop()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.image("https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Python-Dark.svg", width=50)
st.sidebar.title("🎛️ Simulation Controls")
st.sidebar.markdown("Test dynamic sensitivity parameters to eliminate margin leakage.")

# Dynamic Discount Slider (The Star Feature)
discount_slider = st.sidebar.slider(
    "🛡️ Maximum Allowed Discount (%)",
    min_value=0,
    max_value=50,
    value=15,
    step=1,
    help="Transactions with discounts exceeding this threshold will be capped at this value."
)

elasticity_choice = st.sidebar.radio(
    "Price Sensitivity (Elasticity)",
    options=["Moderate (0.8x volume drop)", "Conservative (0.5x volume drop)", "Aggressive (1.2x volume drop)"],
    index=0
)
elasticity_val = 0.8 if "Moderate" in elasticity_choice else (0.5 if "Conservative" in elasticity_choice else 1.2)

st.sidebar.divider()
st.sidebar.subheader("🔍 Demographic Filters")

all_regions = ["All"] + sorted(list(df_raw["Region"].unique()))
selected_region = st.sidebar.selectbox("Geographic Region", all_regions, index=0)

all_categories = ["All"] + sorted(list(df_raw["Category"].unique()))
selected_category = st.sidebar.selectbox("Product Category", all_categories, index=0)

# Apply demographic filters
df_filtered = df_raw.copy()
if selected_region != "All":
    df_filtered = df_filtered[df_filtered["Region"] == selected_region]
if selected_category != "All":
    df_filtered = df_filtered[df_filtered["Category"] == selected_category]

# ----------------- SIMULATION EXECUTION -----------------
sim_results = simulate_discount_policy(
    df=df_filtered,
    max_discount_pct=discount_slider,
    elasticity=elasticity_val
)
df_curve = get_discount_sensitivity_curve(df_filtered)

# ----------------- HEADER & EXECUTIVE CALLOUT -----------------
st.markdown('<div class="main-title">📈 Smart E-Commerce Profit Optimizer & Pricing Simulator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">A real-time analytics framework diagnosing profit margin leakage and simulating dynamic discount caps.</div>', unsafe_allow_html=True)

# Executive Callout Card
profit_recovered = sim_results["profit_gained"]
rescued = sim_results["rescued_orders"]
new_margin = sim_results["sim_margin"]
old_margin = sim_results["base_margin"]
margin_delta = new_margin - old_margin

st.markdown(f"""
<div class="highlight-card">
    <h4 style="margin-top:0; color:#1E40AF;">💡 Real-Time Scenario Insight</h4>
    By capping discounts at <b>{discount_slider}%</b> with <b>{elasticity_choice.split()[0]}</b> elasticity, 
    the enterprise recovers <b>${profit_recovered:,.2f}</b> in net profit! 
    <b>{rescued:,}</b> formerly loss-making orders turn profitable, lifting total profit margin from <b>{old_margin:.1f}%</b> to <b>{new_margin:.1f}%</b> (<b>+{margin_delta:.1f}%</b>).
</div>
""", unsafe_allow_html=True)

# ----------------- TOP-LEVEL METRICS -----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Simulated Net Revenue",
        value=f"${sim_results['sim_revenue']:,.0f}",
        delta=f"${sim_results['sim_revenue'] - sim_results['base_revenue']:,.0f} (Vol Adj)"
    )

with col2:
    st.metric(
        label="Simulated Net Profit",
        value=f"${sim_results['sim_profit']:,.0f}",
        delta=f"+${profit_recovered:,.0f} Recovered",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="Operating Profit Margin",
        value=f"{new_margin:.2f}%",
        delta=f"+{margin_delta:.2f}% Margin Gain"
    )

with col4:
    st.metric(
        label="Loss Orders Rescued",
        value=f"{rescued:,} Orders",
        delta=f"Active Cap: {discount_slider}%"
    )

st.write("")

# ----------------- TABBED ANALYTICS -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🎚️ Sensitivity Curve & Simulator",
    "📦 Category & Sub-Category Leakage",
    "🗺️ Geographic & State Performance",
    "🔍 Transaction Explorer & Data Export"
])

with tab1:
    st.subheader("Dynamic Profit Sensitivity Curve")
    st.caption("Visualizes projected net operating profit across discount caps from 0% to 50%. The diamond marks your active slider setting.")
    
    fig_curve = plot_sensitivity_curve(df_curve, current_cap=discount_slider)
    st.plotly_chart(fig_curve, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 📉 Baseline State (No Policy)")
        st.write(f"- **Gross Revenue:** `${sim_results['base_revenue']:,.2f}`")
        st.write(f"- **Operating Profit:** `${sim_results['base_profit']:,.2f}`")
        st.write(f"- **Profit Margin:** `{sim_results['base_margin']:.2f}%`")
        st.write(f"- **Loss-Making Transactions:** `{sim_results['base_loss_count']:,}` orders")
        st.write(f"- **Total Cumulative Loss Leaked:** `-${abs(sim_results['base_total_loss']):,.2f}`")
    with col_b:
        st.markdown(f"#### 🚀 Optimized Scenario (Cap = {discount_slider}%)")
        st.write(f"- **Optimized Revenue:** `${sim_results['sim_revenue']:,.2f}`")
        st.write(f"- **Optimized Profit:** `${sim_results['sim_profit']:,.2f}`")
        st.write(f"- **Optimized Profit Margin:** `{sim_results['sim_margin']:.2f}%`")
        st.write(f"- **Remaining Loss Orders:** `{sim_results['sim_loss_count']:,}` orders")
        st.write(f"- **Net Profit Improvement:** `+${profit_recovered:,.2f}`")

with tab2:
    st.subheader("Sub-Category Profitability Comparison")
    st.caption("Diagnose severe profit leak culprits (e.g. Tables, Bookcases) vs high-margin engines (Copiers, Phones).")

    fig_subcat = plot_subcat_comparison(sim_results["subcat_summary"])
    st.plotly_chart(fig_subcat, use_container_width=True)

    st.markdown("#### 📋 Detailed Sub-Category Impact Table")
    display_subcat = sim_results["subcat_summary"].copy()
    display_subcat["Base_Profit"] = display_subcat["Base_Profit"].apply(lambda x: f"${x:,.2f}")
    display_subcat["Sim_Profit"] = display_subcat["Sim_Profit"].apply(lambda x: f"${x:,.2f}")
    display_subcat["Profit_Recovered"] = display_subcat["Profit_Recovered"].apply(lambda x: f"${x:,.2f}")
    display_subcat["Base_Sales"] = display_subcat["Base_Sales"].apply(lambda x: f"${x:,.2f}")
    display_subcat["Sim_Sales"] = display_subcat["Sim_Sales"].apply(lambda x: f"${x:,.2f}")
    st.dataframe(display_subcat, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("The 'Discount Leakage Cliff'")
    st.caption("Visual proof showing how discounts above 20% drag profit margin below the zero break-even line.")
    fig_scatter = plot_discount_vs_margin(df_filtered)
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.subheader("Geographic Profit Distribution by State")
    st.caption("Identifies regional vulnerabilities where uncontrolled discounts in Texas, Ohio, and Illinois cause heavy cumulative losses.")
    fig_state = plot_state_profitability(df_filtered)
    st.plotly_chart(fig_state, use_container_width=True)

with tab4:
    st.subheader("Simulated Transaction Ledger")
    st.caption("Review individual simulated order rows with recalculated margins and discount caps.")
    
    sim_df_display = sim_results["sim_df"][[
        "Order ID", "Order Date", "Category", "Sub-Category", "State",
        "Sales", "Discount", "Profit", "Sim_Discount", "Sim_Sales", "Sim_Profit", "Profit_Delta"
    ]].head(500)
    
    st.dataframe(sim_df_display, use_container_width=True, hide_index=True)

    csv_data = sim_results["sim_df"].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Simulated Scenario (CSV)",
        data=csv_data,
        file_name=f"simulated_scenario_cap_{discount_slider}pct.csv",
        mime="text/csv"
    )

# ----------------- FOOTER -----------------
st.divider()
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 0.88rem; padding: 12px 0;">
    <b>Smart E-Commerce Profit Optimizer & Dynamic Pricing Simulator</b> | BCA 4-Year (Sem 7) Capstone Project<br>
    Developed under Sardar Patel University (SPU) OJT Guidelines | Author: <b>Prathamesh Mistari</b><br>
    Built with 100% Pure Python (Streamlit + Plotly + Pandas + NumPy) | GitHub: <a href="https://github.com/pratham-mistari/smart-profit-optimizer" target="_blank">pratham-mistari/smart-profit-optimizer</a>
</div>
""", unsafe_allow_html=True)
