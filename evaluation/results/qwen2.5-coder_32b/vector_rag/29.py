import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть данные о расходе воды для реки Узын Каргалы
uzyn_kargaly_discharge = [
    {"date": "2023-03-15", "discharge_m3s": 150.0},
    {"date": "2023-03-20", "discharge_m3s": 180.0},
    {"date": "2023-03-25", "discharge_m3s": 200.0},
    {"date": "2023-04-01", "discharge_m3s": 220.0}
]

# Вывод данных о расходе воды
for entry in uzyn_kargaly_discharge:
    print(f"Дата: {entry['date']}, Расход воды (м³/с): {entry['discharge_m3s']}")

# Сохранение карты в файл
m.save("29.html")