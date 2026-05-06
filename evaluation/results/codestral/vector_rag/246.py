import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the shapefile
m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries containing coordinates (WKT) from the context
points = [{'name': 'Shilik River', 'coordinates': wkt.loads('POINT (longitude1 latitude1)'), 'type': 'river'},
          {'name': 'Osek River Confluence', 'coordinates': wkt.loads('POINT (longitude2 latitude2)'), 'type': 'confluence'}]

# Add points to the map
for point in points:
    folium.Marker(location=[point['coordinates'].y, point['coordinates'].x], popup=point['name']).add_to(m)

# Coordinates for Orion constellation (not provided in context)
orion = {'name': 'Orion Constellation', 'coordinates': wkt.loads('POINT (longitude3 latitude3)')}
folium.Marker(location=[orion['coordinates'].y, orion['coordinates'].x], popup=orion['name'], icon=folium.Icon(color='red')).add_to(m)

# Add line between Orion and Shilik River
folium.PolyLine([[orion['coordinates'].y, orion['coordinates'].x], [points[0]['coordinates'].y, points[0]['coordinates'].x]], color="red").add_to(m)

# Save the final map
m.save("246.html")