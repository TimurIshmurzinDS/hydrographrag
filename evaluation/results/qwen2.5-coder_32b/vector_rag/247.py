import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне реки Каскелен
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположительные координаты притоков реки Каскелен (в формате WKT)
inlets_wkt = [
    "POINT(71.4563 49.8765)",
    "POINT(71.4678 49.8890)"
]

# Преобразование координат из WKT в GeoDataFrame
inlets_gdf = gpd.GeoDataFrame(geometry=[wkt.loads(wkt_str) for wkt_str in inlets_wkt], crs='EPSG:4326')

# Добавление точек притоков на карту
for _, row in inlets_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup="Приток реки Каскелен").add_to(m)

# Сохранение карты в файл
m.save("247.html")