import folium

# Create a map centered around the river Kish Osek
m = folium.Map(location=[52.2370, 21.0175], zoom_start=13)

# Add the source of water (river Kish Osek) to the map
folium.Marker([52.2370, 21.0175], popup='River Kish Osek').add_to(m)

# Choose a suitable location for pickling vegetables based on accessibility and other factors
pickling_location = [52.2456, 21.0289]

# Add the pickling location to the map with a marker
folium.Marker(pickling_location, popup='Pickling Location').add_to(m)

# Save the final map as "261.html"
m.save("261.html")