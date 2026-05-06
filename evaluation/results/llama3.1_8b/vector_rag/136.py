import geopandas as gpd
import folium
from shapely import wkt

# Загрузите данные о речной сети региона из файла shapefile.
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создайте карту с центром в середине области речной сети.
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавьте область речной сети на карту.
folium.GeoJson(data=basin_data.unary_union.__geo_interface__, name='basin').add_to(m)

# Создайте список точек измерения уровня воды.
water_level_points = [
    {'location': [55.7558, 37.6173], 'level': 10, 'quality': 1},
    {'location': [40.7128, -74.0060], 'level': 15, 'quality': 2},
    {'location': [51.5074, -0.1278], 'level': 12, 'quality': 3}
]

# Добавьте точки измерения уровня воды на карту.
for point in water_level_points:
    folium.Marker(point['location'], popup=f'Уровень воды: {point["level"]} м, Качество воды: {point["quality"]}/5').add_to(m)

# Сохраните карту в файл.
m.save("136.html")