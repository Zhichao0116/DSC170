import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
import io

# Set Streamlit page
st.set_page_config(layout="wide")
st.title("Jordan Soviet")

gdf = gpd.read_file("dataset/Soviet/layer_0.shp")
generate_map = st.button("Generate Map")
if generate_map:
    with st.spinner("Generating map..."):
        m = gdf.explore()
        folium_static(m, width=800, height=600)
        st.subheader("Generated GeoDataFrame")
        gdf['geometry'] = gdf['geometry'].astype(str)
        st.dataframe(gdf, width=1300)