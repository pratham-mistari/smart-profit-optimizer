import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib


# ==============================================================================
# 1. PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="BharatCart | Profit Optimizer & Operations Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. ULTRA-PREMIUM MODERN DESIGN SYSTEM (CUSTOM CSS)
# ==============================================================================
custom_css = """
<style>
    /* Import Modern Typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Typography & Backgrounds */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }

    /* Hero Header Banner */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #1E40AF 100%);
        border-radius: 18px;
        padding: 32px 36px;
        color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25), 0 8px 10px -6px rgba(15, 23, 42, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    .hero-container::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, rgba(59, 130, 246, 0) 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(8px);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.75px;
        color: #93C5FD;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 14px;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
        animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
        0% { transform: scale(0.95); opacity: 0.8; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.8; }
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.2;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    .hero-title .gradient-text {
        background: linear-gradient(90deg, #60A5FA, #93C5FD, #34D399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 0.98rem;
        color: #CBD5E1;
        max-width: 800px;
        line-height: 1.5;
        margin-bottom: 14px;
    }
    .hero-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 10px;
    }
    .tech-pill {
        background: rgba(15, 23, 42, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #E2E8F0;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Executive KPI Metric Cards */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.04);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px -4px rgba(37, 99, 235, 0.12);
        border-color: #93C5FD;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: #64748B !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        letter-spacing: -0.5px !important;
    }

    /* Profit Simulator Card Container */
    .simulator-card {
        background: #FFFFFF;
        border: 1.5px solid #DBEAFE;
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 8px 20px -4px rgba(30, 64, 175, 0.06);
        margin-bottom: 24px;
    }
    .simulator-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 12px;
    }
    .sim-badge {
        background: #EFF6FF;
        color: #1E40AF;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: 1px solid #BFDBFE;
    }
    .sim-result-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 1px solid #86EFAC;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }

    /* Modern Styled Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        padding: 0 16px;
        font-weight: 600;
        font-size: 0.88rem;
        color: #64748B;
        border: none;
        background-color: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #1E40AF !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
    }

    /* Playbook Containers in Tab 5 */
    .playbook-high-risk {
        background: #FEF2F2;
        border: 1.5px solid #FCA5A5;
        border-radius: 14px;
        padding: 20px 24px;
        margin-top: 14px;
    }
    .playbook-low-risk {
        background: #F0FDF4;
        border: 1.5px solid #86EFAC;
        border-radius: 14px;
        padding: 20px 24px;
        margin-top: 14px;
    }
    .playbook-title {
        font-size: 1.05rem;
        font-weight: 800;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .playbook-step {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 10px;
        font-size: 0.92rem;
        line-height: 1.45;
    }
    .step-icon {
        background: #FFFFFF;
        padding: 6px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 1.1rem;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 0 20px 0;
        border-bottom: 1px solid #F1F5F9;
        margin-bottom: 18px;
    }
    .sidebar-stats-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px;
        margin-top: 24px;
        font-size: 0.8rem;
        color: #64748B;
        line-height: 1.6;
    }

    /* Footer Styling */
    .footer-container {
        margin-top: 50px;
        padding: 24px 0;
        border-top: 1px solid #E2E8F0;
        text-align: center;
        font-size: 0.85rem;
        color: #64748B;
    }
    .footer-container strong {
        color: #0F172A;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ==============================================================================
# 3. HIGH-PERFORMANCE DATA & MODEL LOADERS
# ==============================================================================
@st.cache_data
def load_processed_data():
    """Load and cache the 100,000 pan-India e-commerce transaction dataset."""
    data_path = "data/processed/indian_ecommerce_processed.csv"
    data = pd.read_csv(data_path)
    return data

@st.cache_resource
def load_trained_ml_pipeline():
    """Load and cache the trained Random Forest classifier and feature schema."""
    model = joblib.load('models/rto_rf_model.joblib')
    features = joblib.load('models/model_features.joblib')
    return model, features

df = load_processed_data()
ml_model, ml_features = load_trained_ml_pipeline()


# ==============================================================================
# 4. SIDEBAR CONTROLS & MARKETPLACE FILTERS
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span style="font-size: 1.8rem;">📦</span>
        <div>
            <div style="font-weight: 800; font-size: 1.05rem; color: #0F172A;">BharatCart</div>
            <div style="font-size: 0.72rem; font-weight: 600; color: #2563EB; text-transform: uppercase;">Operations Intelligence v2.4</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🔍 Slicing Filters")
    selected_state = st.selectbox("Geographic State / Region:", ["All States"] + sorted(df['state'].unique().tolist()))
    selected_category = st.selectbox("Retail Product Category:", ["All Categories"] + sorted(df['category'].unique().tolist()))
    selected_payment = st.selectbox("Customer Payment Channel:", ["All Methods"] + sorted(df['payment_method'].unique().tolist()))

    st.markdown("---")
    st.markdown("#### ⚙️ Display Settings")
    show_raw_table = st.checkbox("Show Raw Transaction Inspector", value=False)

    st.markdown("""
    <div class="sidebar-stats-box">
        <strong>⚡ Pipeline Telemetry:</strong><br>
        • Total Ingested: <strong>100,000 Orders</strong><br>
        • Total GMV: <strong>₹61.96 Crores</strong><br>
        • Active Model: <strong>Random Forest (100 Trees)</strong><br>
        • Accuracy / ROC-AUC: <strong>87.28% | 0.7431</strong><br>
        • Caching: <strong>In-Memory Active</strong>
    </div>
    """, unsafe_allow_html=True)


# Apply filters to working dataset
filtered_df = df.copy()
if selected_state != "All States":
    filtered_df = filtered_df[filtered_df['state'] == selected_state]
if selected_category != "All Categories":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
if selected_payment != "All Methods":
    filtered_df = filtered_df[filtered_df['payment_method'] == selected_payment]


# ==============================================================================
# 5. HERO HEADER BANNER
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span class="status-dot"></span>
        <span>PRODUCTION PIPELINE CONNECTED • 100,000 PAN-INDIA ORDERS • AI MODEL ACTIVE</span>
    </div>
    <div class="hero-title">🇮🇳 BharatCart <span class="gradient-text">Profit Optimizer</span></div>
    <div class="hero-subtitle">
        Enterprise Operations Intelligence & Predictive Decision Support System investigating Cash on Delivery (COD) Return Traps, Delivery SLA Latency Cliffs, and Live Multi-Lever EBITDA Expansion across ₹61.96 Cr GMV.
    </div>
    <div class="hero-pills">
        <span class="tech-pill">Python 3.11</span>
        <span class="tech-pill">Streamlit 1.30+</span>
        <span class="tech-pill">Scikit-Learn Random Forest</span>
        <span class="tech-pill">Plotly Express</span>
        <span class="tech-pill">Pandas Dataframes</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 6. EXECUTIVE FINANCIAL PERFORMANCE KPI DECK
# ==============================================================================
total_gmv_cr = filtered_df['order_value_inr'].sum() / 10000000
total_orders = len(filtered_df)
total_profit_cr = filtered_df['net_profit_inr'].sum() / 10000000
margin_pct = (filtered_df['net_profit_inr'].sum() / filtered_df['order_value_inr'].sum() * 100) if filtered_df['order_value_inr'].sum() > 0 else 0
cod_subset = filtered_df[filtered_df['payment_method'] == 'Cash on Delivery (COD)']
cod_rto_pct = (cod_subset['order_status'] == 'RTO / Returned').mean() * 100 if len(cod_subset) > 0 else 0

st.markdown("### 📊 Executive Financial Performance Deck")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Marketplace GMV", f"₹{total_gmv_cr:.2f} Cr")
kpi2.metric("Audited Orders", f"{total_orders:,}")
kpi3.metric("Operating Profit", f"₹{total_profit_cr:.2f} Cr")
kpi4.metric("Net Margin %", f"{margin_pct:.2f}%")
kpi5.metric(
    "COD RTO Failure Rate",
    f"{cod_rto_pct:.2f}%",
    delta="High Risk (>15%)" if cod_rto_pct > 15 else "Normal",
    delta_color="inverse" if cod_rto_pct > 15 else "normal"
)


# Optional Raw Transaction Inspector
if show_raw_table:
    with st.expander("🔍 Filtered Transaction Inspector (First 100 Records)", expanded=True):
        st.dataframe(filtered_df.head(100), use_container_width=True)


# ==============================================================================
# 7. LIVE MULTI-LEVER PROFIT OPTIMIZATION SIMULATOR
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="simulator-card">
    <div class="simulator-header">
        <div>
            <span class="sim-badge">EXECUTIVE DECISION ENGINE</span>
            <div style="font-size: 1.25rem; font-weight: 800; color: #0F172A; margin-top: 4px;">⚡ Live Multi-Lever Profit Optimization Simulator</div>
            <div style="font-size: 0.88rem; color: #64748B;">Dynamically tune strategic policy levers to project EBITDA operating cash flow expansion across filtered orders:</div>
        </div>
    </div>
""", unsafe_allow_html=True)

col_sim1, col_sim2, col_sim3 = st.columns(3)
with col_sim1:
    cod_reduction = st.slider(
        "🛡️ Lever 1: COD OTP & Shield Adoption (%)",
        min_value=0, max_value=80, value=40, step=5,
        help="Simulated % of risky COD return orders converted to delivered prepaid sales via WhatsApp verification & instant UPI discount."
    )

with col_sim2:
    shipping_cutoff = st.select_slider(
        "🚚 Lever 2: Free Delivery Threshold (₹)",
        options=[499, 599, 699, 799, 999],
        value=799,
        help="Orders below this cutoff are charged a nominal ₹40 shipping fee to recover carrier subsidies."
    )

with col_sim3:
    seller_penalty = st.slider(
        "⏱️ Lever 3: Late Seller SLA Penalty (₹ / order)",
        min_value=0, max_value=150, value=50, step=10,
        help="Contractual SLA breach penalty fee recovered from chronic late merchants per delayed dispatch."
    )

# Compute simulated EBITDA metrics
cod_rto_orders = filtered_df[(filtered_df['payment_method'] == 'Cash on Delivery (COD)') & (filtered_df['order_status'] == 'RTO / Returned')]
saved_cod_count = int(len(cod_rto_orders) * (cod_reduction / 100))
avg_cod_val = cod_rto_orders['order_value_inr'].mean() if len(cod_rto_orders) > 0 else 0
recovered_cod_lakhs = (saved_cod_count * 110 + saved_cod_count * avg_cod_val * 0.20) / 100000

sub_threshold_orders = filtered_df[(filtered_df['order_value_inr'] >= 499) & (filtered_df['order_value_inr'] < shipping_cutoff)]
recovered_shipping_lakhs = (len(sub_threshold_orders) * 40) / 100000

delayed_seller_orders = filtered_df[(filtered_df['is_chronic_late_seller'] == True) & (filtered_df['is_delayed'] == True)]
recovered_penalty_lakhs = (len(delayed_seller_orders) * seller_penalty) / 100000

sim_recovered_lakhs = recovered_cod_lakhs + recovered_shipping_lakhs + recovered_penalty_lakhs
sim_recovered_cr = sim_recovered_lakhs / 100
sim_optimized_profit_cr = total_profit_cr + sim_recovered_cr
sim_growth_pct = (sim_recovered_cr / total_profit_cr * 100) if total_profit_cr > 0 else 0

st.markdown("<br>", unsafe_allow_html=True)
sim_res1, sim_res2, sim_res3, sim_res4 = st.columns(4)
sim_res1.metric("Lever 1 (COD Shield)", f"+₹{recovered_cod_lakhs:.2f} L", delta=f"{saved_cod_count:,} Saved Orders")
sim_res2.metric("Lever 2 (Shipping Policy)", f"+₹{recovered_shipping_lakhs:.2f} L", delta=f"{len(sub_threshold_orders):,} Sub-₹{shipping_cutoff} Carts")
sim_res3.metric("Lever 3 (Seller Penalty)", f"+₹{recovered_penalty_lakhs:.2f} L", delta=f"{len(delayed_seller_orders):,} Penalized Delays")
sim_res4.metric(
    "Simulated Total EBITDA",
    f"₹{sim_optimized_profit_cr:.2f} Cr",
    delta=f"+₹{sim_recovered_lakhs:.2f} L (+{sim_growth_pct:.2f}%)",
    delta_color="normal"
)

st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# 8. DEEP-DIVE ANALYTICS TABS & ML CHECKOUT PREDICTOR
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📈 Deep-Dive Operational Analytics & Diagnostic Charts")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💳 Payment Risk & COD Trap",
    "🏷️ Category Margin Matrix",
    "🗺️ Regional Logistics Hubs",
    "🚚 Courier SLA & Review Cliff",
    "🤖 AI Checkout RTO Predictor"
])

# Global Plotly Theme Settings
chart_font = dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#0F172A")
chart_margins = dict(l=30, r=20, t=45, b=30)

# TAB 1: PAYMENT RISK
with tab1:
    st.markdown("#### Payment Mode Distribution vs RTO Return Failure Risk")
    pay_col1, pay_col2 = st.columns([1.2, 1])

    pay_summary = filtered_df.groupby('payment_method').agg(
        total_orders=('order_id', 'count'),
        rto_rate_pct=('order_status', lambda x: round((x == 'RTO / Returned').mean() * 100, 2)),
        total_profit_lakhs=('net_profit_inr', lambda x: round(x.sum() / 100000, 2))
    ).reset_index().sort_values(by='rto_rate_pct', ascending=False)

    with pay_col1:
        fig_pay = px.bar(
            pay_summary, x='rto_rate_pct', y='payment_method', orientation='h', text='rto_rate_pct',
            labels={'rto_rate_pct': 'RTO Return Failure Rate (%)', 'payment_method': 'Payment Channel'},
            title="RTO Return Rate by Payment Channel (%)",
            color='rto_rate_pct', color_continuous_scale=['#10B981', '#F59E0B', '#EF4444']
        )
        fig_pay.update_layout(
            showlegend=False, height=360, font=chart_font, margin=chart_margins,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        fig_pay.update_xaxes(showgrid=True, gridcolor="#F1F5F9")
        st.plotly_chart(fig_pay, use_container_width=True)

    with pay_col2:
        fig_pie = px.pie(
            pay_summary, values='total_orders', names='payment_method', hole=0.5,
            title="Checkout Channel Volume Share (%)",
            color_discrete_sequence=['#EF4444', '#10B981', '#3B82F6', '#8B5CF6']
        )
        fig_pie.update_layout(
            height=360, font=chart_font, margin=chart_margins,
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# TAB 2: CATEGORY MARGIN MATRIX
with tab2:
    st.markdown("#### Category Margin Vulnerability vs RTO Return Rate")
    cat_summary = filtered_df.groupby('category').agg(
        total_orders=('order_id', 'count'),
        total_sales_cr=('order_value_inr', lambda x: round(x.sum() / 10000000, 2)),
        net_margin_pct=('profit_margin_pct', 'mean'),
        rto_rate_pct=('order_status', lambda x: round((x == 'RTO / Returned').mean() * 100, 2))
    ).reset_index()

    fig_cat = px.scatter(
        cat_summary, x='rto_rate_pct', y='net_margin_pct', size='total_sales_cr', color='category', text='category',
        labels={'rto_rate_pct': 'RTO Return Rate (%)', 'net_margin_pct': 'Net Profit Margin (%)',
                'total_sales_cr': 'GMV (₹ Cr)'},
        title="Category Matrix: Margin % vs Return % (Bubble Size = GMV ₹ Cr)",
        size_max=45, color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_cat.add_vline(x=15, line_dash="dash", line_color="#EF4444", annotation_text="High Risk Threshold (15%)")
    fig_cat.update_layout(
        height=430, font=chart_font, margin=chart_margins,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    fig_cat.update_xaxes(showgrid=True, gridcolor="#F1F5F9")
    fig_cat.update_yaxes(showgrid=True, gridcolor="#F1F5F9")
    st.plotly_chart(fig_cat, use_container_width=True)

# TAB 3: REGIONAL LOGISTICS
with tab3:
    st.markdown("#### Geographic Revenue Contribution Across States")
    state_summary = filtered_df.groupby('state').agg(
        total_gmv_cr=('order_value_inr', lambda x: round(x.sum() / 10000000, 2)),
        total_orders=('order_id', 'count'),
        rto_rate_pct=('order_status', lambda x: round((x == 'RTO / Returned').mean() * 100, 2))
    ).reset_index().sort_values(by='total_gmv_cr', ascending=True)

    fig_state = px.bar(
        state_summary, x='total_gmv_cr', y='state', orientation='h', text='total_gmv_cr',
        labels={'total_gmv_cr': 'Marketplace GMV (₹ Crores)', 'state': 'State / Region'},
        title="Top States by Total Marketplace GMV (₹ Crores)",
        color='total_gmv_cr', color_continuous_scale='Blues'
    )
    fig_state.update_layout(
        height=430, font=chart_font, margin=chart_margins,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    fig_state.update_xaxes(showgrid=True, gridcolor="#F1F5F9")
    st.plotly_chart(fig_state, use_container_width=True)

# TAB 4: COURIER SLA CLIFF
with tab4:
    st.markdown("#### Courier Partner Delay Rates & The Customer SLA Cliff")
    cour_col1, cour_col2 = st.columns([1, 1.3])

    with cour_col1:
        courier_diag = filtered_df.groupby('courier_partner').agg(
            total_orders=('order_id', 'count'),
            delay_rate_pct=('is_delayed', lambda x: round(x.mean() * 100, 2)),
            avg_review=('review_score', lambda x: round(x.mean(), 2))
        ).reset_index().sort_values(by='delay_rate_pct', ascending=True)

        fig_cour = px.bar(
            courier_diag, x='courier_partner', y='delay_rate_pct', text='delay_rate_pct', color='courier_partner',
            labels={'delay_rate_pct': 'Delay Rate (%)', 'courier_partner': 'Courier Partner'},
            title="3PL Partner Delay Rate (%)",
            color_discrete_sequence=['#10B981', '#3B82F6', '#F59E0B', '#EF4444']
        )
        fig_cour.update_layout(
            showlegend=False, height=380, font=chart_font, margin=chart_margins,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        fig_cour.update_yaxes(showgrid=True, gridcolor="#F1F5F9")
        st.plotly_chart(fig_cour, use_container_width=True)

    with cour_col2:
        delay_trend = filtered_df.groupby('delivery_delay_days')['review_score'].mean().reset_index()
        fig_cliff = px.line(
            delay_trend, x='delivery_delay_days', y='review_score', markers=True,
            labels={'delivery_delay_days': 'Delivery Delay (Days: Negative=Early, Positive=Late)',
                    'review_score': 'Avg Customer Review (1-5)'},
            title="The Delivery SLA Cliff: Review Score vs Delay Days"
        )
        fig_cliff.add_vline(x=0, line_dash="dash", line_color="#EF4444", annotation_text="Promised SLA Deadline")
        fig_cliff.update_traces(line_color="#2563EB", line_width=3)
        fig_cliff.update_layout(
            height=380, font=chart_font, margin=chart_margins,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        fig_cliff.update_xaxes(showgrid=True, gridcolor="#F1F5F9")
        fig_cliff.update_yaxes(showgrid=True, gridcolor="#F1F5F9")
        st.plotly_chart(fig_cliff, use_container_width=True)

# TAB 5: AI CHECKOUT RTO PREDICTOR
with tab5:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px 24px; margin-bottom: 20px;">
        <div style="font-size: 1.15rem; font-weight: 800; color: #0F172A;">🤖 Real-Time AI Pre-Dispatch RTO Risk Classifier</div>
        <div style="font-size: 0.88rem; color: #64748B; margin-top: 2px;">
            Simulate any incoming order at the checkout gateway to predict its RTO return probability using our trained Random Forest model (<strong>87.28% Accuracy, 0.7431 ROC-AUC</strong>).
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_pred_in, col_pred_out = st.columns([1.1, 1])

    with col_pred_in:
        st.markdown("##### 📝 Order Simulation Parameters")
        in_cat = st.selectbox(
            "Product Category",
            options=sorted(df['category'].unique()),
            index=sorted(df['category'].unique()).index('Fashion & Ethnic Wear')
        )
        in_pay = st.selectbox(
            "Payment Method",
            options=sorted(df['payment_method'].unique()),
            index=sorted(df['payment_method'].unique()).index('Cash on Delivery (COD)')
        )
        in_state = st.selectbox(
            "Destination State",
            options=sorted(df['state'].unique()),
            index=sorted(df['state'].unique()).index('Uttar Pradesh')
        )

        c_val1, c_val2 = st.columns(2)
        with c_val1:
            in_price = st.number_input("Item Price (₹)", min_value=100, max_value=100000, value=1499, step=50)
        with c_val2:
            in_shipping = st.number_input("Shipping Fee (₹)", min_value=0, max_value=500, value=49, step=10)

        in_chronic = st.checkbox("Seller has Chronic Late Dispatch History (>25% Delays)", value=True)

    with col_pred_out:
        st.markdown("##### 🎯 Real-Time Risk Diagnostic")

        # Encode live user inputs to align with model one-hot feature schema
        input_data = {col: 0 for col in ml_features}
        input_data['price_inr'] = in_price
        input_data['shipping_fee_inr'] = in_shipping
        input_data['order_value_inr'] = in_price + in_shipping
        input_data['is_chronic_late_seller'] = 1 if in_chronic else 0

        cat_dummy = f"category_{in_cat}"
        if cat_dummy in input_data:
            input_data[cat_dummy] = 1

        pay_dummy = f"payment_method_{in_pay}"
        if pay_dummy in input_data:
            input_data[pay_dummy] = 1

        state_dummy = f"state_{in_state}"
        if state_dummy in input_data:
            input_data[state_dummy] = 1

        input_df = pd.DataFrame([input_data])[ml_features]
        rto_prob = ml_model.predict_proba(input_df)[0][1]
        rto_pct = round(rto_prob * 100, 2)

        # Operational Risk Classification & Playbook Recommendations
        if rto_pct >= 20.0:
            st.error(f"⚠️ **HIGH RTO RISK DETECTED: {rto_pct}% Return Probability**")
            st.metric(label="Predicted RTO Risk Score", value=f"{rto_pct}%", delta="High Risk", delta_color="inverse")
            st.progress(min(int(rto_pct), 100))
            
            st.markdown("""
            <div class="playbook-high-risk">
                <div class="playbook-title" style="color: #991B1B;">
                    <span>🛡️ Automated Pre-Dispatch Intervention Playbook:</span>
                </div>
                <div class="playbook-step">
                    <span class="step-icon">📲</span>
                    <div><strong>Trigger Automated WhatsApp/IVR Call:</strong> Require one-click customer confirmation before generating warehouse packing label.</div>
                </div>
                <div class="playbook-step">
                    <span class="step-icon">💸</span>
                    <div><strong>Offer Instant ₹50 UPI Discount:</strong> Incentivize customer to convert COD into prepaid, completely eliminating doorstep refusal.</div>
                </div>
                <div class="playbook-step">
                    <span class="step-icon">🚚</span>
                    <div><strong>Route via BlueDart Express:</strong> Assign premium SLA courier partner to eliminate transit fatigue and prevent cancellation.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"✅ **LOW RTO RISK DETECTED: {rto_pct}% Return Probability**")
            st.metric(label="Predicted RTO Risk Score", value=f"{rto_pct}%", delta="Normal / Safe", delta_color="normal")
            st.progress(min(int(rto_pct), 100))
            
            st.markdown("""
            <div class="playbook-low-risk">
                <div class="playbook-title" style="color: #166534;">
                    <span>🚀 Fast-Track Fulfillment Playbook:</span>
                </div>
                <div class="playbook-step">
                    <span class="step-icon">📦</span>
                    <div><strong>Auto-Dispatch to Conveyor:</strong> Immediate routing to warehouse picking conveyor with zero verification latency.</div>
                </div>
                <div class="playbook-step">
                    <span class="step-icon">🚚</span>
                    <div><strong>Standard Surface Routing:</strong> Optimize net margin by utilizing cost-effective standard logistics partners.</div>
                </div>
                <div class="playbook-step">
                    <span class="step-icon">🛡️</span>
                    <div><strong>Zero Friction Checkout:</strong> Maintain customer delight without intrusive verification interruptions.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# 9. EXECUTIVE SCENARIO EXPORT & ONE-CLICK DOWNLOAD
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📥 Executive Scenario Export")
st.write("Export the simulated strategy outcome or filtered operational data for C-Level review and academic audit:")

sim_export_df = pd.DataFrame({
    'Strategy Dimension': [
        'Current Baseline Profit',
        'Lever 1 (COD RTO Shield Recovery)',
        'Lever 2 (Shipping Policy Optimization)',
        'Lever 3 (Seller SLA Delay Penalization)',
        'Simulated Total EBITDA Profit',
        'Net Profit Expansion %'
    ],
    'Financial Impact': [
        f"₹{total_profit_cr:.2f} Cr",
        f"+₹{recovered_cod_lakhs:.2f} Lakhs",
        f"+₹{recovered_shipping_lakhs:.2f} Lakhs",
        f"+₹{recovered_penalty_lakhs:.2f} Lakhs",
        f"₹{sim_optimized_profit_cr:.2f} Cr",
        f"+{sim_growth_pct:.2f}%"
    ]
})

col_exp1, col_exp2 = st.columns([1.2, 1])
with col_exp1:
    st.dataframe(sim_export_df, use_container_width=True, hide_index=True)
with col_exp2:
    csv_data = sim_export_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Strategy Summary Report (CSV)",
        data=csv_data,
        file_name="BharatCart_Profit_Optimization_Scenario.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==============================================================================
# 10. ENTERPRISE FOOTER
# ==============================================================================
st.markdown("""
<div class="footer-container">
    <div><strong>BharatCart: Indian E-Commerce Profit Optimizer & Operations Intelligence Platform</strong></div>
    <div style="margin-top: 4px;">
        BCA 4-Year (Honours) Capstone Project • <strong>Prathamesh Mistari</strong> (Semester 7)<br>
        Department of Computer Science • <strong>Mercantile College of Science</strong> • Sardar Patel University (SPU)
    </div>
</div>
""", unsafe_allow_html=True)
