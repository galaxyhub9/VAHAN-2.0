import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- Dummy Data Setup ----------

# Vehicle category based on maker
data_category_maker = pd.DataFrame({
    'Maker': ['3GB TECHNOLOGY PVT LTD', '3S INDUSTRIES PRIVATE LIMITED'],
    '2WIC': [0, 0], '2WN': [0, 0], '2WT': [0, 0],
    '3WIC': [0, 0], '3WN': [0, 0], '3WT': [0, 66],
    '4WIC': [0, 0], 'HGV': [0, 0], 'HMV': [0, 0], 'HPV': [0, 0],
    'LGV': [4, 74], 'LMV': [0, 0], 'LPV': [0, 0], 'MGV': [0, 0],
    'MMV': [0, 0], 'MPV': [0, 0], 'OTH': [1, 2], 'Year': [2020, 2020], 'Total': [5, 142]
})

# Month-wise vehicle category data
data_category_month = pd.DataFrame({
    'Vehicle Category': ['FOUR WHEELER (INVALID CARRIAGE)', 'HEAVY GOODS VEHICLE', 'HEAVY MOTOR VEHICLE'],
    'JAN': [166, 18154, 534], 'FEB': [144, 22232, 551], 'MAR': [151, 28400, 637],
    'APR': [105, 3322, 194], 'MAY': [14, 88, 35], 'JUN': [94, 464, 168],
    'JUL': [97, 1360, 267], 'AUG': [120, 2635, 262], 'SEP': [132, 5281, 367],
    'OCT': [129, 7506, 295], 'NOV': [162, 9041, 338], 'DEC': [165, 12007, 406],
    'Year': [2020, 2020, 2020], 'Total': [1479, 110490, 4054]
})

# Month-wise maker/manufacturer data
data_maker_month = pd.DataFrame({
    'Maker': ['3GB TECHNOLOGY PVT LTD', '3S INDUSTRIES PRIVATE LIMITED', 'A1 HEAVY EQUIPMENTS DEVELOPER', 'A3T INCORPORTED', 'AADHYA ENTERPRISES'],
    'JAN': [0, 41, 8, 3, 20], 'FEB': [3, 38, 4, 3, 21], 'MAR': [1, 23, 3, 4, 25],
    'APR': [0, 1, 5, 0, 1], 'MAY': [0, 1, 1, 0, 0], 'JUN': [0, 1, 1, 0, 0],
    'JUL': [0, 6, 0, 0, 0], 'AUG': [1, 1, 3, 0, 0], 'SEP': [0, 9, 0, 0, 0],
    'OCT': [0, 6, 1, 0, 1], 'NOV': [0, 10, 1, 0, 1], 'DEC': [0, 5, 10, 1, 0],
    'Year': [2020]*5, 'Total': [5, 142, 37, 11, 69]
})

# ---------- Streamlit Dashboard ----------
st.title("🚘 Vehicle Analysis Dashboard - Prototype")

# Sidebar Filters
st.sidebar.header("Filters")
year_filter = st.sidebar.selectbox("Select Year", data_category_maker['Year'].unique())
st.sidebar.write("You can expand the dashboard for deeper insights.")

# Filter data based on year
category_maker_filtered = data_category_maker[data_category_maker['Year'] == year_filter]
category_month_filtered = data_category_month[data_category_month['Year'] == year_filter]
maker_month_filtered = data_maker_month[data_maker_month['Year'] == year_filter]

# Section 1: Category-wise Distribution per Maker
st.subheader("1. Vehicle Category Distribution per Maker")
category_sum = category_maker_filtered.drop(columns=['Maker', 'Year', 'Total']).sum()
st.bar_chart(category_sum)

# Section 2: Month-wise Vehicle Registrations by Category
st.subheader("2. Monthly Vehicle Registrations by Category")
category_month_chart = category_month_filtered.set_index('Vehicle Category').drop(columns=['Year', 'Total']).T
st.line_chart(category_month_chart)

# Section 3: Monthly Vehicle Registrations by Manufacturer
st.subheader("3. Monthly Vehicle Registrations by Maker")
maker_month_chart = maker_month_filtered.set_index('Maker').drop(columns=['Year', 'Total'])
st.area_chart(maker_month_chart.T)

# Section 4: Top Makers by Total Registration
st.subheader("4. Top Manufacturers (Total Vehicles)")
top_makers = category_maker_filtered[['Maker', 'Total']].sort_values(by='Total', ascending=False)
st.dataframe(top_makers)

# Section 5: Heatmap-like view for Category vs Maker
st.subheader("5. Vehicle Type Matrix (Maker vs Category)")
st.dataframe(category_maker_filtered.set_index('Maker').drop(columns=['Year', 'Total']).style.background_gradient(cmap='Oranges'))
