import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Initialize folium Map with specified tiles
m = folium.Map(location=map_center, zoom_start=10, tiles='CartoDB positron')

# 5. Add the basin boundary to the map
# Using specified colors: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    name="Talgar River Basin",
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# 6. Handle coordinates from context (WKT)
# Since the context provided "г. Talgar" as observations without specific WKT strings,
# we define the observation point based on the city's general location if needed.
# However, strictly following the rule: if WKT is not in context, we don't invent it,
# but we ensure the structure for hardcoded lists is present if data existed.
observations = [] 
# Example of how it would be added if WKT were present:
# observations = [{"name": "Talgar Obs 1", "geometry": wkt.loads("POINT(x y)")}]

for obs in observations:
    coords = [obs['geometry'].y, obs['geometry'].x]
    folium.Marker(location=coords, popup=obs['name']).add_to(m)

# 7. Save the final map strictly as "166.html"
m.save("166.html")