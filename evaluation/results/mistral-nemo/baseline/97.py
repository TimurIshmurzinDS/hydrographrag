import geopandas as gpd
from shapely.geometry import LineString
import folium

# Load rivers data
emel_river = gpd.read_file('emel_river.shp')
karatal_river = gpd.read_file('karatal_river.shp')

# Find common part of Emel river that flows towards Karatal river
common_part = LineString(list(emel_river.geometry.intersection(karatal_river.geometry).coords))

# Calculate length of the common part
length = common_part.length

# Check if Emel river is a tributary of Karatal river
is_tributary = False
if common_part:
    is_tributary = True

# Print results
print(f"Is Emel river a tributary of Karatal river? {is_tributary}")
print(f"Length of the common part: {length} km")

# Visualize on map (if required)
m = folium.Map(location=[emel_river.centroid.y.mean(), emel_river.centroid.x.mean()], zoom_start=8)

folium.GeoJson(
    emel_river.to_json(),
    style_function=lambda x: {'fillColor': 'blue', 'color': 'black'},
    highlight_function=lambda x: folium.GeoJsonHighlight(style_function).add_to(m),
    tooltip=folium.GeoJsonTooltip(fields=['name'], labels=True, aliases=['Emel River'])
).add_to(m)

folium.GeoJson(
    karatal_river.to_json(),
    style_function=lambda x: {'fillColor': 'blue', 'color': 'black'},
    highlight_function=lambda x: folium.GeoJsonHighlight(style_function).add_to(m),
    tooltip=folium.GeoJsonTooltip(fields=['name'], labels=True, aliases=['Karatal River'])
).add_to(m)

m.save("97.html")