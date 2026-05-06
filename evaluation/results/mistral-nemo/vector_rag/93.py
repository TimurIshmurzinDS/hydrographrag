import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize map using centroid of the shapefile
m = folium.Map(location=gdf.centroid, tiles='CartoDB positron')

# Add basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of dictionaries for coordinates (WKT)
rivers = [
    {'name': 'Каратал', 'length_km': 150},
    {'name': 'Коктал', 'length_km': 100},
    {'name': 'Байанкол', 'length_km': 150}
]

# Calculate total length of tributaries
total_length = sum(r['length_km'] for r in rivers if r['name'] != 'Каратал')

# Save the final map
m.save("93.html")