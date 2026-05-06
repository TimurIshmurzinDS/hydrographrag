import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile strictly using a raw string
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(data=basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.__geo_interface__)).add_to(m)

# Create a hardcoded list of dictionaries for coordinates
coordinates = [
    {'lat': 43.033333, 'lon': 76.983333},
    {'lat': 43.066667, 'lon': 77.016667},
    {'lat': 43.100000, 'lon': 77.050000},
    {'lat': 43.133333, 'lon': 77.083333}
]

# Add markers to the map
for coord in coordinates:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Наблюдение').add_to(m)

# Save the final map
m.save("10.html")