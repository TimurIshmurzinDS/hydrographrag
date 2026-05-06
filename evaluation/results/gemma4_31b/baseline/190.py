import folium
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import LineString, Polygon, Point

# 1. Генерация синтетических данных для реки Киши Осек и угодий
# Координаты (примерные для демонстрации)
river_coords = [
    (43.10, 45.20), (43.12, 45.25), (43.15, 45.30), 
    (43.18, 45.35), (43.20, 45.40), (43.22, 45.45)
]
river_line = LineString(river_coords)

# Коэффициенты водопотребления (м3 на гектар в год)
WATER_CONSUMPTION_RATE = 5000 

# Создаем текущие сельхозугодья (полигоны вокруг реки)
current_fields_data = [
    {'id': 1, 'geometry': Polygon([(43.11, 45.21), (43.11, 45.24), (43.13, 45.24), (43.13, 45.21)]), 'type': 'current'},
    {'id': 2, 'geometry': Polygon([(43.16, 45.31), (43.16, 45.34), (43.18, 45.34), (43.18, 45.31)]), 'type': 'current'},
]

# Создаем зоны расширения (новые полигоны)
expansion_fields_data = [
    {'id': 3, 'geometry': Polygon([(43.14, 45.25), (43.14, 45.28), (43.16, 45.28), (43.16, 45.25)]), 'type': 'expansion'},
    {'id': 4, 'geometry': Polygon([(43.19, 45.36), (43.19, 45.39), (43.21, 45.39), (43.21, 45.36)]), 'type': 'expansion'},
]

# Преобразование в GeoDataFrame
gdf_current = gpd.GeoDataFrame(current_fields_data)
gdf_expansion = gpd.GeoDataFrame(expansion_fields_data)
gdf_all = pd.concat([gdf_current, gdf_expansion])

# 2. Расчет нагрузки
def calculate_area(poly):
    # Упрощенный расчет площади для демонстрации (в гектарах)
    # В реальном проекте используется .area после проекции в UTM
    return poly.area * 100000 

gdf_all['area_ha'] = gdf_all['geometry'].apply(calculate_area)
gdf_all['water_load'] = gdf_all['area_ha'] * WATER_CONSUMPTION_RATE

total_current_load = gdf_current['area_ha'].apply(lambda x: x * WATER_CONSUMPTION_RATE).sum()
total_expansion_load = gdf_expansion['area_ha'].apply(lambda x: x * WATER_CONSUMPTION_RATE).sum()

print(f"Текущая нагрузка на водные ресурсы: {total_current_load:.2f} м3/год")
print(f"Дополнительная нагрузка при расширении: {total_expansion_load:.2f} м3/год")
print(f"Общая прогнозная нагрузка: {total_current_load + total_expansion_load:.2f} м3/год")

# 3. Визуализация с помощью folium
# Центр карты
m = folium.Map(location=[43.15, 45.30], zoom_start=12, tiles='CartoDB positron')

# Отрисовка реки
folium.PolyLine(river_coords, color='blue', weight=4, opacity=0.8, tooltip="Река Киши Осек").add_to(m)

# Отрисовка угодий
for idx, row in gdf_all.iterrows():
    # Конвертация координат из (lat, lon) в (lon, lat) для folium
    coords = [[p[0], p[1]] for p in row['geometry'].exterior.coords]
    
    color = 'green' if row['type'] == 'current' else 'orange'
    label = 'Текущие угодья' if row['type'] == 'current' else 'Зона расширения'
    
    folium.Polygon(
        locations=coords,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.5,
        tooltip=f"{label} | Нагрузка: {row['water_load']:.2f} м3/год"
    ).add_to(m)

# Добавление легенды через HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда нагрузки:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Текущие угодья<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Зона расширения<br>
     <i style="background:blue; width:10px; height:10px; display:inline-block"></i> Река Киши Осек
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("190.html")
print("Карта успешно сохранена в файл 190.html")