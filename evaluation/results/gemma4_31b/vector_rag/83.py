import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to initialize the map
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# Initialize folium Map with the specified tiles
m = folium.Map(
    location=[mean_lat, mean_lon], 
    zoom_start=12, 
    tiles='CartoDB positron'
)

# Add the basin boundary to the map with strict styling
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

# Context entities: Temirlik River, Turgen River, Temirlik village.
# Since specific WKT coordinates were not provided in the context, 
# we define the logic for adding them if they were available.
# Example of how coordinates would be handled if present:
# entities = [
#     {"name": "Temirlik River", "type": "River", "coords": "POINT(lon lat)"},
#     {"name": "Turgen River", "type": "River", "coords": "POINT(lon lat)"},
#     {"name": "Temirlik village", "type": "Observation", "coords": "POINT(lon lat)"},
# ]
# for entity in entities:
#     point = wkt.loads(entity["coords"])
#     folium.Marker([point.y, point.x], popup=entity["name"]).add_to(m)

# Save the final map strictly as 83.html
m.save("83.html")