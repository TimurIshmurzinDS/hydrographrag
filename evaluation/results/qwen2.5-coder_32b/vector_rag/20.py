import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование CRS
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты Folium с центром в центроиде бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о потреблении воды и уровне воды (заменить на реальные данные)
data = [
    {"date": "2023-05-15", "water_level": 150, "water_consumption": 100},
    {"date": "2023-05-16", "water_level": 160, "water_consumption": 120},
    {"date": "2023-05-17", "water_level": 180, "water_consumption": 150},
    {"date": "2023-05-18", "water_level": 200, "water_consumption": 200},
    {"date": "2023-05-19", "water_level": 190, "water_consumption": 180},
    {"date": "2023-05-20", "water_level": 170, "water_consumption": 140}
]

# Преобразование данных в DataFrame для анализа
import pandas as pd
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Визуализация данных на карте (пример: добавление маркеров с уровнями воды)
for _, row in df.iterrows():
    folium.Marker(
        location=[centroid.y, centroid.x],  # Используем центр бассейна для примера
        popup=f"Date: {row['date'].strftime('%Y-%m-%d')}, Water Level: {row['water_level']} m, Consumption: {row['water_consumption']} m³/s",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("20.html")