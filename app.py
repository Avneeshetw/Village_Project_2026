import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import plotly.express as px

st.set_page_config(page_title="DBR Live Dashboard", layout="wide")

st.title("📂 Strategic Business Dashboard")

# 1. Shapefile Load logic
@st.cache_data
def load_map():
    try:
        gdf = gpd.read_file("Franchise_village_Mar2026.shp")
        if gdf.crs is not None and not gdf.crs.is_geographic:
            gdf = gdf.to_crs(epsg=4326)
        gdf.columns = gdf.columns.str.strip() # Spaces hatane ke liye
        return gdf
    except:
        return None

gdf = load_map()

# 2. File Uploader
uploaded_file = st.sidebar.file_uploader("Upload Excel", type=['xlsx', 'csv'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    # Dashboard Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Rows", len(df))
    
    # Auto-find numeric columns for charts
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    left, right = st.columns([1.5, 1])

    with left:
        st.subheader("📍 DBR Coverage Map")
        # Yahan hum check kar rahe hain ki 'DBR_Area' column dono jagah hai ya nahi
        if gdf is not None and 'DBR_Area' in df.columns:
            # Merge logic with fillna to avoid TypeError
            merged = gdf.merge(df, on="DBR_Area", how="left")
            merged = merged.fillna(0) 
            
            m = folium.Map(location=[26.8467, 80.9462], zoom_start=9)
            
            # Agar koi number column mil jaye toh use rangne ke liye use karein
            color_col = num_cols[0] if num_cols else None
            
            if color_col:
                folium.Choropleth(
                    geo_data=merged,
                    data=merged,
                    columns=["DBR_Area", color_col],
                    key_on="feature.properties.DBR_Area",
                    fill_color="YlOrRd",
                    nan_fill_color="white",
                    legend_name=f"Scale: {color_col}"
                ).add_to(m)
            
            folium.GeoJson(merged, tooltip=folium.GeoJsonTooltip(fields=["DBR_Area"])).add_to(m)
            st_folium(m, width="100%", height=500)
        else:
            st.warning("Excel mein 'DBR_Area' naam ka column hona zaroori hai.")

    with right:
        st.subheader("📊 Data Insights")
        if num_cols:
            fig = px.bar(df, x=df.columns[0], y=num_cols[0], title="Quick Comparison")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("📑 Data Preview")
    st.dataframe(df.head(10))

else:
    st.info("👈 Dashboard shuru karne ke liye Excel upload karein.")