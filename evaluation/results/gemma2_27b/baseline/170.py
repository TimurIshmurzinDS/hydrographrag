import geopandas as gpd
import folium

# Загрузить данные о гидрографической сети
rivers = gpd.read_file("path/to/rivers.shp")

# Найти ручей Терисбутак
terisbutak = rivers[rivers["name"] == "Терисбутак"]

# Определить иерархию речной сети (например, с помощью функции upstream)
# ...

# Найти основные артерии (например, по длине или площади бассейна)
main_arteries = rivers[rivers["length"] > 100] # Пример: реки длиннее 100 км

# Создать карту Folium
m = folium.Map(location=[terisbutak.y.iloc[0], terisbutak.x.iloc[0]], zoom_start=8)

# Добавить ручей Терисбутак на карту
folium.GeoJson(terisbutak, name="Терисбутак", style_geojson={'color': 'blue', 'weight': 3}).add_to(m)

# Добавить основные артерии на карту
folium.GeoJson(main_arteries, name="Основные артерии", style_geojson={'color': 'red', 'weight': 2}).add_to(m)

# Сохранить карту
m.save("170.html")