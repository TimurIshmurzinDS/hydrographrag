import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Create map with basin boundaries
m = folium.Map(location=[basin_gdf.centroid.y, basin_gdf.centroid.x], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt), name='basin').add_to(m)
m

# Define coordinates for river Doss and Emeley
river_doss_coords = [
    {'lat': 54.1234, 'lon': 23.4567},
    {'lat': 54.2345, 'lon': 23.5678}
]

river_emeleys_coords = [
    {'lat': 54.3456, 'lon': 24.6789},
    {'lat': 54.4567, 'lon': 24.7890}
]

# Calculate distance between two points
def calculate_distance(point1, point2):
    lat1, lon1 = point1['lat'], point1['lon']
    lat2, lon2 = point2['lat'], point2['lon']
    radius = 6371  # Radius of the Earth in km

    dlat = (lat2 - lat1) * np.pi / 180
    dlon = (lon2 - lon1) * np.pi / 180

    a = (np.sin(dlat/2)**2 + np.cos(lat1*np.pi/180)*np.cos(lat2*np.pi/180)*np.sin(dlon/2)**2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    distance = radius * c
    return distance

# Calculate distances between river Doss and Emeley
distance_doss_emeleys = calculate_distance(river_doss_coords[0], river_emeleys_coords[0])
print(f"Расстояние между устьем реки Дос и началом реки Емель: {distance_doss_emeleys:.2f} км")

# Save map
m.save("92.html")