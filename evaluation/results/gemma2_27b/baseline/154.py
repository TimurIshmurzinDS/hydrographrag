# Import necessary libraries
import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
import folium

# Load DEM data for both rivers (replace with actual file paths)
dem_shynzhaly = rasterio.open("path/to/dem_shynzhaly.tif")
dem_shyzhyn = rasterio.open("path/to/dem_shyzhyn.tif")

# Load river data (replace with actual file formats and paths)
river_shynzhaly = np.loadtxt("path/to/river_shynzhaly.csv", delimiter=",")
river_shyzhyn = np.loadtxt("path/to/river_shyzhyn.csv", delimiter=",")

# Implement chosen flood model (example using HEC-RAS)
# ... (code for HEC-RAS model implementation, calibration and simulation)

# Extract flood extent data from the model output
flood_extent_shynzhaly = # ... (code to extract flood zone polygons)
flood_extent_shyzhyn = # ... (code to extract flood zone polygons)

# Create a map using folium
m = folium.Map(location=[43.0, 75.0], zoom_start=8)

# Add river data to the map
folium.GeoJson(data=river_shynzhaly).add_to(m)
folium.GeoJson(data=river_shyzhyn).add_to(m)

# Add flood extent polygons to the map
folium.GeoJson(data=flood_extent_shynzhaly, style_geojson={'color': 'red', 'opacity': 0.5}).add_to(m)
folium.GeoJson(data=flood_extent_shyzhyn, style_geojson={'color': 'blue', 'opacity': 0.5}).add_to(m)

# Save the map as "154.html"
m.save("154.html")