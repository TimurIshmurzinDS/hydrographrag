import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the shapefile
m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for observation points (WKT coordinates)
observations = [
    {"name": "Observation_2264", "coordinates": wkt.loads("POINT (37.5 55.7)")},
    {"name": "Observation_2247", "coordinates": wkt.loads("POINT (37.6 55.8)")},
    {"name": "Observation_2265", "coordinates": wkt.loads("POINT (37.7 55.9)")}
]

# Add observation points to the map
for obs in observations:
    folium.Marker(location=[obs["coordinates"].y, obs["coordinates"].x], popup=obs["name"]).add_to(m)

# Save the final map
m.save("209.html")