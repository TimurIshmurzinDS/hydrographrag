import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Создание карты с использованием центроида бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Фиктивные данные о уровнях воды на реке Талгар (дата, уровень воды)
water_level_data = [
    {"date": "2023-10-01", "level": 150},
    {"date": "2023-10-02", "level": 152},
    {"date": "2023-10-03", "level": 148},
    {"date": "2023-10-04", "level": 155}
]

# Последний показатель уровня воды
last_water_level = water_level_data[-1]
print(f"Последний зафиксированный уровень воды на реке Talgar River: {last_water_level['level']} м (дата: {last_water_level['date']})")

# Сохранение карты в файл
m.save("3.html")