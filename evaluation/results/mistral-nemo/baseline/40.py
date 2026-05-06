import pandas as pd
from scipy.interpolate import Rbf
import folium

# Шаг 1: Подготовка данных
data = pd.read_csv('water_quality_data.csv')  # Замените 'water_quality_data.csv' на путь к вашему файлу данных
longitudes = data['longitude']
latitudes = data['latitude']
pollution_levels = data['pollution_level']

# Шаг 2: Геостатистическое интерполирование
interpolator = Rbf(longitudes, latitudes, pollution_levels)
xi = [74.6158, 74.6309, 74.6461]  # Замените на координаты точек, где вы хотите предсказать уровень загрязнения
yi = [43.2522, 43.2673, 43.2824]
zi = interpolator(xi, yi)

# Шаг 3: Визуализация
m = folium.Map(location=[43.25, 74.63], zoom_start=12)  # Замените на координаты центра карты и уровень масштабирования

for i in range(len(longitudes)):
    folium.CircleMarker(
        location=(latitudes[i], longitudes[i]),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

for i in range(len(xi)):
    folium.CircleMarker(
        location=(yi[i], xi[i]),
        radius=7,
        color='red',
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

m.save("40.html")