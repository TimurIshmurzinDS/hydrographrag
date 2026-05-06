import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Load data for 2022 and 2023
data_2022 = pd.read_csv('sarykan_river_water_levels_2022.csv')
data_2023 = pd.read_csv('sarykan_river_water_levels_2023.csv')

# Create GeoDataFrame for 2022
geometry_2022 = [Point(xy) for xy in zip(data_2022['longitude'], data_2022['latitude'])]
gdf_2022 = gpd.GeoDataFrame(data_2022, geometry=geometry_2022)

# Create GeoDataFrame for 2023
geometry_2023 = [Point(xy) for xy in zip(data_2023['longitude'], data_2023['latitude'])]
gdf_2023 = gpd.GeoDataFrame(data_2023, geometry=geometry_2023)

# Create map for 2022
m_2022 = folium.Map(location=[data_2022['latitude'].mean(), data_2022['longitude'].mean()], zoom_start=10)
for _, row in gdf_2022.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=f'Уровень воды в 2022 году: {row["water_level"]} м').add_to(m_2022)

# Create map for 2023
m_2023 = folium.Map(location=[data_2023['latitude'].mean(), data_2023['longitude'].mean()], zoom_start=10)
for _, row in gdf_2023.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=f'Уровень воды в 2023 году: {row["water_level"]} м').add_to(m_2023)

# Save maps
m_2022.save("2022.html")
m_2023.save("2023.html")