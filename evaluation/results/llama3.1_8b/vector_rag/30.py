import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты с бассейном
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt), 
               name='бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 3. Создание списка точек с координатами (WKT)
points = [
    {
        'location': wkt.loads('POINT(55.123456 37.654321)'),
        'name': '2 км выше устья реки Prokhodnaya River'
    }
]

# 4. Добавление точек на карту
for point in points:
    folium.Marker(point['location'], popup=point['name']).add_to(m)

# 5. Рассчет индекса риска наводнения
water_consumption_value = 1000  # м³/с
water_level_value = 10  # м
flood_risk_index = (water_consumption_value - water_level_value) / water_consumption_value

# 6. Добавление индекса риска наводнения на карту
folium.Marker(basin_data.centroid, popup=f'Индекс риска наводнения: {flood_risk_index:.2f}').add_to(m)

# 7. Сохранение карты в файл
m.save("30.html")