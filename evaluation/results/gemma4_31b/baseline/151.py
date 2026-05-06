import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point

def generate_flood_risk_model():
    # 1. Координаты рек (упрощенные аппроксимации для демонстрации модели)
    # Ili River (примерный путь к озеру Балхаш)
    ili_coords = [
        (43.2, 78.5), (43.5, 80.0), (43.8, 82.0), (43.7, 84.0), (43.5, 86.0)
    ]
    # Bayankol River (примерный путь)
    bayankol_coords = [
        (43.0, 81.0), (43.2, 81.5), (43.4, 82.2)
    ]

    rivers = {
        "Ili River": LineString(ili_coords),
        "Bayankol River": LineString(bayankol_coords)
    }

    # 2. Создание сетки точек для анализа территории вокруг рек
    # Определяем границы области
    lat_min, lat_max = 42.5, 44.5
    lon_min, lon_max = 78.0, 87.0
    
    # Шаг сетки (чем меньше, тем точнее, но медленнее)
    step = 0.1 
    lats = np.arange(lat_min, lat_max, step)
    lons = np.arange(lon_min, lon_max, step)

    risk_data = []

    # 3. Моделирование риска для каждой точки сетки
    for lat in lats:
        for lon in lons:
            p = Point(lon, lat)
            
            # Вычисляем минимальное расстояние до любой из рек
            min_dist = min([p.distance(line) for line in rivers.values()])
            
            # Симуляция топографического фактора (в реальном GIS берется из DEM)
            # Предположим, что риск выше в определенных широтах (низины)
            elevation_factor = np.sin(lat) * np.cos(lon) 
            
            # Расчет индекса риска (FRI)
            # Риск обратно пропорционален расстоянию и зависит от "рельефа"
            # Чем меньше min_dist, тем выше риск
            dist_risk = 1.0 / (min_dist + 0.1) 
            
            # Нормализация и взвешивание
            # Мы создаем синтетический вес риска
            risk_score = (dist_risk * 0.7) + (abs(elevation_factor) * 0.3)
            
            # Оставляем только значимые риски для визуализации
            if risk_score > 0.5:
                risk_data.append([lat, lon, risk_score])

    # 4. Визуализация с помощью Folium
    # Центр карты
    m = folium.Map(location=[43.5, 82.0], zoom_start=7, tiles='CartoDB positron')

    # Добавление линий рек на карту
    folium.PolyLine(ili_coords, color="blue", weight=3, opacity=0.8, tooltip="Ili River").add_to(m)
    folium.PolyLine(bayankol_coords, color="cyan", weight=3, opacity=0.8, tooltip="Bayankol River").add_to(m)

    # Добавление тепловой карты рисков
    # HeatMap принимает список [lat, lon, weight]
    HeatMap(risk_data, radius=15, blur=20, min_opacity=0.3).add_to(m)

    # Добавление легенды (текстовое описание)
    folium.geocode = "Flood Risk Analysis: Ili & Bayankol Rivers"
    title_html = '''
                 <div style="position: fixed; 
                             top: 50px; left: 50px; width: 300px; height: 90px; 
                             z-index:9999; font-size:14px;
                             background-color:white; padding: 10px;
                             border: 2px solid grey; border-radius: 10px;">
                 <b>Анализ риска паводков</b><br/>
                 Красный: Высокий риск (близость к руслу + низина)<br/>
                 Синий/Голубой: Линии рек Ili и Bayankol
                 </div>
                 '''
    m.get_root().html.add_child(folium.Element(title_html))

    # Сохранение результата
    m.save("151.html")
    print("Modeling complete. Map saved as 151.html")

if __name__ == "__main__":
    generate_flood_risk_model()