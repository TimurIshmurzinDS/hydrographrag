import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT)
wkt_coords = [
    {'type': 'Feature', 'geometry': wkt.loads('POINT(76.1234 43.5678)')},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(77.2345 44.6789)')}
]

# Add markers to the map
for coord in wkt_coords:
    folium.Marker(location=[coord['geometry'].coords[1], coord['geometry'].coords[0]], popup='Река Шыжын').add_to(m)

# Save the final map
m.save("95.html")