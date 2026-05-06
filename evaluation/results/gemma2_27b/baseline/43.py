import geopandas as gpd
from shapely.geometry import Polygon
import folium

# Загрузка данных о реке Аягоз (замените на актуальные пути к файлам)
river_data = gpd.read_file("path/to/river_ayagoz.shp")

# Загрузка данных о землепользовании (замените на актуальные пути к файлам)
landuse_data = gpd.read_file("path/to/landuse.shp")

# Фильтрация зон орошения
irrigation_zones = landuse_data[landuse_data["type"] == "Irrigation"]

# Расчет площади зон орошения
total_area = irrigation_zones.geometry.area.sum()

# Установка среднего расхода воды на единицу площади (в м³/га/год)
average_water_consumption = 5000  

# Расчет объема воды, выделяемой на орошение
total_water_volume = total_area * average_water_consumption / 10000 # Перевод в м³

# Создание карты
m = folium.Map(location=[43.5, 79.5], zoom_start=8)

# Добавление данных о реке на карту
folium.GeoJson(river_data).add_to(m)

# Добавление зон орошения на карту
folium.GeoJson(irrigation_zones).add_to(m)

# Добавление текстовой информации о объеме воды
folium.Marker([43.5, 79.5], popup=f"Объем воды на орошение: {total_water_volume:.2f} м³").add_to(m)

# Сохранение карты
m.save("43.html")