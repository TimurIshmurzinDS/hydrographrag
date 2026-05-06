import folium

# Create a map centered on the Aksu River location (assuming coordinates are available)
m = folium.Map(location=[37.5, -120], zoom_start=8)

# Add a marker for the Aksu River location
folium.Marker([37.5, -120], popup='Aksu River').add_to(m)

# Assume we have some optimal colony locations as coordinates [(lat, lon), ...]
colonies = [(-4.59, 165.78), (18.16, 77.83), (-14.22, -90.53)]

# Add markers for each colony location
for colony in colonies:
    folium.Marker(colony, popup='Mars Colony').add_to(m)

# Save the map as an HTML file
m.save("248.html")