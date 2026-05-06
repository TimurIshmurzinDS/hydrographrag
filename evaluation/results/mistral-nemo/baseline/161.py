import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
import numpy as np
import folium

# Load DTM data
dtm = rasterio.open('dtm.tif')
dtm_data = dtm.read(1)

# Load river data
rivers = gpd.read_file('rivers.shp')

# Calculate flood potential zones based on DTM and rivers data
flood_zones = np.where(dtm_data < rivers['elevation'].values, 1, 0)
flood_zones_gdf = gpd.GeoDataFrame({'flood_potential': flood_zones}, geometry=rivers.geometry)

# Calculate water flow using a suitable model (not implemented here)
# ...

# Analyze risk areas based on flood zones and critical infrastructure data
# ...

# Create map with folium
m = folium.Map(location=[43.2, 70.2], zoom_start=10)

# Add flood potential zones to the map
folium.GeoJson(flood_zones_gdf[['flood_potential', 'geometry']]).add_to(m)

# Save the map as HTML file
m.save("161.html")