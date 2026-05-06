import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Define river data (replace with actual coordinates and lengths)
rivers = [
    {'name': 'Коктал', 'coordinates': wkt.loads('POINT (78.5 43.5)'), 'length_km': 150},
    {'name': 'Баянкуль', 'coordinates': wkt.loads('POINT (79.2 42.8)'), 'length_km': 120}
]

# Process river data and calculate total length of tributaries

m.save("93.html")