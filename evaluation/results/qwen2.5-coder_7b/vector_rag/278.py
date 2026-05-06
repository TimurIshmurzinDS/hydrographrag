import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to EPSG:4326 CRS
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Calculate the centroid of the basin
centroid = basin_data.geometry.centroid[0]

# Initialize folium map using the centroid and set tiles to 'CartoDB positron'
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data.geometry.to_json(), 
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Save the final map
m.save("278.html")