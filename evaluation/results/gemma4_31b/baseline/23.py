import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap
from shapely.geometry import LineString, Point

def generate_flood_risk_model():
    # 1. Эмуляция координат реки Prokhodnaya (Центральная точка и русло)
    # В реальном сценарии здесь будет загрузка GeoJSON/Shapefile
    river_coords = [
        [55.123, 37.456], [55.125, 37.460], [55.128, 37.465], 
        [55.132, 37.470], [55.135, 37.475], [55.140, 37.480]
    ]
    river_line = LineString(river_coords)
    
    # 2. Генерация синтетической сетки данных вокруг реки (имитация DEM)
    # Создаем сетку точек вокруг русла для анализа высот и расстояний
    points = []
    risk_values = []
    
    # Создаем область вокруг реки
    for lat in np.linspace(55.11, 55.15, 50):
        for lon in np.linspace(37.44, 37.49, 50):
            p = Point(lon, lat)
            # Расстояние до русла реки (имитация близости к воде)
            dist = p.distance(river_line) * 111000 # Приблизительный перевод в метры
            
            # Имитация высоты над руслом (HAND model)
            # Чем ближе к реке, тем ниже высота. Добавляем случайный шум для рельефа.
            elevation_diff = dist * 0.5 + np.random.uniform(0, 2)
            
            # Расчет индекса риска (0 - низкий, 1 - высокий)
            # Риск высок, если расстояние мало и высота над руслом низкая
            if elevation_diff < 2:
                risk = 1.0
            elif elevation_diff < 5:
                risk = 0.6
            elif elevation_diff < 10:
                risk = 0.3
            else:
                risk = 0.1
                
            points.append([lat, lon])
            risk_values.append(risk)

    # 3. Визуализация с помощью Folium
    # Создаем карту, центрированную на реке
    m = folium.Map(location=[55.13, 37.46], zoom_start=13, tiles='OpenStreetMap')

    # Добавляем русло реки на карту
    folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Prokhodnaya River").add_to(m)

    # Подготовка данных для HeatMap (интенсивность риска)
    heat_data = []
    for i in range(len(points)):
        # Добавляем только точки с риском выше 0.3 для наглядности
        if risk_values[i] > 0.3:
            heat_data.append([points[i][0], points[i][1], risk_values[i]])

    # Добавляем слой тепловой карты рисков
    HeatMap(heat_data, radius=15, blur=10, min_opacity=0.4).add_to(m)

    # Добавляем легенду через HTML
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 160px; height: 90px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; opacity: 0.8; padding: 10px;">
    <b>Риск наводнения:</b><br>
    <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий<br>
    <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний<br>
    <i style="background:yellow; width:10px; height:10px; display:inline-block"></i> Низкий
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение карты
    m.save("23.html")
    print("Modeling complete. Map saved as 23.html")

if __name__ == "__main__":
    generate_flood_risk_model()