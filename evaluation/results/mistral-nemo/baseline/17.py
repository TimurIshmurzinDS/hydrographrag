import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Load data
data = pd.read_csv('tekes_river_water_discharge.csv')

# Create GeoDataFrame
geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Ensure the CRS is set to WGS84
gdf.crs = 'EPSG:4326'

# Initialize folium map centered on Tekes River
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# Add water discharge data to the map as a choropleth map
folium.Choropleth(
    geo_data=gdf,
    name='Water Discharge',
    data=data,
    columns=['latitude', 'longitude'],
    key_on='feature.properties.id',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.8,
    highlight=True
).add_to(m)

# Save the map as HTML file
m.save("17.html")