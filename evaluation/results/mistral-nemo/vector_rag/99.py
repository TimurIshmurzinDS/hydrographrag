import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
ulken_almaty_source = {"type": "Point", "coordinates": [71.45, 43.26]} # Example coordinates for Ulken Almaty source
urjar_source = {"type": "Point", "coordinates": [70.98, 43.56]} # Example coordinates for Urjar source

# Add the sources to the map
folium.Marker(location=ulken_almaty_source['coordinates'], popup='Улькен Алматы').add_to(m)
folium.Marker(location=urjar_source['coordinates'], popup='Уржар').add_to(m)

# Save the final map
m.save("99.html")