import pandas as pd
import folium

# Предполагаем, что данные о датчиках находятся в CSV файле 'osek_sensors.csv'
# Структура файла: id, latitude, longitude, status (0 - норма, 1 - неисправность)

# Шаг 1: Чтение данных
data = pd.read_csv('osek_sensors.csv')

# Шаг 2: Предварительная обработка данных
# Проверка на пропуски
data.dropna(inplace=True)

# Шаг 3: Анализ состояния датчиков
# Предположим, что статус 1 означает неисправность
malfunctioning_sensors = data[data['status'] == 1]

# Шаг 4: Визуализация результатов
# Создание карты с центром в среднем значении широты и долготы датчиков
map_center = [data['latitude'].mean(), data['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=10)

# Добавление маркеров для всех датчиков
for index, row in data.iterrows():
    if row['status'] == 0:
        color = 'green'
    else:
        color = 'red'
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Датчик ID: {row['id']} Статус: {'Норма' if row['status'] == 0 else 'Неисправность'}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Шаг 5: Сохранение карты
m.save("68.html")