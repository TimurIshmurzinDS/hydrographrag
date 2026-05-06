from geopy.distance import geodesic
import folium

# Coordinates of the mouth of Dos River and the start of Emele River
dos_river_mouth = (45.0703, 39.0182)
emele_river_start = (45.0651, 39.0012)

# Calculate distance between two points using haversine formula
distance = geodesic(dos_river_mouth, emele_river_start).km

print(f"Distance between Dos River mouth and Emele River start is {distance} kilometers.")

# Create a map centered at the midpoint of the two points
m = folium.Map(location=[(dos_river_mouth[0] + emele_river_start[0]) / 2, (dos_river_mouth[1] + emele_river_start[1]) / 2], zoom_start=13)

# Add markers for both points
folium.Marker(dos_river_mouth, popup="Dos River Mouth").add_to(m)
folium.Marker(emele_river_start, popup="Emele River Start").add_to(m)

# Draw a line between the two points
folium.PolyLine([dos_river_mouth, emele_river_start], weight=2).add_to(m)

# Save the map as html file
m.save("92.html")