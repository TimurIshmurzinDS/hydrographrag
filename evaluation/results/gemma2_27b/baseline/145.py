import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузить данные о реках из базы данных (замените на ваш код)
rivers = pd.read_sql("SELECT * FROM rivers", engine)

# Загрузить данные о датчиках из базы данных (замените на ваш код)
sensors = pd.read_sql("SELECT * FROM sensors", engine)

# Преобразовать координаты датчиков в геометрические точки
geometry = [Point(xy) for xy in zip(sensors["longitude"], sensors["latitude"])]
sensors["geometry"] = geometry
sensors = gpd.GeoDataFrame(sensors, crs="EPSG:4326")

# Создать карту с помощью folium
m = folium.Map(location=[45, 0], zoom_start=4)

# Добавить точки датчиков на карту
for index, row in sensors.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=row["sensor_type"]).add_to(m)

# Сохранить карту в файл
m.save("145.html")