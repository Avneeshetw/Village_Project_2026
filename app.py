import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import plotly.express as px

st.set_page_config(page_title="Dynamic Business Dashboard", layout="wide")

# Title and Sidebar
st.title("📂 Automated Business Intelligence Dashboard")
st.sidebar.header("Configuration")

# 1. File Uploader in Sidebar
uploaded_file = st.sidebar.file_uploader("Upload your Excel file", type=['xlsx', 'csv'])

# 2. Shapefile Load (Local folder se)
@st.cache_data
def load_map():
    try:
        gdf = gpd.read_file("Franchise_village_Mar2026.shp")
        if gdf.crs is not None and not gdf.crs.is_geographic:
            gdf = gdf.to_crs(epsg=4326)
        return gdf
    except:
        return None

gdf = load_map()

if uploaded_file is not None:
    # Data Reading
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean Column Names
    df.columns = df.columns.str.strip()

    # --- KPI ROW ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", len(df))
    
    # Dynamics Metrics (Agar columns exist karte hain)
    if 'Population' in df.columns:
        col2.metric("Total Population", f"{df['Population'].sum():,}")
    if 'Volume_This_Year' in df.columns:
        col3.metric("Current Volume", f"{df['Volume_This_Year'].sum():,}")
    
    st.divider()

    # --- MAP & CHART SECTION ---
    left, right = st.columns([1.5, 1])

    with left:
        st.subheader("📍 Real-time Area Map")
        if gdf is not None and 'DBR_Area' in df.columns:
            merged = gdf.merge(df, on="DBR_Area")
            m = folium.Map(location=[26.8467, 80.9462], zoom_start=9)
            
            folium.Choropleth(
                geo_data=merged,
                data=merged,
                columns=["DBR_Area", df.columns[1]], # Second column for coloring
                key_on="feature.properties.DBR_Area",
                fill_color="YlOrRd",
                legend_name="Data Intensity"
            ).add_to(m)
            st_folium(m, width="100%", height=500)
        else:
            st.info("Shapefile aur Excel join karne ke liye 'DBR_Area' column zaroori hai.")

    with right:
        st.subheader("📊 Data Visualizer")
        # User dynamic chart choose kar sakta hai
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            y_axis = st.selectbox("Select metric for Chart", numeric_cols)
            fig = px.bar(df, x=df.columns[0], y=y_axis, color=y_axis, 
                         title=f"{y_axis} by {df.columns[0]}")
            st.plotly_chart(fig, use_container_width=True)

    # --- FULL DATA TABLE ---
    st.subheader("📑 Preview Uploaded Data")
    st.dataframe(df, use_container_width=True)

else:
    st.info("👈 Dashboard dekhne ke liye sidebar se Excel file upload karein.")
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)