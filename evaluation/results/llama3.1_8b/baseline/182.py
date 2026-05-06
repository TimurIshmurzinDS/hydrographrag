import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium

# Сбор и подготовка данных
river_network = gpd.read_file('river_network.shp')
water_resources = gpd.read_file('water_resources.shp')
climate_data = pd.read_csv('climate_data.csv')
agriculture_data = pd.read_csv('agriculture_data.csv')

# Обработка данных
river_network['geometry'] = river_network['geometry'].apply(lambda x: x.simplify(0.001))
water_resources['geometry'] = water_resources['geometry'].apply(lambda x: x.simplify(0.001))

# Анализ рисков дефицита воды
def calculate_water_risk(geometry, climate_data, agriculture_data):
    # Оценка рисков дефицита воды на основе данных о климате и сельскохозяйственной деятельности
    water_risk = 0
    for point in geometry:
        climate = climate_data.loc[climate_data['geometry'].contains(point), 'precipitation']
        agriculture = agriculture_data.loc[agriculture_data['geometry'].contains(point), 'yield']
        water_risk += (1 - climate) * (1 + agriculture)
    return water_risk / len(geometry)

river_network['water_risk'] = river_network['geometry'].apply(lambda x: calculate_water_risk(x, climate_data, agriculture_data))

# Визуализация результатов
m = folium.Map(location=[53.5, 60], zoom_start=8)
folium.Choropleth(
    geo_data=river_network,
    name='water_risk',
    data=river_network,
    columns=['geometry', 'water_risk'],
    key_on='feature.properties.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)
m.save("182.html")