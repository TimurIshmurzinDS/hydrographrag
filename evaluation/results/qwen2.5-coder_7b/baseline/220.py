import pandas as pd
import folium

# Загрузка данных из CSV файла
data = pd.read_csv('batareyka_river_data.csv')

# Предварительная обработка данных
# Удаление выбросов и заполнение пропущенных значений
data.dropna(inplace=True)
data.fillna(method='ffill', inplace=True)

# Анализ данных
print(data.describe())

# Создание модели корабля (пример: простая модель на основе средних значений)
average_speed = data['speed'].mean()
average_direction = data['direction'].mode()[0]

# Визуализация модели на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=13)

for index, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Speed: {row['speed']}, Direction: {row['direction']}").add_to(m)

# Добавление модели корабля на карту (пример: простая модель)
folium.CircleMarker(
    location=[data['latitude'].mean(), data['longitude'].mean()],
    radius=10,
    color='red',
    fill=True,
    fill_color='red',
    popup=f"Average Speed: {average_speed}, Average Direction: {average_direction}"
).add_to(m)

# Сохранение карты
m.save("220.html")