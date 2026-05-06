import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Шарын
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровне воды в реке Шарын (заменить на реальные данные)
water_level_data = [
    {"date": "2023-01-01", "level": 150},
    {"date": "2023-02-01", "level": 160},
    {"date": "2023-03-01", "level": 170},
    {"date": "2023-04-01", "level": 180},
    {"date": "2023-05-01", "level": 190},
    {"date": "2023-06-01", "level": 200},  # Максимальный уровень
    {"date": "2023-07-01", "level": 185},
    {"date": "2023-08-01", "level": 175},
    {"date": "2023-09-01", "level": 165},
    {"date": "2023-10-01", "level": 155},
    {"date": "2023-11-01", "level": 145},
    {"date": "2023-12-01", "level": 140}
]

# Расчет максимального уровня воды
max_level = max(data['level'] for data in water_level_data)

# Расчет исторического среднего значения уровня воды
average_level = sum(data['level'] for data in water_level_data) / len(water_level_data)

# Расчет разницы между максимальным и историческим средним значением уровня воды
difference = max_level - average_level

print(f"Максимальный уровень воды: {max_level}")
print(f"Историческое среднее значение уровня воды: {average_level}")
print(f"Разница: {difference}")

# Сохранение карты
m.save("127.html")