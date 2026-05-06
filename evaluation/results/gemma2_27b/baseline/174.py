import geopandas as gpd
import folium

# Загрузка данных о водоразделах из Shapefile
watersheds_emely = gpd.read_file("path/to/emely_watershed.shp")
watersheds_tentek = gpd.read_file("path/to/tentek_watershed.shp")

# Вычисление точек пересечения
intersection = gpd.overlay(watersheds_emely, watersheds_tentek, how='intersection')

# Извлечение координат точек пересечения
intersection_points = intersection[['geometry']]

# Создание карты с Folium
m = folium.Map(location=[43.5, 78.5], zoom_start=10)

# Добавление точек пересечения на карту
for index, row in intersection_points.iterrows():
    folium.Marker(location=row['geometry'].coords[0]).add_to(m)

# Сохранение карты в HTML-файл
m.save("174.html")