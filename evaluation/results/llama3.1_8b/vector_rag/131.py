import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с внешними границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(data=basin_gdf.to_json(), name='basin').add_to(m)

# Создайте список словарей с координатами (WKT) для реки Sharyn River
sharyn_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.2345, 'lon': 76.6543},
    # Добавьте остальные координаты вручную
]

# Создайте список словарей с координатами (WKT) для реки Kishi Almaty River
kishi_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.2345, 'lon': 76.6543},
    # Добавьте остальные координаты вручную
]

# Создайте карту расхода воды для реки Sharyn River
sharyn_water_usage_map = folium.Map(location=[43.1234, 76.5432], zoom_start=10)
folium.Marker([43.1234, 76.5432], popup='Река Шарын').add_to(sharyn_water_usage_map)

# Создайте карту расхода воды для реки Kishi Almaty River
kishi_water_usage_map = folium.Map(location=[43.2345, 76.6543], zoom_start=10)
folium.Marker([43.2345, 76.6543], popup='Река Кіші Алматы').add_to(kishi_water_usage_map)

# Сохраните карту расхода воды для реки Sharyn River в файл
m.save("sharyn_water_usage.html")

# Сохраните карту расхода воды для реки Kishi Almaty River в файл
kishi_water_usage_map.save("kishi_water_usage.html")