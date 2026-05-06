import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from folium.plugins import HeatMap
from shapely.geometry import Point, LineString, Polygon

# 1. Генерация синтетических данных для реки Бутак и окрестностей
# Координаты примерно соответствуют региону (условно)
river_coords = [
    (43.5, 75.0), (43.6, 75.2), (43.7, 75.5), 
    (43.8, 75.8), (43.9, 76.1), (44.0, 76.4)
]
river_line = LineString(river_coords)

# Источники загрязнения (название, координаты, уровень выброса)
pollution_sources_data = {
    'name': ['Завод А', 'Город Б', 'Свалка В'],
    'lat': [43.62, 43.75, 43.92],
    'lon': [75.25, 75.55, 76.15],
    'intensity': [80, 50, 30] # Условные единицы загрязнения
}
df_sources = pd.DataFrame(pollution_sources_data)

# Сельскохозяйственные угодья (центры полей и их радиус)
agri_fields_data = {
    'field_id': ['Поле 1', 'Поле 2', 'Поле 3', 'Поле 4'],
    'lat': [43.55, 43.72, 43.85, 44.02],
    'lon': [75.1, 75.4, 75.7, 76.3],
    'area_ha': [100, 250, 150, 300]
}
df_fields = pd.DataFrame(agri_fields_data)

# 2. Моделирование влияния
def calculate_pollution_impact(field_lat, field_lon, sources_df):
    """
    Рассчитывает суммарный уровень загрязнения для конкретной точки 
    на основе расстояния до источников и их интенсивности.
    """
    total_impact = 0
    for _, source in sources_df.iterrows():
        # Упрощенный расчет евклидова расстояния (для малых масштабов)
        dist = np.sqrt((field_lat - source['lat'])**2 + (field_lon - source['lon'])**2)
        # Модель затухания: влияние = интенсивность / (1 + расстояние^2)
        total_impact += source['intensity'] / (1 + (dist * 10)**2)
    return total_impact

# Применяем расчет для каждого поля
df_fields['pollution_level'] = df_fields.apply(
    lambda row: calculate_pollution_impact(row['lat'], row['lon'], df_sources), axis=1
)

# 3. Визуализация с помощью Folium
m = folium.Map(location=[43.75, 75.5], zoom_start=8, tiles='CartoDB positron')

# Рисуем реку Бутак
folium.PolyLine(river_coords, color='blue', weight=4, opacity=0.8, tooltip='Река Бутак').add_to(m)

# Добавляем источники загрязнения
for _, source in df_sources.iterrows():
    folium.CircleMarker(
        location=[source['lat'], source['lon']],
        radius=7,
        color='red',
        fill=True,
        fill_color='red',
        popup=f"Источник: {source['name']} (Интенсивность: {source['intensity']})"
    ).add_to(m)

# Добавляем сельскохозяйственные поля с цветовой индикацией риска
for _, field in df_fields.iterrows():
    # Определяем цвет в зависимости от уровня загрязнения
    if field['pollution_level'] > 10:
        color = 'darkred'
        risk = 'Высокий'
    elif field['pollution_level'] > 2:
        color = 'orange'
        risk = 'Средний'
    else:
        color = 'green'
        risk = 'Низкий'
        
    folium.Circle(
        location=[field['lat'], field['lon']],
        radius=5000, # Радиус поля в метрах
        color=color,
        fill=True,
        fill_opacity=0.4,
        popup=f"{field['field_id']} - Риск: {risk} (Уровень: {field['pollution_level']:.2f})"
    ).add_to(m)

# Создаем тепловую карту загрязнения на основе источников
heat_data = [[row['lat'], row['lon'], row['intensity']] for index, row in df_sources.iterrows()]
HeatMap(heat_data, radius=25, blur=15).add_to(m)

# Сохранение карты
m.save("186.html")

print("Анализ завершен. Карта сохранена в файл 186.html")