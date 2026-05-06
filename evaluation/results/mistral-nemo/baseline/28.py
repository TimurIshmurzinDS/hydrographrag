import folium
import geopandas as gpd

# Load river data and flood warning data
river_data = gpd.read_file("shyzhyn_river.geojson")
flood_warnings = gpd.read_file("flood_warnings.geojson")

# Filter flood warnings by river name
shyzhyn_floods = flood_warnings[flood_warnings['river_name'] == 'Shyzhyn River']

# Create a map centered on the Shyzhyn River
m = folium.Map(location=[shyzhyn_river.centroid.y, shyzhyn_river.centroid.x], zoom_start=10)

# Add river line to the map
folium.GeoJson(river_data, style_function=lambda x: {'color': 'blue'}).add_to(m)

# Add flood warning points to the map
for _, row in shyzhyn_floods.iterrows():
    folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5, color='red').add_to(m)

# Save the map as HTML file
m.save("28.html")