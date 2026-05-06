import pandas as pd
import folium
from geopy.geocoders import Nominatim

# Пример данных о темпах инфляции для различных регионов
data = {
    'Регион': ['Актюбинск', 'Караганда', 'Шымкент', 'Талас'],
    'Темп инфляции (%)': [7.5, 6.2, 8.1, 5.9]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Инициализация геокодера
geolocator = Nominatim(user_agent="geoapiExercises")

# Функция для получения координат по названию региона
def get_coordinates(region):
    location = geolocator.geocode(region)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Получение координат для каждого региона
df['Координаты'] = df['Регион'].apply(get_coordinates)

# Создание карты с центром в Шымкенте
m = folium.Map(location=[47.2315, 69.4085], zoom_start=6)

# Добавление маркеров на карту
for _, row in df.iterrows():
    if row['Координаты']:
        folium.CircleMarker(
            location=row['Координаты'],
            radius=10,
            color='red' if row['Темп инфляции (%)'] > 7 else 'green',
            fill=True,
            fill_color='red' if row['Темп инфляции (%)'] > 7 else 'green',
            popup=f"Регион: {row['Регион']}<br>Темп инфляции: {row['Темп инфляции (%)']}%"
        ).add_to(m)

# Сохранение карты в файл
m.save("272.html")