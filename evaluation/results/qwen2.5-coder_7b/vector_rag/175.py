import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат реки Сарыкан (если они доступны)
# В реальном случае эти данные должны быть получены из соответствующих источников
sarykan_river_coords = [
    {'geometry': wkt.loads('LINESTRING(45.123 78.901, 46.234 79.012)'), 'properties': {'length_km': 10}},
    {'geometry': wkt.loads('LINESTRING(47.345 80.123, 48.456 81.234)'), 'properties': {'length_km': 15}}
]

# Расчет суммарной длины реки Сарыкан
total_length_km = sum(feature['properties']['length_km'] for feature in sarykan_river_coords)

# Получение площади бассейна в километрах квадратных
basin_area_km2 = basin_data.geometry.area[0] / 1e6

# Расчет коэффициента связности
coefficient_of_connectivity = total_length_km / basin_area_km2

print(f"Коэффициент связности речной сети: {coefficient_of_connectivity:.4f}")

# Сохранение карты
m.save("175.html")