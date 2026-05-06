import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Талгар
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты мониторинговых станций (WKT)
monitoring_stations_wkt = [
    "POINT(76.95 43.15)",
    "POINT(77.00 43.20)"
]

# Преобразование WKT в GeoDataFrame
monitoring_stations = gpd.GeoDataFrame(geometry=[wkt.loads(point) for point in monitoring_stations_wkt], crs='EPSG:4326')

# Добавление точек мониторинговых станций на карту
for idx, row in monitoring_stations.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=f"Мониторинговая станция {idx+1}").add_to(m)

# Сохранение карты в файл
m.save("40.html")