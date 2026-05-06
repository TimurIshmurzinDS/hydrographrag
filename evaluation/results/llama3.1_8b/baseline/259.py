import folium
import geopandas as gpd
from shapely.geometry import Point

# Загрузка данных о реке Баскан
baskun_river = gpd.read_file('path/to/baskun_river.shp')

# Геопозиционирование данных о космическом корабле
spacecraft_position = Point(40.7128, -74.0060)  # примерная позиция космического корабля

# Анализ доступности воды в реке Баскан для использования в качестве охладителя
available_water = baskun_river.sjoin_nearest(spacecraft_position, how='inner')

# Оценка соответствия требованиям охлаждающей системы космического корабля
if available_water['distance'].values[0] < 1000:  # примерное расстояние для охлаждения двигателей
    print("Вода в реке Баскан доступна для использования в качестве охладителя.")
else:
    print("Вода в реке Баскан не доступна для использования в качестве охладителя.")

# Создание интерактивной карты
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
folium.Marker([40.7128, -74.0060], popup='Космический корабль').add_to(m)
folium.Polygon(available_water.geometry.values[0].exterior.coords[:], color='red', fill=True).add_to(m)

# Сохранение карты
m.save("259.html")