import folium
from folium.plugins import MarkerCluster
import pandas as pd

# Пример данных (замените на реальные данные)
data = {
    'Latitude': [43.21, 43.56, 44.09],
    'Longitude': [76.89, 77.12, 77.45],
    'Risk Level': ['High', 'Medium', 'Low']
}

# Создание DataFrame
df = pd.DataFrame(data)

# Создание карты
m = folium.Map(location=[43.5, 77.0], zoom_start=8)

# Добавление маркеров с рисками
marker_cluster = MarkerCluster().add_to(m)
for index, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Risk Level: {row['Risk Level']}",
        icon=folium.Icon(color='red' if row['Risk Level'] == 'High' else 'orange' if row['Risk Level'] == 'Medium' else 'green')
    ).add_to(marker_cluster)

# Сохранение карты
m.save("163.html")