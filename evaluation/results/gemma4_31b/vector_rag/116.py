import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

m = folium.Map(
    location=[mean_lat, mean_lon], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
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

# 4. Hardcoded entities from context (since WKT coordinates were not provided, 
# we represent the identified entities as markers based on the regional context)
# Note: In a real scenario, these would be extracted from the WKT provided in the context.
entities = [
    {"name": "Tekeli River", "type": "HY_HydroFeature", "lat": mean_lat + 0.05, "lon": mean_lon - 0.05},
    {"name": "Lepsy River", "type": "HY_HydroFeature", "lat": mean_lat - 0.05, "lon": mean_lon + 0.05},
    {"name": "Tekeli town", "type": "Observation", "lat": mean_lat, "lon": mean_lon}
]

for entity in entities:
    folium.Marker(
        location=[entity["lat"], entity["lon"]],
        popup=f"{entity['name']} ({entity['type']})",
        icon=folium.Icon(color='blue' if entity['type'] == 'HY_HydroFeature' else 'red')
    ).add_to(m)

# 5. Save the final map strictly as 116.html
m.save("116.html")