# 📊 Smart E-Commerce Profit Optimizer & Dynamic Pricing Simulator

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Express-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end interactive Business Intelligence and Data Analytics platform engineered to diagnose **profit margin leakage**, simulate **dynamic discounting thresholds**, and segment customers using mathematical **RFM (Recency, Frequency, Monetary)** analytics.

---

## 🎯 Key Capabilities
* **Interactive What-If Sensitivity Simulator:** Real-time discount slider showing live net profit impacts.
* **Executive KPI Ribbon:** Live delta tracking for Gross Revenue, Operating Margin %, and Active Customers.
* **Geospatial Profit Heatmaps:** Interactive state-level choropleth visualization for regional leakage diagnostics.
* **RFM Customer Segmentation:** Automated quintile scoring categorizing customers into Champions, Loyalists, At Risk, and Churned.

---

## 📁 Repository Architecture
```text
smart-profit-optimizer/
├── data/
│   ├── raw/                 # Original raw transactions (51k+ records)
│   └── processed/           # Cleaned gold-standard CSV
├── notebooks/
│   ├── 01_data_cleaning_eda.ipynb
│   └── 02_rfm_customer_cohorts.ipynb
├── src/
│   ├── data_loader.py       # Data caching & validation
│   ├── metrics_engine.py    # KPI calculations & RFM logic
│   └── chart_builder.py     # Interactive Plotly figures
├── assets/
│   └── screenshots/         # UI previews for reports
├── .streamlit/
│   └── config.toml          # Custom theme configuration
├── app.py                   # Main Streamlit Dashboard
├── requirements.txt         # Dependencies
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Clone & Navigate
```bash
git clone https://github.com/pratham-mistari/smart-profit-optimizer.git
cd smart-profit-optimizer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Web Dashboard
```bash
streamlit run app.py
```
The interactive application will automatically launch in your browser at `http://localhost:8501`.

---

## 👨‍💻 Author
* **Student Name:** Prathamesh Mistari
* **Course:** BCA 4-Year (Semester 7)
* **University:** SPU (Sankalchand Patel University / Sardar Patel University)
* **Project Guide:** Faculty Coordinator / OJT Mentor
