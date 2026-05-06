import pandas as pd
import folium

# Загрузка данных
data_2021 = pd.read_csv('shilik_river_temperature_2021.csv')
data_2022 = pd.read_csv('shilik_river_temperature_2022.csv')

# Предположим, что данные имеют следующую структуру:
# data['latitude'], data['longitude'], data['temperature']

# Очистка данных (если необходимо)
data_2021.dropna(subset=['latitude', 'longitude', 'temperature'], inplace=True)
data_2022.dropna(subset=['latitude', 'longitude', 'temperature'], inplace=True)

# Создание карт
m = folium.Map(location=[data_2021['latitude'].mean(), data_2021['longitude'].mean()], zoom_start=10)

# Добавление маркеров для 2021 года
for index, row in data_2021.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Температура в {index}: {row['temperature']}°C",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Добавление маркеров для 2022 года
for index, row in data_2022.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Температура в {index}: {row['temperature']}°C",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("53.html")