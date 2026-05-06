import folium
import pandas as pd
import numpy as np

# 1. Подготовка данных
# Координаты реки Текес (приблизительный маршрут от истоков к слиянию с Иртышом)
# Данные являются репрезентативными для демонстрации GIS-моделирования
data = {
    'station_name': ['Верхний Текес', 'Средний Текес', 'Нижний Текес', 'Устье Текеса', 'Пост-1', 'Пост-2'],
    'lat': [48.5, 48.3, 48.1, 47.9, 48.4, 48.2],
    'lon': [84.5, 84.2, 83.8, 83.5, 84.3, 84.0],
    'spring_discharge': [45.2, 88.7, 120.5, 155.3, 62.1, 101.4] # Расход воды в м3/с
}

df = pd.DataFrame(data)

# 2. Инициализация карты
# Центрируем карту на среднем расположении реки Текес
m = folium.Map(location=[48.2, 84.0], zoom_start=7, tiles='OpenStreetMap')

# 3. Отрисовка русла реки (упрощенная линия)
river_coords = [
    [48.5, 84.5], [48.4, 84.3], [48.3, 84.2], 
    [48.2, 84.0], [48.1, 83.8], [47.9, 83.5]
]
folium.PolyLine(river_coords, color="blue", weight=4, opacity=0.7, tooltip="Русло реки Текес").add_to(m)

# 4. Функция для определения цвета маркера в зависимости от расхода воды
def get_color(discharge):
    if discharge < 60:
        return 'green'
    elif discharge < 110:
        return 'orange'
    else:
        return 'red'

# 5. Добавление точек замера расхода воды на карту
for index, row in df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['spring_discharge'] / 5, # Размер зависит от объема воды
        popup=f"Станция: {row['station_name']}<br>Весенний расход: {row['spring_discharge']} м³/с",
        color=get_color(row['spring_discharge']),
        fill=True,
        fill_color=get_color(row['spring_discharge']),
        fill_opacity=0.6,
        tooltip=row['station_name']
    ).add_to(m)

# Добавление легенды (простой текстовый элемент через HTML)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 100px; 
     border:2px solid black; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Расход воды (весна):</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкий (< 60 м³/с)<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний (60-110 м³/с)<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий (> 110 м³/с)
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# 6. Сохранение результата
m.save("17.html")

print("Modeling complete. The map has been saved as 17.html")