python
import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize map centered on basin centroid with tiles='CartoDB positron'
m = folium.Map(location=basin.centroid.values[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(data=basin, name="Basin", style_function=lambda feature: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Save the map
m.save("250.html")