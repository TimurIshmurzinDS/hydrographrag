import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
import folium

# Load elevation data (replace with actual file path)
with rasterio.open('elevation_data.tif') as src:
    elevation = src.read(1)

# Calculate flow direction (simplified example, requires specialized algorithms for accuracy)
flow_direction = np.gradient(elevation, axis=0, edgeorder='wrap')

# Accumulate flow (simplified example, requires advanced hydrological modeling for accuracy)
accumulation = np.zeros_like(elevation)
for i in range(len(elevation)):
    for j in range(len(elevation[i])):
        if flow_direction[i][j] > 0:
            accumulation[i][j] += 1

# Create Folium map
m = folium.Map(location=[43.25, 76.9], zoom_start=12)

# Color code cells based on accumulated flow (example color scheme)
colorscale = plt.cm.get_cmap('viridis')
for i in range(len(accumulation)):
    for j in range(len(accumulation[i])):
        folium.CircleMarker(location=[src.bounds[1] + i * src.res[1], src.bounds[0] + j * src.res[0]], radius=5, color=colorscale(accumulation[i][j])).add_to(m)

# Save the map
m.save("225.html")