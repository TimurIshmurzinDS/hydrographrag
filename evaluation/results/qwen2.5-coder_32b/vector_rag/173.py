import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование в CRS EPSG:4326
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs(epsg=4326)

# Инициализация карты с центроидом бассейна и тайлами 'CartoDB positron'
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты реки Шынжалы в формате WKT (пример)
shynzhaly_coords_wkt = "LINESTRING(76.9438 43.1540, 76.9442 43.1545, 76.9445 43.1550)"
shynzhaly_line = gpd.GeoSeries([wkt.loads(shynzhaly_coords_wkt)], crs="EPSG:4326")

# Добавление линии реки Шынжалы на карту
folium.GeoJson(shynzhaly_line.to_json(), name="Shynzhaly River", style_function=lambda x: {'color': 'blue', 'weight': 3}).add_to(m)

# Сохранение карты в файл
m.save("173.html")