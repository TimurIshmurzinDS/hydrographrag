import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the shapefile
# Calculate the centroid of the basin polygon
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

m = folium.Map(
    location=[mean_lat, mean_lon], 
    tiles='CartoDB positron', 
    zoom_start=6
)

# 3. Add the basin to the map using folium.GeoJson
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# 4. Coordinates handling
# The context provided entities (Koksu River, Emel River, Koktal River) 
# but did not provide specific WKT coordinates. 
# If coordinates were provided, they would be added here as a hardcoded list.
# Example structure if coordinates existed:
# points = [{"name": "Koksu River", "coords": [lat, lon]}, ...]
# for pt in points:
#     folium.Marker([pt["coords"][0], pt["coords"][1]], popup=pt["name"]).add_to(m)

# 5. SAVE the final map strictly using the required filename
m.save("196.html")