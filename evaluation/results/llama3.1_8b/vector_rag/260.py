import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.__geo_interface__, name='Basin').add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.1245, 'lon': 76.5443},
    {'lat': 43.1256, 'lon': 76.5454}
]

# Add markers to the map
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Marker').add_to(m)

# Save the final map
m.save("260.html")