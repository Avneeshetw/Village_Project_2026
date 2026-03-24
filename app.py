import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("📍 Village Live Map - Lucknow")

@st.cache_data
def load_data():
    # Shapefile aur Excel load ho rahi hai
    gdf = gpd.read_file("Franchise_village_Mar2026.shp")
    df = pd.read_excel("Distributor & Spoke Location 2026.xlsx")
    
    # Dono ko join karne ka logic (V_ID common column hona chahiye)
    # Agar column ka naam alag hai toh yahan change karein
    merged = gdf.merge(df, on="V_ID") 
    return merged

try:
    data = load_data()
    # Map Lucknow par set hai
    m = folium.Map(location=[26.8467, 80.9462], zoom_start=10)
    
    folium.Choropleth(
        geo_data=data,
        name="Status",
        data=data,
        columns=["V_ID", "Target_Value"], # Excel ka column name yahan aayega
        key_on="feature.properties.V_ID",
        fill_color="YlOrRd",
        legend_name="Sales Scale"
    ).add_to(m)

    st_folium(m, width="100%", height=600)
except Exception as e:
    st.error(f"Error: {e}")