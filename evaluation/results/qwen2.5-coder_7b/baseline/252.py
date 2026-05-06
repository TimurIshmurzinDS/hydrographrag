import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о географических координатах реки Дос (замените на реальные данные)
coordinates = [
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [56.0123, 90.4567]}, "properties": {"time": "2023-04-01T00:00:00Z"}},
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [56.0124, 90.4568]}, "properties": {"time": "2023-04-02T00:00:00Z"}},
    # Добавьте больше точек по мере необходимости
]

# Создание карты
m = folium.Map(location=[56.0123, 90.4567], zoom_start=12)

# Добавление геоданных на карту
TimestampedGeoJson(coordinates, period="PT1D").add_to(m)

# Сохранение карты в HTML файл
m.save("252.html")