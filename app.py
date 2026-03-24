import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("📍 Village Live Map - Lucknow")

@st.cache_data
def load_data():
    # 1. Shapefile load karein
    gdf = gpd.read_file("Franchise_village_Mar2026.shp")
    
    # 2. Excel load karein
    df = pd.read_excel("Distributor & Spoke Location 2026.xlsx")
    
    # Data Cleaning: Column names se extra space hatayein
    gdf.columns = gdf.columns.str.strip()
    df.columns = df.columns.str.strip()
    
    # 3. 'DBR_Area' column ka use karke join karein
    merged = gdf.merge(df, on="DBR_Area") 
    return merged

try:
    data = load_data()
    
    # Map ka center (Lucknow coordinates)
    m = folium.Map(location=[26.8467, 80.9462], zoom_start=9)
    
    # Map par data dikhana (Choropleth)
    folium.Choropleth(
        geo_data=data,
        name="Sales Status",
        data=data,
        columns=["DBR_Area", "Target"], # Yahan 'Target' ki jagah Excel ka sales column name likhein
        key_on="feature.properties.DBR_Area",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Performance Scale"
    ).add_to(m)

    # Tooltip: Jab mouse map par le jayein toh naam dikhe
    folium.GeoJson(
        data,
        tooltip=folium.GeoJsonTooltip(fields=["DBR_Area"], aliases=["Area Name:"])
    ).add_to(m)

    st_folium(m, width="100%", height=600)
    
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Check karein ki Excel aur Shapefile dono mein 'DBR_Area' column ki spelling same hai.")