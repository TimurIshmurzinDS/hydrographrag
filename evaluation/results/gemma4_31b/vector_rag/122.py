import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per critical instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.iloc[0], centroid.x.iloc[0]]

m = folium.Map(
    location=map_center, 
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

# 4. Handle coordinates if provided in context (WKT)
# In this context, specific WKT coordinates were not provided, 
# but the structure is implemented for consistency.
observations = [] 
# Example of how a point would be added if WKT existed:
# observations.append({"name": "Observation Point", "geometry": wkt.loads("POINT(lon lat)")})

for obs in observations:
    geom = obs["geometry"]
    folium.Marker(
        location=[geom.y, geom.x],
        popup=obs["name"],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as 122.html
m.save("122.html")