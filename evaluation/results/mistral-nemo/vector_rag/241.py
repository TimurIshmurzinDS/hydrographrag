import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=gdf.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Coordinates of Talgar River in WKT format
talgar_wkt = 'POINT(71.3564 43.2897)'
talgar_geom = wkt.loads(talgar_wkt)

# Coordinates of the Moon (hardcoded)
moon_coords = {'lat': 0, 'lon': 0}

# Calculate distance between Talgar River and the Moon using Haversine formula
R = 6371 # Earth's radius in kilometers
dLat = moon_coords['lat'] - talgar_geom.y
dLon = moon_coords['lon'] - talgar_geom.x
a = (np.sin(dLat/2))**2 + np.cos(talgar_geom.y) * np.cos(moon_coords['lat']) * (np.sin(dLon/2))**2
c = 2 * np.arcsin(np.sqrt(a))
distance = R * c

# Save the final map
m.save("241.html")