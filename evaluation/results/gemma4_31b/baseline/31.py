import folium
from folium.plugins import MarkerCluster
import pandas as pd
import numpy as np

def solve_water_consumption():
    # 1. Имитация данных о русле реки Или (упрощенные координаты от Китая до оз. Балхаш)
    # В реальном проекте здесь будет загрузка GeoJSON или Shapefile
    ili_river_coords = [
        [42.5, 80.0], [42.8, 81.0], [43.1, 82.0], 
        [43.2, 83.0], [43.0, 84.0], [42.5, 85.0], 
        [42.2, 86.0], [42.0, 87.0]
    ]

    # 2. Данные по точкам водозабора (имитация текущих показателей)
    # Объем потребления указан в млн м3/год
    consumption_data = {
        'Location': ['Upper Ili (CN)', 'Middle Ili (KZ)', 'Almaty Region Irrigation', 'Industrial Zone A', 'Municipal Center B', 'Lower Ili Delta'],
        'Lat': [42.7, 43.1, 43.0, 42.6, 42.3, 42.1],
        'Lon': [80.5, 82.5, 83.5, 84.2, 85.5, 86.5],
        'Volume': [1200, 800, 2500, 400, 300, 600], # млн м3
        'Type': ['Agriculture', 'Agriculture', 'Agriculture', 'Industry', 'Municipal', 'Agriculture']
    }
    
    df = pd.DataFrame(consumption_data)
    
    # Расчет общего уровня потребления
    total_consumption = df['Volume'].sum()
    print(f"Текущий расчетный уровень потребления воды для реки Или: {total_consumption} млн м3/год")

    # 3. Создание ГИС-карты
    # Центрируем карту на среднем течении реки
    m = folium.Map(location=[42.5, 83.0], zoom_start=6, tiles='CartoDB positron')

    # Отрисовка русла реки
    folium.PolyLine(
        locations=ili_river_coords, 
        color='blue', 
        weight=5, 
        opacity=0.7, 
        tooltip='Русло реки Или'
    ).add_to(m)

    # Цветовая схема в зависимости от типа потребления
    color_map = {
        'Agriculture': 'green',
        'Industry': 'red',
        'Municipal': 'orange'
    }

    # Добавление точек водозабора на карту
    for index, row in df.iterrows():
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=row['Volume'] / 100, # Радиус зависит от объема
            color=color_map.get(row['Type'], 'gray'),
            fill=True,
            fill_color=color_map.get(row['Type'], 'gray'),
            fill_opacity=0.6,
            popup=f"Объект: {row['Location']}<br>Тип: {row['Type']}<br>Потребление: {row['Volume']} млн м3"
        ).add_to(m)

    # Добавление легенды через HTML
    legend_html = f'''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 120px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; opacity: 0.8; padding: 10px;">
    <b>Легенда потребления:</b><br>
    <i style="background:green; width:10px; height:10px; display:inline-block"></i> Сельское хозяйство<br>
    <i style="background:red; width:10px; height:10px; display:inline-block"></i> Промышленность<br>
    <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Муниципальное<br>
    <hr>
    <b>Итого: {total_consumption} млн м3/год</b>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение карты
    m.save("31.html")
    print("Карта успешно сохранена в файл 31.html")

if __name__ == "__main__":
    solve_water_consumption()