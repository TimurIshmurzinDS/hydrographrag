import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster

# 1. Генерация синтетических данных для реки Dos River
# Предположим, у нас есть 6 станций мониторинга вдоль русла реки
np.random.seed(42)
stations = {
    'Station_A': [45.523, -122.676],
    'Station_B': [45.530, -122.650],
    'Station_C': [45.540, -122.630],
    'Station_D': [45.555, -122.610],
    'Station_E': [45.570, -122.590],
    'Station_F': [45.585, -122.570],
}

years = [2019, 2020, 2021, 2022, 2023]
data_list = []

for station, coords in stations.items():
    for year in years:
        # Генерируем случайную нагрузку наносов (в тоннах в год)
        # Добавляем небольшой тренд для наглядности
        base_load = np.random.uniform(1000, 5000)
        trend = (year - 2019) * np.random.uniform(-200, 300)
        annual_load = max(0, base_load + trend)
        
        data_list.append({
            'station': station,
            'lat': coords[0],
            'lon': coords[1],
            'year': year,
            'sediment_load': annual_load
        })

df = pd.DataFrame(data_list)

# 2. Анализ данных
# Вычисляем среднюю нагрузку за 5 лет и разницу между первым и последним годом
summary = df.groupby('station').agg({
    'sediment_load': ['mean', lambda x: x.iloc[-1] - x.iloc[0]],
    'lat': 'first',
    'lon': 'first'
}).reset_index()

summary.columns = ['station', 'avg_load', 'load_diff', 'lat', 'lon']

# Функция для определения цвета маркера в зависимости от средней нагрузки
def get_color(load):
    if load < 2500:
        return 'green'  # Низкая нагрузка
    elif load < 4000:
        return 'orange' # Средняя нагрузка
    else:
        return 'red'    # Высокая нагрузка

# 3. Визуализация на карте
# Центрируем карту по средней точке реки
m = folium.Map(location=[45.55, -122.62], zoom_start=13, tiles='CartoDB positron')

# Добавляем станции на карту
for index, row in summary.iterrows():
    # Создаем текст для всплывающего окна
    # Получаем данные по годам для конкретной станции для детального описания
    station_data = df[df['station'] == row['station']]
    history_text = "<br>".join([f"{int(y)}: {int(v):,} t" for y, v in zip(station_data['year'], station_data['sediment_load'])])
    
    popup_content = f"""
    <strong>Station: {row['station']}</strong><br>
    Avg Load (5y): {int(row['avg_load']):,} t<br>
    Trend (2019-2023): {int(row['load_diff']):,} t<br>
    <hr>
    <strong>History:</strong><br>{history_text}
    """
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=folium.Popup(popup_content, max_width=300),
        color=get_color(row['avg_load']),
        fill=True,
        fill_color=get_color(row['avg_load']),
        fill_opacity=0.7
    ).add_to(m)

# Добавляем легенду
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <strong>Sediment Load</strong><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Low (<2500t)<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Medium (2500-4000t)<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> High (>4000t)
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("56.html")

print("Modeling complete. The map has been saved as 56.html")