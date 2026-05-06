import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap
import random

def generate_urzhar_basin_data():
    """
    Симуляция геопространственных данных для бассейна реки Уржар.
    В реальном проекте здесь будет загрузка GeoTIFF и Shape-файлов.
    """
    # Примерные координаты бассейна реки Уржар (Казахстан)
    center_lat, center_lon = 47.5, 82.5 
    grid_size = 20  # Сетка 20x20 точек
    
    data = []
    for i in range(grid_size):
        for j in range(grid_size):
            lat = center_lat + (i * 0.1)
            lon = center_lon + (j * 0.1)
            
            # Симуляция: Осадки (мм/год)
            precipitation = np.random.uniform(200, 400)
            
            # Симуляция: Потенциальная эвапотранспирация (мм/год)
            pet = np.random.uniform(600, 900)
            
            # Коэффициент культуры (средний для региона)
            kc = 0.8 
            water_demand = pet * kc
            
            # Доступная ирригация (симуляция наличия каналов)
            irrigation = np.random.uniform(0, 300)
            
            # Расчет дефицита: Demand - (Precipitation + Irrigation)
            deficit = water_demand - (precipitation + irrigation)
            
            # Определение уровня риска
            if deficit < 0:
                risk_level = 0 # Низкий
            elif 0 <= deficit < 150:
                risk_level = 1 # Средний
            else:
                risk_level = 2 # Высокий
                
            data.append([lat, lon, deficit, risk_level])
            
    return data

def main():
    # 1. Генерация данных
    basin_data = generate_urzhar_basin_data()
    df = pd.DataFrame(basin_data, columns=['lat', 'lon', 'deficit', 'risk'])

    # 2. Создание карты Folium
    # Центрируем карту на регионе Уржар
    m = folium.Map(location=[47.5, 82.5], zoom_start=7, tiles='OpenStreetMap')

    # 3. Добавление тепловой карты дефицита (HeatMap)
    # Для HeatMap нужны данные в формате [[lat, lon, weight], ...]
    heat_data = [[row['lat'], row['lon'], row['deficit']] for index, row in df.iterrows()]
    HeatMap(heat_data, name="Интенсивность дефицита воды", radius=15).add_to(m)

    # 4. Добавление точечных маркеров рисков для детального анализа
    for index, row in df.iterrows():
        color = 'green' if row['risk'] == 0 else 'orange' if row['risk'] == 1 else 'red'
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=3,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"Дефицит: {row['deficit']:.2f} мм",
            fill_opacity=0.7
        ).add_to(m)

    # Добавление легенды (простой текстовый элемент)
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Риски дефицита:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкий<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # 5. Сохранение результата
    m.save("182.html")
    print("Анализ завершен. Карта сохранена в файл 182.html")

if __name__ == "__main__":
    main()