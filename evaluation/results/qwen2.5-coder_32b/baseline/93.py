import geopandas as gpd
from shapely.geometry import LineString, Point
import folium

# Предположим, что у нас есть GeoDataFrame с реками и их протяженностью.
# Для примера создадим такой DataFrame вручную. В реальном проекте данные обычно берутся из геоданных.

data = {
    'name': ['Каратал', 'Река1', 'Река2', 'Река3'],
    'length_km': [150, 45, 30, 25],
    'geometry': [
        LineString([(76.9, 42.8), (77.0, 42.9), (77.1, 43.0)]),
        LineString([(76.8, 42.7), (76.9, 42.8)]),
        LineString([(77.05, 42.85), (77.1, 42.9)]),
        LineString([(77.15, 43.05), (77.1, 43.0)])
    ],
    'tributary_of': [None, 'Каратал', 'Каратал', 'Каратал']
}

# Создаем GeoDataFrame
rivers_gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Фильтруем притоки реки Каратал
karatal_tributaries = rivers_gdf[rivers_gdf['tributary_of'] == 'Каратал']

# Вычисляем общую протяженность притоков
total_length = karatal_tributaries['length_km'].sum()

print(f"Общая протяженность притоков реки Каратал: {total_length} км")

# Визуализация на карте с использованием folium
m = folium.Map(location=[42.9, 77.0], zoom_start=10)

# Добавляем реку Каратал на карту
folium.PolyLine(
    locations=rivers_gdf[rivers_gdf['name'] == 'Каратал']['geometry'].iloc[0].coords,
    color='blue',
    weight=5,
    opacity=0.7,
    popup='Река Каратал'
).add_to(m)

# Добавляем притоки реки Каратал на карту
for _, row in karatal_tributaries.iterrows():
    folium.PolyLine(
        locations=row['geometry'].coords,
        color='green',
        weight=3,
        opacity=0.7,
        popup=f"{row['name']}, протяженность: {row['length_km']} км"
    ).add_to(m)

# Сохраняем карту
m.save("93.html")