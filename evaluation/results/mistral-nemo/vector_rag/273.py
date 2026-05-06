import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[gdf.centroid.y.mean(), gdf.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=gdf,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
rivers = [
    {"name": "Karatal River", "wkt": "LINESTRING(...)"},  # Replace ... with actual WKT coordinates
    {"name": "Koktal River", "wkt": "LINESTRING(...)"},
    {"name": "Bayankol River", "wkt": "LINESTRING(...)"},
    {"name": "Karaoy River", "wkt": "LINESTRING(...)"},
    {"name": "Karkara River", "wkt": "LINESTRING(...)"}
]

# Add rivers to the map
for river in rivers:
    folium.GeoJson(
        data=[river],
        style_function=lambda x: {'color': 'blue', 'weight': 2},
    ).add_to(m)

# Save the final map
m.save("273.html")