import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
from shapely.geometry import Point

# Шаг 1: Сбор данных о водных ресурсах и сельскохозяйственных угодьях в бассейнах рек Temirlik River и Byzhy River.
data_temirlik = {
    'geometry': [
        Point(45.123, 40.456),  # Координаты точки на поверхности Земли
        Point(45.234, 40.567),
        # Добавьте остальные координаты...
    ],
    'water_resources': [10, 20, 30],  # Объем водных ресурсов в каждом бассейне (в кубических метрах)
    'agricultural_land': [50, 60, 70]  # Площадь сельскохозяйственных угодий в каждом бассейне (в гектарах)
}

data_byzhy = {
    'geometry': [
        Point(45.123, 40.456),  # Координаты точки на поверхности Земли
        Point(45.234, 40.567),
        # Добавьте остальные координаты...
    ],
    'water_resources': [15, 25, 35],  # Объем водных ресурсов в каждом бассейне (в кубических метрах)
    'agricultural_land': [55, 65, 75]  # Площадь сельскохозяйственных угодий в каждом бассейне (в гектарах)
}

# Шаг 2: Создание географической модели.
gdf_temirlik = gpd.GeoDataFrame(data_temirlik, geometry='geometry')
gdf_byzhy = gpd.GeoDataFrame(data_byzhy, geometry='geometry')

# Шаг 3: Анализ потребления воды для сельского хозяйства в каждом бассейне реки.
def calculate_water_consumption(gdf):
    water_resources = gdf['water_resources'].sum()
    agricultural_land = gdf['agricultural_land'].sum()
    return (water_resources / agricultural_land) * 100

temirlik_water_consumption = calculate_water_consumption(gdf_temirlik)
byzhy_water_consumption = calculate_water_consumption(gdf_byzhy)

# Шаг 4: Визуализация результатов на карте с помощью библиотеки Folium.
m = Map(location=[45.123, 40.456], zoom_start=10)

marker_temirlik = Marker(
    location=[45.123, 40.456],
    popup='Temirlik River',
    icon=CircleMarker(color='red', radius=5)
).add_to(m)

marker_byzhy = Marker(
    location=[45.234, 40.567],
    popup='Byzhy River',
    icon=CircleMarker(color='blue', radius=5)
).add_to(m)

m.fit_bounds([[45.0, 40.0], [46.0, 41.0]])

# Добавление информации о потреблении воды для сельского хозяйства в каждом бассейне реки.
html = """
    <h3>Потребление воды для сельского хозяйства:</h3>
    <p>Река Temirlik: {temirlik_water_consumption:.2f}%</p>
    <p>Река Byzhy: {byzhy_water_consumption:.2f}%</p>
""".format(temirlik_water_consumption=temirlik_water_consumption, byzhy_water_consumption=byzhy_water_consumption)

m.get_root().html.add_child(folium.Element(html))

# Сохранение карты в файл.
m.save("115.html")