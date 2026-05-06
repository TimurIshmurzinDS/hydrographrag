import geopandas as gpd
import folium
from shapely import wkt

# Предположим, что у нас есть данные о протяженности рек в виде списка словарей
rivers_data = [
    {"name": "Karatal River", "Length_km": 250.0},
    {"name": "Koktal River", "Length_km": 120.0},
    {"name": "Bayankol River", "Length_km": 80.0}
]

# Фильтруем притоки реки Каратал
tributaries = [river for river in rivers_data if river["name"] != "Karatal River"]

# Вычисляем общую протяженность притоков
total_length = sum(river["Length_km"] for river in tributaries)

print(f"Общая протяженность притоков реки Каратал: {total_length} км")

# Загружаем данные о водоснабжающей бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создаем карту с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавляем водоснабжающий бассейн на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохраняем карту в файл
m.save("93.html")