import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[gdf.centroid.y, gdf.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If coordinates (WKT) are provided in the context, create a list of dictionaries and add them as markers on the map
coordinates = [
    {'name': 'Shilik River', 'wkt': 'POINT(74.95 43.18)'},
    {'name': 'Kishi Almaty River', 'wkt': 'POINT(76.92 43.25)'}
]

for coord in coordinates:
    folium.Marker(wkt.loads(coord['wkt']), popup=coord['name']).add_to(m)

# Save the final map
m.save("126.html")