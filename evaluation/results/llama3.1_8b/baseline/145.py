import pandas as pd
from folium import Map, Marker, Icon
from folium.plugins import HeatMap

# Подключаемся к базе данных (в этом случае используем SQLite)
import sqlite3
conn = sqlite3.connect('database.db')

# Получаем список всех рек из базы данных
rivers_df = pd.read_sql_query("SELECT * FROM rivers", conn)

# Для каждой реки получаем список датчиков и их текущее состояние
sensors_df = pd.read_sql_query("""
    SELECT r.name, s.latitude, s.longitude, s.status 
    FROM sensors s JOIN rivers r ON s.river_id = r.id
""", conn)

# Создаем географическую карту
m = Map(location=[55.7558, 37.6173], zoom_start=10)

# Добавляем маркеры для каждого датчика на карте
for index, row in sensors_df.iterrows():
    icon_color = 'green' if row['status'] == 'good' else 'red'
    Marker(location=[row['latitude'], row['longitude']], 
           icon=Icon(color=icon_color)).add_to(m)

# Добавляем легенду к карте
legend_html = """
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; height: 50px; background-color: #f2f2f2; padding: 10px;">
        <b>Легенда:</b>
        <br>
        <span style="color: green;">Здоровое состояние</span>
        <br>
        <span style="color: red;">Поврежденное состояние</span>
    </div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Сохраняем карту в файл
m.save("145.html")