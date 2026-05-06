import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are historical data about flow, create a hardcoded list of dictionaries with coordinates (WKT) and corresponding flow values
historical_flow_data = [
    {'wkt': 'POINT(123.456 78.901)', 'flow_value': 100},
    {'wkt': 'POINT(234.567 89.012)', 'flow_value': 150}
]

# Add historical flow data to the map (if available)
for data in historical_flow_data:
    folium.Marker(wkt.loads(data['wkt']), popup=f'Flow value: {data["flow_value"]}').add_to(m)

# Save the final map
m.save("193.html")