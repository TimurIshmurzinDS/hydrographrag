import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster

# 1. Симуляция данных (так как реальные данные Sarykan River требуют доступа к закрытым API)
# Создаем синтетический набор данных для гидропостов вдоль реки
np.random.seed(42)

stations_data = {
    'station_id': [1, 2, 3, 4, 5],
    'lat': [48.123, 48.150, 48.180, 48.210, 48.250],
    'lon': [65.450, 65.480, 65.520, 65.560, 65.600],
    'name': ['Upper Sarykan', 'Mid-Upper Sarykan', 'Central Sarykan', 'Mid-Lower Sarykan', 'Lower Sarykan']
}

df_stations = pd.DataFrame(stations_data)

# Генерируем случайные уровни воды для 2022 и 2023 годов
# Уровни в метрах
df_stations['level_2022'] = np.random.uniform(1.5, 3.0, size=5)
df_stations['level_2023'] = np.random.uniform(1.2, 3.2, size=5)

# 2. Расчет разницы (анализ)
df_stations['diff'] = df_stations['level_2023'] - df_stations['level_2022']

# 3. Визуализация на карте
# Центрируем карту по средним координатам реки
map_center = [df_stations['lat'].mean(), df_stations['lon'].mean()]
m = folium.Map(location=map_center, zoom_start=10, tiles='OpenStreetMap')

# Функция для определения цвета в зависимости от изменения уровня
def get_color(diff):
    if diff > 0.1:
        return 'blue'   # Уровень поднялся
    elif diff < -0.1:
        return 'red'    # Уровень упал
    else:
        return 'green'  # Уровень стабилен

# Добавление точек на карту
for index, row in df_stations.iterrows():
    color = get_color(row['diff'])
    
    # Формируем текст для всплывающего окна
    popup_text = (
        f"<b>Станция:</b> {row['name']}<br>"
        f"<b>Уровень 2022:</b> {row['level_2022']:.2f} м<br>"
        f"<b>Уровень 2023:</b> {row['level_2023']:.2f} м<br>"
        f"<b>Разница:</b> {row['diff']:.2f} м"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Добавление легенды (простой текстовый элемент в HTML)
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 160px; height: 90px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Легенда:</b><br>
     <i style="background:blue; width:10px; height:10px; display:inline-block"></i> Повышение<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Понижение<br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Стабильно
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("46.html")

print("Анализ завершен. Карта сохранена в файл 46.html")