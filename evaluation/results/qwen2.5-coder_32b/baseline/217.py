import pandas as pd
import folium

# Предположим, что у нас есть данные с датчиков Kishi Almaty River в формате CSV
# Данные должны содержать столбцы: 'latitude', 'longitude', 'temperature', 'humidity', 'precipitation'

# Загрузка данных
data = pd.read_csv('kishi_almaty_river_data.csv')

# Определение оптимальных условий для кактусов:
# Предположим, что оптимальные условия: температура от 15 до 30 градусов Цельсия,
# влажность менее 40%, осадки менее 20 мм в месяц

optimal_conditions = (data['temperature'] >= 15) & (data['temperature'] <= 30) & \
                     (data['humidity'] < 40) & (data['precipitation'] < 20)

# Фильтрация данных по оптимальным условиям
optimal_locations = data[optimal_conditions]

# Создание карты с помощью folium
m = folium.Map(location=[43.2567, 76.9285], zoom_start=10)  # Координаты Алматы

# Добавление маркеров на карту для оптимальных мест
for _, row in optimal_locations.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Температура: {row['temperature']}°C, Влажность: {row['humidity']}%, Осадки: {row['precipitation']} мм",
        icon=folium.Icon(color='green')
    ).add_to(m)

# Сохранение карты в файл
m.save("217.html")