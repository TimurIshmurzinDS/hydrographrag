import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Hardcoded list of dictionaries containing Coordinates (WKT) for Karaoy River posts
posts = [
    {"name": "Post 1", "geometry": wkt.loads("POINT(74.5639 -38.0176)")},
    {"name": "Post 2", "geometry": wkt.loads("POINT(74.5712 -38.0243)")}
]

# Add posts to the map using folium.Marker
for post in posts:
    folium.Marker(location=post['geometry'].coords[:], popup=post['name']).add_to(m)

# Save the final map
m.save("82.html")