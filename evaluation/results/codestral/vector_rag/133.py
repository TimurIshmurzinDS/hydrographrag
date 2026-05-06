import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium map
m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron')

# Add the basins to the map
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for river coordinates (if available in the context)
river_coordinates = [{'name': 'Kurty River', 'coordinates': 'POINT (...)'}, {'name': 'Dos River', 'coordinates': 'POINT (...)'}]

# Add rivers to the map (if coordinates are available)
for river in river_coordinates:
    folium.Marker(location=wkt.loads(river['coordinates']).coords[0], popup=river['name'], icon=folium.Icon(color='blue')).add_to(m)

# Save the final map
m.save("133.html")