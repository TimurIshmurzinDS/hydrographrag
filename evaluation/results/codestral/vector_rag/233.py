import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map with basin centroid
m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries with water level data (replace this with actual data)
water_levels = [{'Date': '2022-01-01', 'Water Level': 5.6}, {'Date': '2022-01-02', 'Water Level': 5.8}]

# Add water level markers to the map
for level in water_levels:
    folium.CircleMarker(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], radius=level['Water Level'], color='blue', fill=True, fill_color='blue').add_to(m)

# Save the final map
m.save("233.html")