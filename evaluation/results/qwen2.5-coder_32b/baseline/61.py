import folium
import requests
from branca.colormap import LinearColormap

# Предположим, что данные датчиков доступны по URL в формате GeoJSON
url = "https://example.com/aksu_river_water_level_sensors.geojson"

# Загрузка данных с сервера
response = requests.get(url)
data = response.json()

# Создание карты Folium, центрированной на примерных координатах реки Аксу (42.8657, 79.1304)
m = folium.Map(location=[42.8657, 79.1304], zoom_start=10)

# Определение цветовой карты для статуса датчиков
colormap = LinearColormap(['green', 'red'], vmin=0, vmax=1)
colormap.add_to(m)

# Добавление слоя с данными датчиков на карту
for feature in data['features']:
    properties = feature['properties']
    coordinates = feature['geometry']['coordinates']
    
    # Предположим, что статус датчика хранится в поле 'status' (1 - работает, 0 - не работает)
    status = properties.get('status', 0)
    
    # Определение цвета маркера на основе статуса
    color = 'green' if status == 1 else 'red'
    
    # Добавление маркера на карту с поп-апом, содержащим информацию о датчике
    folium.CircleMarker(
        location=coordinates,
        radius=8,
        popup=f"ID: {properties.get('id', 'N/A')}\nStatus: {'Работает' if status == 1 else 'Не работает'}",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Добавление легенды на карту
folium.map.LayerControl().add_to(m)
colormap.caption = "Статус датчиков уровня воды"
colormap.add_to(m)

# Сохранение карты в файл 61.html
m.save("61.html")