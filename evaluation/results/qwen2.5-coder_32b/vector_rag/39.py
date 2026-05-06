import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Или из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть данные о точках потребления воды (например, для полива)
# Создание списка словарей с координатами и объемом потребления воды
consumption_points = [
    {'coordinates': 'POINT(46.0 39.5)', 'volume_m3s': 10},
    {'coordinates': 'POINT(46.2 39.7)', 'volume_m3s': 15},
    {'coordinates': 'POINT(46.1 39.8)', 'volume_m3s': 20}
]

# Добавление точек потребления воды на карту
for point in consumption_points:
    geom = wkt.loads(point['coordinates'])
    folium.CircleMarker(
        location=[geom.y, geom.x],
        radius=point['volume_m3s'],
        popup=f"Объем: {point['volume_m3s']} м³/с",
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Сохранение карты в файл
m.save("39.html")