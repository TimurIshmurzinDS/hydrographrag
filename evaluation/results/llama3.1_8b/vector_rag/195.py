import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Create map with centroid of the shapefile and tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add basin to the map
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt), name='basin').add_to(m)

# Create hardcoded list of dictionaries for coordinates (WKT)
wkt_coords = [
    {'lat': 52.373, 'lon': 4.895},
    {'lat': 52.378, 'lon': 4.900},
    {'lat': 52.383, 'lon': 4.905},
    {'lat': 52.388, 'lon': 4.910}
]

# Add coordinates to the map
for coord in wkt_coords:
    folium.CircleMarker(location=[coord['lat'], coord['lon']], radius=5).add_to(m)

# Save final map
m.save("195.html")