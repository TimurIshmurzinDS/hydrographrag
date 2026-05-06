import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries containing coordinates (WKT) of Butak village observations
observations = [{'name': 'Observation 1', 'coordinates': 'POINT (37.65489 55.75206)'},
                {'name': 'Observation 2', 'coordinates': 'POINT (37.65589 55.75306)'},
                # Add more observations as needed
]

# Convert WKT coordinates to Shapely Point objects and add them to the map
for observation in observations:
    point = wkt.loads(observation['coordinates'])
    folium.Marker([point.y, point.x], popup=observation['name']).add_to(m)

# Save the final map
m.save("192.html")