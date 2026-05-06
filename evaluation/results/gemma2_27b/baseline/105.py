import pandas as pd
from folium import Map, GeoJson

# Загрузить данные о реках
rivers = pd.read_csv("rivers.csv")

# Определить регион (пример)
region_coordinates = [40.5, 75.5, 41.5, 76.5] # Координаты региона в формате [lat_min, lon_min, lat_max, lon_max]

# Фильтрация по координатам
rivers_in_region = rivers[
    (rivers["latitude"] >= region_coordinates[0]) & 
    (rivers["longitude"] >= region_coordinates[1]) &
    (rivers["latitude"] <= region_coordinates[2]) &
    (rivers["longitude"] <= region_coordinates[3])
]

# Вывести список рек в регионе
print(rivers_in_region)

# Визуализация (необязательно)
m = Map(location=[41, 76], zoom_start=8) # Создать карту с центром в регионе

GeoJson(rivers_in_region[['latitude', 'longitude']]).add_to(m)

m.save("105.html")