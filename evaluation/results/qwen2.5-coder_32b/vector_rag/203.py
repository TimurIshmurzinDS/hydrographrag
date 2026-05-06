import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Коксу из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Коксу
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Koksu Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример исторических данных уровня воды для реки Коксу
historical_water_levels = [
    {"date": "2010-05-15", "level": 345.2},
    {"date": "2011-06-20", "level": 350.1},
    {"date": "2012-07-10", "level": 355.8},
    {"date": "2013-08-25", "level": 349.6},
    {"date": "2014-09-15", "level": 360.3},
    {"date": "2015-10-05", "level": 370.5},
    {"date": "2016-11-20", "level": 380.4},
    {"date": "2017-12-10", "level": 390.2},
    {"date": "2018-01-25", "level": 365.1},
    {"date": "2019-02-15", "level": 375.4},
    {"date": "2020-03-05", "level": 385.6},
    {"date": "2021-04-20", "level": 395.8},
    {"date": "2022-05-10", "level": 400.7},
    {"date": "2023-06-25", "level": 410.9}
]

# Извлечение уровней воды из исторических данных
water_levels = [entry['level'] for entry in historical_water_levels]

# Расчет квантиля 0.98 (порога 50-летнего паводка)
import numpy as np
threshold_50_year_flood = np.percentile(water_levels, 98)

# Вывод порога 50-летнего паводка
print(f"Порог 50-летнего паводка для реки Коксу: {threshold_50_year_flood} м")

# Расчет вероятности превышения порога 50-летнего паводка
exceedance_probability = sum(level > threshold_50_year_flood for level in water_levels) / len(water_levels)
print(f"Вероятность превышения порога 50-летнего паводка: {exceedance_probability * 100:.2f}%")

# Сохранение карты
m.save("203.html")