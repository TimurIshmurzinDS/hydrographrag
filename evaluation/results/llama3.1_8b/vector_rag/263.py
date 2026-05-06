import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string: r"data/basin_data.shp"
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT) if available
wkt_coords = [
    {'lat': 43.123, 'lon': 76.456},
    {'lat': 43.789, 'lon': 77.012}
]

# Add markers to the map using folium.Marker
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], popup='Marker').add_to(m)

# SAVE the final map: m.save("263.html")
m.save("263.html")