import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Vehicle Registration Data (Maker Wise)")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Combined Excel File", type=["xlsx"])

if uploaded_file:
    # Load data
    df = pd.read_excel(uploaded_file)

    # Clean column names (optional)
    df.columns = df.columns.str.strip()

    # Sidebar filters
    st.sidebar.header("Filter Options")
    # st.write("🔍 Column names in your file:")
    # st.write(df.columns.tolist())


    years = df["Year"].unique()
    selected_years = st.sidebar.multiselect("Select Year(s)", years, default=years)

    makers = df["Maker"].unique()
    selected_makers = st.sidebar.multiselect("Select Maker(s)", makers, default=makers)

    # Filter data
    filtered_df = df[df["Year"].isin(selected_years) & df["Maker"].isin(selected_makers)]

    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Total Vehicles by Maker
    st.subheader("Total Vehicles by Maker")
    totals_by_maker = filtered_df.groupby("Maker")["Total"].sum().sort_values(ascending=False)
    st.bar_chart(totals_by_maker)

    # Total per Vehicle Category
    category_columns = df.columns[2:-2]  # skips S No, Maker, Year, TOTAL
    st.subheader("Total by Vehicle Category")
    # Convert category columns to numeric, forcing errors to NaN
    filtered_df[category_columns] = filtered_df[category_columns].apply(pd.to_numeric, errors='coerce')

    # Now sum and sort
    totals_by_category = filtered_df[category_columns].sum().sort_values(ascending=False)

    st.bar_chart(totals_by_category)

    # Trend over years
    st.subheader("Year-wise Total Vehicles")
    year_wise_totals = filtered_df.groupby("Year")["Total"].sum()
    st.line_chart(year_wise_totals)
