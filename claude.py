import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Vehicle Registration Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .filter-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(uploaded_file):
    """Load and process the Excel data"""
    try:
        # Read all sheets from the Excel file
        excel_file = pd.ExcelFile(uploaded_file)
        
        # Initialize empty list to store data from all sheets
        all_data = []
        
        # Process each sheet
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            
            # Clean column names
            df.columns = df.columns.astype(str).str.strip()
            
            # Find the manufacturer column (assuming it's column B or contains 'Maker')
            manufacturer_col = None
            for col in df.columns:
                if 'maker' in col.lower() or df.columns.get_loc(col) == 1:  # Column B is index 1
                    manufacturer_col = col
                    break
            
            if manufacturer_col is None:
                manufacturer_col = df.columns[1]  # Default to second column
            
            # Vehicle category columns (excluding manufacturer, year, total)
            vehicle_categories = ['2WN', '2WT', '3WN', '3WT', '3WH', 'LMV', 'HMV', 'LGV', 'LMV', 'LPV', 'MCV', 'MMV', 'MPV', 'OTH']
            
            # Find actual vehicle category columns in the data
            available_categories = []
            for cat in vehicle_categories:
                matching_cols = [col for col in df.columns if cat in str(col).upper()]
                if matching_cols:
                    available_categories.extend(matching_cols)
            
            # If no matching categories found, use columns between manufacturer and year/total
            if not available_categories:
                start_idx = df.columns.get_loc(manufacturer_col) + 1
                end_idx = len(df.columns) - 2  # Exclude last two columns (Year, Total)
                available_categories = df.columns[start_idx:end_idx].tolist()
            
            # Find year and total columns
            year_col = None
            total_col = None
            
            for col in df.columns:
                if 'year' in str(col).lower():
                    year_col = col
                elif 'total' in str(col).lower():
                    total_col = col
            
            # If not found, assume last two columns
            if year_col is None:
                year_col = df.columns[-2]
            if total_col is None:
                total_col = df.columns[-1]
            
            # Clean the data
            df = df.dropna(subset=[manufacturer_col])
            df = df[df[manufacturer_col].str.strip() != '']
            
            # Convert numeric columns
            numeric_cols = available_categories + [total_col]
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Add year information if not present
            if year_col not in df.columns or df[year_col].isna().all():
                # Extract year from sheet name or use a default
                if any(str(year) in sheet_name for year in ['2020', '2021', '2022', '2023']):
                    sheet_year = [year for year in ['2020', '2021', '2022', '2023'] if str(year) in sheet_name][0]
                    df[year_col] = int(sheet_year)
                else:
                    st.warning(f"Could not determine year for sheet: {sheet_name}")
                    continue
            
            # Select relevant columns
            relevant_cols = [manufacturer_col] + available_categories + [year_col, total_col]
            relevant_cols = [col for col in relevant_cols if col in df.columns]
            df_clean = df[relevant_cols].copy()
            
            # Rename columns for consistency
            column_mapping = {manufacturer_col: 'Manufacturer', year_col: 'Year', total_col: 'Total'}
            df_clean = df_clean.rename(columns=column_mapping)
            
            all_data.append(df_clean)
        
        # Combine all data
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            return combined_data, available_categories
        else:
            st.error("No valid data found in the Excel file")
            return None, None
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

def calculate_growth(df, groupby_cols, value_col, period_type='year'):
    """Calculate growth rates"""
    if period_type == 'year':
        df_grouped = df.groupby(groupby_cols + ['Year'])[value_col].sum().reset_index()
        df_grouped = df_grouped.sort_values(groupby_cols + ['Year'])
        df_grouped['Growth'] = df_grouped.groupby(groupby_cols)[value_col].pct_change() * 100
        df_grouped['Absolute_Growth'] = df_grouped.groupby(groupby_cols)[value_col].diff()
    
    return df_grouped

def create_trend_chart(df, x_col, y_col, color_col=None, title="Trend Analysis"):
    """Create trend line chart"""
    if color_col:
        fig = px.line(df, x=x_col, y=y_col, color=color_col, 
                     title=title, markers=True)
    else:
        fig = px.line(df, x=x_col, y=y_col, title=title, markers=True)
    
    fig.update_layout(
        height=400,
        showlegend=True,
        hovermode='x unified'
    )
    return fig

def create_bar_chart(df, x_col, y_col, color_col=None, title="Bar Chart"):
    """Create bar chart"""
    if color_col:
        fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=title)
    else:
        fig = px.bar(df, x=x_col, y=y_col, title=title)
    
    fig.update_layout(height=400)
    return fig

def main():
    # Main header
    st.markdown('<h1 class="main-header">🚗 Vehicle Registration Dashboard</h1>', unsafe_allow_html=True)
    
    # File upload
    st.sidebar.markdown('<div class="filter-header">📁 Upload Data</div>', unsafe_allow_html=True)
    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel file", 
        type=['xlsx', 'xls'],
        help="Upload your vehicle registration Excel file"
    )
    
    if uploaded_file is not None:
        # Load data
        with st.spinner("Loading data..."):
            data, vehicle_categories = load_data(uploaded_file)
        
        if data is not None:
            st.success("✅ Data loaded successfully!")
            
            # Display data info
            st.sidebar.markdown('<div class="filter-header">📊 Data Overview</div>', unsafe_allow_html=True)
            st.sidebar.info(f"""
            **Records**: {len(data):,}  
            **Manufacturers**: {data['Manufacturer'].nunique():,}  
            **Years**: {sorted(data['Year'].unique())}  
            **Vehicle Categories**: {len(vehicle_categories)}
            """)
            
            # Filters
            st.sidebar.markdown('<div class="filter-header">🔍 Filters</div>', unsafe_allow_html=True)
            
            # Year range filter
            available_years = sorted(data['Year'].unique())
            year_range = st.sidebar.select_slider(
                "Select Year Range",
                options=available_years,
                value=(min(available_years), max(available_years))
            )
            
            # Vehicle category filter
            selected_categories = st.sidebar.multiselect(
                "Select Vehicle Categories",
                options=vehicle_categories,
                default=vehicle_categories[:5] if len(vehicle_categories) > 5 else vehicle_categories
            )
            
            # Manufacturer filter
            top_manufacturers = data.groupby('Manufacturer')['Total'].sum().nlargest(20).index.tolist()
            selected_manufacturers = st.sidebar.multiselect(
                "Select Manufacturers",
                options=sorted(data['Manufacturer'].unique()),
                default=top_manufacturers[:10],
                help="Select specific manufacturers (default: top 10 by total registrations)"
            )
            
            # Filter data
            filtered_data = data[
                (data['Year'] >= year_range[0]) & 
                (data['Year'] <= year_range[1]) &
                (data['Manufacturer'].isin(selected_manufacturers) if selected_manufacturers else True)
            ].copy()
            
            if filtered_data.empty:
                st.warning("No data available for selected filters.")
                return
            
            # Main dashboard
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_registrations = filtered_data['Total'].sum()
                st.metric("Total Registrations", f"{total_registrations:,}")
            
            with col2:
                avg_per_year = filtered_data.groupby('Year')['Total'].sum().mean()
                st.metric("Avg Registrations/Year", f"{avg_per_year:,.0f}")
            
            with col3:
                total_manufacturers = filtered_data['Manufacturer'].nunique()
                st.metric("Total Manufacturers", f"{total_manufacturers:,}")
            
            with col4:
                latest_year = filtered_data['Year'].max()
                latest_total = filtered_data[filtered_data['Year'] == latest_year]['Total'].sum()
                st.metric(f"{latest_year} Registrations", f"{latest_total:,}")
            
            # Tabs for different analyses
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Year-over-Year Analysis", "📊 Category Analysis", "🏭 Manufacturer Analysis", "📋 Data Table"])
            
            with tab1:
                st.subheader("Year-over-Year Growth Analysis")
                
                # Overall YoY growth
                col1, col2 = st.columns(2)
                
                with col1:
                    # Total registrations by year
                    yearly_total = filtered_data.groupby('Year')['Total'].sum().reset_index()
                    yearly_total['YoY_Growth'] = yearly_total['Total'].pct_change() * 100
                    yearly_total['Absolute_Growth'] = yearly_total['Total'].diff()
                    
                    fig_yoy = create_trend_chart(
                        yearly_total, 'Year', 'Total', 
                        title="Total Vehicle Registrations (Year-over-Year)"
                    )
                    st.plotly_chart(fig_yoy, use_container_width=True)
                
                with col2:
                    # YoY Growth Rate
                    fig_growth = create_bar_chart(
                        yearly_total[yearly_total['YoY_Growth'].notna()], 
                        'Year', 'YoY_Growth',
                        title="Year-over-Year Growth Rate (%)"
                    )
                    st.plotly_chart(fig_growth, use_container_width=True)
                
                # Growth table
                st.subheader("Growth Summary")
                growth_summary = yearly_total[['Year', 'Total', 'YoY_Growth', 'Absolute_Growth']].copy()
                growth_summary['YoY_Growth'] = growth_summary['YoY_Growth'].round(2)
                growth_summary['Absolute_Growth'] = growth_summary['Absolute_Growth'].fillna(0).astype(int)
                st.dataframe(growth_summary, use_container_width=True)
            
            with tab2:
                st.subheader("Vehicle Category Analysis")
                
                if selected_categories:
                    # Category-wise analysis
                    category_data = filtered_data[selected_categories + ['Year', 'Manufacturer']].copy()
                    category_yearly = category_data.groupby('Year')[selected_categories].sum().reset_index()
                    
                    # Melt data for plotting
                    category_melted = category_yearly.melt(
                        id_vars=['Year'], 
                        value_vars=selected_categories,
                        var_name='Category', 
                        value_name='Registrations'
                    )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Category trends
                        fig_cat_trend = px.line(
                            category_melted, x='Year', y='Registrations', color='Category',
                            title="Category-wise Registration Trends", markers=True
                        )
                        fig_cat_trend.update_layout(height=400)
                        st.plotly_chart(fig_cat_trend, use_container_width=True)
                    
                    with col2:
                        # Category distribution (latest year)
                        latest_year_data = category_yearly[category_yearly['Year'] == category_yearly['Year'].max()]
                        latest_melted = latest_year_data.melt(
                            id_vars=['Year'], 
                            value_vars=selected_categories,
                            var_name='Category', 
                            value_name='Registrations'
                        )
                        
                        fig_pie = px.pie(
                            latest_melted, values='Registrations', names='Category',
                            title=f"Category Distribution ({latest_year_data['Year'].iloc[0]})"
                        )
                        fig_pie.update_layout(height=400)
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    # Category growth analysis
                    st.subheader("Category Growth Analysis")
                    category_growth = category_yearly.copy()
                    for cat in selected_categories:
                        category_growth[f'{cat}_Growth'] = category_growth[cat].pct_change() * 100
                    
                    growth_cols = [col for col in category_growth.columns if '_Growth' in col]
                    if growth_cols:
                        growth_display = category_growth[['Year'] + growth_cols].dropna()
                        st.dataframe(growth_display.round(2), use_container_width=True)
                else:
                    st.warning("Please select at least one vehicle category.")
            
            with tab3:
                st.subheader("Manufacturer Analysis")
                
                if selected_manufacturers:
                    # Top manufacturers by total registrations
                    mfg_total = filtered_data.groupby('Manufacturer')['Total'].sum().nlargest(10).reset_index()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig_mfg_bar = create_bar_chart(
                            mfg_total, 'Total', 'Manufacturer',
                            title="Top 10 Manufacturers (Total Registrations)"
                        )
                        fig_mfg_bar.update_layout(height=500)
                        st.plotly_chart(fig_mfg_bar, use_container_width=True)
                    
                    with col2:
                        # Manufacturer trends over years
                        top_5_mfg = mfg_total.head(5)['Manufacturer'].tolist()
                        mfg_yearly = filtered_data[filtered_data['Manufacturer'].isin(top_5_mfg)].groupby(['Year', 'Manufacturer'])['Total'].sum().reset_index()
                        
                        fig_mfg_trend = create_trend_chart(
                            mfg_yearly, 'Year', 'Total', 'Manufacturer',
                            title="Top 5 Manufacturers - Yearly Trends"
                        )
                        fig_mfg_trend.update_layout(height=500)
                        st.plotly_chart(fig_mfg_trend, use_container_width=True)
                    
                    # Manufacturer growth analysis
                    st.subheader("Manufacturer Growth Analysis")
                    mfg_growth_data = []
                    
                    for mfg in top_5_mfg:
                        mfg_data = filtered_data[filtered_data['Manufacturer'] == mfg].groupby('Year')['Total'].sum().reset_index()
                        mfg_data['YoY_Growth'] = mfg_data['Total'].pct_change() * 100
                        mfg_data['Manufacturer'] = mfg
                        mfg_growth_data.append(mfg_data)
                    
                    if mfg_growth_data:
                        combined_growth = pd.concat(mfg_growth_data, ignore_index=True)
                        growth_pivot = combined_growth.pivot(index='Year', columns='Manufacturer', values='YoY_Growth')
                        st.dataframe(growth_pivot.round(2), use_container_width=True)
                else:
                    st.warning("Please select at least one manufacturer.")
            
            with tab4:
                st.subheader("Data Table")
                
                # Display options
                col1, col2 = st.columns(2)
                with col1:
                    show_all = st.checkbox("Show all data", value=False)
                with col2:
                    records_to_show = st.number_input("Records to display", min_value=10, max_value=1000, value=100)
                
                # Display data
                display_data = filtered_data if show_all else filtered_data.head(records_to_show)
                st.dataframe(display_data, use_container_width=True)
                
                # Download option
                csv = filtered_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download Filtered Data as CSV",
                    data=csv,
                    file_name=f"vehicle_registrations_{year_range[0]}_{year_range[1]}.csv",
                    mime="text/csv"
                )
        
        else:
            st.error("Failed to load data. Please check your Excel file format.")
    
    else:
        st.info("👆 Please upload your Excel file to get started.")
        
        # Sample data format info
        st.markdown("""
        ### 📋 Expected Data Format
        
        Your Excel file should contain:
        - **Column B**: Manufacturer names
        - **Vehicle Category Columns**: 2WN, 2WT, 3WN, 3WT, 3WH, LMV, HMV, etc.
        - **Year Column**: Year information
        - **Total Column**: Total registrations per manufacturer
        
        The dashboard will automatically detect and process multiple sheets/years in your Excel file.
        """)

if __name__ == "__main__":
    main()