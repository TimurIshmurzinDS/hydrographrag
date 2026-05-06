import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster

# 1. Симуляция данных (так как реальные данные требуют доступа к закрытым API гидропостов)
# Координаты примерно соответствуют течению реки Шилик (Казахстан)
data = {
    'station_id': [1, 2, 3, 4, 5, 6],
    'lat': [44.85, 44.70, 44.55, 44.40, 44.25, 44.10],
    'lon': [82.10, 82.30, 82.50, 82.70, 82.90, 83.10],
    'temp_2021': [12.5, 13.2, 11.8, 14.1, 15.0, 14.8],
    'temp_2022': [13.1, 12.8, 12.5, 14.8, 15.5, 14.2]
}

df = pd.DataFrame(data)

# 2. Расчет разницы температур
df['diff'] = df['temp_2022'] - df['temp_2021']

# Функция для определения цвета маркера в зависимости от изменения температуры
def get_color(diff):
    if diff > 0.2:
        return 'red'    # Значительное повышение
    elif diff < -0.2:
        return 'blue'   # Значительное понижение
    else:
        return 'green'  # Стабильная температура

# 3. Создание карты
# Центрируем карту на среднем значении координат реки Шилик
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], 
               zoom_start=7, 
               tiles='OpenStreetMap')

# Добавление кластера для маркеров
marker_cluster = MarkerCluster().add_to(m)

for index, row in df.iterrows():
    color = get_color(row['diff'])
    
    # Формирование текста для всплывающего окна
    popup_text = (
        f"Станция: {row['station_id']}<br>"
        f"Температура 2021: {row['temp_2021']}°C<br>"
        f"Температура 2022: {row['temp_2022']}°C<br>"
        f"Разница: {row['diff']:.2f}°C"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=popup_text,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(marker_cluster)

# 4. Сохранение результата
m.save("53.html")

print("Анализ завершен. Карта сохранена в файл 53.html")