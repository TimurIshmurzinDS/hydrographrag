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

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
byzhy_river = {'name': 'Byzhy River', 'wkt': 'POLYGON((...))'}
tekeli_river = {'name': 'Tekeli River', 'wkt': 'POLYGON((...))'}

# Create a GeoDataFrame from the list of dictionaries
rivers = gpd.GeoDataFrame([byzhy_river, tekeli_river], geometry=gpd.GeoSeries.from_wkt([river['wkt'] for river in rivers]))

# Add rivers to the map
for _, river in rivers.iterrows():
    folium.GeoJson(river, fillColor='blue', color='darkblue', fillOpacity=0.2).add_to(m)

# Save the final map
m.save("119.html")