import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
river_coords = [{'type': 'FeatureCollection', 'features': [{'geometry': {'type': 'LineString', 'coordinates': [(x, y) for x, y in zip(Kurty_River['X'], Kurty_River['Y'])]}]}}]

# Add the river to the map
folium.GeoJson(river_coords).add_to(m)

# Save the final map
m.save("51.html")