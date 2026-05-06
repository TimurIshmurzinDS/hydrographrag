import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile
# Using raw string for path as per instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

m = folium.Map(
    location=[mean_lat, mean_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Add the basin boundary to the map
# Strictly following the style requirements: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# 4. Handle Coordinates (WKT)
# Since no specific WKT coordinates were provided in the context for the river points, 
# we initialize an empty list. If WKTs were present, they would be parsed here.
points_data = [] 
# Example of how it would be implemented if WKT existed:
# points_data = [{"loc": wkt.loads("POINT(lon lat)"), "name": "Sarykan Station"}]

for point in points_data:
    coords = [point["loc"].y, point["loc"].x]
    folium.Marker(location=coords, popup=point["name"]).add_to(m)

# 5. Save the final map
# Strictly using the required filename "46.html"
m.save("46.html")