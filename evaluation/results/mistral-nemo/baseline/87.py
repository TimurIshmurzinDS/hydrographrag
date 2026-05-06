import pandas as pd
import folium

# Шаг 1: Подготовьте данные
current_data = pd.read_csv('current_river_flow.csv')
historical_data = pd.read_csv('historical_flood_data.csv')

# Шаг 2: Преобразование данных (в данном примере мы просто используем средние значения)
current_avg = current_data['flow'].mean()
historical_avg = historical_data['flow'].mean()

# Шаг 3: Сравнение данных
difference = abs(current_avg - historical_avg)

# Шаг 4: Визуализация результатов
m = folium.Map(location=[55.7821, 61.8469], zoom_start=10)  # Координаты реки Prokhodnaya River

folium.CircleMarker(
    location=[55.7821, 61.8469],
    radius=difference/10,
    color='blue',
    fill=True,
    fill_opacity=0.5
).add_to(m)

# Шаг 5: Сохранение результатов
m.save("87.html")