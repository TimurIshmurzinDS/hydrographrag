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

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
hydro_posts = [
    {'name': 'Tokyraun River Hydro Post 1', 'wkt': 'POINT(74.56 -3.21)', 'water_consumption': 100, 'water_level': 5},
    {'name': 'Tokyraun River Hydro Post 2', 'wkt': 'POINT(74.89 -3.45)', 'water_consumption': 150, 'water_level': 6},
    # Add more hydro posts as needed
]

# Convert WKT to Shapely points and add them to the map
for post in hydro_posts:
    point = wkt.loads(post['wkt'])
    folium.Marker(location=tuple(point.coords), popup=f"{post['name']}\nWater Consumption: {post['water_consumption']} m³/s\nWater Level: {post['water_level']}").add_to(m)

# Save the final map
m.save("84.html")