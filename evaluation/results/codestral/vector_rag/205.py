import geopandas as gpd
import folium
from shapely import wkt
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map
m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Load the data about snow melt and river flow
data = pd.read_csv('data/snow_melt_river_flow.csv')

# Perform Granger causality test to determine if there is a relationship between snow melt dates and river flow
grangercausalitytests(data[['Snow Melt Date', 'River Flow']], maxlag=12)

# Save the final map
m.save("205.html")