import folium
from folium import plugins
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point

def generate_sharyn_river_coords():
    """
    Генерация приблизительных координат русла реки Шарын (упрощенно).
    """
    return [
        [43.8, 79.2], [43.7, 79.4], [43.6, 79.6], 
        [43.5, 79.8], [43.4, 80.1], [43.3, 80.4],
        [43.2, 80.7], [43.1, 81.0]
    ]

def calculate_biodiversity_index(distance, water_level):
    """
    Модель влияния уровня воды на биоразнообразие.
    distance: расстояние от русла (км)
    water_level: 'low', 'medium', 'high'
    """
    # Оптимальное расстояние для биоразнообразия зависит от уровня воды
    optimums = {'low': 0.1, 'medium': 0.5, 'high': 1.2}
    opt = optimums[water_level]
    
    # Гауссова функция для имитации распределения биоразнообразия
    # Чем ближе к оптимуму увлажнения, тем выше индекс (0.0 - 1.0)
    index = np.exp(-((distance - opt)**2) / (2 * 0.3**2))
    return index

def main():
    # 1. Инициализация данных
    river_coords = generate_sharyn_river_coords()
    river_line = LineString(river_coords)
    
    # Создаем карту, центрированную на реке Шарын
    m = folium.Map(location=[43.5, 79.8], zoom_start=8, tiles='CartoDB positron')
    
    # 2. Отрисовка русла реки
    folium.PolyLine(river_coords, color="blue", weight=4, opacity=0.8, tooltip="Река Шарын").add_to(m)
    
    # 3. Моделирование сценариев уровней воды
    scenarios = {
        'low': {'color': 'orange', 'width': 0.2, 'label': 'Низкий уровень (Засуха)'},
        'medium': {'color': 'green', 'width': 0.8, 'label': 'Средний уровень (Норма)'},
        'high': {'color': 'purple', 'width': 1.5, 'label': 'Высокий уровень (Паводок)'}
    }
    
    # Для визуализации влияния создадим сетку точек вокруг реки
    biodiversity_data = []
    
    for level, params in scenarios.items():
        # Рисуем буферную зону для каждого сценария
        # В folium мы имитируем буфер через PolyLine с разной толщиной или дополнительные линии
        # Для простоты визуализируем границы влияния
        
        # Генерируем точки для тепловой карты биоразнообразия при данном уровне
        for coord in river_coords:
            lat, lon = coord
            for dx in np.linspace(-2, 2, 20):
                for dy in np.linspace(-2, 2, 20):
                    # Упрощенный расчет расстояния (в градусах ~ км)
                    dist = np.sqrt(dx**2 + dy**2) * 111 
                    val = calculate_biodiversity_index(dist, level)
                    if val > 0.3: # Сохраняем только значимые зоны
                        biodiversity_data.append([lat + dx/10, lon + dy/10, val])

    # 4. Визуализация зон влияния (Буферы)
    # Создаем имитацию буферов вокруг реки
    for level, params in scenarios.items():
        # Создаем линию с разным весом для демонстрации зоны влияния
        folium.PolyLine(river_coords, color=params['color'], weight=params['width']*20, 
                        opacity=0.3, tooltip=params['label']).add_to(m)

    # 5. Добавление тепловой карты биоразнообразия (на основе среднего сценария)
    # Формат для HeatMap: [[lat, lon, weight], ...]
    heat_data = [[p[0], p[1], p[2]] for p in biodiversity_data if p[2] > 0.5]
    plugins.HeatMap(heat_data, radius=15, blur=10, min_opacity=0.4).add_to(m)

    # Добавление легенды
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 250px; height: 150px; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                padding: 10px; font-family: Arial;">
        <b>Легенда влияния уровня воды:</b><br>
        <i style="background:orange; width:10px; height:10px; display:inline-block;"></i> Низкий уровень (Риск засухи)<br>
        <i style="background:green; width:10px; height:10px; display:inline-block;"></i> Средний уровень (Оптимум)<br>
        <i style="background:purple; width:10px; height:10px; display:inline-block;"></i> Высокий уровень (Затопление)<br>
        <i style="background:red; width:10px; height:10px; display:inline-block;"></i> Тепловая карта: Биоразнообразие
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение результата
    m.save("181.html")
    print("Modeling complete. Map saved as 181.html")

if __name__ == "__main__":
    main()