import folium
from shapely.geometry import Polygon, Point

# Пример данных: высота над уровнем моря (H) для каждой точки в бассейне и на реке
# В реальном случае эти данные должны быть получены из источников геоданных
data = {
    'points': [
        {'lat': 43.123, 'lon': 76.543, 'H': 100},
        {'lat': 43.124, 'lon': 76.544, 'H': 98},
        # Добавьте больше точек
    ],
    'FP': 100  # Уровень паводка
}

# Создание карты
m = folium.Map(location=[data['points'][0]['lat'], data['points'][0]['lon']], zoom_start=12)

# Определение зон паводкового затопления
flooded_areas = []
for point in data['points']:
    if point['H'] <= data['FP']:
        flooded_areas.append((point['lat'], point['lon']))

# Добавление точек на карте
for point in data['points']:
    folium.Marker([point['lat'], point['lon']], popup=f"Height: {point['H']}").add_to(m)

# Добавление зон паводкового затопления на карту
folium.CircleMarker(
    location=[sum(flooded_area[0] for flooded_area in flooded_areas) / len(flooded_areas),
              sum(flooded_area[1] for flooded_area in flooded_areas) / len(flooded_areas)],
    radius=5,
    color='red',
    fill=True,
    fill_color='red',
    popup="Flooded Area"
).add_to(m)

# Сохранение карты
m.save("161.html")