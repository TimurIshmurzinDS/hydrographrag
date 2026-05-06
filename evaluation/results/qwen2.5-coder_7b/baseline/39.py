import folium
from shapely.geometry import Polygon
import geopandas as gpd
import pandas as pd

# Определение границ бассейна реки Или (пример данных)
il_basin_polygon = Polygon([(105.0, 43.0), (106.0, 43.0), (106.0, 44.0), (105.0, 44.0)])

# Создание GeoDataFrame для бассейна реки Или
il_basin_gdf = gpd.GeoDataFrame({'geometry': [il_basin_polygon]}, crs='EPSG:4326')

# Загрузка данных о доступности воды (пример данных)
water_supply_data = pd.DataFrame({
    'id': [1, 2, 3],
    'latitude': [43.5, 43.7, 43.9],
    'longitude': [105.5, 106.2, 105.8],
    'volume': [1000, 1500, 2000]  # объемы в кубических метрах
})

# Создание GeoDataFrame для данных о доступности воды
water_supply_gdf = gpd.GeoDataFrame(water_supply_data, geometry=gpd.points_from_xy(water_supply_data.longitude, water_supply_data.latitude), crs='EPSG:4326')

# Определение потребностей полива (пример данных)
irrigation_needs_data = pd.DataFrame({
    'id': [1, 2, 3],
    'latitude': [43.5, 43.7, 43.9],
    'longitude': [105.5, 106.2, 105.8],
    'volume': [500, 750, 1000]  # объемы в кубических метрах
})

# Создание GeoDataFrame для потребностей полива
irrigation_needs_gdf = gpd.GeoDataFrame(irrigation_needs_data, geometry=gpd.points_from_xy(irrigation_needs_data.longitude, irrigation_needs_data.latitude), crs='EPSG:4326')

# Визуализация на карте
m = folium.Map(location=[43.5, 105.8], zoom_start=7)

folium.GeoJson(il_basin_gdf.to_json(), style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)
folium.GeoJson(water_supply_gdf.to_json(), style_function=lambda x: {'color': 'green', 'weight': 1}).add_to(m)
folium.GeoJson(irrigation_needs_gdf.to_json(), style_function=lambda x: {'color': 'red', 'weight': 1}).add_to(m)

# Сохранение карты
m.save("39.html")