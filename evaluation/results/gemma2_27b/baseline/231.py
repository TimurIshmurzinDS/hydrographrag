import folium
import geopandas as gpd

# Загрузить данные о реке Коктал
river = gpd.read_file("river_koktal.shp")

# Загрузить данные о затоплении
flood = gpd.read_file("flood_zones.shp")

# Загрузить данные о посадках пшеницы и помидоров
wheat = gpd.read_file("wheat_fields.shp")
tomatoes = gpd.read_file("tomato_fields.shp")

# Создать карту
m = folium.Map(location=[43.25, 78.1], zoom_start=10)

# Добавить слой реки
folium.GeoJson(river).add_to(m)

# Добавить слой затопления
folium.GeoJson(flood, style_function=lambda feature: {'fillColor': 'blue', 'fillOpacity': 0.5}).add_to(m)

# Добавить слой пшеницы
folium.GeoJson(wheat).add_to(m)

# Добавить слой помидоров
folium.GeoJson(tomatoes).add_to(m)

# Сохранить карту
m.save("231.html")