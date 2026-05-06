import pandas as pd
import folium
from geopy.geocoders import Nominatim

# Шаг 1: Сбор данных
# Предположим, у нас есть DataFrame с данными о предприятиях и их потреблении воды.
data = {
    'Название': ['Предприятие A', 'Предприятие B', 'Предприятие C'],
    'Адрес': ['г. Москва, улица Ленина 10', 'г. Санкт-Петербург, проспект Победы 20', 'г. Новосибирск, улица Гагарина 30'],
    'Потребление воды (куб. м/мес)': [5000, 7000, 6000]
}

df = pd.DataFrame(data)

# Шаг 2: Подготовка данных
# В данном случае данные уже подготовлены, но можно добавить дополнительные шаги очистки при необходимости.

# Шаг 3: Геокодирование
geolocator = Nominatim(user_agent="geoapiExercises")

def get_coordinates(address):
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

df['Координаты'] = df['Адрес'].apply(get_coordinates)

# Шаг 4: Создание модели
# В данном случае модель представляет собой DataFrame с географическими координатами и данными о потреблении воды.

# Шаг 5: Визуализация
m = folium.Map(location=[56.0105, 92.8531], zoom_start=4)  # Координаты Новосибирска для примера

for _, row in df.iterrows():
    if row['Координаты']:
        folium.Marker(
            location=row['Координаты'],
            popup=f"{row['Название']}: {row['Потребление воды (куб. м/мес)']} куб. м/мес",
            icon=folium.Icon(color='blue')
        ).add_to(m)

# Шаг 6: Сохранение результата
m.save("45.html")