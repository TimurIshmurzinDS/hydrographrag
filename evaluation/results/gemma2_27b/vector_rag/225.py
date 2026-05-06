import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize map centered on basin centroid
m = folium.Map(location=basin.centroid.y, 
                tiles='CartoDB positron',
                zoom_start=10)

# Add the basin to the map
folium.GeoJson(data=basin, name="Basin",
               fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Save the map
m.save("225.html")