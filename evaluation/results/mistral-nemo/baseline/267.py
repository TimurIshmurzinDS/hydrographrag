import folium

# Define the coordinates of Baskun River and the ice collection point
baskun_river = (41.0383, 67.1525)
ice_collection_point = (41.0390, 67.1530)

# Create a map centered on Baskun River
m = folium.Map(location=baskun_river, zoom_start=15)

# Add Baskun River to the map as a blue line
folium.PolyLine(locations=[baskun_river], weight=5, color='blue').add_to(m)

# Add ice collection point to the map as a red marker
folium.Marker(ice_collection_point, popup='Ice Collection Point', icon=folium.Icon(color='red')).add_to(m)

# Save the final map
m.save("267.html")