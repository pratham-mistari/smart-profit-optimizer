# 🇮🇳 BharatCart: Indian E-Commerce Profit Optimizer & Operations Intelligence

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2+-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Data_Viz-4C72B0)](https://seaborn.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade Data Analytics & Business Intelligence project investigating **silent margin leakage, Cash on Delivery (COD) Return to Origin (RTO) risks, delivery latency SLAs, and discount sensitivity** across **100,000+ Indian e-commerce orders** (Flipkart / Meesho / Amazon IN model).

---

## 🎯 Business Context & Problem Statement
Indian e-commerce marketplaces handle millions of transactions across high-growth metros (Delhi NCR, Mumbai, Bengaluru) and Tier-2/3 cities (Surat, Rajkot, Jaipur). However, profitability is severely challenged by:
1. **The Cash on Delivery (COD) Trap:** COD orders experience a **25.02% RTO (Return to Origin)** failure rate compared to only **8.03% for UPI**, eroding forward and reverse logistics costs.
2. **Delivery Latency & Review Rating Penalty:** Orders delayed beyond the promised SLA deadline trigger an exponential drop in customer review score (from 4.5+ ⭐ down to 1.8 ⭐).
3. **Logistics Courier Reliability:** Comparative evaluation of carrier SLAs across Delhivery, BlueDart, Ecom Express, and Shadowfax.
4. **Festive Sale Discount Margin Erosion:** Pricing thresholds during Great Indian / Big Billion sale events.

---

## 📁 Repository Architecture
```text
smart-profit-optimizer/
├── data/
│   └── raw/
│       └── indian_ecommerce_100k.csv      # 100,000 real-world Indian orders (₹61.96 Cr GMV)
├── analysis.ipynb                         # Core Jupyter Notebook written cell-by-cell in PyCharm
├── .gitignore                             # Hygiene filter (excluding .venv, .idea, cache)
├── requirements.txt                       # Python dependencies
└── README.md                              # Project documentation
```

---

## 📊 Key Findings Discovered
* **Total Transactions Audited:** 100,000 orders
* **Gross Merchandise Value (GMV):** **₹61.96 Crores**
* **Payment Mode Share:** UPI leads checkout with **48.27%** share, followed by COD at **27.79%**.
* **COD RTO Risk Factor:** COD orders are **3.1x more likely to fail and return** than prepaid UPI orders.
* **Top States by Order Volume:** Gujarat (20%), Maharashtra (22%), Delhi NCR (14%), Karnataka (12%).

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/pratham-mistari/smart-profit-optimizer.git
cd smart-profit-optimizer
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

### 3. Open in PyCharm / Jupyter Notebook
Launch `analysis.ipynb` and run the cells sequentially to reproduce the end-to-end data auditing, visualizations, and financial findings.

---

## 👨‍💻 Project Information & Academic Credits
* **Student Name:** Prathamesh Mistari
* **GitHub:** [@pratham-mistari](https://github.com/pratham-mistari)
* **Degree:** Bachelor of Computer Applications (BCA - 4 Year Honors)
* **Semester:** Semester 7 (Capstone On-the-Job Training - 6 Credits / 180 Hours)
* **University:** Sardar Patel University (SPU)
* **Focus Area:** Data Analytics & E-Commerce Business Intelligence
