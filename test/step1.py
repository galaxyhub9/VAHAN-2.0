import streamlit as st
import pandas as pd
import numpy as np
import calendar
import plotly.express as px

# Page Configuration
st.set_page_config(
    layout="wide", page_title="Vehicle Dashboard", page_icon="🚗")

st.title("Vehicle Registration Dashboard (2020–2022)")

# Load Excel data
@st.cache_data
def load_data():
    df_maker_category = pd.read_excel(
        "reportTable 2020 - 22.xlsx", engine="openpyxl")
    df_category_month = pd.read_excel(
        "month wise v category 20-22.xlsx", engine="openpyxl")
    df_maker_month = pd.read_excel(
        "Maker Month Wise Data  20-22.xlsx", engine="openpyxl")

    df_maker_category['Maker'] = df_maker_category['Maker'].astype(
        str).str.strip().str.replace('"', '').str.replace("'", '')

    return df_maker_category, df_category_month, df_maker_month

df_maker_category, df_category_month, df_maker_month = load_data()

# ---- FILTERS ROW ----
st.markdown("## 🔍 Filter Options")
col1, col2, col3, col4 = st.columns([1, 2.5, 2.5, 1])

with col1:
    # 1. Year Filter (Single select)
    years = sorted(df_maker_category['Year'].dropna().unique())
    selected_year = st.selectbox("📅 Select Year", years)

with col2:
    # 2. Manufacturer Filter (Multi-select with only one default)
    all_makers = sorted(df_maker_category['Maker'].dropna().unique())
    default_maker = "SURINDERA AGRO INSDUSTRIES"  # Default to first in list
    selected_maker = st.multiselect(
        "🏭 Select Manufacturer(s)",
        all_makers,
        default=[default_maker],
        key="maker_multiselect"
    )

with col3:
    # 3. Vehicle Category Filter (Multi-select with only one default)
    all_categories = sorted(
        df_category_month['Vehicle Category'].dropna().unique())
    default_category = all_categories[0]
    selected_category = st.multiselect(
        "🚗 Select Vehicle Category(s)",
        all_categories,
        default=[default_category],
        key="category_multiselect"
    )
    
with col4:
    view_option = st.radio(
        "📈 View Growth By:", ["Year-over-Year", "Quarter-over-Quarter"], horizontal=False)

# Add some space after filters
st.markdown("---")

# ---- MAIN DASHBOARD LAYOUT ----
# Create two main columns: left for manufacturer growth, right for other content
main_left, main_middle, main_right = st.columns([1, 1,1])  # Left slightly smaller


with main_left:
    st.markdown("### 🚗 Total Vehicle Overview")

    # --- TOP CARD (Total + YoY) ---
    df_total = df_maker_category.copy()
    df_total['Maker'] = df_total['Maker'].str.strip()

    current_year_total = df_total[
        (df_total['Year'] == selected_year) & 
        (df_total['Maker'].isin(selected_maker))
    ]['Total'].sum()

    prev_year_total = df_total[
        (df_total['Year'] == selected_year - 1) & 
        (df_total['Maker'].isin(selected_maker))
    ]['Total'].sum()

    if prev_year_total != 0:
        pct_change = ((float(current_year_total) - float(prev_year_total)) / float(prev_year_total)) * 100
    else:
        pct_change = 0.0

    pct_color = "green" if pct_change >= 0 else "red"
    sign = "+" if pct_change >= 0 else ""

    current_year_total = float(current_year_total or 0)
    formatted_total = f"{current_year_total/1_000_000:.1f}M" if current_year_total >= 1_000_000 else f"{int(current_year_total):,}"

    st.markdown(f"""
        <div style="padding:25px; border-radius:15px; background-color:#f5f5f5;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom:25px;">
            <h2 style="margin:0; color:#223354;">{formatted_total}</h2>
            <p style="margin:0; color:#555;">Total Vehicles (YTD)</p>
            <p style="margin:5px 0 0; color:{pct_color}; font-weight:bold;">
                🔼 {sign}{pct_change:.1f}% YoY
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- NEW BLOCK: TOP 5 MANUFACTURERS BY MARKET SHARE ---
    st.markdown("#### 🏭 Top Manufacturers - Market Share")

    df_market = df_total[
        (df_total['Year'] == selected_year) &
        (df_total['Maker'].isin(selected_maker))
    ].groupby("Maker")["Total"].sum().reset_index()

    df_market["Market Share (%)"] = (df_market["Total"].astype(float) / df_market["Total"].astype(float).sum()) * 100
    df_market = df_market.sort_values(by="Market Share (%)", ascending=False).head(5)

    market_fig = px.bar(
        df_market,
        x="Maker", y="Market Share (%)",
        color="Maker",
        text="Market Share (%)",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=350
    )
    market_fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    market_fig.update_layout(
        showlegend=False,
        xaxis_title="",
        yaxis_title="Market Share %",
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis_range=[0, df_market["Market Share (%)"].max() * 1.3]
    )

    st.plotly_chart(market_fig, use_container_width=True)



with main_right:
    # ---- MANUFACTURER GROWTH SECTION (TOP-LEFT) ----
    st.markdown("### 📈 Manufacturer Growth Analysis")

    # Process data for manufacturer growth
    df = df_maker_month.copy()
    selected_makers = selected_maker

    # Filter only selected makers
    df_filtered = df[df['Maker'].isin(selected_makers)].copy()
    df_filtered['Maker'] = df_filtered['Maker'].str.strip().str.replace("'", "")

    # Convert wide monthly format to long format
    month_cols = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                  'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    df_long = df_filtered.melt(
        id_vars=['Maker', 'Year'],
        value_vars=month_cols,
        var_name='Month',
        value_name='Registrations'
    )

    # Convert month names to datetime
    month_map = {
        'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
        'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
    }
    df_long['Month_Num'] = df_long['Month'].map(month_map)
    df_long['Date'] = pd.to_datetime(
        dict(year=df_long['Year'], month=df_long['Month_Num'], day=1))

    # Create Quarter column
    df_long['Quarter'] = df_long['Date'].dt.to_period('Q').astype(str)

    # Display growth chart based on selected view
    if view_option == "Year-over-Year":
        df_yoy = df_long.groupby(['Year', 'Maker'])[
            'Registrations'].sum().reset_index()
        df_yoy.sort_values(by=["Maker", "Year"], inplace=True)

        # Calculate % growth
        insights = []
        for maker in selected_maker:
            df_m = df_yoy[df_yoy["Maker"] == maker]
            if len(df_m) >= 2:
                latest = df_m.iloc[-1]["Registrations"]
                prev = df_m.iloc[-2]["Registrations"]
                if prev != 0:
                    pct_change = ((latest - prev) / prev) * 100
                    color = "green" if pct_change >= 0 else "red"
                    sign = "+" if pct_change >= 0 else ""
                    insights.append(
                        f"<span style='color:{color}; font-weight:bold;'>{sign}{pct_change:.1f}%</span>")

        growth_str = " | ".join(insights)

        st.markdown(
            f"<p style='color:#666; font-size:16px; margin-bottom:15px;'>Year-over-Year Growth: {growth_str}</p>",
            unsafe_allow_html=True
        )

        fig = px.line(df_yoy, x="Year", y="Registrations",
                    color="Maker", markers=True,
                    title="")
        
    else:  # Quarter-over-Quarter
        df_qoq = df_long[df_long['Year'] == selected_year].copy()
        df_qoq['Quarter_Label'] = df_qoq['Date'].dt.quarter.apply(
            lambda x: f"Q{x}")
        df_qoq_grouped = df_qoq.groupby(['Quarter_Label', 'Maker'])[
            'Registrations'].sum().reset_index()
        df_qoq_grouped.sort_values(by=["Maker", "Quarter_Label"], inplace=True)

        # Calculate QoQ % change
        insights = []
        for maker in selected_maker:
            df_m = df_qoq_grouped[df_qoq_grouped["Maker"] == maker]
            if len(df_m) >= 2:
                latest = df_m.iloc[-1]["Registrations"]
                prev = df_m.iloc[-2]["Registrations"]
                if prev != 0:
                    pct_change = ((latest - prev) / prev) * 100
                    color = "green" if pct_change >= 0 else "red"
                    sign = "+" if pct_change >= 0 else ""
                    insights.append(
                        f"<span style='color:{color}; font-weight:bold;'>{sign}{pct_change:.1f}%</span>")

        growth_str = " | ".join(insights)

        st.markdown(
            f"<p style='color:#666; font-size:16px; margin-bottom:15px;'>Quarter-over-Quarter Growth ({selected_year}): {growth_str}</p>",
            unsafe_allow_html=True
        )

        fig = px.line(df_qoq_grouped, x="Quarter_Label",
                    y="Registrations", color="Maker", markers=True,
                    title="")

    # Style the chart
    fig.update_layout(
        height=400,
        xaxis_title="",
        yaxis_title="Registrations",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with main_middle:
    # ---- RIGHT SIDE CONTENT ----
    # You can add other dashboard components here
    st.markdown("### 📊 Additional Analytics")
    
    # Placeholder for other charts/components
    st.markdown(
        """
        <div style="padding:20px; border:2px solid #e0e0e0; border-radius:15px; 
                   box-shadow: 0 4px 12px rgba(0,0,0,0.1); background-color: #fafafa; 
                   height:450px; display:flex; align-items:center; justify-content:center;">
            <p style="color:#999; font-size:18px;">Space for additional charts and analytics</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- BOTTOM SECTION FOR MORE COMPONENTS ----
st.markdown("---")
st.markdown("### 📈 Additional Dashboard Components")

# You can add more rows of components here
bottom_col1, bottom_col2 = st.columns(2)

with bottom_col1:
    st.markdown(
        """
        <div style="padding:20px; border:2px solid #e0e0e0; border-radius:15px; 
                   box-shadow: 0 4px 12px rgba(0,0,0,0.1); background-color: #fafafa; 
                   height:300px; display:flex; align-items:center; justify-content:center;">
            <p style="color:#999; font-size:16px;">Category Analysis</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with bottom_col2:
    st.markdown(
        """
        <div style="padding:20px; border:2px solid #e0e0e0; border-radius:15px; 
                   box-shadow: 0 4px 12px rgba(0,0,0,0.1); background-color: #fafafa; 
                   height:300px; display:flex; align-items:center; justify-content:center;">
            <p style="color:#999; font-size:16px;">Monthly Trends</p>
        </div>
        """,
        unsafe_allow_html=True
    )