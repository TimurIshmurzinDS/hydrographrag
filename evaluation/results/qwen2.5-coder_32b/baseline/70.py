import pandas as pd
import folium

# Предположим, что у нас есть CSV файл с данными о гидрологических уровнях на реке Шарын.
# Файл содержит столбцы: 'station_id', 'latitude', 'longitude', 'water_level'
data = pd.read_csv('sharyn_river_data.csv')

# Определим критический уровень воды (например, 10 метров)
critical_level = 10.0

# Фильтруем данные для постов с уровнем выше критического
critical_stations = data[data['water_level'] > critical_level]

# Создаем карту folium с центром в средних координатах всех станций
map_center = [data['latitude'].mean(), data['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=10)

# Добавляем маркеры для всех гидрологических постов
for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Станция: {row['station_id']}, Уровень воды: {row['water_level']} м",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Добавляем маркеры для критических гидрологических постов
for index, row in critical_stations.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Станция: {row['station_id']}, Уровень воды: {row['water_level']} м",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохраняем карту в файл
m.save("70.html")