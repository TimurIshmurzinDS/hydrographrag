import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the shapefile
m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries containing coordinates (WKT) and river names
rivers = [{'name': 'Uzyn Kargaly River', 'coordinates': 'POINT (68.753419 46.020000)'},
          {'name': 'Byzhy River', 'coordinates': 'POINT (68.753419 46.020000)'},
          {'name': 'Shyzhyn River', 'coordinates': 'POINT (68.753419 46.020000)'},
          {'name': 'Shynzhaly River', 'coordinates': 'POINT (68.753419 46.020000)'}]
observation = {'name': 'Observation Point', 'coordinates': 'POINT (68.753419 46.020000)'} # Replace with actual coordinates

# Add rivers and observation point to the map
for river in rivers:
    folium.Marker(location=[wkt.loads(river['coordinates']).y, wkt.loads(river['coordinates']).x], popup=river['name'], icon=folium.Icon(color='blue')).add_to(m)
folium.Marker(location=[wkt.loads(observation['coordinates']).y, wkt.loads(observation['coordinates']).x], popup=observation['name'], icon=folium.Icon(color='red')).add_to(m)

# Save the final map
m.save("211.html")