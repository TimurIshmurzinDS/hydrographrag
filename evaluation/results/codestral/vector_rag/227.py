import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium map
m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron', zoom_start=10)

# Add the basin to the map
folium.GeoJson(basin_data, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Save the final map
m.save("227.html")