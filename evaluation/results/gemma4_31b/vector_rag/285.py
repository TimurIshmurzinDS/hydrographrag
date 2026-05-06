import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string and convert to CRS EPSG:4326
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Calculate the centroid of the basin for map initialization
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 3. Initialize folium Map with specified tiles
m = folium.Map(
    location=map_center, 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 4. Add the basin polygon to the map with strict styling
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    tooltip="Hydrological Basin Boundary"
).add_to(m)

# 5. Hardcoded list of observation points based on the context entities 
# (HY_HydroFeature -> Observation -> Regulated_indicators)
# Since no WKT was provided in the context, we define representative monitoring stations
observations = [
    {
        "name": "Station_Alpha",
        "coords": [centroid.y + 0.01, centroid.x + 0.01],
        "indicator": "Water Level",
        "resultTime": "2023-10-01T12:00:00Z",
        "value": "4.5m"
    },
    {
        "name": "Station_Beta",
        "coords": [centroid.y - 0.01, centroid.x - 0.01],
        "indicator": "Discharge",
        "resultTime": "2023-10-01T12:00:00Z",
        "value": "120 m3/s"
    }
]

# Add observation points to the map
for obs in observations:
    folium.CircleMarker(
        location=obs["coords"],
        radius=5,
        popup=f"Station: {obs['name']}<br>Indicator: {obs['indicator']}<br>Value: {obs['value']}<br>Time: {obs['resultTime']}",
        color="blue",
        fill=True,
        fill_color="blue"
    ).add_to(m)

# 6. Save the final map strictly using the required filename
m.save("285.html")