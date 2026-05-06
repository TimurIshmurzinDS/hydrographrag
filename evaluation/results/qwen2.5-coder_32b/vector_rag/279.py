import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Инициализация карты folium с центром в центроиде бассейна
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_gdf.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о ценах на недвижимость и их координатах (WKT)
properties_data = [
    {"price": 500000, "geometry": wkt.loads("POINT(37.6173 55.7558)")},  # Пример для Москвы
    {"price": 400000, "geometry": wkt.loads("POINT(30.3158 59.9391)")},  # Пример для Санкт-Петербурга
    {"price": 600000, "geometry": wkt.loads("POINT(37.6225 55.7447)")}   # Еще один пример для Москвы
]

# Преобразование данных в GeoDataFrame
properties_gdf = gpd.GeoDataFrame(properties_data, crs='EPSG:4326')

# Добавление точек на карту
for _, row in properties_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=f"Price: {row.price}").add_to(m)

# Сохранение карты в HTML файл
m.save("279.html")