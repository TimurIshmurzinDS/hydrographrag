import pandas as pd
import folium
from folium.plugins import HeatMapWithTime

# Шаг 1: Подготовка данных
shilik_data = pd.read_csv('shilik_river_discharge.csv')
kishi_almaty_data = pd.read_csv('kishi_almaty_river_discharge.csv')

# Шаг 2: Анализ данных (в данном примере мы просто вычисляем средний сток для каждого месяца)
shilik_seasonal_change = shilik_data.groupby(pd.to_datetime(shilik_data['date']).dt.month).mean()
kishi_almaty_seasonal_change = kishi_almaty_data.groupby(pd.to_datetime(kishi_almaty_data['date']).dt.month).mean()

# Шаг 3: Визуализация данных
m = folium.Map(location=[43.25, 76.9], zoom_start=8)

# Добавляем данные о стоке реки Шилик на карту
for idx, row in shilik_seasonal_change.iterrows():
    folium.CircleMarker(
        location=[43.25, 76.9],
        radius=row['discharge'] / 10,
        fill=True,
        color='blue',
        fill_opacity=0.5
    ).add_to(m)

# Добавляем данные о стоке реки Киши Алматы на карту
for idx, row in kishi_almaty_seasonal_change.iterrows():
    folium.CircleMarker(
        location=[43.25, 76.9],
        radius=row['discharge'] / 10,
        fill=True,
        color='red',
        fill_opacity=0.5
    ).add_to(m)

# Шаг 4: Сохранение результатов
m.save("126.html")