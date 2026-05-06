import folium
import numpy as np
import pandas as pd
from folium.plugins import HeatMap

def generate_river_system():
    """
    Симуляция координат рек Sarykan и Shyzhyn.
    В реальном проекте здесь будет загрузка GeoJSON/Shapefile.
    """
    # Примерные координаты (Центральная Азия/Казахстан регион)
    sarykan_coords = [
        [50.1, 62.5], [50.2, 62.7], [50.3, 62.9], [50.5, 63.1], [50.7, 63.3]
    ]
    shyzhyn_coords = [
        [50.4, 62.6], [50.5, 62.8], [50.6, 63.0], [50.8, 63.2]
    ]
    return sarykan_coords, shyzhyn_coords

def simulate_flood_risk_data(river_coords):
    """
    Генерация синтетических данных о риске вокруг рек.
    Имитирует анализ DEM и близости к руслу.
    """
    risk_points = []
    for coord in river_coords:
        lat, lon = coord
        # Создаем облако точек вокруг каждой точки реки для имитации зоны риска
        for _ in range(20):
            # Случайное смещение (имитация поймы)
            d_lat = np.random.normal(0, 0.02)
            d_lon = np.random.normal(0, 0.02)
            
            # Вес риска: чем ближе к центру (реке), тем выше значение
            # В реальности здесь был бы расчет: Risk = f(Elevation, Slope, Distance)
            risk_value = np.random.uniform(0.5, 1.0) if abs(d_lat) < 0.01 else np.random.uniform(0.1, 0.5)
            
            risk_points.append([lat + d_lat, lon + d_lon, risk_value])
            
    return risk_points

def main():
    # 1. Получаем данные рек
    sarykan, shyzhyn = generate_river_system()
    
    # 2. Генерируем данные по рискам (имитация GIS-анализа)
    sarykan_risk = simulate_flood_risk_data(sarykan)
    shyzhyn_risk = simulate_flood_risk_data(shyzhyn)
    all_risks = sarykan_risk + shyzhyn_risk
    
    # 3. Инициализация карты Folium
    # Центрируем карту по средним координатам
    m = folium.Map(location=[50.4, 62.9], zoom_start=9, tiles='OpenStreetMap')
    
    # 4. Визуализация рек (Синие линии)
    folium.PolyLine(sarykan, color="blue", weight=4, opacity=0.8, tooltip="Sarykan River").add_to(m)
    folium.PolyLine(shyzhyn, color="blue", weight=4, opacity=0.8, tooltip="Shyzhyn River").add_to(m)
    
    # 5. Визуализация зон риска с помощью HeatMap
    # HeatMap принимает список [lat, lon, weight]
    HeatMap(all_risks, radius=15, blur=20, gradient={0.4: 'blue', 0.65: 'yellow', 1: 'red'}).add_to(m)
    
    # 6. Добавление маркеров критических узлов (имитация)
    critical_points = [
        {"loc": [50.3, 62.9], "name": "Критический узел A (Sarykan)"},
        {"loc": [50.6, 63.0], "name": "Критический узел B (Shyzhyn)"},
    ]
    
    for pt in critical_points:
        folium.Marker(
            location=pt["loc"], 
            popup=pt["name"], 
            icon=folium.Icon(color='red', icon='exclamation-triangle', prefix='fa')
        ).add_to(m)
    
    # Добавление легенды через HTML
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда рисков:</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий риск<br>
     <i style="background:yellow; width:10px; height:10px; display:inline-block"></i> Средний риск<br>
     <i style="background:blue; width:10px; height:10px; display:inline-block"></i> Низкий риск<br>
     <span style="color:blue; font-weight:bold">___</span> Русло реки
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Сохранение результата
    m.save("163.html")
    print("Отчет по рискам успешно сгенерирован и сохранен в файл 163.html")

if __name__ == "__main__":
    main()