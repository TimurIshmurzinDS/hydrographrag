import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map with basin centroid
m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded coordinates for Temirlik River and village (replace with actual data if available)
entities = [
    {"name": "Temirlik River", "coordinates": "POINT(69.183574 42.300000)"},
    {"name": "Temirlik Village", "coordinates": "POINT(69.183574 42.300000)"}
]

# Add entities to the map
for entity in entities:
    point = wkt.loads(entity["coordinates"])
    folium.Marker([point.y, point.x], popup=entity["name"]).add_to(m)

# Save the final map
m.save("66.html")