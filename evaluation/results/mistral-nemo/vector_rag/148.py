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

# Create a hardcoded list of dictionaries for coordinates (WKT)
water_level_data = [
    {'geometry': wkt.loads('POINT(123.456 78.901)'), 'Water_level_Value': 123, 'Date_water_level_Value': '2022-01-01', 'Observation': 'above Bartogay Reservoir'},
    {'geometry': wkt.loads('POINT(234.567 89.012)'), 'Water_level_Value': 234, 'Date_water_level_Value': '2022-01-02', 'Observation': 'above Bartogay Reservoir'},
    {'geometry': wkt.loads('POINT(345.678 90.123)'), 'Water_level_Value': 345, 'Date_water_level_Value': '2022-01-03', 'Observation': 'above Bartogay Reservoir'}
]

# Create a GeoDataFrame for water level data
water_level_gdf = gpd.GeoDataFrame(water_level_data)

# Filter data for rivers with increased water levels based on the latest measurements
increased_water_levels = water_level_gdf[water_level_gdf['Water_level_Value'] > 100]

# Add points to the map for rivers with increased water levels
for _, row in increased_water_levels.iterrows():
    folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5, color='red').add_to(m)

# Save the final map
m.save("148.html")