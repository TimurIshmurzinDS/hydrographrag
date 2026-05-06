import folium
import geopandas as gpd
from shapely.geometry import Polygon, Point
import numpy as np
import pandas as pd

def solve_ili_water_modeling():
    # 1. Симуляция геоданных бассейна реки Или
    # Координаты примерно охватывают регион бассейна (Казахстан/Китай)
    basin_coords = [
        [42.0, 75.0], [43.5, 78.0], [44.0, 81.0], 
        [42.0, 82.0], [40.0, 80.0], [39.0, 76.0], [42.0, 75.0]
    ]
    basin_poly = Polygon(basin_coords)
    
    # 2. Симуляция данных по орошаемым участкам (Irrigation Zones)
    # Создаем несколько зон с разной площадью и нормами полива
    # В реальности здесь был бы Shapefile или Raster
    zones_data = {
        'zone_id': [1, 2, 3, 4, 5],
        'center': [
            [42.5, 77.5], [41.8, 79.2], [43.1, 78.8], [40.5, 78.0], [42.2, 76.5]
        ],
        'area_ha': [15000, 22000, 12000, 30000, 8000], # Площадь в гектарах
        'water_norm_m3_ha': [4500, 5000, 4200, 5500, 4000] # Норма полива м3 на га
    }
    
    df_zones = pd.DataFrame(zones_data)
    
    # 3. Расчет объемов воды
    # Объем = Площадь * Норма
    df_zones['total_volume_m3'] = df_zones['area_ha'] * df_zones['water_norm_m3_ha']
    
    total_basin_water = df_zones['total_volume_m3'].sum()
    
    print(f"Общий расчетный объем воды для полива в бассейне реки Или: {total_basin_water:,.2f} м³")
    
    # 4. Визуализация с помощью folium
    # Центр карты
    m = folium.Map(location=[42.0, 78.5], zoom_start=6, tiles='CartoDB positron')
    
    # Добавляем границу бассейна
    folium.Polygon(
        locations=basin_coords,
        color='blue',
        weight=3,
        fill=True,
        fill_opacity=0.1,
        popup='Бассейн реки Или'
    ).add_to(m)
    
    # Добавляем зоны полива
    for index, row in df_zones.iterrows():
        # Определяем цвет в зависимости от объема воды
        color = 'green' if row['total_volume_m3'] < 80000000 else 'orange' if row['total_volume_m3'] < 120000000 else 'red'
        
        folium.Circle(
            location=row['center'],
            radius=row['area_ha'] * 10, # Масштабирование радиуса для визуализации
            color=color,
            fill=True,
            fill_color=color,
            popup=f"Зона {row['zone_id']}: {row['total_volume_m3']:,.0f} м³"
        ).add_to(m)
    
    # Добавление легенды через HTML
    legend_html = f'''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 100px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; padding: 10px;">
    <b>Объемы полива:</b><br>
    <i style="background:green;width:10px;height:10px;display:inline-block"></i> Низкий <br>
    <i style="background:orange;width:10px;height:10px;display:inline-block"></i> Средний <br>
    <i style="background:red;width:10px;height:10px;display:inline-block"></i> Высокий <br>
    <b>Итого:</b> {total_basin_water/1e6:.2f} млн м³
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Сохранение карты
    m.save("39.html")
    print("Карта успешно сохранена в файл 39.html")

if __name__ == "__main__":
    solve_ili_water_modeling()