import folium
import geopandas as gpd

# Загружаем данные о реке Караой в формате GeoJSON
river_data = gpd.read_file("karaoy_river.geojson")

# Создаем карту с центром над рекой Караой
m = folium.Map(location=[river_data.geometry.centroid.y.mean(), river_data.geometry.centroid.x.mean()], zoom_start=10)

# Добавляем реку Караой на карту
folium.GeoJson(river_data, style_function=lambda x: {'fillColor': 'blue', 'color': 'black'}).add_to(m)

# Определяем путь для робота по течению реки от истока до устья
path_coords = [(x, y) for _, (x, y) in river_data.geometry.centroid.coords]

# Добавляем путь для робота на карту
folium.PolyLine(path_coords, weight=5, color='red').add_to(m)

# Сохраняем карту в формате HTML с именем "224.html"
m.save("224.html")