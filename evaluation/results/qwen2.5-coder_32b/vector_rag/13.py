import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне из файла shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты, центрированной по центроиду водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Представление последних показаний уровня воды для реки Kumbel River
# Для примера создадим список словарей с координатами и значением уровня воды
water_level_data = [
    {'coordinates': wkt.loads('POINT(36.25 48.01)'), 'level_cm': 150},
    {'coordinates': wkt.loads('POINT(36.27 48.02)'), 'level_cm': 155}
]

# Добавление маркеров на карту с уровнями воды
for data in water_level_data:
    folium.Marker(
        location=[data['coordinates'].y, data['coordinates'].x],
        popup=f"Уровень воды: {data['level_cm']} см",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("13.html")