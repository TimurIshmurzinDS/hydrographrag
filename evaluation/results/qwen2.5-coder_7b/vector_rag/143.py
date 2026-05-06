import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках из контекста
karatal_river = {
    "name": "Karatal River",
    "geometry": wkt.loads("POLYGON((...))")  # Здесь нужно вставить WKT координаты Каратал ручья
}

koktal_river = {
    "name": "Koktal River",
    "geometry": wkt.loads("POLYGON((...))")  # Здесь нужно вставить WKT координаты Лепского ручья
}

# Создание GeoDataFrame для рек
rivers_gdf = gpd.GeoDataFrame([karatal_river, koktal_river], crs='EPSG:4326')

# Загрузка данных о гидропостах (если есть)
# Пример данных:
hydro_stations = [
    {"name": "Station 1", "geometry": wkt.loads("POINT(...)")},  # Здесь нужно вставить WKT координаты первого гидропоста
    {"name": "Station 2", "geometry": wkt.loads("POINT(...)")}   # Здесь нужно вставить WKT координаты второго гидропоста
]

# Создание GeoDataFrame для гидропостов
stations_gdf = gpd.GeoDataFrame(hydro_stations, crs='EPSG:4326')

# Загрузка границ бассейна из контекста (если есть)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.to_crs('EPSG:4326', inplace=True)

# Создание карты
m = folium.Map(location=[basin_data.geometry.centroid.y.mean(), basin_data.geometry.centroid.x.mean()], tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Добавление рек на карту
folium.GeoJson(rivers_gdf, style_function=lambda x: {'color': 'blue'}).add_to(m)

# Добавление гидропостов на карту
for idx, row in stations_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=row['name']).add_to(m)

# Сохранение карты
m.save("143.html")