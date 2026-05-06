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
    zoom_start=11, 
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

# 4. Hardcoded list of entities from context (since WKT was not provided, 
# we use representative coordinates for the mentioned entities)
entities = [
    {"name": "Tekeli River", "type": "HY_HydroFeature", "lat": mean_lat + 0.01, "lon": mean_lon + 0.01},
    {"name": "Byzhy River", "type": "HY_HydroFeature", "lat": mean_lat - 0.02, "lon": mean_lon - 0.01},
    {"name": "Shyzhyn River", "type": "HY_HydroFeature", "lat": mean_lat + 0.02, "lon": mean_lon - 0.02},
    {"name": "Tekeli town", "type": "Observation", "lat": mean_lat, "lon": mean_lon}
]

# Add markers for each entity
for entity in entities:
    folium.Marker(
        location=[entity["lat"], entity["lon"]],
        popup=f"{entity['name']} ({entity['type']})",
        icon=folium.Icon(color='blue' if entity['type'] == 'HY_HydroFeature' else 'red')
    ).add_to(m)

# 5. Save the final map strictly as 119.html
m.save("119.html")