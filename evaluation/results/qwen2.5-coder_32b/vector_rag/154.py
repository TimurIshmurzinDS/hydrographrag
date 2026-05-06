import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты точек наблюдений для водного уровня (WKT)
# В реальности эти данные должны быть загружены из соответствующего источника
water_level_points = [
    {'name': 'Shynzhaly River', 'wkt': 'POINT(76.923077 43.185664)', 'level': 120},
    {'name': 'Shyzhyn River', 'wkt': 'POINT(76.923077 43.185664)', 'level': 130}
]

# Добавление точек наблюдений на карту
for point in water_level_points:
    geom = wkt.loads(point['wkt'])
    folium.Marker([geom.y, geom.x], popup=f"{point['name']}: Уровень воды {point['level']} м").add_to(m)

# Сохранение карты в файл
m.save("154.html")