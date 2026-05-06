import geopandas as gpd
import folium

# Загрузка данных о реках Уржар, Дос и Каратал в GeoDataFrame
rivers = gpd.read_file('rivers.shp')

# Получение координат для каждой реки
coords = rivers.geometry.coords.xy

# Создание карты с помощью Folium
m = folium.Map(location=[43.2, 68.9], zoom_start=5)

# Добавление рек на карту
for river in rivers.itertuples():
    folium.GeoJson(
        river.geometry,
        style_function=lambda x, y, z: {'fillColor': 'blue', 'color': 'black'},
        highlight_function=lambda x: {'weight': 2}
    ).add_to(m)

# Сохранение карты в файл HTML
m.save("103.html")