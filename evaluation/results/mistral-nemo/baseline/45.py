import folium
from geopy.geocoders import Nominatim

# Сбор данных о потреблении воды предприятий вдоль реки Кумбель
water_consumption_data = [
    {"name": "Предприятие 1", "address": "Адрес предприятия 1", "consumption": 50},
    {"name": "Предприятие 2", "address": "Адрес предприятия 2", "consumption": 30},
    # Добавьте другие предприятия и их данные о потреблении воды
]

# Геокодирование адресов предприятий для получения географических координат
geolocator = Nominatim(user_agent="water_consumption")
for data in water_consumption_data:
    location = geolocator.geocode(data["address"])
    data["latitude"] = location.latitude
    data["longitude"] = location.longitude

# Создание карты реки Кумбель с использованием библиотеки folium
m = folium.Map(location=[51.7098, 56.2734], zoom_start=12)  # Координаты реки Кумбель в качестве начальной точки карты

# Добавление маркеров предприятий на карту с размером маркера пропорциональным объему потребления воды
for data in water_consumption_data:
    folium.CircleMarker(
        location=[data["latitude"], data["longitude"]],
        radius=data["consumption"] / 10,
        fill=True,
        color="blue",
        fill_opacity=0.5,
        popup=f"{data['name']}\nПотребление воды: {data['consumption']} куб. м"
    ).add_to(m)

# Сохранение карты в файл HTML
m.save("45.html")