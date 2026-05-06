import geopandas as gpd
import folium

# Загрузить данные о координатах русел рек
shynzhy_river = gpd.read_file("path/to/shynzhy_river.shp")
talgar_river = gpd.read_file("path/to/talgar_river.shp")

# Выполнить операцию пересечения координат
intersection = gpd.overlay(shynzhy_river, talgar_river, how='intersection')

# Создать карту с помощью folium
m = folium.Map(location=[43.25, 76.9], zoom_start=10)

# Добавить слой пересечения на карту
folium.GeoJson(data=intersection).add_to(m)

# Сохранить карту в html файл
m.save("169.html")