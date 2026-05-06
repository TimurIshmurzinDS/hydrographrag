import folium

# Create a map centered on the Moon's coordinates (approximate)
m = folium.Map(location=[0, 0], zoom_start=3)

# Add a marker for the farm location (approximate)
folium.Marker([-15.0, 47.0]).add_to(m)

# Add a polyline to represent the river Kish Osek irrigation system
river_coords = [(lat, lon) for lat in range(-30, 30, 5) for lon in range(30, -30, -5)]
folium.PolyLine(river_coords, weight=2.5).add_to(m)

# Save the map as "269.html"
m.save("269.html")