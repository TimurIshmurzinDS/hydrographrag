import folium
import json

# Пример данных о уровне воды в реках Или и Каратал (GeoJSON)
water_level_data = '''
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Или", "level": 120},
            "geometry": {"type": "Point", "coordinates": [76.85, 43.25]}
        },
        {
            "type": "Feature",
            "properties": {"name": "Каратал", "level": 90},
            "geometry": {"type": "Point", "coordinates": [76.90, 43.15]}
        }
    ]
}
'''

# Парсинг данных
data = json.loads(water_level_data)

# Создание карты с центром в районе рек Или и Каратал
m = folium.Map(location=[43.20, 76.88], zoom_start=10)

# Добавление маркеров на карту
for feature in data['features']:
    name = feature['properties']['name']
    level = feature['properties']['level']
    coordinates = feature['geometry']['coordinates']
    
    # Создание всплывающей подсказки с информацией о уровне воды
    popup_text = f"Река: {name}<br>Уровень воды: {level} м"
    
    # Добавление маркера на карту
    folium.Marker(
        location=coordinates,
        popup=popup_text,
        icon=folium.Icon(color='blue' if level < 100 else 'red')
    ).add_to(m)

# Сохранение карты в HTML-файл
m.save("9.html")