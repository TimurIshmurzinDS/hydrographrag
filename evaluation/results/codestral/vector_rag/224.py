# Import necessary libraries
import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=[basin_data.geometry.centroid.y, basin_data.geometry.centroid.x], tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Since the context does not contain Coordinates (WKT), we will skip this step

# Save the final map
m.save("224.html")