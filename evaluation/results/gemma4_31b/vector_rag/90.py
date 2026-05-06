import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path and converting to WGS84 (EPSG:4326)
basin_df = gpd.read_file(r"data/basin_data.shp")
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_df, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Hardcoded river data (Coordinates were not provided in context, 
# but structure is implemented as per instructions if they were present)
# Example structure for rivers: Karaoy River, Baskan River, Temirlik River
rivers_data = [
    # {"name": "Karaoy River", "geometry": "POINT(lon lat)"},
    # {"name": "Baskan River", "geometry": "POINT(lon lat)"},
    # {"name": "Temirlik River", "geometry": "POINT(lon lat)"},
]

for river in rivers_data:
    point = wkt.loads(river["geometry"])
    folium.Marker(
        location=[point.y, point.x], 
        popup=river["name"], 
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as 90.html
m.save("90.html")