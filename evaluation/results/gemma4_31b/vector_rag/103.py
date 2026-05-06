import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string and convert to CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the shapefile
# Calculate centroid for map centering
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2
).add_to(m)

# 4. Hardcoded list of rivers found in context (Coordinates are representative as WKT was not provided in context)
# Note: 'Dos' river is omitted as it was not present in the provided entity context.
rivers_data = [
    {"name": "Karatal River", "lat": 43.5, "lon": 77.5},
    {"name": "Urzhar River", "lat": 46.2, "lon": 82.1},
]

# Add markers for the rivers to the map
for river in rivers_data:
    folium.Marker(
        location=[river["lat"], river["lon"]],
        popup=river["name"],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as 103.html
m.save("103.html")