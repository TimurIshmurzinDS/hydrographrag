import folium
import pandas as pd
from datetime import datetime

# 1. Симуляция данных гидрологического мониторинга
# В реальном сценарии здесь будет запрос к базе данных (PostGIS) или API
data = {
    'station_id': [101, 102, 103, 104, 105],
    'station_name': ['Верхний Проходной', 'Средний Проходной', 'Мостовой пост', 'Нижний Проходной', 'Устьевой пост'],
    'river': ['Prokhodnaya River'] * 5,
    'lat': [62.1234, 62.2567, 62.3890, 62.5123, 62.6456],
    'lon': [35.1122, 35.2345, 35.3567, 35.4789, 35.5901],
    'water_level': [1.25, 2.10, 1.85, 3.40, 4.12], # уровень в метрах
    'timestamp': ['2023-10-27 10:00', '2023-10-27 10:00', '2023-10-27 09:00', '2023-10-27 10:00', '2023-10-27 08:00']
}

df = pd.DataFrame(data)

# 2. Фильтрация данных по конкретной реке
river_name = "Prokhodnaya River"
river_df = df[df['river'] == river_name]

# 3. Создание карты
# Центрируем карту по средним координатам постов
center_lat = river_df['lat'].mean()
center_lon = river_df['lon'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles='OpenStreetMap')

# 4. Добавление постов на карту
for index, row in river_df.iterrows():
    # Определяем цвет маркера в зависимости от уровня воды (условно)
    # Зеленый < 2.0, Желтый 2.0-3.0, Красный > 3.0
    if row['water_level'] < 2.0:
        color = 'green'
    elif row['water_level'] < 3.0:
        color = 'orange'
    else:
        color = 'red'
    
    # Формируем текст для всплывающего окна
    popup_text = (
        f"<b>Пост:</b> {row['station_name']}<br>"
        f"<b>Уровень воды:</b> {row['water_level']} м.<br>"
        f"<b>Дата замера:</b> {row['timestamp']}"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Добавление легенды (простой текстовый элемент)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Уровни воды:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Норма<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Повышенный<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# 5. Сохранение результата
m.save("67.html")

print("Карта успешно создана и сохранена в файл 67.html")