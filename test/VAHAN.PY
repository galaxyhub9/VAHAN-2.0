# DISPLAYS UPDATED UI OF (KP'S) + ADDED MAIN SECTION (completed)
# 4.3 - Fuel Category Analysis 
#4.4 - complete UI with all sections and styles
#completed fuel world
# 4.5- started the category vs manufacturer section
#4.5- completed the category vs manufacturer section + market insights ( but need to work on it more)
import itertools
import streamlit as st
import pandas as pd
import numpy as np
import calendar
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import textwrap
import streamlit.components.v1 as components


# Custom CSS for investor-grade styling with consistent pastel KPIs
st.markdown("""
<style>
    /* Global Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
        position: relative;
        z-index: 2;
    }
    
    /* Animated Car */
    .animated-car {
        position: absolute;
        top: 50%;
        left: -100px;
        transform: scaleX(-1) translateY(-50%) ;
        font-size: 9rem;
        z-index: 1;
        animation: carMove 1.0s ease-out forwards;
        pointer-events: none;

    }
    
    @keyframes carMove {
        0% {
            left: -100px;
            opacity: 1;
            transform: scaleX(-1) translateY(-50%) scale(1);
        }
        70% {
            opacity: 0.8;
            transform:scaleX(-1) translateY(-50%) scale(1.1);
        }
        100% {
            left: calc(100% - 200px);
            opacity: 0.2;
            transform: scaleX(-1) translateY(-50%) scale(1.1);
        }
    }
    
    @keyframes trailFade {
        0% { opacity: 0; }
        30% { opacity: 0.6; }
        100% { opacity: 0; }
    }
    
    /* Filter Section */
    .filter-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    .filter-title {
        color: #2c3e50;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Enhanced Consistent Pastel KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #faf7ff 0%, #f0f4ff 50%, #f7faff 100%);
        backdrop-filter: blur(10px);
        padding: 2rem 1.5rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 
            0 8px 32px rgba(139, 123, 255, 0.12),
            inset 0 1px 0 rgba(255,255,255,0.6);
        border: 1px solid rgba(139, 123, 255, 0.15);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        height: 180px;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        opacity: 0;
        transition: opacity 0.4s ease;
        border-radius: 25px;
        background: linear-gradient(135deg, #e8dcff 0%, #d4c5ff 50%, #c0b0ff 100%);
    }
    
    .kpi-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(139, 123, 255, 0.25),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    .kpi-card:hover::before {
        opacity: 1;
    }
    
    .kpi-icon {
        font-size: 2.0rem;
        margin-bottom: 0rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
        animation: floatIcon 3s ease-in-out infinite;
        color: #6b5ce7;
    }
    
    @keyframes floatIcon {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #4c3d87;
        margin: 0.5rem 0;
        line-height: 0;
        text-shadow: 0 2px 4px rgba(255,255,255,0.5);
        position: relative;
        z-index: 2;
    }
    
    .kpi-label {
        color: #5a4b8a;
        font-size: 1rem;
        font-weight: 600;
        margin: 0.5rem 0;
        position: relative;
        z-index: 2;
        letter-spacing: 0.5px;
    }
    
    .kpi-trend {
        font-weight: 700;
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        margin-top: 0.5rem;
        position: relative;
        z-index: 2;
        backdrop-filter: blur(5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .kpi-trend:hover {
        transform: scale(1.05);
    }
    
    .trend-positive {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.3) 100%);
        color: #15803d;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .trend-negative {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.3) 100%);
        color: #dc2626;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .trend-neutral {
        background: linear-gradient(135deg, rgba(107, 114, 128, 0.2) 0%, rgba(107, 114, 128, 0.3) 100%);
        color: #4b5563;
        border: 1px solid rgba(107, 114, 128, 0.3);
    }
    
    /* Market Intelligence Banner */
    .market-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .market-insight {
        font-size: 0.95rem;
        font-weight: 500;
        margin: 0;
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 0rem 0;
        border: none;
    }
    
    /* Investment Metrics Section */
    .investment-section {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .investment-title {
        color: #2d3436;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Shimmer effect for cards */
    .kpi-card::after {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.8), transparent);
        border-radius: 25px;
        opacity: 0;
        transition: opacity 0.6s ease;
        animation: shimmer 2s infinite;
        pointer-events: none;
    }
    
    .kpi-card:hover::after {
        opacity: 1;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title { font-size: 2rem; }
        .kpi-card { 
            height: auto; 
            padding: 1.5rem 1rem; 
            border-radius: 20px;
        }
        .kpi-value { font-size: 2rem; }
        .kpi-icon { font-size: 2.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# Page Configuration
st.set_page_config(
    layout="wide",
    page_title="Vehicle Market Intelligence",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

# Enhanced Header
st.markdown("""
<div class="main-header">
    <div class="animated-car" >🚗</div>
    <h1 class="main-title"  style="margin-bottom:0px;">VAHAN 2.0 DASHBOARD</h1>
    <p class="subtitle" style="margin-top:0px;">Vehicle Market Intelligence & Insights</p>
</div>
""", unsafe_allow_html=True)

# Load Excel data
@st.cache_data
def load_data():
    df_maker_category = pd.read_excel(
        "reportTable 2020 - 22.xlsx", engine="openpyxl")
    df_maker_category_raw = pd.read_excel(
        "reportTable 2020 - 22.xlsx", engine="openpyxl")
    df_category_month = pd.read_excel(
        "month wise v category 20-22.xlsx", engine="openpyxl")
    df_maker_month = pd.read_excel(
        "Maker Month Wise Data  20-22.xlsx", engine="openpyxl")
    df_fuel_category = pd.read_excel(
        "fuel Vehicle data 20-23.xlsx", engine="openpyxl")

    df_maker_category['Maker'] = df_maker_category['Maker'].astype(
        str).str.strip().str.replace('"', '').str.replace("'", '')

    return df_maker_category, df_maker_category_raw, df_category_month, df_maker_month, df_fuel_category


df_maker_category, df_maker_category_raw, df_category_month, df_maker_month, df_fuel_category = load_data()


def clean_dataframe(df):
    for col in df.columns:
        # Clean text columns
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].str.replace(
                '"', '', regex=False).str.replace("'", '', regex=False)
            # For Maker / Category / Fuel columns → uppercase
            if col.lower() in ['maker', 'vehicle category', 'fuel']:
                df[col] = df[col].str.upper()
            # Try to convert numeric-looking strings
            df[col] = df[col].replace({',': ''}, regex=True)
            try:
                # Only convert if all values can be converted to numeric
                numeric_series = pd.to_numeric(df[col])
                df[col] = numeric_series
            except (ValueError, TypeError):
                # Keep as string if conversion fails
                pass
    return df


# Apply to all
df_maker_category = clean_dataframe(df_maker_category)
df_category_month = clean_dataframe(df_category_month)
df_maker_month = clean_dataframe(df_maker_month)
df_fuel_category = clean_dataframe(df_fuel_category)

# Enhanced Filter Section
col1, col2, col3, col4 = st.columns([1, 2, 2, 1])

with col1:
    # 1. Year Filter (Single select)
    df_category_month ['Year'] = pd.to_numeric(
        df_category_month ['Year'], errors='coerce')
    years = sorted(df_category_month ['Year'].dropna().unique())
    selected_year = st.selectbox(
        "📅 Calender Year", years, help="Select reporting year for analysis")

with col2:
    # 2. Manufacturer Filter (Multi-select with only one default)
    df_maker_category['Maker'] = df_maker_category['Maker'].astype(
        str).str.strip().str.replace('"', '').str.replace("'", '')
    all_makers = sorted(df_maker_category['Maker'].dropna().unique())
    default_maker = "SURINDERA AGRO INSDUSTRIES"
    selected_maker = st.multiselect(
        "🏭 Manufacturer",
        all_makers,
        default=[default_maker],
        key="maker_multiselect",
        help="Select manufacturers for comparative analysis"
    )

with col3:
    # 3. Vehicle Category Filter (Multi-select with only one default)
    all_categories = sorted(
        df_category_month['Vehicle Category'].dropna().unique())
    default_category = "THREE WHEELER(T)"
    selected_category = st.multiselect(
        "🚗 Vehicle Segments",
        all_categories,
        default=[default_category],
        key="category_multiselect",
        help="Choose vehicle categories for market analysis"
    )

with col4:
    view_option = st.radio(
        "📈 Growth Metrics",
        ["YOY", "QOQ"],
        horizontal=True,
        help="Year-over-Year vs Quarter-over-Quarter analysis"
    )

# Investment Opportunity Section
st.markdown('<hr class="custom-divider" style="margin-top:2px;">', unsafe_allow_html=True)

# --- Helper: Human readable numbers ---
def human_format(num):
    if num >= 10_000_000:  # Crores
        return f"{num/10_000_000:.1f}Cr"
    elif num >= 100_000:   # Lakhs
        return f"{num/100_000:.1f}L"
    elif num >= 1_000:     # Thousands
        return f"{num/1_000:.1f}K"
    else:
        return str(int(num))


# --- Determine latest year ---
latest_year = int(df_maker_category['Year'].max())
prev_year = latest_year - 1

# Enhanced KPI Section with Pastel Colors
# Create five columns for KPIs
col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

# --- 1️⃣ Total Registrations ---
total_all_years = df_maker_category['Total'].sum()
total_latest = df_maker_category[df_maker_category['Year']
                                 == latest_year]['Total'].sum()
total_prev = df_maker_category[df_maker_category['Year']
                               == prev_year]['Total'].sum()
yoy_all = ((total_latest - total_prev) / total_prev * 100) if total_prev else 0

trend_class = "trend-positive" if yoy_all >= 0 else "trend-negative"
# trend_icon = "📈" if yoy_all >= 0 else "📉"

with col_kpi1:
    st.markdown(f"""
    <div class="kpi-card kpi-card-1">
        <div class="kpi-icon">🚗</div>
        <div class="kpi-value">{human_format(total_all_years)}</div>
        <div class="kpi-label">Total Market Volume</div>
        <div class="kpi-trend {trend_class}">
            {yoy_all:+.1f}% YoY
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2️⃣ EV Market Share ---
# Ensure 'Total' is numeric before doing calculations
df_fuel_category['Total'] = pd.to_numeric(df_fuel_category['Total'], errors='coerce').fillna(0)
df_fuel_category['Year'] = pd.to_numeric(df_fuel_category['Year'], errors='coerce')

ev_total_all = df_fuel_category[df_fuel_category['Fuel'].str.contains(
    "ELECTRIC", case=False, na=False)]['Total'].sum()
market_total_all = df_fuel_category['Total'].sum()
ev_share_all = (ev_total_all / market_total_all *
                100) if market_total_all else 0

ev_share_latest = df_fuel_category[(df_fuel_category['Year'] == latest_year) &
                                   (df_fuel_category['Fuel'].str.contains("ELECTRIC", case=False, na=False))]['Total'].sum() / \
    df_fuel_category[df_fuel_category['Year']
                     == latest_year]['Total'].sum() * 100

ev_share_prev = df_fuel_category[(df_fuel_category['Year'] == prev_year) &
                                 (df_fuel_category['Fuel'].str.contains("ELECTRIC", case=False, na=False))]['Total'].sum() / \
    df_fuel_category[df_fuel_category['Year']
                     == prev_year]['Total'].sum() * 100

ev_yoy_all = ev_share_latest - ev_share_prev
ev_trend_class = "trend-positive" if ev_yoy_all >= 0 else "trend-negative"
# ev_trend_icon = "⚡" if ev_yoy_all >= 0 else "🔋"

with col_kpi2:
    st.markdown(f"""
    <div class="kpi-card kpi-card-2">
        <div class="kpi-icon">⚡</div>
        <div class="kpi-value">{ev_share_all:.1f}%</div>
        <div class="kpi-label">EV Penetration Rate</div>
        <div class="kpi-trend {ev_trend_class}">
            {ev_yoy_all:+.1f}pp YoY
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3️⃣ Two-Wheeler Share ---
two_wheeler_all = df_category_month[df_category_month['Vehicle Category'].str.contains(
    "TWO WHEELER", case=False)]['Total'].sum()
market_all = df_category_month['Total'].sum()
two_share_all = (two_wheeler_all / market_all * 100) if market_all else 0

with col_kpi3:
    st.markdown(f"""
    <div class="kpi-card kpi-card-3">
        <div class="kpi-icon">🏍️</div>
        <div class="kpi-value">{two_share_all:.1f}%</div>
        <div class="kpi-label">2-Wheeler Dominance</div>
        <div class="kpi-trend trend-negative">
            -2.1% QoQ
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4️⃣ Fastest Growing Category ---
# Calculate totals for current and previous year
cat_curr_all = df_category_month[df_category_month['Year'] == latest_year] \
    .groupby('Vehicle Category')['Total'].sum()
cat_prev_all = df_category_month[df_category_month['Year'] == prev_year] \
    .groupby('Vehicle Category')['Total'].sum()

# Filter out small base categories (prev year < 20k)
min_base = 20000
valid_cats = cat_prev_all[cat_prev_all >= min_base].index

# Calculate % growth only for valid categories
cat_growth_all = ((cat_curr_all[valid_cats] - cat_prev_all[valid_cats]) /
                  cat_prev_all[valid_cats].replace(0, np.nan) * 100) \
    .sort_values(ascending=False)

# Get top growth category
top_cat_all = cat_growth_all.index[0]
top_growth_all = cat_growth_all.iloc[0]
top_trend_class = "trend-positive" if top_growth_all >= 0 else "trend-negative"


# Short form mapping
category_short_map = {
    "LIGHT PASSENGER VEHICLE": "LPV",
    "LIGHT MOTOR VEHICLE": "LMV",
    "HEAVY MOTOR VEHICLE": "HMV",
    "TWO WHEELER": "TW",
    "THREE WHEELER(T)": "3W(T)",
}

# Clean category string before lookup
top_cat_clean = top_cat_all.strip().upper()
top_cat_all = category_short_map.get(top_cat_clean, top_cat_all)  

with col_kpi4:
    st.markdown(f"""
    <div class="kpi-card kpi-card-4">
        <div class="kpi-icon">🚀</div>
        <div class="kpi-value">{top_cat_all}</div>
        <div class="kpi-label">Fastest Growing Segment</div>
        <div class="kpi-trend {top_trend_class}">
            {top_growth_all:+.1f}% YoY
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5️⃣ Top Manufacturer ---
maker_all = df_maker_category.groupby('Maker')['Total'].sum()
top_maker_all = maker_all.idxmax()
top_share_all = maker_all.max() / maker_all.sum() * 100

# Truncate long manufacturer names for display
display_maker = top_maker_all
with col_kpi5:
    st.markdown(f"""
    <div class="kpi-card kpi-card-5">
        <div class="kpi-icon">👑</div>
        <div class="kpi-value" style="font-size: 1.4rem;">{display_maker}</div>
        <div class="kpi-label">Market Leader</div>
        <div class="kpi-trend trend-positive">
            {top_share_all:.1f}% Share
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---- MAIN DASHBOARD LAYOUT ----
# Create two main columns: left for manufacturer growth, right for other content
main_left, main_middle, main_right = st.columns(
    [0.5, 0.5, 0.5])  # Left slightly smaller


with main_left:
    # ---- MANUFACTURER GROWTH SECTION (TOP-LEFT) ----
    st.markdown(
        '<h3 style="margin-top:5px">Manufacturer Growth</h3>',
        unsafe_allow_html=True
    )
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
    if view_option == "YOY":
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
                        f"<span title='{maker}' style='color:{color}; font-weight:bold; font-size:23px; cursor:pointer;'>{sign}{pct_change:.1f}%</span>")

                    # insights.append(f"<span style='color:{color}; font-weight:bold; font-size:23px;'>{sign}{pct_change:.1f}%</span>")

        growth_str = " | ".join(insights)

        st.markdown(
            f"<p style='color:#666; font-size:16px;'>Year-over-Year Growth: {growth_str}</p>",
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
                    # insights.append(f"<span style='color:{color}; font-weight:bold; font-size:23px;'>{sign}{pct_change:.1f}%</span>")
                    insights.append(
                        f"<span title='{maker}' style='color:{color}; font-weight:bold; font-size:23px; cursor:pointer;'>{sign}{pct_change:.1f}%</span>")

        growth_str = " | ".join(insights)

        st.markdown(
            f"<p style='color:#666; font-size:16px; margin-bottom:0px;'>Quarter-over-Quarter Growth {selected_year}: {growth_str}</p>",
            unsafe_allow_html=True
        )

        fig = px.line(df_qoq_grouped, x="Quarter_Label",
                      y="Registrations", color="Maker", markers=True,
                      title="")

    # Style the chart
    fig.update_layout(
        height=300,
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
    # st.markdown("### Vehicle Category Growth")
    st.markdown(
        '<h3 style="margin-top:5px">Vehicle Category Growth</h3>',
        unsafe_allow_html=True
    )

    # Step 1: Copy & Clean
    df = df_category_month.copy()
    df['Vehicle Category'] = df['Vehicle Category'].astype(str).str.strip()

    # Convert month values to numeric (if in thousands with commas)
    month_cols = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                  'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    def clean_and_convert(val):
        if isinstance(val, str):
            val = val.replace(",", "")
        try:
            return float(val)
        except:
            return 0  # fallback

    for col in month_cols:
        df[col] = df[col].apply(clean_and_convert)

    # Filter
    df_filtered = df[df['Vehicle Category'].isin(selected_category)].copy()

    # Step 2: Melt to Long Format
    df_long = df_filtered.melt(
        id_vars=['Vehicle Category', 'Year'],
        value_vars=month_cols,
        var_name='Month',
        value_name='Registrations'
    )

    # Step 3: Parse Dates
    month_map = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
                 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
    df_long['Month_Num'] = df_long['Month'].map(month_map)
    df_long['Date'] = pd.to_datetime(
        dict(year=df_long['Year'], month=df_long['Month_Num'], day=1))
    df_long['Quarter'] = df_long['Date'].dt.to_period('Q').astype(str)

    # Step 4: YOY or QOQ logic
    if view_option == "YOY":
        df_yoy = df_long.groupby(['Year', 'Vehicle Category'])[
            'Registrations'].sum().reset_index()
        df_yoy.sort_values(by=["Vehicle Category", "Year"], inplace=True)

        insights = []
        for cat in selected_category:
            df_c = df_yoy[df_yoy["Vehicle Category"] == cat]
            if len(df_c) >= 2:
                latest = df_c.iloc[-1]["Registrations"]
                prev = df_c.iloc[-2]["Registrations"]
                if prev != 0:
                    pct_change = ((latest - prev) / prev) * 100
                    color = "green" if pct_change >= 0 else "red"
                    sign = "+" if pct_change >= 0 else ""
                    # insights.append(f"<span style='color:{color}; font-weight:bold;font-size:23px'>{sign}{pct_change:.1f}%</span>")
                    insights.append(
                        f"<span title='{cat}' style='color:{color}; font-weight:bold; font-size:23px; cursor:pointer;'>{sign}{pct_change:.1f}%</span>")

        growth_str = " | ".join(insights)
        st.markdown(
            f"<p style='color:#666; font-size:16px;'>Year-over-Year Growth: {growth_str}</p>",
            unsafe_allow_html=True
        )

        fig = px.line(df_yoy, x="Year", y="Registrations",
                      color="Vehicle Category", markers=True,
                      )

    else:
        df_qoq = df_long[df_long['Year'] == selected_year].copy()
        df_qoq['Quarter_Label'] = df_qoq['Date'].dt.quarter.apply(
            lambda x: f"Q{x}")
        df_qoq_grouped = df_qoq.groupby(['Quarter_Label', 'Vehicle Category'])[
            'Registrations'].sum().reset_index()
        df_qoq_grouped.sort_values(
            by=["Vehicle Category", "Quarter_Label"], inplace=True)

        insights = []
        for cat in selected_category:
            df_c = df_qoq_grouped[df_qoq_grouped["Vehicle Category"] == cat]
            if len(df_c) >= 2:
                latest = df_c.iloc[-1]["Registrations"]
                prev = df_c.iloc[-2]["Registrations"]
                if prev != 0:
                    pct_change = ((latest - prev) / prev) * 100
                    color = "green" if pct_change >= 0 else "red"
                    sign = "+" if pct_change >= 0 else ""
                    # insights.append(f"<span style='color:{color}; font-weight:bold; font-size:23px'>{sign}{pct_change:.1f}%</span>")
                    insights.append(
                        f"<span title='{cat}' style='color:{color}; font-weight:bold; font-size:23px; cursor:pointer;'>{sign}{pct_change:.1f}%</span>")

        growth_str = " | ".join(insights)
        st.markdown(
            f"<p style='color:#666; font-size:16px;'> Quarter-over-Quarter Growth {selected_year}: {growth_str}</p>",
            unsafe_allow_html=True
        )

        fig = px.line(df_qoq_grouped, x="Quarter_Label", y="Registrations",
                      color="Vehicle Category", markers=True,
                      )

    # Step 5: Style and Show Chart
    fig.update_layout(
        height=300,
        xaxis_title="",
        yaxis_title="sales",
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


with main_right:

    df_total = df_maker_category_raw.copy()
    # ---- RIGHT SECTION: Top Manufacturers Market Share ----
    st.markdown(
        '<h3 style="margin-top:5px">Top Manufacturers Market Share</h3>',
        unsafe_allow_html=True
    )

    # Group and clean data
    df_market = df_total.groupby("Maker")["Total"].sum().reset_index()
    df_market["Total"] = df_market["Total"].str.replace(",", "").astype(float)

    # Calculate market share %
    df_market["Market Share (%)"] = (
        df_market["Total"] / df_market["Total"].sum()) * 100

    # Get Top 5 manufacturers
    df_market = df_market.sort_values(
        by="Market Share (%)", ascending=False).head(5)

    # Shorten names for x-axis (but keep full name in hover)
    df_market["Short Name"] = df_market["Maker"].apply(
        lambda x: x.split()[0][:6] + "..." if len(x) > 8 else x)

    # Create bar chart
    market_fig = px.bar(
        df_market,
        x="Short Name",
        y="Market Share (%)",
        color="Maker",  # Color by original Maker for legend consistency
        text="Market Share (%)",
        hover_name="Maker",  # Show full name on hover
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=335  # Taller chart
    )

    # Format chart
    market_fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        marker_line_width=1,
        marker_line_color='black'
    )

    market_fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title=None,
        xaxis_tickangle=0,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis_range=[0, df_market["Market Share (%)"].max() * 1.3],
        font=dict(size=13)
    )

    # Display chart
    st.plotly_chart(market_fig, use_container_width=True)



# ---- BOTTOM DASHBOARD LAYOUT ----
bottom_left, bottom_middle = st.columns(
    [1.5, 2])


def bottom_left_code():
    # st.set_page_config(page_title="Top 5 Fuels Market Share", layout="wide")
    st.markdown(
        "<h3 >Fuel World 🌍</h3>",
        unsafe_allow_html=True
    )

    # ---- Calculate Top 5 Fuels ----
    fuel_totals = (
        df_fuel_category.groupby("Fuel", as_index=False)["Total"]
        .sum()
        .sort_values(by="Total", ascending=False)
    )

    top_5_fuels = fuel_totals.head(5)
    total_market = top_5_fuels["Total"].sum()
    top_5_fuels["Market Share (%)"] = (
        top_5_fuels["Total"] / total_market
    ) * 100

    # ---- Tabs ----
    tab1, tab2 , tab3= st.tabs([
        "📊 Market Share",
        "⚡Performace Highlights",
        "💡Top 5"
        # "check"
    ])
    
    pastel = {
            "header_bg": "linear-gradient(135deg, #A8DADC, #F1FAEE)",
            "metric1": "linear-gradient(135deg, #B5EAD7, #C7CEEA)",
            "metric2": "linear-gradient(135deg, #B5EAD7, #C7CEEA)",
            "insight1": "#B5EAD7",
            "insight2": "#C7CEEA",
            "recommend_bg": "linear-gradient(135deg, #FFDAC1, #E2F0CB)",
            "takeaway_bg": "#F1FAEE"
        }

    # ================== TAB 1: PIE CHART ==================
    with tab1:
        # col1, col2 = st.columns([3, 2])

        # with col1:
        fig = px.pie(
            top_5_fuels,
            names="Fuel",
            values="Market Share (%)",
            # title="Market Share Distribution - Top 5 Fuels",
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Tealgrn
        )
        fig.update_traces(
            textinfo="percent+label",
            pull=[0.05] * len(top_5_fuels),
            textfont_size=12
        )
        st.plotly_chart(fig, use_container_width=False)

        # with col2:
        #     st.markdown("#### 🏆 Top 5 Quick Overview")
        #     for _, row in top_5_fuels.iterrows():
        #         st.markdown(
        #             f"""
        #             <div style='background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
        #                         padding: 15px; margin-bottom: 10px; border-radius: 10px;
        #                         color: white; font-size: 16px;'>
        #                 <b>{row['Fuel']}</b><br>
        #                 <span style='font-size:24px;'>{row['Market Share (%)']:.1f}%</span><br>
        #                 {row['Total']:,.0f} units
        #             </div>
        #             """,
        #             unsafe_allow_html=True
        #         )

  

    # ---- Calculate YoY Growth for Fuels ----
    def calculate_fuel_yoy_growth():
        # Get current year and previous year data
        current_year = df_fuel_category['Year'].max()
        previous_year = current_year - 1
        
        # Current year totals
        current_year_data = df_fuel_category[df_fuel_category['Year'] == current_year].groupby('Fuel')['Total'].sum().reset_index()
        current_year_data.rename(columns={'Total': 'Current_Total'}, inplace=True)
        
        # Previous year totals
        previous_year_data = df_fuel_category[df_fuel_category['Year'] == previous_year].groupby('Fuel')['Total'].sum().reset_index()
        previous_year_data.rename(columns={'Total': 'Previous_Total'}, inplace=True)
        
        # Merge and calculate YoY growth
        yoy_data = pd.merge(current_year_data, previous_year_data, on='Fuel', how='left')
        yoy_data['YoY_Growth'] = ((yoy_data['Current_Total'] - yoy_data['Previous_Total']) / yoy_data['Previous_Total'] * 100).round(1)
        
        return yoy_data

    # ---- Performance Classification Function ----
    def classify_performance(yoy_growth):
        if pd.isna(yoy_growth):
            return "N/A"
        elif yoy_growth >= 10:
            return "High"
        elif yoy_growth >= 0:
            return "Medium"
        else:
            return "Low"



    with tab2:
        market_leader = top_5_fuels.iloc[0]
        top2_control = top_5_fuels.iloc[0:2]['Market Share (%)'].sum()


                        # ====== Reusable Card ======
        def card(title, value, icon="", bg="#fff", subtitle=""):
            return f"""
            <div style="background:{bg}; padding:20px; border-radius:12px;
                        box-shadow:0 3px 8px rgba(0,0,0,0.05); text-align:center;">
                <div style="font-size:2rem; margin-bottom:8px;">{icon}</div>
                <div style="font-size:1.8rem; font-weight:1000; color:#2D3748;">{value}</div>
                <div style="color:#4A5568; font-size:1.2rem;">{title}</div>
                {f"<div style='color:#718096; font-size:1.0rem; margin-top:5px;'>{subtitle}</div>" if subtitle else ""}
            </div>
            """

        # ====== KPI Section ======
        col1, col2 = st.columns(2)
        col1.markdown(card("Market Leader", market_leader["Fuel"], "🏆", pastel["metric1"], 
                        f"{market_leader['Market Share (%)']:.1f}% share"), unsafe_allow_html=True)
        col2.markdown(card("Top 2 Control", f"{top2_control:.1f}%", "📈", pastel["metric2"], 
                        "Duopoly strength"), unsafe_allow_html=True)

        st.markdown('<hr class="custom-divider" style="margin-bottom:0px;">', unsafe_allow_html=True)


        st.markdown("""
            <div style='background: linear-gradient(135deg, #fbc2eb, #a6c1ee); padding: 10px; border-radius: 12px; 
                        margin-bottom: 10px; box-shadow: 0 3px 8px rgba(0,0,0,0.05); margin-top: 20px;'>
                <div style='display: flex; justify-content: space-between; align-items: center; 
                            padding: 10px; background:linear-gradient(135deg, #fbc2eb, #a6c1ee);
                            border-radius: 8px; margin-bottom: 0px;'>
                    <div style='flex: 1;'><strong style='color: #2D3748; align-items: left;'>Fuel Type</strong></div>
                    <div style='flex: 1; text-align: ;'><strong style='color: #2D3748;'>Market Share</strong></div>
                    <div style='flex: 1; text-align: center;'><strong style='color: #2D3748;'>YoY Growth</strong></div>
                    <div style='flex: 1; text-align: center;'><strong style='color: #2D3748;'>Performance</strong></div>
                </div>
        """, unsafe_allow_html=True)

        # --- Prepare Data ---
        fuel_yoy_data = calculate_fuel_yoy_growth()
        top_fuels_list = top_5_fuels['Fuel'].tolist()
        filtered_yoy_data = fuel_yoy_data[fuel_yoy_data['Fuel'].isin(top_fuels_list)]
        performance_table = pd.merge(
            top_5_fuels[['Fuel', 'Market Share (%)']],
            filtered_yoy_data[['Fuel', 'YoY_Growth']],
            on='Fuel',
            how='left'
        )
        performance_table['Performance'] = performance_table['YoY_Growth'].apply(classify_performance)

        # --- Row Rendering ---
        for _, row in performance_table.iterrows():
            market_share = f"{row['Market Share (%)']:.1f}%"
            yoy_growth = (
                f"+{row['YoY_Growth']:.1f}%" if pd.notna(row['YoY_Growth']) and row['YoY_Growth'] > 0
                else f"{row['YoY_Growth']:.1f}%" if pd.notna(row['YoY_Growth'])
                else "N/A"
            )
            performance = row['Performance']

            badge_color = {
                'High': ['#2F855A', '#C6F6D5'],    # Deep green text / light green bg
                'Medium': ['#975A16', '#FAF089'],  # Amber text / pale yellow bg
                'Low': ['#C53030', '#FED7D7']      # Red text / soft red bg
            }.get(performance, ['#4A5568', '#E2E8F0'])  # Default grey

            st.markdown(f"""
                <div style='background: #F7FAFC; padding: 10px; border-radius: 12px; 
                            margin-bottom: 1px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='flex: 1; font-size: 1.0rem; font-weight: 600; color: #2D3748;'>{row['Fuel']}</div>
                        <div style='flex: 1; text-align: center; font-size: 1.1rem; font-weight: 500; color: #2B6CB0;'>{market_share}</div>
                        <div style='flex: 1; text-align: center; font-size: 1.1rem; font-weight: 500; color: {"#2F855A" if "+" in yoy_growth else "#C53030"};'>{yoy_growth}</div>
                        <div style='flex: 1; text-align: center;'>
                            <div style='display: inline-block; padding: 4px 12px; border-radius: 12px; 
                                        background-color: {badge_color[1]}; color: {badge_color[0]}; 
                                        font-weight: 700; font-size: 0.9rem;'>
                                {performance}
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)



    # ================== TAB 2: INSIGHTS ==================
    with tab3:


 

        # ====== KPI Calculations ======
        market_leader = top_5_fuels.iloc[0]
        top2_control = top_5_fuels.head(2)["Market Share (%)"].sum()
        top5_dominance = top_5_fuels["Market Share (%)"].sum()
        leader_advantage = int(market_leader["Total"] - top_5_fuels.iloc[1]["Total"])
        avg_top5_share = top_5_fuels["Market Share (%)"].mean()
        remaining_market = 100 - top5_dominance
        market_gap = market_leader["Market Share (%)"] - top_5_fuels.iloc[1]["Market Share (%)"]

        # --- Vehicle category columns ---
        vehicle_cols = ["2WIC", "2WN", "2WT", "3WIC", "3WN", "3WT", 
                        "4WIC", "HGV", "HMV", "HPV", "LGV", "LMV", 
                        "LPV", "MGV", "MMV", "MPV", "OTH"]

        # --- Find top vehicle category for each fuel ---
        top_fuel_vehicle = []

        for fuel in top_5_fuels["Fuel"]:
            # Filter for the specific fuel
            fuel_data = df_fuel_category[df_fuel_category["Fuel"] == fuel].copy()

            # Ensure numeric for vehicle columns
            fuel_data[vehicle_cols] = fuel_data[vehicle_cols].apply(pd.to_numeric, errors='coerce')

            # Sum across all years for each vehicle category
            vehicle_sums = fuel_data[vehicle_cols].sum()

            # Drop NaNs just in case
            vehicle_sums = vehicle_sums.dropna()

            # If all NaNs, skip
            if vehicle_sums.empty:
                top_vehicle_cat = None
                top_vehicle_val = 0
            else:
                top_vehicle_cat = vehicle_sums.idxmax()
                top_vehicle_val = vehicle_sums.max()

            top_fuel_vehicle.append({
                "Fuel": fuel,
                "Top Vehicle Category": top_vehicle_cat,
                "Units": int(top_vehicle_val)
            })

        # --- Create DataFrame for display ---
        df_top_vehicle = pd.DataFrame(top_fuel_vehicle)

        # --- Merge with market share info ---
        result_table = top_5_fuels.merge(df_top_vehicle, on="Fuel")

        # --- Enhanced UI ---
        st.subheader("Which Wheels Drive the Fuels? ")

        html_content = """
        <style>
        .scroll-container {
            display: flex;
            overflow-x: auto;
            gap: 20px;
            padding: 40px 0;
            width: 100%;
            scrollbar-width: none; /* Firefox */
        }
        .scroll-container::-webkit-scrollbar {
            display: none; /* Chrome, Safari */
        }
        .card {
            flex: 0 0 auto;
            width: 340px;
            background: #ffffff;
            border-radius: 18px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
            transition: transform 0.25s ease;
            position: relative;
            font-family: 'Segoe UI', sans-serif;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .rank-badge {
            position: absolute;
            top: -30px;
            left: -0px;
            background: linear-gradient(135deg, #ff9a9e, #fad0c4);
            color: white;
            font-size: 20px;
            font-weight: 800;
            padding: 12px 18px;
            border-radius: 50%;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 18px;
            background: linear-gradient(135deg, #fdfbfb, #ebedee);
            border-top-left-radius: 18px;
            border-top-right-radius: 18px;
        }
        .card-header h3 {
            margin: 0;
            font-size: 22px;
            font-weight: 800;
            color: #333;
        }
        .card-header span {
            font-size: 20px;
            font-weight: 800;
            color: #444;
        }
        .card-header small {
            display: block;
            font-size: 12px;
            color: #666;
        }
        .card-body {
            padding: 20px;
            background-color: #fafafa;
            border-bottom-left-radius: 18px;
            border-bottom-right-radius: 18px;
        }
        .vehicle-category {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, #d4fc79, #96e6a1);
            border-radius: 12px;
            padding: 12px 16px;
            margin-top: 12px;
        }
        .vehicle-category h4 {
            margin: 0;
            font-size: 16px;
            font-weight: 800;
            color: #2c3e50;
        }
        .vehicle-category small {
            display: block;
            font-size: 12px;
            color: #555;
        }
        .vehicle-category span {
            font-size: 18px;
            font-weight: 800;
            color: #2c3e50;
        }
        </style>
        <div class="scroll-container">
        """

        # Format number to show in Crore / Lakh / Thousand
        def format_units(value):
            if value >= 1e7:
                return f"{value/1e7:.2f} Cr"
            elif value >= 1e5:
                return f"{value/1e5:.2f} L"
            elif value >= 1e3:
                return f"{value/1e3:.1f}K"
            else:
                return str(int(value))

        for idx, row in result_table.iterrows():
            html_content += f"""
            <div class="card">
                <div class="rank-badge">#{idx+1}</div>
                <div class="card-header" style="background: linear-gradient(135deg, #a1c4fd, #c2e9fb);">
                    <div>
                        <h3>{row['Fuel']}</h3>
                        <small>Fuel Type</small>
                    </div>
                    <div style="text-align:right;">
                        <span>{row['Market Share (%)']:.1f}%</span>
                        <small>Market Share</small>
                    </div>
                </div>
                <div class="card-body">
                    <div class="vehicle-category" style="background: linear-gradient(135deg, #fbc2eb, #a6c1ee);">
                        <div>
                            <h4>{row['Top Vehicle Category']}</h4>
                            <small>Dominant Vehicle Category</small>
                        </div>
                        <span>{format_units(row['Units'])}</span>
                    </div>
                </div>
            </div>
            """

        html_content += "</div>"

        components.html(html_content, height=420, scrolling=True)




with bottom_left:
    bottom_left_code()

with bottom_middle:
    
 

    # --- Prepare data ---
    year_df = df_maker_category[df_maker_category['Year'] == int(selected_year)].copy()
    exclude_cols = ['S No', 'Maker', 'Year', 'Total']
    category_cols = [col for col in year_df.columns if col not in exclude_cols]
    year_df = clean_dataframe(year_df)
    year_df[category_cols] = year_df[category_cols].apply(pd.to_numeric, errors='coerce')
    category_totals = year_df[category_cols].sum().sort_values(ascending=False)
    top_5 = category_totals.head(5).reset_index()
    top_5.columns = ['Vehicle Category', 'Total Units Sold']

    # Calculate total market for percentage calculation
    total_market = top_5['Total Units Sold'].sum()

    top_makers = []
    for category in top_5['Vehicle Category']:
        top_row = year_df.loc[year_df[category].idxmax()]
        top_makers.append({
            'Vehicle Category': category,
            'Top Maker': top_row['Maker'],
            'Units Sold': int(top_row[category])
        })

    top_makers_df = pd.DataFrame(top_makers)
    merged_df = top_5.merge(top_makers_df, on='Vehicle Category')

    # Add category share calculation
    merged_df['Category Share (%)'] = (merged_df['Total Units Sold'] / total_market * 100).round(1)

    # --- Redesigned Modern Category Cards ---
    st.markdown(
        '<h3 style="margin-bottom:0px">Top Vehicle Category & Manufacturer</h3>',
        unsafe_allow_html=True
    )
    st.markdown('<hr class="custom-divider" style="margin-top:40px; margin-bottom:0px; background: #">', unsafe_allow_html=True)

    html_content = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .cards-container {
        display: flex;
        overflow-x: auto;
        gap: 24px;
        padding: 24px 8px;
        scrollbar-width: none;
        -ms-overflow-style: none;  

    }

    .cards-container::-webkit-scrollbar { 
        display: none;
    }

    .cards-container::-webkit-scrollbar-track { 
        background: rgba(139, 123, 255, 0.1);
        border-radius: 10px;
    }

    .cards-container::-webkit-scrollbar-thumb { 
        background: rgba(139, 123, 255, 0.3);
        border-radius: 10px;
        transition: background 0.3s ease;
    }

    .cards-container::-webkit-scrollbar-thumb:hover { 
        background: rgba(139, 123, 255, 0.5);
    }

    .category-card {
        flex: 0 0 auto;
        width: 300px;
        background: linear-gradient(135deg, #faf7ff 0%, #f0f4ff 50%, #f7faff 100%);
        border-radius: 28px;
        box-shadow: 
            0 12px 40px rgba(139, 123, 255, 0.15),
            inset 0 1px 0 rgba(255,255,255,0.6);
        border: 1px solid rgba(139, 123, 255, 0.12);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        padding: 18px 20px;
        overflow: hidden;
    }

    .category-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #e8dcff 0%, #d4c5ff 50%, #c0b0ff 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
        border-radius: 28px;
        z-index: 1;
    }

    .category-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 
            0 25px 80px rgba(139, 123, 255, 0.25),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }

    .category-card:hover::before {
        opacity: 1;
    }

    .category-card > * {
        position: relative;
        z-index: 2;
    }

    .rank-badge {
        position: absolute;
        top: -1px;
        left: 1px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        font-weight: 800;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        z-index: 3;
        border: 3px solid white;
    }

    .category-icon {
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, #6b5ce7 0%, #8b7cf6 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(107, 92, 231, 0.3);
    }

    .category-name {
        font-size: 25px;
        font-weight: 700;
        color: #1e1b4b;
        margin: 0 0 8px 0;
        line-height: 1.2;
        letter-spacing: -0.5px;
        text-align: center;
    }

    .category-subtitle {
        font-size: 14px;
        color: #6b5ce7;
        margin: 0 0 24px 0;
        font-weight: 500;
        opacity: 0.8;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-bottom: 24px;
    }

    .stat-item {
        background: rgba(255, 255, 255, 0.7);
        padding: 10px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.5);
        transition: all 0.3s ease;
    }

    .stat-item:hover {
        background: rgba(255, 255, 255, 0.9);
        transform: translateY(-2px);
    }

    .stat-value {
        font-size: 20px;
        font-weight: 500;
        color: #1e1b4b;
        margin: 0 0 4px 0;
        line-height: 1;
    }

    .stat-label {
        font-size: 12px;
        color: #6b7280;
        font-weight: 500;
        text-transform: capitalize;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    .leader-section {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.6);
    }

    .leader-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }

    .leader-title {
        font-size: 12px;
        color: #6b7280;
        font-weight: 600;
        text-transform: Captitalize;
        letter-spacing: 0.5px;
        margin: 0;
    }

    .crown-icon {
        width: 50px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .leader-name {
        font-size: 18px;
        font-weight: 600;
        color: #1e1b4b;
        margin: 0 0 2px 0;
        line-height: 1.2;
    }

    .leader-stats {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .leader-units {
        font-size: 16px;
        font-weight: 700;
        color: #059669;
        margin: 0;
    }

    .leader-dominance {
        font-size: 14px;
        font-weight: 600;
        color: #6b5ce7;
        background: rgba(107, 92, 231, 0.1);
        padding: 6px 12px;
        border-radius: 20px;
        margin: 0;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .category-card {
            width: 300px;
            padding: 24px 20px;
        }
        
        .category-name {
            font-size: 20px;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
            gap: 12px;
        }
    }

    /* Animation keyframes */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .category-card {
        animation: slideIn 0.6s ease-out forwards;
    }

    .category-card:nth-child(2) { animation-delay: 0.1s; }
    .category-card:nth-child(3) { animation-delay: 0.2s; }
    .category-card:nth-child(4) { animation-delay: 0.3s; }
    .category-card:nth-child(5) { animation-delay: 0.4s; }
    </style>

    <div class="cards-container">
    """

    def format_units(n):
        if n >= 1e7: 
            return f"{n/1e7:.1f} Cr"
        elif n >= 1e5: 
            return f"{n/1e5:.1f} L"
        elif n >= 1e3: 
            return f"{n/1e3:.0f}K"
        return f"{n:,.0f}"



    for i, row in merged_df.iterrows():
        dominance = (row['Units Sold'] / row['Total Units Sold']) * 100
        # icon = category_icons.get(row['Vehicle Category'].upper(), category_icons['default'])
        
        html_content += f"""
        <div class="category-card">
            <div class="rank-badge">#{i+1}</div>
            
            
            <div class="category-name">{row['Vehicle Category']}
                    <div class="leader-title">Top Vehicle</div>
            </div>
             
              
            
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{format_units(row['Total Units Sold'])}
                    <div class="stat-label">Total Units</div>
                </div>
                    
                </div>
                <div class="stat-item">
                    <div class="stat-value">{row['Category Share (%)']:.1f}%</div>
                    <div class="stat-label">Market Share</div>
                </div>
            </div>
            
            <div class="leader-section">

                <div class="leader-name">{row['Top Maker'][:28]}{'...' if len(row['Top Maker'])>28 else ''}</div>
                <div class="leader-header">
                    <div class="leader-title">Dominant Manufacturer</div>
                </div>
                <div class="leader-stats">
                    <div class="leader-units">{format_units(row['Units Sold'])} units</div>
                    <div class="leader-dominance">{dominance:.1f}% dominance</div>
                </div>
            </div>
        </div>
        """

    html_content += "</div>"

    components.html(html_content, height=460, scrolling=True)
    
    





# Copy original data
df = df_maker_category.copy()
df_fuel = df_fuel_category.copy()

# --- Preprocess Data ---
exclude_cols = ['S No', 'Maker', 'Year', 'Total']
vehicle_cols = [col for col in df.columns if col not in exclude_cols]

# Ensure numeric
df[vehicle_cols + ['Total']] = df[vehicle_cols + ['Total']].apply(pd.to_numeric, errors='coerce')
df_fuel[vehicle_cols + ['Total']] = df_fuel[vehicle_cols + ['Total']].apply(pd.to_numeric, errors='coerce')

# --- 1. Electric Vehicles Growth ---
ev_fuel_rows = df_fuel[df_fuel['Fuel'].str.contains('ELECTRIC', case=False)]
ev_per_year = ev_fuel_rows.groupby('Year')[vehicle_cols].sum().sum(axis=1)
ev_growth = ((ev_per_year.iloc[-1] - ev_per_year.iloc[-2]) / ev_per_year.iloc[-2]) * 100 if len(ev_per_year) > 1 else 0

# --- 2. Top Manufacturer in 2-Wheelers ---
two_wheelers_cols = ['2WIC', '2WN', '2WT']
maker_2w_totals = df.groupby('Maker')[two_wheelers_cols].sum().sum(axis=1)
top_maker = maker_2w_totals.idxmax()
top_maker_share = (maker_2w_totals.max() / maker_2w_totals.sum()) * 100

# Identify new/emerging players
maker_year_total = df.groupby(['Maker', 'Year'])[vehicle_cols].sum().sum(axis=1).unstack(fill_value=0)
this_year = maker_year_total.columns[-1]

# Filter makers that were not present last year
previous_year = maker_year_total.columns[-2]
new_players = maker_year_total[(maker_year_total[previous_year] == 0) & (maker_year_total[this_year] > 1000)][this_year]

# Pick top emerging player based on absolute units
if not new_players.empty:
    top_emerging_maker = new_players.sort_values(ascending=False).head(1)
    name = top_emerging_maker.index[0]
    units = int(top_emerging_maker.iloc[0])
    insight = f"**{name}** entered the market with {units:,} units this year, making a strong entry in the commercial vehicle space."
    print(insight)
else:
    insight = "No major new entrants this year."


# --- 4. Diesel Decline ---
# --- Diesel Decline Insight (Pure Diesel Only) ---

# Filter only rows where Fuel column contains exactly 'DIESEL'
diesel_rows = df_fuel[df_fuel['Fuel'].str.upper() == 'DIESEL']

# Group by Year and sum total registrations
diesel_per_year = diesel_rows.groupby('Year')['Total'].sum().sort_index()

# Calculate Year-over-Year change safely
if len(diesel_per_year) > 1:
    last_year = diesel_per_year.index[-2]
    this_year = diesel_per_year.index[-1]
    diesel_change = ((diesel_per_year[this_year] - diesel_per_year[last_year]) / diesel_per_year[last_year]) * 100
else:
    diesel_change = 0

# Add + or - sign
sign = "+" if diesel_change >= 0 else "-"
diesel_change_str = f"{sign}{abs(diesel_change):.1f}%"


# --- 5. Heavy Vehicles Growth (HGV + HMV) ---
df['Heavy Vehicles'] = df['HGV'] + df['HMV']
hv_per_year = df.groupby('Year')['Heavy Vehicles'].sum()
hv_growth = ((hv_per_year.iloc[-1] - hv_per_year.iloc[-2]) / hv_per_year.iloc[-2]) * 100 if len(hv_per_year) > 1 else 0

# --- Display Insights ---
insights = [
    f"🚗 EVs Are on Fire\nRegistrations soared {ev_growth:.1f}% YoY—prime time to invest in EV startups, battery tech, and charging infra.",
    f"🏍️ {top_maker} Holds the Throne\nWith {top_maker_share:.1f}% in 2-wheelers, {top_maker} stays dominant—stable, high-volume, and trusted.",
    f"⚡ {name} Makes a Bold Entry\nDebuts with {units:,} units—strong momentum in the commercial EV space.",
    f"🛢️ Diesel Isn’t Done Yet\nRegistrations rose {diesel_change_str} YoY—still holding ground as cleaner tech gains pace.",
    f"🚚 Heavy Vehicles on the Move\nHGV & HMV up {hv_growth:.1f}% YoY—driven by infrastructure and logistics boom."
]


for insight in insights:
    print(insight + "\n")
    



# --- Generate enhanced HTML for investment insights ---
html_content = """
<style>
/* Container */
.insight-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 12px 0;
}

/* Card */
.insight-card {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    padding: 22px 28px;
    background: linear-gradient(135deg, #f9f9ff 0%, #eef2ff 100%);
    border-radius: 22px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-left: 6px solid #667eea;
    margin-bottom: 0px;
}
.insight-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.15);
}

/* Number Badge */
.insight-number {
    font-size: 28px;
    font-weight: 800;
    color: white;
    min-width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    flex-shrink: 0;
}

/* Text section */
.insight-text {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.insight-title {
    font-size: 18px;
    font-weight: 700;
    color: #1e1b4b;
}
.insight-detail {
    font-size: 15px;
    color: #333;
    line-height: 1.6;
}

/* Highlight key numbers inside detail */
.insight-detail span {
    font-weight: 700;
    color: #4f46e5;
}

/* Responsive */
@media (max-width: 768px) {
    .insight-card {
        flex-direction: column;
        align-items: flex-start;
        border-left: none;
        border-top: 6px solid #667eea;
    }
    .insight-number {
        margin-bottom: 12px;
    }
}
</style>
<div class="insight-container">
"""
st.markdown(
        "<h3 style='margin:0px' >💰Investment Insights</h3>",
        unsafe_allow_html=True
    )
# --- Add each insight safely with highlighted numbers ---
for i, insight in enumerate(insights, start=1):
    parts = insight.split('\n', 1)  # Split at first newline only
    title = parts[0]
    detail = parts[1] if len(parts) > 1 else ""
    
    # Highlight numbers in the detail text
    import re
    detail = re.sub(r'([\d,.]+%?)', r'<span>\1</span>', detail)
    
    html_content += f"""
    <div class="insight-card">
        <div class="insight-number">{i}</div>
        <div class="insight-text">
            <div class="insight-title">{title}</div>
            <div class="insight-detail">{detail}</div>
        </div>
    </div>
    """

html_content += "</div>"

# --- Render using components ---
components.html(html_content, height=700, scrolling=True)



#  footer
st.markdown('<hr class="custom-divider" style="margin-top:0px; padding:0px">', unsafe_allow_html=True)
simple_footer = """
<div style="text-align: center; margin-top: 0px; padding-top: 20px; font-size: 14px;">
    Data Period: <strong>2020 - 2022</strong> | © 2024 Dashboard | Source: <a href="https://vahan.parivahan.gov.in/" style="color: #3b82f6;">VAHAN Dashboard</a>
</div>
"""

st.markdown(simple_footer, unsafe_allow_html=True)
