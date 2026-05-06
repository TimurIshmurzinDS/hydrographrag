import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the shapefile
m = folium.Map(location=[basin.geometry.centroid.y.mean(), basin.geometry.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for rivers (replace with actual data if available)
rivers = [{'name': 'Shilik River'}, {'name': 'Sharyn River'}]

# This is a placeholder for the coordinates, replace with actual data if available
coordinates = ['POINT(0 0)', 'POINT(0 0)']

for river, coord in zip(rivers, coordinates):
    # Convert WKT to Shapely geometry object
    point = wkt.loads(coord)
    # Add the river to the map
    folium.Marker([point.y, point.x], popup=river['name']).add_to(m)

# Save the final map
m.save("135.html")