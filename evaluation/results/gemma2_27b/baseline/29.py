import pandas as pd
import folium

# Загрузка данных о расходе воды (замените 'data.csv' на фактический файл)
data = pd.read_csv('data.csv')

# Фильтрация данных по весеннему паводку (пример, измените даты)
spring_flood_data = data[(data['Date'] >= '2023-03-15') & (data['Date'] <= '2023-05-15')]

# Создание карты
m = folium.Map(location=[43.8, 76.9], zoom_start=10)  # Замените координаты на координаты реки

# Добавление маркеров с данными о расходе воды
for index, row in spring_flood_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']], 
        popup=f"Дата: {row['Date']}<br>Расход: {row['Discharge']} м³/с"
    ).add_to(m)

# Сохранение карты
m.save("29.html")