import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd

def generate_shynzhaly_model():
    # 1. Координаты примерного расположения реки Шынжалы (Центральная Азия/Казахстан)
    # Примечание: Координаты упрощены для демонстрации модели
    river_start = [45.5, 62.0] 
    river_end = [45.2, 62.5]
    
    # Генерируем точки русла реки
    lats = np.linspace(river_start[0], river_end[0], 50)
    lons = np.linspace(river_start[1], river_end[1], 50)
    river_coords = list(zip(lats, lons))

    # 2. Симуляция точек водозабора (Consumption Points)
    water_intakes = [
        {"name": "Station A", "coords": [45.4, 62.2], "volume": "High"},
        {"name": "Station B", "coords": [45.3, 62.35], "volume": "Medium"},
        {"name": "Station C", "coords": [45.25, 62.4], "volume": "High"},
    ]

    # 3. Симуляция анализа NDVI (здоровье растительности)
    # Создаем данные: чем ближе к точке водозабора ниже по течению, тем ниже NDVI
    ecosystem_data = []
    for lat, lon in river_coords:
        # Имитируем падение индекса NDVI от 0.8 (здоровый) до 0.3 (деградировавший)
        # В реальности здесь был бы расчет: NDVI_2023 - NDVI_2018
        dist_from_start = np.sqrt((lat - river_start[0])**2 + (lon - river_start[1])**2)
        ndvi_loss = 0.1 + (dist_from_start * 0.5) + np.random.normal(0, 0.05)
        ndvi_loss = min(max(ndvi_loss, 0.1), 0.7) # Ограничение значений
        ecosystem_data.append([lat, lon, ndvi_loss])

    # Создание карты
    m = folium.Map(location=[45.35, 62.25], zoom_start=9, tiles="CartoDB positron")

    # Рисуем русло реки
    folium.PolyLine(river_coords, color="blue", weight=4, opacity=0.7, tooltip="Река Шынжалы").add_to(m)

    # Добавляем тепловую карту деградации экосистемы (на основе потери NDVI)
    # Формат HeatMap: [[lat, lon, weight], ...]
    heat_data = [[point[0], point[1], point[2]] for point in ecosystem_data]
    HeatMap(heat_data, name="Деградация растительности (NDVI Loss)", 
            gradient={0.2: 'green', 0.4: 'yellow', 0.6: 'orange', 1: 'red'}).add_to(m)

    # Добавляем маркеры точек водозабора
    for intake in water_intakes:
        color = 'red' if intake['volume'] == 'High' else 'orange'
        folium.CircleMarker(
            location=intake['coords'],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"Водозабор: {intake['name']}<br>Объем: {intake['volume']}"
        ).add_to(m)

    # Добавляем легенду через HTML
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 250px; height: 120px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; opacity: 0.8; padding: 10px;">
        <b>Легенда анализа:</b><br>
        <i style="background:blue; width:10px; height:10px; display:inline-block"></i> Русло реки<br>
        <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий водозабор<br>
        <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний водозабор<br>
        <span style="color:red">Красные зоны</span>: Высокая потеря NDVI
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение карты
    m.save("36.html")
    print("Modeling complete. Map saved as 36.html")

if __name__ == "__main__":
    generate_shynzhaly_model()