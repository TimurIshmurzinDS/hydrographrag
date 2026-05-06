import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile with raw string and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(data=gdf.to_json(), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT) if available
wkt_coords = [
    {'type': 'Feature', 'geometry': wkt.loads('POINT(48.6784 35.0231)'), 'properties': {'name': 'Koksu River'}},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(47.6503 36.2832)'), 'properties': {'name': 'Byzhy River'}}
]

# Add coordinates to the map
for coord in wkt_coords:
    folium.Marker(location=coord['geometry'].coords[0], popup=coord['properties']['name']).add_to(m)

# Save the final map strictly using a string filename: m.save("208.html")
m.save("208.html")