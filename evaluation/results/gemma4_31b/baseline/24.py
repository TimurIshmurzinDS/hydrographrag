import folium
import pandas as pd
import numpy as np

# 1. Подготовка синтетических исторических данных (имитация данных гидропостов)
# В реальном сценарии здесь будет загрузка из CSV или API гидрологической службы
data = {
    'year': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'water_level_m': [2.1, 2.5, 1.8, 3.2, 2.0, 3.8, 2.4, 2.9, 3.1], # Уровень воды в метрах
    'lat': [43.15, 43.16, 43.17, 43.18, 43.19, 43.20, 43.21, 43.22, 43.23],
    'lon': [76.85, 76.86, 76.87, 76.88, 76.89, 76.90, 76.91, 76.92, 76.93],
    'severity': ['Low', 'Medium', 'Low', 'High', 'Low', 'Critical', 'Medium', 'High', 'High']
}

df = pd.DataFrame(data)

# Координаты русла реки (упрощенная аппроксимация для визуализации)
river_coords = [
    [43.14, 76.84], [43.15, 76.85], [43.16, 76.86], [43.17, 76.87], 
    [43.18, 76.88], [43.19, 76.89], [43.20, 76.90], [43.21, 76.91], 
    [43.22, 76.92], [43.23, 76.93], [43.24, 76.94]
]

# 2. Инициализация карты
# Центрируем карту на районе реки Большая Алматинка
m = folium.Map(location=[43.19, 76.89], zoom_start=12, tiles='OpenStreetMap')

# 3. Отрисовка русла реки
folium.PolyLine(
    locations=river_coords, 
    color='blue', 
    weight=5, 
    opacity=0.7, 
    tooltip='Русло реки Большая Алматинка'
).add_to(m)

# 4. Функция для определения цвета маркера в зависимости от уровня паводка
def get_color(severity):
    colors = {
        'Low': 'green',
        'Medium': 'yellow',
        'High': 'orange',
        'Critical': 'red'
    }
    return colors.get(severity, 'blue')

# 5. Добавление исторических данных о паводках на карту
for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['water_level_m'] * 3, # Радиус зависит от уровня воды
        color=get_color(row['severity']),
        fill=True,
        fill_color=get_color(row['severity']),
        fill_opacity=0.6,
        popup=f"Год: {row['year']}<br>Уровень: {row['water_level_m']}м<br>Статус: {row['severity']}",
        tooltip=f"Паводок {row['year']} г."
    ).add_to(m)

# Добавление легенды (через HTML)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Уровень паводка:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкий<br>
     <i style="background:yellow; width:10px; height:10px; display:inline-block"></i> Средний<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Высокий<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Критический
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# 6. Сохранение результата
m.save("24.html")

print("Карта с историческими данными паводков успешно создана и сохранена в файл 24.html")