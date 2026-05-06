import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, FeatureGroup, GeoJson

# Загрузка данных о уровне воды из CSV файлов
bayankol_data = pd.read_csv("bayankol_river_data.csv", index_col="date")
kishi_almaty_data = pd.read_csv("kishi_almaty_river_data.csv", index_col="date")

# Расчет волатильности для каждой реки
bayankol_volatility = (bayankol_data["max_level"] - bayankol_data["min_level"])
kishi_almaty_volatility = (kishi_almaty_data["max_level"] - kishi_almaty_data["min_level"])

# Вывод средней годовой волатильности
print("Средняя годовая волатильность Bayankol River:", bayankol_volatility.mean())
print("Средняя годовая волатильность Kishi Almaty River:", kishi_almaty_volatility.mean())

# Визуализация данных на карте (необязательно)
m = Map(location=[42.87, 79.61], zoom_start=8)

# Добавление данных о реках на карту
bayankol_river_geojson = GeoJson("bayankol_river_geojson.geojson")
kishi_almaty_river_geojson = GeoJson("kishi_almaty_river_geojson.geojson")

FeatureGroup(name="Bayankol River").add_to(m)
FeatureGroup(name="Kishi Almaty River").add_to(m)

# Сохранение карты
m.save("134.html")