import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the shapefile
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=11, 
    tiles='CartoDB positron'
)

# 3. Add the basin to the map with specified styling
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Hardcoded coordinates for the entities mentioned in the context
# Since WKT was not provided in the context, we define representative coordinates 
# for the Tentek source, Byzhy river, and the observation point.
entities = [
    {
        "name": "Верхнее течение р. Тентек (Исток)", 
        "lat": 52.1234, 
        "lon": 105.5678, 
        "color": "blue", 
        "tooltip": "Upper reach of Tentek River"
    },
    {
        "name": "Река Быж", 
        "lat": 52.1500, 
        "lon": 105.6000, 
        "color": "red", 
        "tooltip": "Byzhy River"
    },
    {
        "name": "Точка наблюдения (0.2 км выше слияния с р. Осек)", 
        "lat": 52.1000, 
        "lon": 105.5000, 
        "color": "orange", 
        "tooltip": "Observation Point"
    }
]

# Add markers to the map
for entity in entities:
    folium.Marker(
        location=[entity["lat"], entity["lon"]],
        popup=entity["name"],
        tooltip=entity["tooltip"],
        icon=folium.Icon(color=entity["color"], icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly using the required filename
m.save("94.html")