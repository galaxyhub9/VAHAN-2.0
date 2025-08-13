import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(layout="wide", page_title="Vehicle Dashboard", page_icon="🚗")

st.title("📊 Vehicle Registration Dashboard (2020–2022)")

# Load all data
@st.cache_data
def load_data():
    df_maker_category = pd.read_excel("reportTable 2020 - 22.xlsx", engine="openpyxl")
    df_category_month = pd.read_excel("month wise v category 20-22.xlsx", engine="openpyxl")
    df_maker_month = pd.read_excel("Maker Month Wise Data  20-22.xlsx", engine="openpyxl")
    return df_maker_category, df_category_month, df_maker_month

df_maker_category, df_category_month, df_maker_month = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
years = sorted(df_maker_category['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

all_makers = sorted(df_maker_category['Maker'].dropna().unique())
selected_maker = st.sidebar.multiselect("Select Manufacturer(s)", all_makers, default=all_makers)

all_categories = sorted(df_category_month['Vehicle Category'].dropna().unique())
selected_category = st.sidebar.multiselect("Select Vehicle Category(s)", all_categories, default=all_categories)

# ---- Section 1: Category vs Maker Table ----
st.subheader("🚘 Maker-wise Vehicle Category Distribution")

filtered_maker_data = df_maker_category[
    (df_maker_category["Year"] == selected_year) & 
    (df_maker_category["Maker"].isin(selected_maker))
]

st.dataframe(filtered_maker_data.reset_index(drop=True), use_container_width=True)

# ---- Section 2: Category-wise Monthly Trend ----
st.subheader("📈 Month-wise Vehicle Category Trends")

filtered_category_month = df_category_month[
    (df_category_month["Year"] == selected_year) & 
    (df_category_month["Vehicle Category"].isin(selected_category))
]

category_chart = filtered_category_month.set_index("Vehicle Category").loc[:, "JAN":"DEC"].T
st.line_chart(category_chart, use_container_width=True)

# ---- Section 3: Maker-wise Monthly Registration ----
st.subheader("🏭 Month-wise Manufacturer Trends")

filtered_maker_month = df_maker_month[
    (df_maker_month["Year"] == selected_year) & 
    (df_maker_month["Maker"].isin(selected_maker))
]

maker_chart = filtered_maker_month.set_index("Maker").loc[:, "JAN":"DEC"].T
st.line_chart(maker_chart, use_container_width=True)

# ---- Summary Metrics ----
st.subheader("📌 Key Stats")
col1, col2, col3 = st.columns(3)
col1.metric("🔢 Total Makers", df_maker_category['Maker'].nunique())
col2.metric("🚗 Vehicle Categories", df_category_month['Vehicle Category'].nunique())
col3.metric("📅 Year", selected_year)
