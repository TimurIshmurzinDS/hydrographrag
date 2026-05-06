import pandas as pd
import folium

# Загрузка данных об уровнях воды (замените на ваши файлы)
data_2022 = pd.read_csv("sarykan_water_levels_2022.csv")
data_2023 = pd.read_csv("sarykan_water_levels_2023.csv")

# Создание карты
m = folium.Map(location=[42.5, 71.5], zoom_start=10)  # Установите координаты реки Sarykan

# Добавление слоя реки (замените на ваш GeoJSON файл)
folium.GeoJson("sarykan_river.geojson", name="Sarykan River").add_to(m)

# Визуализация уровней воды за 2022 год
folium.plugins.HeatMap(data_2022[['latitude', 'longitude', 'water_level']]).add_to(m)

# Визуализация уровней воды за 2023 год
folium.plugins.HeatMap(data_2023[['latitude', 'longitude', 'water_level']]).add_to(m)

# Сохранение карты
m.save("46.html")