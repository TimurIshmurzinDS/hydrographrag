import geopandas as gpd
import folium

# Загрузка данных о расходе воды (замените на путь к вашим данным)
data = gpd.read_file("tekes_river_flow.shp") 

# Создание карты
m = folium.Map(location=[43.0, 65.0], zoom_start=8)  # Установите координаты центральной точки реки

# Добавление слоя данных о расходе воды на карту
folium.GeoJson(data, style_function=lambda feature: {
    'fillColor': 'green',
    'color': 'black',
    'weight': 1,
    'fillOpacity': 0.7
}).add_to(m)

# Сохранение карты
m.save("17.html")