import requests
import folium

# 1. Получение данных о уровнях воды (замените на актуальный источник)
url = "https://example.com/api/water_levels?river=Shyzhyn"  
response = requests.get(url)
data = response.json()

# 2. Определение порогового значения (пример)
high_water_threshold = 3.5  # метры

# 3. Сравнение уровней воды с порогом
for station in data:
    if station["level"] > high_water_threshold:
        print(f"Оповещение: Высокий уровень воды в {station['location']}")

# 4. Визуализация (необязательно)
m = folium.Map(location=[51.5074, 0.1278], zoom_start=12)  # Замените на координаты реки Shyzhyn River

for station in data:
    if station["level"] > high_water_threshold:
        folium.Marker(
            location=[station["latitude"], station["longitude"]],
            popup=f"Высокий уровень воды: {station['level']} м",
            icon=folium.Icon(color="red"),
        ).add_to(m)

m.save("28.html")