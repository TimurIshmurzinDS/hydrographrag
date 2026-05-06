import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование CRS
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне Коктал
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты станции мониторинга на реке Koktal River в формате WKT
monitoring_stations = [
    {'name': 'Koktal Monitoring Station', 'geometry': wkt.loads('POINT(80.2345 41.7654)')}
]

# Добавление станций мониторинга на карту
for station in monitoring_stations:
    folium.Marker(
        location=[station['geometry'].y, station['geometry'].x],
        popup=station['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("4.html")