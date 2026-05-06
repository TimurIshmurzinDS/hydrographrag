import requests
import folium

# Предположим, что у нас есть API для получения данных о глубине воды в реках.
# Для примера создадим функцию, которая будет имитировать получение данных из API.
def get_water_depth_data():
    # Имитация ответа от API
    return {
        "river": "Koktal",
        "latitude": 42.8603,
        "longitude": 75.1951,
        "depth": 2.5  # Глубина воды в метрах
    }

# Получение данных о глубине воды
data = get_water_depth_data()

# Создание карты с помощью folium
m = folium.Map(location=[data['latitude'], data['longitude']], zoom_start=13)

# Добавление маркера на карту с информацией о глубине воды
folium.Marker(
    location=[data['latitude'], data['longitude']],
    popup=f"Глубина воды в реке {data['river']}: {data['depth']} м",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в файл
m.save("11.html")

print(f"Текущая глубина воды в реке {data['river']}: {data['depth']} м")