import pandas as pd
import folium

# Загрузить данные о гидрологических постах и их уровнях
data = pd.read_csv('sharyn_river_stations.csv')

# Вычислить среднее значение всех уровней и стандартное отклонение
mean_level = data['level'].mean()
std_dev = data['level'].std()

# Определить критический уровень
critical_level = mean_level + 2 * std_dev

# Найти посты, которые показывают уровень выше критического уровня
critical_stations = data[data['level'] > critical_level]

# Создать карту с использованием библиотеки folium
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=8)

# Добавить маркеры для критических гидрологических постов на карту
for index, station in critical_stations.iterrows():
    folium.Marker([station['latitude'], station['longitude']], popup=f'Station ID: {station["id"]}, Level: {station["level"]}').add_to(m)

# Сохранить карту как HTML-файл
m.save("70.html")