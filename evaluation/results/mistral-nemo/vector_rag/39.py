import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(gdf.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    gdf,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Assuming average water consumption for irrigation is 1500 m³/km² (this value may vary)
irrigation_water_consumption = 1500

# Calculate the total volume of water used for irrigation in the basin
total_irrigation_water_volume = gdf['Basin_are_km²'] * irrigation_water_consumption

# Print or use the result as needed
print(f"Общий объем воды, используемый для полива в бассейне реки Или: {total_irrigation_water_volume.sum()} м³")

# Save the final map
m.save("39.html")