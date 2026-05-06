import folium

# Coordinates of the source of Tenete river (approximately)
tenete_source = [49.85, 26.07]

# Coordinates of Byzh river
byzh_coords = [49.31, 25.93]

# Create a map centered at the approximate location of Tenete's source
m = folium.Map(location=tenete_source)

# Add markers for both locations
folium.Marker(tenete_source, popup='Tenete Source').add_to(m)
folium.Marker(byzh_coords, popup='Byzh River').add_to(m)

# Display the map
display(m)

# Save the map as an HTML file
m.save("94.html")