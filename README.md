# 🏭VAHAN 2.0

A data-driven dashboard to analyze and visualize vehicle registration trends in India using **Streamlit**, **Pandas**, and **NumPy**.  
This project processes raw vehicle registration data, performs aggregations, and presents interactive visualizations for market insights.

---
## 📈 key Investor Insights I discovered


| Segment | Insight |
|---------|---------|
| **EV Market** | EVs form only **2.5%** of total registrations, showing huge growth potential but still early-stage adoption. |
| **Two-Wheelers** | **74.2%** of all registrations are two-wheelers, highlighting a larger and more stable market than passenger cars. |

## 📦 Setup Instructions

Follow the steps below to run the project locally:


1️⃣ Clone the repository
```
git clone https://github.com/galaxyhub9/VAHAN-2.0.git
```

2️⃣ Navigate to the 'test' directory

```
cd VAHAN-2.0/test
```

3️⃣ Create a virtual environment

```
python -m venv venv
```

4️⃣ Activate the virtual environment

Windows
```
venv\Scripts\activate
```
Mac/Linux
```
source venv/bin/activate
```

5️⃣ Install dependencies

```
pip install -r requirements.txt
```

6️⃣ Run the Streamlit dashboard

```
streamlit run vahan.py
```

## 📊 Data Assumptions

- **Source**: Data has been downloaded from the [official VAHAN Dashboard](https://vahan.parivahan.gov.in/vahan4dashboard/vahan/dashboardview.xhtml).

- **Data Preparation**:
  - Data is dowmloaded in excel format.  
  - Added a `Year` column for each dataset.
  - Converted it into DataFrame using pandas. 
  - Aggregated monthly and yearly data into separate files for better modularity.
  - Data of year 2020 to 2022 has been used.
  - All datasets are cleaned and structured for easier analysis in the dashboard.

---

## 🚀 Feature Roadmap

If the project is continued, the following features will be added:

1. **Predictive Market Analysis**
   - Use historical trends to forecast future market share for each vehicle category.
   
2. **Advanced Filtering Options**
   - More granular filters such as fuel type, region, manufacturer, and time period.
   
3. **Data Source Integration**
   - Automated scraping or API integration to fetch the latest VAHAN data directly.
   
4. **Export & Reporting**
   - Option to export visualizations and reports as PDF/Excel.

---

## 🛠 Tech Stack

- **Python** → Data processing & dashboard logic
- **Pandas & NumPy** → Data cleaning, transformation, and aggregation
- **Streamlit** → Interactive UI for visualization



