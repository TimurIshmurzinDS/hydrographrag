import pandas as pd
import folium

# Предположим, что данные о датчиках хранятся в CSV-файле 'sensors_data.csv'
# Структура файла: id, latitude, longitude, river, status (0 - без ошибок, 1 - с ошибками)

# Шаг 1: Чтение данных
data = pd.read_csv('sensors_data.csv')

# Шаг 2: Фильтрация данных для датчиков в районе рек Бутак и Сарыкан
filtered_data = data[data['river'].isin(['Бутак', 'Сарыкан'])]

# Шаг 3: Анализ данных на наличие ошибок
working_sensors = filtered_data[filtered_data['status'] == 0]
faulty_sensors = filtered_data[filtered_data['status'] == 1]

# Шаг 4: Создание карты с помощью folium
m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=12)

# Добавление маркеров для работающих датчиков (зеленые)
for idx, row in working_sensors.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Датчик {row['id']} - Работает без ошибок",
        icon=folium.Icon(color='green')
    ).add_to(m)

# Добавление маркеров для датчиков с ошибками (красные)
for idx, row in faulty_sensors.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Датчик {row['id']} - Ошибки в передаче данных",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Шаг 5: Сохранение карты
m.save("147.html")