import pandas as pd
import folium
from sqlalchemy import create_engine

# Шаг 1: Подключение к базе данных
# Предположим, что используется PostgreSQL. Необходимо заменить параметры подключения на актуальные.
db_url = "postgresql://username:password@host:port/database_name"
engine = create_engine(db_url)

# Шаг 2: Загрузка данных
query = """
SELECT 
    sensor_id,
    river_name,
    latitude,
    longitude,
    status,  -- Предположим, что статус датчика хранится в поле 'status'
    measurement_value  -- Пример поля с показаниями датчиков
FROM 
    sensors_data;
"""
df = pd.read_sql(query, engine)

# Шаг 3: Обработка данных
# Проверка на пропущенные значения и удаление строк с ними
df.dropna(subset=['latitude', 'longitude', 'status'], inplace=True)

# Пример преобразования статуса в числовой формат для удобства визуализации
status_mapping = {'работает': 1, 'не работает': 0}
df['status_code'] = df['status'].map(status_mapping)

# Шаг 4: Визуализация на карте
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=5)

for _, row in df.iterrows():
    color = 'green' if row['status_code'] == 1 else 'red'
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Датчик ID: {row['sensor_id']}<br>Река: {row['river_name']}<br>Статус: {row['status']}<br>Показание: {row['measurement_value']}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Шаг 5: Сохранение карты
m.save("145.html")