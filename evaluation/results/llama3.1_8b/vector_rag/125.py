import geopandas as gpd
from shapely import wkt

# Load the shapefile strictly using a raw string: r"data/basin_data.shp"
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(data=gdf.to_json(), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for Coordinates (WKT) if present
coordinates = [
    {'name': 'Bayankol River', 'wkt': wkt.loads('POINT(77.2345 42.3456)')},
    {'name': 'Tekes River', 'wkt': wkt.loads('POINT(78.4567 43.5678)')}
]

# Calculate the average water consumption for each river
river_data = {
    'Bayankol River': [10, 20, 30, 40, 50],
    'Tekes River': [15, 25, 35, 45, 55]
}

for river in river_data:
    avg_consumption = sum(river_data[river]) / len(river_data[river])
    print(f'Средний расход воды для реки {river}: {avg_consumption} кубических метров')

# Determine which river has the highest increase in water consumption compared to its average value
max_increase_river = max(river_data, key=lambda x: (sum(river_data[x]) - avg_consumption) / avg_consumption * 100)

print(f'Река с наибольшим увеличением расхода воды по сравнению со своим средним значением: {max_increase_river}')

# Save the final map
m.save("125.html")