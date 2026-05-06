import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium

# Загрузка данных о реке Аксу
river_data = gpd.read_file('аксу.shp')

# Загрузка данных о населённых пунктах в зоне риска наводнения
population_data = pd.read_csv('населенные_пункты.csv')

# Преобразование данных в геометрические объекты (геометрии)
river_gdf = gpd.GeoDataFrame(river_data, geometry='geometry')
population_gdf = gpd.GeoDataFrame(population_data, geometry=gpd.points_from_xy(population_data['long'], population_data['lat']))

# Создание слоя риска наводнения
risk_layer = river_gdf.copy()
risk_layer['risk'] = risk_layer.apply(lambda row: calculate_risk(row), axis=1)

# Функция для расчета риска наводнения
def calculate_risk(row):
    # Расстояние до ближайшего водоема или точки с высоким риском наводнения
    distance_to_river = row['geometry'].distance(Point(55.7558, 37.6173))
    
    # Факторы риска (высота берега и скорость течения реки)
    risk_factors = row['height'] * row['speed']
    
    return distance_to_river + risk_factors

# Создание интерактивной карты с помощью библиотеки Folium
m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)

# Добавление слоя риска наводнения на карту
folium.GeoJson(risk_layer.to_crs(epsg=3857).to_json(), name='risk_layer').add_to(m)

# Добавление слоев населённых пунктов на карту
population_gdf.to_crs(epsg=3857).plot(ax=m, color='red', alpha=0.5)
folium.Marker([55.7558, 37.6173], popup='Река Аксу').add_to(m)

# Сохранение карты в файл
m.save("229.html")