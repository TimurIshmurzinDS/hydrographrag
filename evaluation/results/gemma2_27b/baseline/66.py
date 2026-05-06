import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о местоположении оборудования
equipment = gpd.read_file("equipment_data.shp")  # Замените на путь к файлу с данными

# Загрузка данных о гидрологической сети реки Temirlik
river = gpd.read_file("temirlik_river.shp") # Замените на путь к файлу с данными

# Расчет расстояния до реки
equipment["distance_to_river"] = equipment.geometry.apply(lambda point: river.geometry.distance(point))

# Выделение оборудования вблизи реки (например, на расстоянии менее 100 метров)
near_river_equipment = equipment[equipment["distance_to_river"] < 100]

# Создание карты
m = folium.Map(location=[equipment.geometry.y.mean(), equipment.geometry.x.mean()], zoom_start=12)

# Добавление гидрологической сети реки на карту
folium.GeoJson(river).add_to(m)

# Добавление оборудования на карту
for index, row in equipment.iterrows():
    folium.Marker(location=[row.geometry.y, row.geometry.x], popup=f"Оборудование {index}").add_to(m)

# Добавление оборудования вблизи реки с другим цветом маркера
for index, row in near_river_equipment.iterrows():
    folium.Marker(location=[row.geometry.y, row.geometry.x], popup=f"Оборудование {index}", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("66.html")