import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the basin data
m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for water consumption points (replace with actual data if available)
water_consumption_points = [{'name': 'Point 1', 'coordinates': wkt.loads('POINT (54.789023 69.442187)'), 'water_consumption': 1000},
                            {'name': 'Point 2', 'coordinates': wkt.loads('POINT (54.788023 69.443187)'), 'water_consumption': 1500}]

# Add water consumption points to the map with markers and popups
for point in water_consumption_points:
    folium.Marker(location=[point['coordinates'].y, point['coordinates'].x],
                  popup=f"Name: {point['name']}<br>Water Consumption: {point['water_consumption']} m³",
                  icon=folium.Icon(color='red')).add_to(m)

# Save the final map
m.save("195.html")