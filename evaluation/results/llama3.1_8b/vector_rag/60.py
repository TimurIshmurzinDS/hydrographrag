import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Bassin',
               style_function=lambda feature: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Данные о водном уровне
water_level_data = [
    {"date": "2018-01-01", "value": 10},
    {"date": "2019-01-01", "value": 12},
    {"date": "2020-01-01", "value": 11},
    {"date": "2021-01-01", "value": 13},
    {"date": "2022-01-01", "value": 14},
    {"date": "2023-01-01", "value": 15}
]

# Данные о осадках
rainfall_data = [
    {"date": "2018-01-01", "value": 20},
    {"date": "2019-01-01", "value": 22},
    {"date": "2020-01-01", "value": 21},
    {"date": "2021-01-01", "value": 23},
    {"date": "2022-01-01", "value": 24},
    {"date": "2023-01-01", "value": 25}
]

# Рассчет среднего уровня воды и стандартного отклонения
water_level_mean = sum([data["value"] for data in water_level_data]) / len(water_level_data)
water_level_std = (sum([(data["value"] - water_level_mean) ** 2 for data in water_level_data]) / len(water_level_data)) ** 0.5

# Рассчет влияния осадков на уровень воды
rainfall_influence = [data["value"] * rainfall_data[i]["value"] for i, data in enumerate(water_level_data)]

# Добавление данных о водном уровне и осадках на карту
folium.Marker([basin_data.centroid.y, basin_data.centroid.x], popup="Средний уровень воды: " + str(water_level_mean) + " см").add_to(m)
folium.Marker([basin_data.centroid.y, basin_data.centroid.x], popup="Стандартное отклонение уровня воды: " + str(water_level_std) + " см").add_to(m)

# Сохранение карты
m.save("60.html")