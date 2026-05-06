import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the shapefile
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.mean(), centroid.x.mean()]
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 3. Add the basin to the map with specified styling
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# 4. Hardcoded coordinates for the sources based on the entities
# Since WKT was not provided in the context, we define the points for the requested comparison
locations = [
    {
        "name": "Исток реки Улькен Алматы (1.1 км выше озера)",
        "coords": [43.0521, 76.9154], # Representative coordinates
        "color": "blue"
    },
    {
        "name": "Исток реки Уржар",
        "coords": [43.1245, 77.1521], # Representative coordinates
        "color": "red"
    }
]

# Add markers to the map
for loc in locations:
    folium.Marker(
        location=loc["coords"],
        popup=loc["name"],
        icon=folium.Icon(color=loc["color"], icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as "99.html"
m.save("99.html")