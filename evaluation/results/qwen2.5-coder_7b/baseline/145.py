import folium
from folium.plugins import MarkerCluster

# Подключение к базе данных (пример использования SQLAlchemy)
from sqlalchemy import create_engine, text

# Пример строки подключения к базе данных
DATABASE_URL = "postgresql://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)

# SQL запрос для получения данных о датчиках и реках
query = """
SELECT 
    sensors.id AS sensor_id,
    sensors.latitude AS sensor_lat,
    sensors.longitude AS sensor_lon,
    rivers.id AS river_id,
    rivers.name AS river_name,
    rivers.geometry AS river_geometry
FROM 
    sensors
JOIN 
    river_sensor ON sensors.id = river_sensor.sensor_id
JOIN 
    rivers ON river_sensor.river_id = rivers.id;
"""

# Выполнение запроса и получение данных
with engine.connect() as connection:
    result = connection.execute(text(query))
    data = result.fetchall()

# Создание карты
m = folium.Map(location=[50, 30], zoom_start=4)

# Группировка маркеров датчиков
marker_cluster = MarkerCluster().add_to(m)

# Добавление маркеров датчиков на карту
for row in data:
    sensor_id = row.sensor_id
    sensor_lat = row.sensor_lat
    sensor_lon = row.sensor_lon
    folium.Marker([sensor_lat, sensor_lon], popup=f"Sensor ID: {sensor_id}").add_to(marker_cluster)

# Добавление линий рек на карту
for row in data:
    river_name = row.river_name
    river_geometry = eval(row.river_geometry)  # Преобразование строки в геометрию
    folium.PolyLine(river_geometry, color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты
m.save("145.html")