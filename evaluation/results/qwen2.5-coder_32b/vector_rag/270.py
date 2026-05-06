import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Талгар
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты уровней воды в реке Талгар (WKT формат)
# Для примера создадим список словарей с координатами и уровнями воды
water_level_data = [
    {'geometry': wkt.loads('POINT(76.923058 43.193108)'), 'level_cm': 150},
    {'geometry': wkt.loads('POINT(76.924058 43.194108)'), 'level_cm': 160},
    {'geometry': wkt.loads('POINT(76.925058 43.195108)'), 'level_cm': 170}
]

# Добавление маркеров уровня воды на карту
for point in water_level_data:
    folium.Marker(
        location=[point['geometry'].y, point['geometry'].x],
        popup=f"Уровень воды: {point['level_cm']} см",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("270.html")