import pandas as pd
import folium

# Шаг 1: Подготовка данных
shilik_data = pd.read_csv('shilik_river_data.csv')
sharyn_data = pd.read_csv('sharyn_river_data.csv')

# Шаг 2: Обработка данных
shilik_series = shilik_data.set_index('year')['water_level']
sharyn_series = sharyn_data.set_index('year')['water_level']

# Шаг 3: Анализ данных
shilik_mean = shilik_series.mean()
sharyn_mean = sharyn_series.mean()

# Шаг 4: Визуализация результатов
m = folium.Map(location=[43.2, 76.9], zoom_start=8)

folium.Marker([43.5, 77.0], popup='Shilik River').add_to(m)
folium.Marker([43.1, 76.8], popup='Sharyn River').add_to(m)

if shilik_mean > sharyn_mean:
    folium.CircleMarker(location=[43.5, 77.0], radius=10, color='red', fill=True).add_to(m)
else:
    folium.CircleMarker(location=[43.5, 77.0], radius=10, color='green', fill=True).add_to(m)

if sharyn_mean > shilik_mean:
    folium.CircleMarker(location=[43.1, 76.8], radius=10, color='red', fill=True).add_to(m)
else:
    folium.CircleMarker(location=[43.1, 76.8], radius=10, color='green', fill=True).add_to(m)

# Шаг 5: Сохранение результатов
m.save("135.html")