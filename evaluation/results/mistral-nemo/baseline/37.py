import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Load data
water_data = pd.read_csv('water_data.csv')
geo_data = gpd.read_file('geo_data.shp')
agro_data = pd.read_csv('agro_data.csv')

# Prepare water data
water_data['geometry'] = [Point(xy) for xy in zip(water_data['longitude'], water_data['latitude'])]

# Perform geospatial analysis
gdf_water = gpd.GeoDataFrame(water_data, geometry='geometry')
gdf_agro = gpd.GeoDataFrame(agro_data, geometry=Point(agro_data['longitude'], agro_data['latitude']))

# Calculate distance from river
gdf_agro['distance_to_river'] = gdf_water.distance(gdf_agro.geometry)

# Perform statistical analysis
usage_stats = agro_data.groupby('complex_id')['water_usage'].mean()

# Create map
m = folium.Map(location=[51.5074, -0.1278], zoom_start=9)

# Add river to map
river_geometry = gdf_water.unary_union
folium.GeoJson(river_geometry).add_to(m)

# Add agro complexes to map with color based on water usage
for index, row in gdf_agro.iterrows():
    folium.CircleMarker(location=[row.geometry.y, row.geometry.x],
                        radius=5,
                        color='blue' if row['water_usage'] > usage_stats.mean() else 'green',
                        fill=True).add_to(m)

# Save map
m.save("37.html")