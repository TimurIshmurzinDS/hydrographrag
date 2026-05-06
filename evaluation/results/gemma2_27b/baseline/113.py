import geopandas as gpd
import folium

# Загрузка данных о реках
rivers = gpd.read_file("rivers.shp")

# Загрузка данных о флоре и фауне
species = gpd.read_file("species.shp")

# Модель снижения уровня воды (пример)
water_level_change = -0.5 # Изменение уровня воды в метрах

# Определение зон, которые будут затронуты
affected_zones = rivers.buffer(distance=water_level_change)

# Оценка воздействия на виды флоры и фауны
affected_species = species[species.intersects(affected_zones)]

# Визуализация результатов
m = folium.Map(location=[rivers.centroid.y, rivers.centroid.x], zoom_start=10)

# Добавление рек на карту
folium.GeoJson("rivers.shp").add_to(m)

# Добавление видов флоры и фауны на карту
folium.GeoJson("species.shp", name="Species").add_to(m)

# Добавление зон, которые будут затронуты снижением уровня воды
folium.GeoJson(affected_zones).add_to(m)

# Сохранение карты
m.save("113.html")