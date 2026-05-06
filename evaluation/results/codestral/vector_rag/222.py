import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map
m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for rivers (replace with actual data if available)
rivers = [{'name': 'Karatal River', 'coordinates': 'POINT(37.123456 41.123456)', 'anomaly': True},
          {'name': 'Koktal River', 'coordinates': 'POINT(38.123456 40.123456)', 'anomaly': False},
          {'name': 'Karaoy River', 'coordinates': 'POINT(37.987654 41.987654)', 'anomaly': False},
          {'name': 'Bayankol River', 'coordinates': 'POINT(36.567890 42.567890)', 'anomaly': False}]

# Add rivers to the map
for river in rivers:
    point = wkt.loads(river['coordinates'])
    folium.Marker([point.y, point.x], popup=river['name'], icon=folium.Icon(color='red' if river['anomaly'] else 'blue')).add_to(m)

# Save the final map
m.save("222.html")