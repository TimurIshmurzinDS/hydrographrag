import pandas as pd
import folium

# Пример данных о местоположении датчиков и их статусе
data = {
    'latitude': [51.234, 51.235, 51.236],
    'longitude': [76.345, 76.346, 76.347],
    'status': ['Active', 'Inactive', 'Active']
}

# Создание DataFrame
df = pd.DataFrame(data)

# Создание карты с центром в Talgar River (пример координат)
m = folium.Map(location=[51.235, 76.346], zoom_start=13)

# Добавление маркеров на карту
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Status: {row['status']}",
        icon=folium.Icon(color='green' if row['status'] == 'Active' else 'red')
    ).add_to(m)

# Сохранение карты
m.save("10.html")