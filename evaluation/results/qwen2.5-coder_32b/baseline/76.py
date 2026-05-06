import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import Point

# Предположим, что у нас есть данные о гидропостах и их текущем расходе воды.
# Для примера создадим фейковые данные.

# Создание данных о гидропостах (координаты и текущий расход воды)
data = {
    'name': ['ГП1', 'ГП2', 'ГП3'],
    'latitude': [45.0, 46.0, 47.0],
    'longitude': [80.0, 81.0, 82.0],
    'current_flow_rate': [100, 200, 300]  # Расход воды в кубических метрах в секунду
}

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=[Point(xy) for xy in zip(data['longitude'], data['latitude'])])

# Предположим, что нормальный расход воды для реки Karaoy River составляет 150 кубических метров в секунду.
normal_flow_rate = 150

# Оценка риска паводка
def assess_flood_risk(flow_rate):
    if flow_rate < normal_flow_rate * 1.2:
        return 'Низкий риск'
    elif flow_rate < normal_flow_rate * 1.5:
        return 'Средний риск'
    else:
        return 'Высокий риск'

gdf['flood_risk'] = gdf['current_flow_rate'].apply(assess_flood_risk)

# Создание цветовой карты для риска паводка
color_map = {
    'Низкий риск': 'green',
    'Средний риск': 'yellow',
    'Высокий риск': 'red'
}

# Создание интерактивной карты с помощью folium
m = folium.Map(location=[46.0, 81.0], zoom_start=9)

for _, row in gdf.iterrows():
    folium.Marker(
        location=(row['latitude'], row['longitude']),
        popup=f"Гидропост: {row['name']}\nТекущий расход воды: {row['current_flow_rate']} м³/с\nРиск паводка: {row['flood_risk']}",
        icon=folium.Icon(color=color_map[row['flood_risk']])
    ).add_to(m)

# Сохранение карты в файл
m.save("76.html")