import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые данные о температуре воды (пример)
temperature_data = [
    {"year": 2021, "value": 15.3, "unit": "°C"},
    {"year": 2022, "value": 16.7, "unit": "°C"}
]

# Вывод данных о температуре воды
for data in temperature_data:
    print(f"Температура воды в реке Шилик за {data['year']} год: {data['value']} {data['unit']}")

# Сохранение карты в файл
m.save("53.html")