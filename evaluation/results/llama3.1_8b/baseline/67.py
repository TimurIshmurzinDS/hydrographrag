import pandas as pd
import folium

# Подключиться к базе данных (в данном случае используем SQLite)
from sqlite3 import connect

# Создать соединение с базой данных
conn = connect('prokhodnaya_river.db')

# Выполнить запрос для получения данных о постах и уровнях воды
cursor = conn.cursor()
query = """
    SELECT p.location, w.level, w.timestamp 
    FROM posts p 
    JOIN water_levels w ON p.id = w.post_id 
    WHERE p.river_name = 'Prokhodnaya River' 
    ORDER BY w.timestamp DESC;
"""
cursor.execute(query)

# Извлечь данные из результата запроса
data = cursor.fetchall()

# Создать карту с использованием библиотеки folium
m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)

# Добавить маркеры на карту для каждого поста
for row in data:
    location = row[0]
    level = row[1]
    timestamp = row[2]
    
    # Создать маркер с информацией о уровне воды и времени измерения
    folium.Marker(location=location, 
                  popup=f'Уровень воды: {level} м\nВремя измерения: {timestamp}',
                  icon=folium.Icon(color='blue')).add_to(m)

# Сохранить карту в файле HTML
m.save("67.html")

# Закрыть соединение с базой данных
conn.close()