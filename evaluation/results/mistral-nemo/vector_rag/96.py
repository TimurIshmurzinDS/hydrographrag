import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=gdf.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT)
hydro_features = [
    {'name': 'Urzhar River', 'wkt': 'POINT(74.56 51.34)', 'type': 'HY_HydroFeature'},
    {'name': 'Dos River', 'wkt': 'POINT(74.89 51.22)', 'type': 'HY_HydroFeature'}
]

# Create Shapely points from WKT
points = [wkt.loads(hf['wkt']) for hf in hydro_features]

# Calculate distance between Urzhar River and Dos River
distance = points[0].distance(points[1])

# Print the distance
print(f"Расстояние между реками Уржар и Дос составляет {distance:.2f} километров.")

# Save the final map
m.save("96.html")