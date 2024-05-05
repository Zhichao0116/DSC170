import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
import io

# Set Streamlit page
st.set_page_config(layout="wide")
st.title("Jordan Standardized Precipitation Index")

def load_data(csv_path):
    data = pd.read_csv(csv_path)
    return data

# Function to create map
def create_map(gdf, selected_column, tooltips):
    gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf.Longitude, gdf.Latitude))
    gdf.crs = "EPSG:4326"
    
    m = gdf.explore(
        column=selected_column,  
        cmap="Blues",
        scheme="FisherJenks",
        tiles="CartoDB dark_matter",
        tooltip=tooltips,
        popup=True,
        k=6,
        highlight=True,
        width="100%",
        legend_kwds={"caption": f"{selected_column} Statistics"},
        style_kwds={'radius': 8}
    )
    return m

# Main data loading
df = load_data("170/SPI_JMD_data_corrected_long_format.csv")

# Time selector
time_options = list(df['Time'].unique())
time_options.insert(0, 'all')
selected_time = st.selectbox('Select Time:', time_options)

# Filter data based on selected time
if selected_time != 'all':
    df_filtered = df[df['Time'] == selected_time]
else:
    df_filtered = df
st.subheader("Map Display:")
map_column = st.selectbox('Select a column to map:', df_filtered.columns)
tooltip_options = st.multiselect('Point Information:', df_filtered.columns)

map_gdf = create_map(df_filtered, map_column, tooltip_options)
folium_static(map_gdf, width=800, height=600)

# Display filtered data
st.subheader("Filtered Results:")
st.dataframe(df_filtered)

# Group and attribute selectors
group_by_attribute = st.selectbox('Group By Attribute:', df.columns)
calc_attribute = st.selectbox('Calculate Attribute:', df.columns)

# Calculate statistics
if st.button('Calculate Statistics'):
    aggregation_functions = {
        calc_attribute: ['max', 'min', 'mean'],
        'Latitude': 'first',
        'Longitude': 'first'
    }
    grouped_df = df.groupby(group_by_attribute).agg(aggregation_functions).reset_index()
    grouped_df.columns = [col[0] if col[-1] == '' or col[-1] == 'first' else '_'.join(col) for col in grouped_df.columns.values]
    st.dataframe(grouped_df)

    # Map related selectors
    map_column = st.selectbox('Select a column to map:', grouped_df.columns)
    tooltip_options = st.multiselect('Point Information:', grouped_df.columns)