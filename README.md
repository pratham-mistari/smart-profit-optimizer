# 🇮🇳 BharatCart: Indian E-Commerce Profit Optimizer & Operations Intelligence

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App_Live-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Random_Forest-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2+-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade Data Analytics & Machine Learning web platform investigating **margin leakage, Cash on Delivery (COD) Return to Origin (RTO) risks, courier delivery SLAs, seller dispatch bottlenecks, AI risk scoring, and real-time multi-lever profit optimization** across **100,000+ Indian e-commerce orders** worth **₹61.96 Crores GMV** (modeled after Flipkart, Meesho, and Amazon India).

---

## 🎯 Business Context & Core Problem Statements
Indian e-commerce marketplaces operate on razor-thin margins. Unlike Western retail models, Indian marketplaces face distinct structural operational challenges:
1. **The Cash on Delivery (COD) RTO Trap:** COD accounts for **27.79%** of volume but suffers a staggering **25.02% RTO failure rate** (compared to only **8.03% for UPI**). Failed deliveries incur forward shipping, return freight, and inventory depreciation.
2. **Delivery Latency & The Review Score Cliff:** When couriers breach promised SLAs, customer reviews plummet from **4.5+ ⭐ down to 1.8 ⭐**, damaging customer lifetime value.
3. **Chronic Late Seller Risk:** Fulfillment delays from chronic late sellers cause a **38.20% delay rate** (7.6x higher than reliable vendors) and crash ratings to **3.07 ⭐**.
4. **Category Freight Bleed:** Fashion & Ethnic Wear (**27.29% RTO**) and Footwear (**22.50% RTO**) bleed reverse freight due to sizing mismatch and impulse trial ordering.

---

## 📁 Repository Architecture
```text
smart-profit-optimizer/
├── data/
│   ├── raw/
│   │   └── indian_ecommerce_100k.csv         # Raw 100,000 real-world Indian orders (₹61.96 Cr GMV)
│   └── processed/
│       └── indian_ecommerce_processed.csv    # Enriched production dataset (24.17 MB, 23 features)
├── models/
│   ├── rto_rf_model.joblib                   # Production Random Forest Classifier (100 Trees, 7.28 MB)
│   └── model_features.joblib                 # Serialized feature alignment schema (23 features)
├── .streamlit/
│   └── config.toml                           # Streamlit server & theme styling configuration
├── app.py                                    # Full Production Streamlit Web Dashboard (310+ LOC)
├── analysis.ipynb                            # Complete 17-step Jupyter Notebook written in PyCharm
├── .gitignore                                # Hygiene filter (excluding .venv, .idea, cache)
├── requirements.txt                          # Python dependencies (Streamlit, Scikit-Learn, Plotly, etc.)
└── README.md                                 # Technical project documentation
```

---

## 🖥️ Interactive Web Dashboard Features (`app.py`)
1. **High-Speed Architecture:** Streamlit cache (`@st.cache_data` & `@st.cache_resource`) for instantaneous loading of 100,000 transactions and ML model inference.
2. **Dynamic Sidebar Filters:** Multi-dimensional slicing across Indian States / Regions, Product Categories, and Payment Channels.
3. **Executive KPI Cards Deck:** Live display of GMV (₹61.96 Cr), Total Orders (100,000), Net Profit (₹11.85 Cr), Net Margin (19.12%), and COD RTO Rate with bright RED High-Risk alert pill.
4. **Live Multi-Lever Profit Simulator:** Real-time recalculation of EBITDA recovery (+₹34.62 Lakhs / +2.92%) and net profit (₹12.19 Cr) across 3 interactive sliders.
5. **Interactive Diagnostic Tabs (Plotly & Scikit-Learn):**
   * **💳 Payment Risk & COD Trap:** Horizontal failure rate bar chart + Volume share donut chart.
   * **🏷️ Category Margin Matrix:** Scatter/Bubble chart of Net Margin % vs RTO Rate with red 15% threshold line.
   * **🗺️ Regional Logistics Hubs:** Top revenue states horizontal bar chart (Maharashtra ₹13.54 Cr, Gujarat ₹12.18 Cr).
   * **🚚 Courier SLA & Review Cliff:** Partner delay rates and the delivery latency review collapse curve.
   * **🤖 AI Checkout RTO Predictor (Phase 3 Flagship):** Real-time order simulation form scoring RTO risk with dynamic alert badges and automated intervention playbooks.
6. **Executive Scenario Export:** One-click CSV download button (`BharatCart_Profit_Optimization_Scenario.csv`) for management review.

---

## 📊 Key Empirical Findings & Metrics

| Dimension | Metric / Discovery | Strategic Business Impact |
| :--- | :--- | :--- |
| **Marketplace Scale** | **100,000 Orders \| ₹61.96 Cr GMV** | High-scale multi-category pan-India dataset. |
| **Baseline Operating Profit** | **₹11.85 Crores** (19.12% Net Margin) | Healthy operational profit before strategic policy simulation. |
| **COD vs UPI Risk** | **25.02% COD RTO vs 8.03% UPI RTO** | COD is **3.12x more prone to return failure**, leaking ₹2.85 Cr. |
| **RFM Champions Cohort** | **8,138 Customers \| ₹33.06 Cr GMV** | >53% of GMV generated by high-frequency Champions. |
| **Category RTO Leakage** | **Fashion (27.29%) & Shoes (22.50%)** | ₹6.23 Lakhs leaked in reverse freight across apparel/shoes. |
| **Chronic Seller Bottleneck**| **38.20% Delay Rate \| 3.07 Star Rating** | 10,086 orders compromised by unreliable dispatch partners. |
| **Geo-Logistics Corridor** | **MH + GJ + NCR + KA = 67.8% Volume** | ₹42.00 Cr concentrated in top 4 states; Bhiwandi/Ahmedabad RFCs. |

---

## 🚀 Multi-Lever Profit Optimization Simulator Results

Our interactive simulation engine evaluated three simultaneous policy interventions:
* **Lever 1 (AI COD RTO Shield):** Pre-dispatch OTP verification and ₹25 instant UPI discount incentives prevent 40% of COD returns (2,781 orders converted to delivered sales), recovering **₹28.23 Lakhs**.
* **Lever 2 (Shipping Threshold Optimization):** Raising the free shipping threshold from ₹499 to ₹799 applies a ₹40 fee on 11,137 low-margin basket orders, recovering **₹4.45 Lakhs**.
* **Lever 3 (Seller SLA Recovery):** Enforcing a ₹50 fulfillment breach fee on 3,853 delayed dispatches from chronic sellers recovers **₹1.93 Lakhs**.

> 🎯 **Bottom-Line Impact:** Expands net operating profit from **₹11.85 Cr to ₹12.19 Cr**, unlocking **+₹34.62 Lakhs (+2.92%) in pure incremental EBITDA cash profit** without any extra marketing spend.

---

## 🤖 Phase 3: Machine Learning Pre-Dispatch RTO Predictive Pipeline

To proactively intercept high-risk orders before warehouse dispatch, we engineered a supervised **Random Forest Classifier**:
* **Dataset Splitting:** 80,000 Training Orders / 20,000 Testing Orders (Stratified 80/20 Split maintaining 12.72% RTO class balance).
* **Model Architecture:** 100 Decision Trees (`n_estimators=100`), Max Depth 10 (`max_depth=10`).
* **Evaluation on 20,000 Unseen Test Orders:**
  * **Overall Accuracy:** **87.28%**
  * **ROC-AUC Score:** **0.7431** (Strong discriminatory power on imbalanced real-world e-commerce data).
* **Top Predictive Feature Importance Drivers:**
  1. `payment_method_UPI`: **19.21%** (Prepaid commitment strongly predicts successful delivery)
  2. `category_Fashion & Ethnic Wear`: **16.44%** (Sizing trials & impulse purchases inflate return risk)
  3. `price_inr`: **14.23%** (Higher value COD items have elevated buyer remorse)
  4. `order_value_inr`: **14.05%** (Basket size correlation with refusal rate)
  5. `payment_method_Credit Card`: **9.12%**
  6. `category_Footwear & Shoes`: **8.21%**
  7. `payment_method_Debit Card`: **6.79%**

---

## 💻 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/pratham-mistari/smart-profit-optimizer.git
cd smart-profit-optimizer
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Interactive Streamlit Web Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to explore the live dashboard, adjust simulator sliders, and inspect diagnostic analytics tabs.

### 4. Or Run the Jupyter Notebook in PyCharm
Launch `analysis.ipynb` and execute the 17 modular cells to review the data auditing, feature engineering, and Random Forest machine learning pipeline.

---

## 👨‍💻 Author & Academic Information
* **Student Name:** Prathamesh Mistari
* **GitHub Profile:** [@pratham-mistari](https://github.com/pratham-mistari)
* **Degree:** Bachelor of Computer Applications (BCA - 4 Year Honours)
* **Semester:** Semester 7 (Capstone On-the-Job Training - 6 Credits / 180 Hours)
* **University:** Sardar Patel University (SPU), Gujarat, India
* **Focus Area:** Data Analytics, Supply Chain Economics & E-Commerce Business Intelligence
