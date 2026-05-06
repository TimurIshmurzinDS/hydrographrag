import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Кумбель
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты (WKT), создаем список словарей
# Например, предположим, что у нас есть следующие данные о реке:
river_coordinates_wkt = "LINESTRING(37.618421 55.755826, 37.620999 55.755826, 37.623577 55.755826)"
river_coordinates = wkt.loads(river_coordinates_wkt)

# Добавление реки на карту
folium.PolyLine(locations=river_coordinates.coords, color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("251.html")