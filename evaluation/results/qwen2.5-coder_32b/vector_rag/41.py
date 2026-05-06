import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки и использованием тайлов 'CartoDB positron'
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна реки на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты фермерских хозяйств в формате WKT
# Создание списка словарей с координатами и данными о потреблении воды
farms = [
    {'name': 'Фермерское хозяйство 1', 'geometry': wkt.loads('POINT(76.923058 42.882004)'), 'consumption_m3s': 0.5},
    {'name': 'Фермерское хозяйство 2', 'geometry': wkt.loads('POINT(76.913058 42.872004)'), 'consumption_m3s': 0.7},
    # Добавьте другие фермерские хозяйства по мере необходимости
]

# Добавление маркеров на карту для каждого фермерского хозяйства с информацией о потреблении воды
for farm in farms:
    folium.Marker(
        location=[farm['geometry'].y, farm['geometry'].x],
        popup=f"Название: {farm['name']}, Потребление воды (м³/с): {farm['consumption_m3s']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("41.html")