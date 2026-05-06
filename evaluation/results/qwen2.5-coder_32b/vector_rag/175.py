import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Инициализация карты с центроидом бассейна
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты реки Сарыкан в формате WKT
sarykan_wkt = "LINESTRING (75.34 41.89, 75.36 41.90, 75.38 41.92)"  # Примерные координаты
sarykan_line = wkt.loads(sarykan_wkt)

# Добавление реки на карту
folium.PolyLine(locations=list(zip(*sarykan_line.xy)), color='blue', weight=2.5, opacity=1).add_to(m)

# Расчет коэффициента связности речной сети
basin_area_km2 = 100  # Примерная площадь бассейна в квадратных километрах (для примера)
sarykan_length_km = sarykan_line.length / 1000  # Длина реки в километрах

connectivity_index = sarykan_length_km / basin_area_km2
print(f"Коэффициент связности речной сети: {connectivity_index:.4f} км/км²")

# Сохранение карты
m.save("175.html")