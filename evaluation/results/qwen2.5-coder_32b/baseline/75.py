import folium
from folium.plugins import MarkerCluster

# Пример координат метеостанций на реках Tentek River и Sharyn River
data = {
    'Tentek River': [
        {'name': 'Метеостанция 1', 'coordinates': [42.85, 79.05], 'status': 'активна'},
        {'name': 'Метеостанция 2', 'coordinates': [43.00, 79.20], 'status': 'неактивна'},
    ],
    'Sharyn River': [
        {'name': 'Метеостанция 1', 'coordinates': [50.60, 82.10], 'status': 'активна'},
        {'name': 'Метеостанция 2', 'coordinates': [50.75, 82.30], 'status': 'активна'},
    ]
}

# Создание карты
m = folium.Map(location=[46.5, 81.0], zoom_start=6)

# Добавление маркеров для Tentek River
marker_cluster_tentek = MarkerCluster(name='Tentek River')
for station in data['Tentek River']:
    color = 'green' if station['status'] == 'активна' else 'red'
    folium.Marker(
        location=station['coordinates'],
        popup=f"{station['name']} - {station['status']}",
        icon=folium.Icon(color=color)
    ).add_to(marker_cluster_tentek)

marker_cluster_tentek.add_to(m)

# Добавление маркеров для Sharyn River
marker_cluster_sharyn = MarkerCluster(name='Sharyn River')
for station in data['Sharyn River']:
    color = 'green' if station['status'] == 'активна' else 'red'
    folium.Marker(
        location=station['coordinates'],
        popup=f"{station['name']} - {station['status']}",
        icon=folium.Icon(color=color)
    ).add_to(marker_cluster_sharyn)

marker_cluster_sharyn.add_to(m)

# Добавление слоя управления
folium.LayerControl().add_to(m)

# Сохранение карты в файл
m.save("75.html")