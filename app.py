import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import random

st.set_page_config(layout="wide")
st.title("📍 DBR Area Coverage Map - Lucknow")

# Cache data taaki map jaldi load ho
@st.cache_data
def load_and_preprocess_shp():
    # Shapefile load karein
    try:
        gdf = gpd.read_file("Franchise_village_Mar2026.shp")
        
        # CRS handle karein (WGS84 lat/lon standard)
        if gdf.crs is not None and not gdf.crs.is_geographic:
            gdf = gdf.to_crs(epsg=4326)
            
        return gdf
    except Exception as e:
        st.error(f"Error loading Shapefile: {e}")
        return None

# Function: Har DBR ko random color dena
def get_color(feature):
    # 'DBR_Area' ke upar logic base karein
    area_name = feature['properties']['DBR_Area']
    if area_name:
        return 'green' if 'Lucknow' in area_name else 'blue' # Bas ek placeholder logice, niche ise final karte hain
    return 'grey'

# Main app logic
gdf = load_and_preprocess_shp()

if gdf is not None:
    # 1. Map ka center (Lucknow coordinates)
    m = folium.Map(location=[26.8467, 80.9462], zoom_start=9)

    # 2. Polygon Boundaries banana with random colors
    def my_style_function(feature):
        return {
            'fillColor': 'green', # Default color
            'color': 'blue', # Border color
            'weight': 1.5,
            'fillOpacity': 0.6,
        }
    
    # 3. GeoJson setup, jisme har area par naam dikhe
    folium.GeoJson(
        gdf,
        name='DBR Coverage Map',
        style_function=my_style_function,
        tooltip=folium.GeoJsonTooltip(fields=["DBR_Area"], aliases=["Area Name:"]),
    ).add_to(m)

    # 4. Mobile mein "Locate Me" button integrate karna
    folium.plugins.LocateControl(auto_start=True).add_to(m)

    # 5. Map ko display karna
    st_folium(m, width="100%", height=600)
    
except Exception as e:
    st.error(f"Main map generation error: {e}")