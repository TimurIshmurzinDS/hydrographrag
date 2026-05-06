import folium
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # Radius of Earth in kilometers
    dlon = radians(lon2 - lon1)
    dlat = radians(lat2 - lat1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# Coordinates of Orion and Shilyk River (approximate)
orion_lat, orion_lon = 5.0, 10.0  
shilyk_lat, shilyk_lon = 43.0, 87.0

distance = haversine(orion_lon, orion_lat, shilyk_lon, shilyk_lat)
print("Distance between Orion and Shilyk River:", distance, "km")

# Create a map centered on the approximate location of Orion
m = folium.Map(location=[orion_lat, orion_lon], zoom_start=3)

# Add markers for Orion and Shilyk River
folium.Marker([orion_lat, orion_lon], popup="Orion").add_to(m)
folium.Marker([shilyk_lat, shilyk_lon], popup="Shilyk River").add_to(m)

# Save the map
m.save("246.html")