import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize Folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    basin,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Create a hardcoded list of dictionaries with coordinates in WKT format
creeks = [
    {"name": "Terisbuthak Creek", "wkt": "LINESTRING(-73.985146 40.673294, -73.984878 40.673562)"},
    {"name": "Talgar River", "wkt": "LINESTRING(-73.986572 40.671211, -73.986203 40.671480)"}
]

# Perform nearest points analysis
for creek in creeks:
    gdf = gpd.GeoDataFrame([{"geometry": wkt.loads(creek["wkt"])}])
    nearest = gpd.sjoin_nearest(gdf, basin, how="first")
    folium.PolyLine(
        list(zip(*zip(*nearest.geometry.xy))),
        tooltip=folium.GeoJsonTooltip(fields=["name"], labels=True),
    ).add_to(m)

# Save the final map
m.save("176.html")