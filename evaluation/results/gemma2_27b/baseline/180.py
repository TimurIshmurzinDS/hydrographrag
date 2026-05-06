import geopandas as gpd
import folium

# Загрузка данных о реках
rivers_tekes = gpd.read_file("tekes.shp")
rivers_sarykan = gpd.read_file("sarykan.shp")

# Объединение сетей
merged_rivers = gpd.overlay(rivers_tekes, rivers_sarykan, how='union')

# Анализ конфигурации сети
total_length = merged_rivers.geometry.length.sum()
number_of_junctions = len(merged_rivers.where(merged_rivers.geometry.type == 'MultiLineString'))

# Создание карты
m = folium.Map(location=[43.0, 75.0], zoom_start=8)

# Добавление рек на карту
folium.GeoJson("tekes.shp").add_to(m)
folium.GeoJson("sarykan.shp").add_to(m)

# Сохранение карты
m.save("180.html")