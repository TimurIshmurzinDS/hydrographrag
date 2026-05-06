import folium
import pandas as pd
import numpy as np
from shapely.geometry import LineString, Point, Polygon
import geopandas as gpd

# 1. Симуляция данных (так как реальные данные по реке Аксу закрыты)
# Координаты реки Аксу (упрощенно, район Казахстана/Китая)
river_coords = [
    (43.5, 81.0), (43.6, 81.2), (43.7, 81.5), 
    (43.8, 81.8), (43.9, 82.1), (44.0, 82.4)
]

# Создаем синтетические данные по фермерским хозяйствам
# Генерируем точки вокруг линии реки
np.random.seed(42)
farms_data = []
for i in range(20):
    # Случайная точка вблизи реки
    lat = np.random.uniform(43.5, 44.0)
    lon = np.random.uniform(81.0, 82.4)
    # Объем потребления воды в тыс. м3
    consumption = np.random.randint(100, 1000) 
    # Площадь хозяйства в га
    area = np.random.randint(50, 500)
    farms_data.append({'id': i, 'lat': lat, 'lon': lon, 'consumption': consumption, 'area': area})

df_farms = pd.DataFrame(farms_data)
df_farms['water_intensity'] = df_farms['consumption'] / df_farms['area'] # м3 на га

# 2. Создание карты
m = folium.Map(location=[43.75, 81.7], zoom_start=8, tiles='CartoDB positron')

# 3. Визуализация реки Аксу
river_line = folium.PolyLine(
    locations=river_coords, 
    color='blue', 
    weight=5, 
    opacity=0.8, 
    tooltip='Река Аксу'
).add_to(m)

# 4. Визуализация фермерских хозяйств
# Определяем цветовую схему в зависимости от интенсивности потребления
def get_color(intensity):
    if intensity < 2: return 'green'
    if intensity < 4: return 'orange'
    return 'red'

for index, row in df_farms.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=7,
        popup=f"Ферма ID: {row['id']}<br>Потребление: {row['consumption']} тыс.м3<br>Интенсивность: {row['water_intensity']:.2f} м3/га",
        color=get_color(row['water_intensity']),
        fill=True,
        fill_color=get_color(row['water_intensity']),
        fill_opacity=0.7
    ).add_to(m)

# Добавление легенды (простой текстовый элемент)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Интенсивность воды:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкая<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средняя<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокая
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение результата
m.save("41.html")

print("Modeling complete. The map has been saved as 41.html")