import geopandas as gpd
import folium
from shapely import wkt
import random

# 1. Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium Map using the centroid of the basin
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Logic for generating random numbers based on Shilik River sinuosity
# Hypothetical Sinuosity Index (SI) for Shilik River (L_actual / L_straight)
# In a real scenario, this would be calculated from the river's geometry
shilik_sinuosity_index = 1.45 

def generate_sinuosity_based_values(si, count=5):
    """
    Generates random numbers where the sinuosity index acts as a 
    scaling factor for the distribution.
    """
    results = []
    for _ in range(count):
        # Generate a random value centered around the sinuosity index
        # simulating morphological variance
        val = random.uniform(si * 0.8, si * 1.2)
        results.append(round(val, 4))
    return results

# Generate the random numbers
random_values = generate_sinuosity_based_values(shilik_sinuosity_index)
print(f"Generated random values based on Shilik River sinuosity ({shilik_sinuosity_index}): {random_values}")

# 5. Save the final map strictly as 254.html
m.save("254.html")