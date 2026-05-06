import folium
import pandas as pd

# Загрузка данных о паводках (замените на ваш файл)
data = pd.read_csv("flood_data.csv")

# Создание карты
m = folium.Map(location=[43.25, 76.9], zoom_start=10)

# Добавление слоя реки Улькен Алматы (замените на ваш слой)
folium.GeoJson("ulken_almaty_river.geojson", name="River").add_to(m)

# Визуализация данных о паводках
for index, row in data.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"Год: {row['year']}<br>Уровень воды: {row['water_level']} м",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("24.html")