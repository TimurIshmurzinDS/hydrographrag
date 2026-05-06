import geopandas as gpd
import folium

# Загрузка данных о сезонных паводках (замените на актуальный путь к файлу)
flood_zones = gpd.read_file("path/to/flood_zones.shp")

# Загрузка данных о русле реки Bayankol River (замените на актуальный путь к файлу)
river = gpd.read_file("path/to/bayankol_river.shp")

# Пространственный запрос для определения пересечений
intersections = flood_zones.intersects(river.unary_union)

# Создание карты с folium
m = folium.Map(location=[48.0, 85.0], zoom_start=8)  # Установите координаты и масштаб по необходимости

# Добавление данных о реке на карту
folium.GeoJson(river).add_to(m)

# Добавление данных о зонах риска паводков на карту
folium.GeoJson(flood_zones[intersections]).add_to(m)

# Сохранение карты в HTML-файл
m.save("18.html")