import numpy as np
from geopy.distance import geodesic
import folium

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
M_jupiter = 1.898e27  # Mass of Jupiter (kg)

# Data
river_points = [(51.5074, -0.1278), (51.5156, -0.1318), ...]  # List of tuples representing river points in latitude and longitude
jupiter_position = (19.336, 279.99)  # Jupiter's position in latitude and longitude

# Calculate distances from each river point to Jupiter
distances = [geodesic(river_point, jupiter_position).km for river_point in river_points]

# Calculate gravitational forces acting on each river point due to Jupiter
forces = [(G * M_jupiter * m / d**2) for m, d in zip([1e3] * len(distances), distances)]

# Calculate average gravitational force
avg_force = np.mean(forces)

# Correct water level using the average gravitational force (assuming a linear relationship)
water_level_correction = avg_force * 0.01  # Example correction factor of 0.01

# Visualize river points and Jupiter's position on a map
m = folium.Map(location=jupiter_position, zoom_start=4)

for point in river_points:
    folium.Marker(point).add_to(m)

folium.CircleMarker(jupiter_position, radius=5, color='red').add_to(m)

# Save the map as an HTML file
m.save("218.html")