import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Load data for 2015 and 2023 water levels
data_2015 = pd.read_csv('water_levels_2015.csv')
data_2023 = pd.read_csv('water_levels_2023.csv')

# Create GeoDataFrame for each year
gdf_2015 = gpd.GeoDataFrame(data_2015, geometry=gpd.points_from_xy(data_2015['longitude'], data_2015['latitude']))
gdf_2023 = gpd.GeoDataFrame(data_2023, geometry=gpd.points_from_xy(data_2023['longitude'], data_2023['latitude']))

# Calculate peak water levels for each year
peak_2015 = gdf_2015['water_level'].max()
peak_2023 = gdf_2023['water_level'].max()

# Create points for peak water levels
point_2015 = Point(gdf_2015.loc[gdf_2015['water_level'] == peak_2015, 'geometry'].x.values[0], gdf_2015.loc[gdf_2015['water_level'] == peak_2015, 'geometry'].y.values[0])
point_2023 = Point(gdf_2023.loc[gdf_2023['water_level'] == peak_2023, 'geometry'].x.values[0], gdf_2023.loc[gdf_2023['water_level'] == peak_2023, 'geometry'].y.values[0])

# Create GeoDataFrame for peak water levels
peak_gdf = gpd.GeoDataFrame({'year': [2015, 2023], 'water_level': [peak_2015, peak_2023]}, geometry=[point_2015, point_2023])

# Create map with Folium
m = folium.Map(location=[gdf_2015['latitude'].mean(), gdf_2015['longitude'].mean()], zoom_start=9)

for idx, row in peak_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=f'Год: {row.year}<br>Уровень воды: {row.water_level} м').add_to(m)

# Save map as HTML file
m.save("49.html")