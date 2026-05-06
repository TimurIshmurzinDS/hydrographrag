import folium
from folium import plugins
import numpy as np

# 1. Имитация геоданных для реки Шарын и туристических объектов
# Координаты примерно соответствуют району каньона Шарын
river_coords = [
    [43.55, 79.20], [43.56, 79.25], [43.58, 79.30], 
    [43.60, 79.35], [43.62, 79.40], [43.65, 79.45]
]

tourism_spots = [
    {"name": "Вход в каньон", "lat": 43.555, "lon": 79.22, "type": "Infrastructure"},
    {"name": "Смотровая площадка 'Долина замков'", "lat": 43.585, "lon": 79.32, "type": "Viewpoint"},
    {"name": "Эко-кемпинг", "lat": 43.61, "lon": 79.38, "type": "Accommodation"},
    {"name": "Нижний маршрут (у реки)", "lat": 43.64, "lon": 79.43, "type": "Trail"},
    {"name": "Музей природы", "lat": 43.54, "lon": 79.18, "type": "Infrastructure"},
]

# 2. Создание карты
m = folium.Map(location=[43.60, 79.30], zoom_start=11, tiles="CartoDB positron")

# 3. Визуализация реки
river_line = folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Река Шарын")
river_line.add_to(m)

# 4. Моделирование гидрологических зон (Буферы)
# В реальности здесь используется гео-анализ (geopandas), здесь имитируем кругами вокруг сегментов
for coord in river_coords:
    # Зона критического обмеления (малый радиус) - влияние на эстетику
    folium.Circle(
        location=coord,
        radius=500, 
        color="orange",
        fill=True,
        fill_opacity=0.2,
        tooltip="Зона влияния обмеления (Риск: Эстетика/Экология)"
    ).add_to(m)
    
    # Зона возможного разлива (большой радиус) - влияние на безопасность
    folium.Circle(
        location=coord,
        radius=2000, 
        color="red",
        fill=True,
        fill_opacity=0.1,
        tooltip="Зона возможного паводка (Риск: Инфраструктура)"
    ).add_to(m)

# 5. Анализ влияния на туристические объекты
for spot in tourism_spots:
    # Простая логика определения риска на основе близости к реке
    # (В реальном GIS это делается через spatial join)
    dist_to_river = np.random.uniform(0.1, 3.0) # Имитация расстояния в км
    
    if dist_to_river < 0.5:
        risk_level = "Высокий"
        color = "red"
        impact = "Прямая угроза затопления или пересыхания"
    elif dist_to_river < 1.5:
        risk_level = "Средний"
        color = "orange"
        impact = "Возможное изменение ландшафта"
    else:
        risk_level = "Низкий"
        color = "green"
        impact = "Минимальное влияние"

    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=f"<b>{spot['name']}</b><br>Тип: {spot['type']}<br>Риск: {risk_level}<br>Эффект: {impact}",
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

# Добавление легенды
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 250px; height: 150px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда гидрологического риска:</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий риск (Затопление)<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний риск (Обмеление)<br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкий риск<br>
     <i style="background:blue; width:10px; height:10px; display:inline-block"></i> Русло реки Шарын
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение результата
m.save("194.html")

print("Modeling complete. Map saved as 194.html")