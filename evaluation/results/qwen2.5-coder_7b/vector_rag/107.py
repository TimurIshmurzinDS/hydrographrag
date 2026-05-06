import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ручья Temirlik River и Tekeli River на карту
temirlik_river_wkt = "POLYGON((...))"  # Замените WKT на реальные данные
tekeli_river_wkt = "POLYGON((...))"   # Замените WKT на реальные данные

temirlik_river_gdf = gpd.GeoDataFrame(geometry=[wkt.loads(temirlik_river_wkt)], crs='EPSG:4326')
tekeli_river_gdf = gpd.GeoDataFrame(geometry=[wkt.loads(tekeli_river_wkt)], crs='EPSG:4326')

folium.GeoJson(temirlik_river_gdf.to_json(), style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)
folium.GeoJson(tekeli_river_gdf.to_json(), style_function=lambda x: {'color': 'red', 'weight': 2}).add_to(m)

# Добавление границы ручья на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохранение карты
m.save("107.html")