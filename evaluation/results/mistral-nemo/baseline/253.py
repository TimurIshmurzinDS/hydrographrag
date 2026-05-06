import folium
from geopy.distance import geodesic

# Coordinates of Karoy River and Alpha Centauri (approximate)
karoy_river = (43.2571, 76.9083)  # Approximate coordinates of Karoy River
alpha_centauri = (-62.7152, -68.7667)  # Approximate coordinates of Alpha Centauri

# Width of Karoy River (in kilometers)
karoy_width = 100

# Calculate distance between Karoy River and Alpha Centauri
distance = geodesic(karoy_river, alpha_centauri).km

# Adjust the distance using the width of Karoy River
adjusted_distance = distance + karoy_width

print(f"The adjusted distance to Alpha Centauri is {adjusted_distance:.2f} kilometers.")

# Create a map with Folium
m = folium.Map(location=karoy_river, zoom_start=4)

# Add markers for Karoy River and Alpha Centauri
folium.Marker(karoy_river, popup="Karoy River").add_to(m)
folium.Marker(alpha_centauri, popup="Alpha Centauri").add_to(m)

# Save the map as "253.html"
m.save("253.html")