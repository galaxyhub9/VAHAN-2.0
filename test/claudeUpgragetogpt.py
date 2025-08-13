import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vehicle Investor Dashboard", layout="wide")

# Header
st.title("🚘 Indian Vehicle Registration Dashboard – Investor Insights")
st.subheader("Analyze category-wise and manufacturer-wise vehicle registration growth")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox("Select Year", ["2021", "2022", "2023", "2024"])
with col2:
    vehicle_type = st.selectbox("Select Vehicle Type", ["2W", "3W", "4W"])
with col3:
    manufacturer = st.selectbox("Select Manufacturer", ["Honda", "TVS", "Bajaj", "Hero", "Other"])

# KPIs
st.markdown("### Key Performance Indicators")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Vehicles", "2,340,000", "+8%")
kpi2.metric("YoY Growth", "6.5%", "↑")
kpi3.metric("QoQ Growth", "3.2%", "↓")
kpi4.metric("Top Manufacturer", "Hero MotoCorp")

st.divider()

# Charts (Mock Data)
st.markdown("### 📊 Vehicle Type-wise Growth")
st.plotly_chart(px.bar(
    pd.DataFrame({
        "Vehicle Type": ["2W", "3W", "4W"],
        "2023": [1000, 400, 800],
        "2024": [1200, 450, 900]
    }).melt(id_vars="Vehicle Type"),
    x="Vehicle Type", y="value", color="variable",
    barmode="group", title="YoY Comparison by Vehicle Type"
), use_container_width=True)

st.markdown("### 📈 Monthly Registrations Trend")
st.plotly_chart(px.line(
    pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr"],
        "Hero": [100, 110, 130, 125],
        "Honda": [90, 95, 100, 110]
    }).melt(id_vars="Month"),
    x="Month", y="value", color="variable",
    title="Manufacturer-wise Monthly Trend"
), use_container_width=True)

st.markdown("### 🥧 Market Share by Manufacturer")
st.plotly_chart(px.pie(
    names=["Hero", "Honda", "Bajaj", "TVS", "Others"],
    values=[35, 25, 15, 15, 10],
    title="Market Share"
), use_container_width=True)

# Table
st.markdown("### 📋 Manufacturer-wise Summary")
st.dataframe(pd.DataFrame({
    "Manufacturer": ["Hero", "Honda", "TVS"],
    "Category": ["2W", "2W", "2W"],
    "Total Registrations": [123000, 110000, 95000],
    "YoY Growth": ["+5%", "+6%", "+4%"],
    "QoQ Growth": ["+1%", "+2%", "0%"]
}))

