import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
import numpy as np
import folium

# Load data
dtm = rasterio.open('dtm.tif')
river = gpd.read_file('river.shp')
sources = gpd.read_file('sources.shp')

# Define flood zones using flood fill operation
def flood_fill(dtm, river):
    # TODO: Implement flood fill operation using DTM and river data

# Calculate risk for each zone
def calculate_risk(zone):
    # TODO: Implement risk calculation based on historical data or other methods

# Load zones of interest (e.g., populated areas)
zones = gpd.read_file('zones.shp')

# Create map
m = folium.Map(location=[river.centroid.y.mean(), river.centroid.x.mean()], zoom_start=12)

# Add DTM data to the map
folium.raster_layers.TileLayer(
    tiles='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attr='Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
    name='Open Street Map'
).add_to(m)

# Add river data to the map
folium.GeoJson(
    river.to_json(),
    style_function=lambda x: {'fillColor': 'blue', 'color': 'black'},
    highlight_function=lambda x: folium.GeoJsonHighlight(style_function=lambda x: {'fillColor': 'yellow'}),
).add_to(m)

# Add sources of flooding to the map
folium.GeoJson(
    sources.to_json(),
    style_function=lambda x: {'fillColor': 'red', 'color': 'black'},
    highlight_function=lambda x: folium.GeoJsonHighlight(style_function=lambda x: {'fillColor': 'yellow'}),
).add_to(m)

# Add zones of interest to the map with risk information
for _, zone in zones.iterrows():
    risk = calculate_risk(zone)
    folium.GeoJson(
        zone.to_json(),
        style_function=lambda x: {'fillColor': '#{:02x}{:02x}{:02x}'.format(int(risk * 255), int((1 - risk) * 255), 0), 'color': 'black'},
        highlight_function=lambda x: folium.GeoJsonHighlight(style_function=lambda x: {'fillColor': '#{:02x}{:02x}{:02x}'.format(255, int((1 - risk) * 255), 0)}),
    ).add_to(m)

# Save the map
m.save("23.html")