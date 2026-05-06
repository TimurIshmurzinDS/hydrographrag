import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the shapefile
m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries containing river names and coordinates (WKT)
rivers = [
    {"name": "Shyzhyn River", "coordinates": "LINESTRING (37.564891 50.264891, 37.565891 50.265891)"},
    {"name": "Byzhy River", "coordinates": "LINESTRING (37.566891 50.266891, 37.567891 50.267891)"},
    {"name": "Shynzhaly River", "coordinates": "LINESTRING (37.568891 50.268891, 37.569891 50.269891)"},
    {"name": "Prokhodnaya River", "coordinates": "LINESTRING (37.570891 50.270891, 37.571891 50.271891)"}
]

# Add rivers to the map
for river in rivers:
    folium.GeoJson(wkt.loads(river["coordinates"]), style_function=lambda x: {'color': 'blue'}).add_child(folium.Popup(river["name"])).add_to(m)

# Save the final map
m.save("100.html")