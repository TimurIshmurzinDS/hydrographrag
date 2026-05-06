import pandas as pd
import folium

# Пример загрузки данных (замените на реальные данные)
data = {
    'River': ['Tentek River', 'Temirlik River'],
    'Sensor_ID': [101, 202],
    'Level': [5.3, 4.8],
    'Status': ['Normal', 'Warning']
}
df = pd.DataFrame(data)

# Создание карты
m = folium.Map(location=[40.7128, -74.0060], zoom_start=5)

# Добавление маркеров на карте
for index, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"River: {row['River']}, Sensor ID: {row['Sensor_ID']}, Level: {row['Level']}, Status: {row['Status']}",
        icon=folium.Icon(color='red' if row['Status'] == 'Warning' else 'green')
    ).add_to(m)

# Сохранение карты
m.save("72.html")