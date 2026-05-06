import folium
import json

# Загрузите данные о местоположении сенсоров в формате GeoJSON
with open('sensors_data.geojson', 'r') as f:
    sensors_data = json.load(f)

active_sensors = []

# Проанализировать каждый сенсор в данных
for sensor in sensors_data['features']:
    if sensor['properties']['status'] == 'active':
        active_sensors.append(sensor['geometry']['coordinates'])

# Создать карту и центрировать ее на реке Byzhy River
m = folium.Map(location=[51.5074, -0.1278], zoom_start=13)

# Установить слой для отображения активных сенсоров
for sensor in active_sensors:
    folium.CircleMarker(location=sensor, radius=5, color='green').add_to(m)

# Сохранить карту как "71.html"
m.save("71.html")