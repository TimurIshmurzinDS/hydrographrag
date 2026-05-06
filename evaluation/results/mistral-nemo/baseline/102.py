import folium
from geopy.distance import geodesic

# Coordinates of Karatal and Ułken Almaty river mouths
karatal = (43.2578, 71.3692)
ulken_almaty = (43.2047, 71.4167)

# Calculate distance between two points using geodesic method
distance = geodesic(karatal, ulken_almaty).km

# Create a map centered on the midpoint of the two points
m = folium.Map(location=[(karatal[0] + ulken_almaty[0]) / 2, (karatal[1] + ulken_almaty[1]) / 2], zoom_start=13)

# Add markers for both points and connect them with a line
folium.Marker(karatal, popup='Karatal').add_to(m)
folium.Marker(ulken_almaty, popup='Ułken Almaty').add_to(m)
folium.PolyLine(locations=[karatal, ulken_almaty], weight=2).add_to(m)

# Display the distance as a label on the map
folium.CircleMarker([(karatal[0] + ulken_almaty[0]) / 2, (karatal[1] + ulken_almaty[1]) / 2],
                    radius=5,
                    color='red',
                    fill=True,
                    popup=f'Distance: {distance:.2f} km').add_to(m)

# Save the map as an HTML file
m.save("102.html")