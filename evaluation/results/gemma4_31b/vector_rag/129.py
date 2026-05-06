import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string and convert to CRS 'EPSG:4326'
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the shapefile
# Using 'CartoDB positron' tiles as requested
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.mean(), centroid.x.mean()]
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 3. Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
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

# 4. Handle coordinates for observation points if provided in WKT
# Context mentions 'с.Tekes' as an observation point. 
# Since specific WKT coordinates were not provided in the context, 
# we define a placeholder list if coordinates were available.
observations = [
    # Example structure: {"name": "с.Tekes", "geometry": "POINT(longitude latitude)"}
]

for obs in observations:
    point_geom = wkt.loads(obs["geometry"])
    folium.Marker(
        location=[point_geom.y, point_geom.x],
        popup=obs["name"],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as "129.html"
m.save("129.html")