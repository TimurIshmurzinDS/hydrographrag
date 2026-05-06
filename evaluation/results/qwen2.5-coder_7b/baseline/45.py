import pandas as pd
import folium

# Пример данных (замените на реальные данные)
data = {
    'Name': ['Factory A', 'Factory B', 'Factory C'],
    'Latitude': [37.123, 37.456, 37.789],
    'Longitude': [-122.123, -122.456, -122.789],
    'WaterConsumption': [1000, 1500, 2000]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Создание карты
m = folium.Map(location=[37.5, -122.5], zoom_start=10)

# Добавление маркеров на карте с информацией о потреблении воды
for index, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Name']}<br>Потребление воды: {row['WaterConsumption']} м³",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("45.html")