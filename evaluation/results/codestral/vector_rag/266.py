import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the shapefile
m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Create a hardcoded list of dictionaries for the irrigation point (centroid of the basin)
irrigation_points = [{'location': [basin.centroid.y, basin.centroid.x], 'name': 'Irrigation Point'}]

# Add the irrigation points to the map as markers
for point in irrigation_points:
    folium.Marker(point['location'], popup=point['name']).add_to(m)

# Save the final map
m.save("266.html")