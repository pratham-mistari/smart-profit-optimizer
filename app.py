import streamlit as st
import pandas as pd
import plotly.express as px
import joblib


# Configure dashboard page title, icon, and wide responsive layout
st.set_page_config(
    page_title="BharatCart | Profit Optimizer & Operations Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-performance cached data loader for the processed 100k transaction dataset
@st.cache_data
def load_processed_data():
    data_path = "data/processed/indian_ecommerce_processed.csv"
    data = pd.read_csv(data_path)
    return data

# Load dataset into memory
df = load_processed_data()

# Header banner and project metadata
st.title("🇮🇳 BharatCart: Profit Optimizer & Logistics Intelligence")
st.caption("Enterprise Operations & Profitability Diagnostic Platform | 100,000 Pan-India Transactions")
st.markdown("---")

# Quick data sanity test on startup
st.success(f"Pipeline Connected: Successfully loaded {len(df):,} orders across {len(df.columns)} operational features!")

# Sidebar interactive filters
st.sidebar.header("🔍 Marketplace Filters")
selected_state = st.sidebar.selectbox("Select State / Region:", ["All States"] + sorted(df['state'].unique().tolist()))
selected_category = st.sidebar.selectbox("Select Category:", ["All Categories"] + sorted(df['category'].unique().tolist()))
selected_payment = st.sidebar.selectbox("Select Payment Mode:", ["All Methods"] + sorted(df['payment_method'].unique().tolist()))
# Apply filters dynamically to dataset
filtered_df = df.copy()
if selected_state != "All States":
    filtered_df = filtered_df[filtered_df['state'] == selected_state]
if selected_category != "All Categories":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
if selected_payment != "All Methods":
    filtered_df = filtered_df[filtered_df['payment_method'] == selected_payment]
# Compute core executive financial KPIs
total_gmv_cr = filtered_df['order_value_inr'].sum() / 10000000
total_orders = len(filtered_df)
total_profit_cr = filtered_df['net_profit_inr'].sum() / 10000000
margin_pct = (filtered_df['net_profit_inr'].sum() / filtered_df['order_value_inr'].sum() * 100) if filtered_df['order_value_inr'].sum() > 0 else 0
cod_subset = filtered_df[filtered_df['payment_method'] == 'Cash on Delivery (COD)']
cod_rto_pct = (cod_subset['order_status'] == 'RTO / Returned').mean() * 100 if len(cod_subset) > 0 else 0
# Render top-level KPI metric cards
st.subheader("📊 Executive Financial Performance Deck")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Marketplace GMV", f"₹{total_gmv_cr:.2f} Cr")
kpi2.metric("Audited Orders", f"{total_orders:,}")
kpi3.metric("Operating Profit", f"₹{total_profit_cr:.2f} Cr")
kpi4.metric("Net Margin %", f"{margin_pct:.2f}%")
kpi5.metric("COD RTO Rate", f"{cod_rto_pct:.2f}%", delta="High Risk" if cod_rto_pct > 15 else "Normal", delta_color="inverse")
st.markdown("---")

# Multi-Lever Profit Optimization Simulator (Interactive UI)
st.subheader("⚡ Live Multi-Lever Profit Optimization Simulator")
st.write("Tune the policy levers below in real-time to simulate EBITDA recovery across the marketplace:")

col_sim1, col_sim2, col_sim3 = st.columns(3)
with col_sim1:
    cod_reduction = st.slider(
        "🛡️ Lever 1: COD OTP & Shield Adoption (%)",
        min_value=0, max_value=80, value=40, step=5,
        help="Expected % of risky COD orders converted to successful deliveries via OTP verification and instant UPI discount."
    )

with col_sim2:
    shipping_cutoff = st.select_slider(
        "🚚 Lever 2: Free Delivery Threshold (₹)",
        options=[499, 599, 699, 799, 999],
        value=799,
        help="Orders below this cutoff are charged a nominal ₹40 shipping fee to recover 3PL carrier subsidies."
    )

with col_sim3:
    seller_penalty = st.slider(
        "⏱️ Lever 3: Late Seller SLA Penalty (₹ / order)",
        min_value=0, max_value=150, value=50, step=10,
        help="Penalty fee recovered from chronic late sellers per delayed dispatch."
    )

# Calculate live simulation financial metrics
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

# Display simulated recovery impact cards
sim_res1, sim_res2, sim_res3, sim_res4 = st.columns(4)
sim_res1.metric("Lever 1 (COD Shield)", f"+₹{recovered_cod_lakhs:.2f} L")
sim_res2.metric("Lever 2 (Shipping Policy)", f"+₹{recovered_shipping_lakhs:.2f} L")
sim_res3.metric("Lever 3 (Seller SLA)", f"+₹{recovered_penalty_lakhs:.2f} L")
sim_res4.metric("Simulated Total Profit", f"₹{sim_optimized_profit_cr:.2f} Cr", delta=f"+₹{sim_recovered_lakhs:.2f} L (+{sim_growth_pct:.2f}%)", delta_color="normal")
st.markdown("---")

# Detailed Analytics Tabs
st.subheader("📈 Deep-Dive Operational Analytics & Diagnostic Charts")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💳 Payment Risk & COD Trap",
    "🏷️ Category Margin Matrix",
    "🗺️ Regional Logistics Hubs",
    "🚚 Courier SLA & Review Cliff",
    "🤖 AI Checkout RTO Predictor"
])

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
            labels={'rto_rate_pct': 'RTO Return Failure Rate (%)', 'payment_method': 'Payment Mode'},
            title="RTO Return Rate by Payment Channel (%)",
            color='rto_rate_pct', color_continuous_scale=['#10B981', '#F59E0B', '#EF4444']
        )
        fig_pay.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_pay, use_container_width=True)

    with pay_col2:
        fig_pie = px.pie(
            pay_summary, values='total_orders', names='payment_method', hole=0.45,
            title="Payment Channel Checkout Share",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

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
        title="Category Vulnerability: Net Margin % vs RTO Rate % (Bubble Size = GMV ₹ Cr)",
        size_max=45
    )
    fig_cat.add_vline(x=15, line_dash="dash", line_color="#EF4444", annotation_text="High Risk Threshold (15%)")
    fig_cat.update_layout(height=450)
    st.plotly_chart(fig_cat, use_container_width=True)

with tab3:
    st.markdown("#### Geographic Revenue Contribution by State")
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
    fig_state.update_layout(height=450)
    st.plotly_chart(fig_state, use_container_width=True)

with tab4:
    st.markdown("#### Courier Partner Performance & The Delivery SLA Cliff")
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
            title="Courier Partner Delay Rate (%)",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_cour.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig_cour, use_container_width=True)

    with cour_col2:
        delay_trend = filtered_df.groupby('delivery_delay_days')['review_score'].mean().reset_index()
        fig_cliff = px.line(
            delay_trend, x='delivery_delay_days', y='review_score', markers=True,
            labels={'delivery_delay_days': 'Delivery Delay (Days: Negative=Early, Positive=Late)',
                    'review_score': 'Avg Review Score (1-5)'},
            title="The Delivery SLA Cliff: Review Score vs Delay Days"
        )
        fig_cliff.add_vline(x=0, line_dash="dash", line_color="#EF4444", annotation_text="Promised SLA Deadline")
        fig_cliff.update_traces(line_color="#2563EB", line_width=3)
        fig_cliff.update_layout(height=380)
        st.plotly_chart(fig_cliff, use_container_width=True)

with tab5:
    st.markdown("#### 🤖 Real-Time AI Pre-Dispatch RTO Risk Classifier")
    st.write("Simulate any incoming order at checkout to predict its RTO return probability using our trained Random Forest model (**87.28% Accuracy, 0.7431 ROC-AUC**).")

    # High-performance cached ML pipeline loader
    @st.cache_resource
    def load_trained_model():
        model = joblib.load('models/rto_rf_model.joblib')
        features = joblib.load('models/model_features.joblib')
        return model, features

    ml_model, ml_features = load_trained_model()

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
            **Automated Pre-Dispatch Intervention Playbook:**
            - 📲 **Trigger WhatsApp/IVR Automated Call** for order confirmation before label generation.
            - 💸 **Offer Instant ₹50 UPI Cashback Discount** to convert COD order into Prepaid.
            - 🚚 **Assign Premium SLA Courier Partner** (BlueDart/Delhivery Express) to avoid transit fatigue.
            """)
        else:
            st.success(f"✅ **LOW RTO RISK DETECTED: {rto_pct}% Return Probability**")
            st.metric(label="Predicted RTO Risk Score", value=f"{rto_pct}%", delta="Normal / Safe", delta_color="normal")
            st.progress(min(int(rto_pct), 100))
            st.markdown("""
            **Automated Pre-Dispatch Intervention Playbook:**
            - 🚀 **Fast-Track Auto Fulfillment**: Dispatch order directly to warehouse conveyor.
            - 📦 **Standard Logistics Routing**: Optimal margin retention with standard Surface courier.
            - 🛡️ **Zero Friction Checkout**: No additional customer verification required.
            """)

# Executive Scenario Export & One-Click Download
st.markdown("---")
st.subheader("📥 Executive Scenario Export")
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
