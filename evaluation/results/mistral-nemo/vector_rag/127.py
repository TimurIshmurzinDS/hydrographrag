import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = "EPSG:4326"

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of dictionaries containing coordinates (WKT) for Sharyn River water level data
water_level_data = [
    {'date': '2021-01-01', 'wkt': 'POINT(74.56 43.29)', 'level': 12.5},
    {'date': '2021-01-02', 'wkt': 'POINT(74.56 43.29)', 'level': 13.2},
    # ... other data points ...
]

# Convert WKT to Shapely geometry and calculate average water level
sharyn_river_data = []
for data_point in water_level_data:
    if data_point['wkt'].startswith('POINT'):
        point = wkt.loads(data_point['wkt'])
        sharyn_river_data.append({'date': data_point['date'], 'geometry': point, 'level': data_point['level']})

sharyn_river_gdf = gpd.GeoDataFrame(sharyn_river_data)
avg_level = sharyn_river_gdf['level'].mean()

# Find maximum water level
max_level = sharyn_river_gdf['level'].max()

# Calculate difference between max and avg levels
diff = max_level - avg_level

print(f"Разница между максимальным уровнем паводка в реке Sharyn River и его историческим средним значением: {diff:.2f} м.")

# Save the final map
m.save("127.html")