import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=gdf.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Define coordinates for Karatal River and Lake Ulken Almaty using WKT
karatal_wkt = 'POINT(71.45 43.28)'
ulken_almaty_wkt = 'POINT(71.52 43.26)'

# Create Shapely points from WKT
karatal_point = wkt.loads(karatal_wkt)
ulken_almaty_point = wkt.loads(ulken_almaty_wkt)

# Calculate distance between the two points using Shapely's distance method
distance = karatal_point.distance(ulken_almaty_point)

# Print the result
print(f"Расстояние между точками впадения реки Каратал и озера Улькен Алматы составляет {distance:.2f} километров.")

# Save the final map
m.save("102.html")