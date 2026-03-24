import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.plugins import LocateControl
import random

st.set_page_config(layout="wide")
st.title("📍 DBR Area Coverage Map - Lucknow")

@st.cache_data
def load_data():
    try:
        # Shapefile load karein
        gdf = gpd.read_file("Franchise_village_Mar2026.shp")
        if gdf.crs is not None and not gdf.crs.is_geographic:
            gdf = gdf.to_crs(epsg=4326)
        return gdf
    except Exception as e:
        st.error(f"Error loading Shapefile: {e}")
        return None

gdf = load_data()

if gdf is not None:
    # Lucknow center par map
    m = folium.Map(location=[26.8467, 80.9462], zoom_start=9)

    # Har DBR ko alag color dene ke liye function
    def style_func(feature):
        # DBR_Area ke naam ke hisaab se random color generate karna
        seed = sum(ord(c) for c in str(feature['properties'].get('DBR_Area', '')))
        random.seed(seed)
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        return {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.5,
        }

    # Boundaries add karein
    folium.GeoJson(
        gdf,
        style_function=style_func,
        tooltip=folium.GeoJsonTooltip(fields=["DBR_Area"], aliases=["DBR Area Name:"])
    ).add_to(m)

    # Mobile Live Location Button
    LocateControl(auto_start=False).add_to(m)

    # Map display
    st_folium(m, width="100%", height=600)
else:
    st.warning("Data load nahi ho paya. Files check karein.")