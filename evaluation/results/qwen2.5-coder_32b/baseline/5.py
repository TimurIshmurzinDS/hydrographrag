import requests
import folium

# Предположим, что у нас есть API, который возвращает данные о водном уровне
api_url = "https://example.com/api/water_level?river=Prokhodnaya_River"

# Получаем данные из API
response = requests.get(api_url)
data = response.json()

# Извлекаем текущий уровень воды и координаты точки из данных
current_water_level = data['water_level']
latitude = data['coordinates']['latitude']
longitude = data['coordinates']['longitude']

# Создаем интерактивную карту с помощью folium
m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Добавляем маркер на карту с информацией о текущем уровне воды
folium.Marker(
    [latitude, longitude],
    popup=f"Текущий уровень воды: {current_water_level} м",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохраняем карту в файл 5.html
m.save("5.html")

print(f"Карта сохранена как 5.html с текущим уровнем воды: {current_water_level} м")