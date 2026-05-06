import geopandas as gpd
from shapely.geometry import Point
import folium

# Load river data (replace with actual file path)
rivers = gpd.read_file("river_data.shp")

# Create a list of potential mining sites (replace with actual coordinates)
mining_sites = [Point(47.25, 83.05), Point(47.15, 83.15)]

# Calculate distances from mining sites to rivers
for site in mining_sites:
    distances = []
    for river in rivers:
        distance = site.distance(river)
        distances.append((distance, river))

# Sort distances and identify closest river for each site
closest_rivers = [sorted(distances)[0][1] for site in mining_sites]

# Create a map using folium
m = folium.Map(location=[47.25, 83.05], zoom_start=10)

# Add rivers to the map
folium.GeoJson(rivers).add_to(m)

# Add mining sites and highlight closest river
for site in mining_sites:
    folium.Marker(location=[site.y, site.x]).add_to(m)
    closest_river = closest_rivers[mining_sites.index(site)]
    folium.GeoJson(closest_river).add_to(m)

# Save the map
m.save("247.html")