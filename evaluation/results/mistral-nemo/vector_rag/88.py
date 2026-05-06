import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(gdf.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    gdf,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Hardcoded list of dictionaries containing coordinates (WKT) and water level data for Koktal River posts
posts_data = [
    {"wkt": "POINT(71.5438 -48.6917)", "water_level_cm": 120, "date_water_level_value": "2022-03-15"},
    {"wkt": "POINT(71.6543 -48.7234)", "water_level_cm": 115, "date_water_level_value": "2022-03-15"},
    # Add more posts data as needed
]

# Create a GeoDataFrame from the posts_data list and add it to the map
gdf_posts = gpd.GeoDataFrame(posts_data, geometry=[wkt.loads(p['wkt']) for p in posts_data])
folium.GeoJson(
    gdf_posts,
    style_function=lambda x: {'color': 'blue', 'weight': 2},
).add_to(m)

# Save the final map
m.save("88.html")