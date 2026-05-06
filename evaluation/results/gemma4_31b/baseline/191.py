import folium
import pandas as pd
import numpy as np
from folium.plugins import HeatMap

# 1. Симуляция геоданных для дельты реки Бызж
# Координаты центральной части дельты (примерные)
center_lat, center_lon = 45.1234, 38.5678 

# Точки интенсивного забора воды
water_intake_points = [
    {"name": "Станция забора 1", "lat": 45.1300, "lon": 38.5700, "capacity": "High"},
    {"name": "Станция забора 2", "lat": 45.1100, "lon": 38.5800, "capacity": "Medium"},
    {"name": "Станция забора 3", "lat": 45.1400, "lon": 38.5500, "capacity": "High"},
]

# 2. Генерация синтетических данных о динамике NDVI (биоразнообразия)
# Создаем сетку точек в районе дельты для имитации растрового анализа
np.random.seed(42)
lats = np.linspace(center_lat - 0.05, center_lat + 0.05, 20)
lons = np.linspace(center_lon - 0.05, center_lon + 0.05, 20)
grid_data = []

for lat in lats:
    for lon in lons:
        # Рассчитываем расстояние до ближайшей точки забора воды
        min_dist = min([np.sqrt((lat-p['lat'])**2 + (lon-p['lon'])**2) for p in water_intake_points])
        
        # Моделируем потерю биоразнообразия: чем ближе к забору, тем сильнее падение NDVI
        # NDVI_T1 (базовый) ~ 0.6-0.8, NDVI_T2 (после) зависит от расстояния
        ndvi_t1 = np.random.uniform(0.6, 0.8)
        impact = 0.3 * np.exp(-min_dist * 10) # Экспоненциальное затухание влияния
        ndvi_t2 = ndvi_t1 - impact + np.random.normal(0, 0.05)
        
        delta_ndvi = ndvi_t2 - ndvi_t1
        grid_data.append([lat, lon, delta_ndvi])

df_biodiversity = pd.DataFrame(grid_data, columns=['lat', 'lon', 'delta_ndvi'])

# 3. Визуализация с помощью Folium
m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles='OpenStreetMap')

# Добавляем тепловую карту деградации (отрицательные значения delta_ndvi = высокая деградация)
# Для HeatMap инвертируем значения, чтобы "горячие" зоны были там, где NDVI упал сильнее всего
heat_data = [[row['lat'], row['lon'], abs(row['delta_ndvi']) if row['delta_ndvi'] < 0 else 0] 
             for index, row in df_biodiversity.iterrows()]
HeatMap(heat_data, name="Зоны деградации биоразнообразия", radius=15, blur=20, gradient={0.4: 'blue', 0.65: 'yellow', 1: 'red'}).add_to(m)

# Добавляем маркеры точек забора воды
for point in water_intake_points:
    color = 'red' if point['capacity'] == 'High' else 'orange'
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=f"{point['name']} (Мощность: {point['capacity']})",
        icon=folium.Icon(color=color, icon='tint')
    ).add_to(m)

# Добавляем легенду через HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда:</b><br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокая деградация<br>
     <i style="background:yellow; width:10px; height:10px; display:inline-block"></i> Средняя деградация<br>
     <i style="background:blue; width:10px; height:10px; display:inline-block"></i> Стабильная зона<br>
     <br>
     <span style="color:red">●</span> Точка забора воды
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("191.html")

print("Анализ завершен. Карта сохранена в файл 191.html")