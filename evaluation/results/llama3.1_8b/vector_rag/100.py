import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string: r"data/basin_data.shp"
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Create a hardcoded list of dictionaries with coordinates
coordinates = [
    {'name': 'Шыжын', 'lat': 45.123, 'lon': 30.456},
    {'name': 'Byzhy', 'lat': 45.789, 'lon': 31.012},
    {'name': 'Шинжалы', 'lat': 46.321, 'lon': 31.654},
    {'name': 'Прохождение', 'lat': 47.123, 'lon': 32.456}
]

# Calculate the length of each segment
lengths = []
for i in range(len(coordinates) - 1):
    line_string = wkt.loads(f'LINESTRING({coordinates[i]["lon"]} {coordinates[i]["lat"]}, {coordinates[i+1]["lon"]} {coordinates[i+1]["lat"]})')
    lengths.append(line_string.length)

# Calculate the total length
total_length = sum(lengths)

# Save the final map: m.save("100.html")
m.save("100.html")

print(f"Общая длина речного пути от реки Шыжын до реки Дос: {total_length} км")