import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах рек
basin_data = r"data/basin_data.shp"
gdf_basins = gpd.read_file(basin_data)
gdf_basins = gdf_basins.to_crs('EPSG:4326')

# Инициализация карты с центром в centroid бассейна
centroid = gdf_basins.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf_basins.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о уровне воды (замените на реальные данные)
water_level_data = [
    {'date': '2018-01-01', 'level': 50, 'river': 'Lepsy River'},
    {'date': '2019-01-01', 'level': 52, 'river': 'Lepsy River'},
    {'date': '2020-01-01', 'level': 53, 'river': 'Lepsy River'},
    {'date': '2018-01-01', 'level': 60, 'river': 'Turgen River'},
    {'date': '2019-01-01', 'level': 62, 'river': 'Turgen River'},
    {'date': '2020-01-01', 'level': 63, 'river': 'Turgen River'}
]

# Визуализация данных о уровне воды на карте
for data in water_level_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Уровень воды: {data['level']} м", icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("198.html")