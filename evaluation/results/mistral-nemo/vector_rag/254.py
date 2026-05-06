import geopandas as gpd
import folium
from shapely import wkt

# a) Load the shapefile and initialize the map
data = gpd.read_file(r"data/basin_data.shp")
data = data.to_crs('EPSG:4326')
m = folium.Map(location=data.centroid, tiles='CartoDB positron')
folium.GeoJson(data[['geometry']], fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# b) If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
shilik_river_wkt = "LINESTRING(...)"
shilik_river_coords = [{'type': 'Feature', 'geometry': wkt.loads(shilik_river_wkt)}]

# c) Calculate river meandering index and generate random numbers based on it
for feature in shilik_river_coords:
    river_line = feature['geometry']
    # Calculate meandering index (example: using simple length comparison)
    meandering_index = len(river_line.coords) / river_line.length

    # Generate random number based on the meandering index
    random_number = meandering_index * 100

# Save the final map
m.save("254.html")