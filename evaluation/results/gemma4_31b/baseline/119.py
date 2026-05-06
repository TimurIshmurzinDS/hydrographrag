import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster

# 1. Генерация синтетических данных для экологического мониторинга
# В реальном сценарии здесь будет загрузка CSV или подключение к БД (PostGIS)
np.random.seed(42)

def generate_river_data(river_name, start_coords, num_points):
    data = []
    lat, lon = start_coords
    for i in range(num_points):
        # Имитируем движение вдоль реки с небольшим смещением
        point_lat = lat + (i * 0.01) + np.random.uniform(-0.005, 0.005)
        point_lon = lon + (i * 0.02) + np.random.uniform(-0.005, 0.005)
        
        # Экологические индикаторы
        ph = np.random.uniform(6.5, 8.5)
        nitrates = np.random.uniform(10, 50) if river_name == "Byzhy" else np.random.uniform(5, 30)
        oxygen = np.random.uniform(5, 12)
        
        data.append({
            "River": river_name,
            "Latitude": point_lat,
            "Longitude": point_lon,
            "pH": round(ph, 2),
            "Nitrates": round(nitrates, 2),
            "Oxygen": round(oxygen, 2)
        })
    return data

# Координаты (примерные локации в Центральной Азии)
byzhy_points = generate_river_data("Byzhy River", (43.1, 78.2), 10)
tekeli_points = generate_river_data("Tekeli River", (43.5, 79.1), 10)

df = pd.DataFrame(byzhy_points + tekeli_points)

# 2. Сравнительный анализ индикаторов
comparison = df.groupby("River").agg({
    "pH": "mean",
    "Nitrates": "mean",
    "Oxygen": "mean"
}).reset_index()

print("Сравнительная таблица средних показателей:")
print(comparison)

# 3. Функция для определения цвета маркера на основе уровня нитратов
def get_color(nitrate_value):
    if nitrate_value > 40:
        return 'red'    # Высокое загрязнение
    elif nitrate_value > 20:
        return 'orange' # Среднее загрязнение
    else:
        return 'green'  # Чистая вода

# 4. Геопространственная визуализация
# Центрируем карту между двумя реками
m = folium.Map(location=[43.3, 78.6], zoom_start=8, tiles='CartoDB positron')

# Создаем кластеры для каждой реки
cluster_byzhy = MarkerCluster().add_to(m)
cluster_tekeli = MarkerCluster().add_to(m)

for idx, row in df.iterrows():
    color = get_color(row['Nitrates'])
    cluster = cluster_byzhy if row['River'] == "Byzhy River" else cluster_tekeli
    
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=7,
        popup=f"<b>{row['River']}</b><br>pH: {row['pH']}<br>Nitrates: {row['Nitrates']} mg/L<br>Oxygen: {row['Oxygen']} mg/L",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(cluster)

# Добавление легенды в виде HTML
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Nitrates Level:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Low (< 20)<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Medium (20-40)<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> High (> 40)
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение результата
m.save("119.html")
print("\nКарта успешно сохранена в файл 119.html")