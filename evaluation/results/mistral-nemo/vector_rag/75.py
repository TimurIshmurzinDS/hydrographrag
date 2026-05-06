import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(gdf.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(
    gdf,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT)
tentek_river = {"name": "Тентек River", "wkt": "POINT(74.56 -13.24)"}
sharyn_river = {"name": "Шарынь River", "wkt": "POINT(75.32 -12.89)"}

# Add rivers to the map using folium.CircleMarker
for river in [tentek_river, sharyn_river]:
    folium.CircleMarker(
        location=tuple(wkt.loads(river["wkt"])),
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.5,
        popup=river["name"]
    ).add_to(m)

# Save the final map
m.save("75.html")