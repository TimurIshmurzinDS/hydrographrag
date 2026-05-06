import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries with water level data (replace this with actual data)
water_level_data = [{'Date': '2021-01-01', 'Water_level_Valuecm': 50}, {'Date': '2021-01-02', 'Water_level_Valuecm': 52}]

# Add water level data to the map as markers
for point in water_level_data:
    folium.Marker([point['Latitude'], point['Longitude']], popup=f"Date: {point['Date']}, Water Level: {point['Water_level_Valuecm']} cm").add_to(m)

# Save the final map
m.save("213.html")