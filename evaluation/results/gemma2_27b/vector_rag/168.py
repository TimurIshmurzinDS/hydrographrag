import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium map centered on the centroid of the basin data
m = folium.Map(location=basin_data.centroid.values[0], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(data=basin_data, name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Save the map
m.save("168.html")