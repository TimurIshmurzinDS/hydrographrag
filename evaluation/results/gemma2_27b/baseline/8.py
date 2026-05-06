import folium
import geopandas as gpd

# Загрузка данных о датчиках (замените на актуальные пути)
sensors = gpd.read_file("sensors_ulken_almaty.shp") 

# Загрузка данных о реке Ulken Almaty River (замените на актуальный источник)
river = gpd.read_file("ulken_almaty_river.shp")

# Создание карты
m = folium.Map(location=[43.25, 76.9], zoom_start=10)

# Добавление реки на карту
folium.GeoJson(river).add_to(m)

# Проверка состояния датчиков (замените на ваш метод получения данных о состоянии)
for index, row in sensors.iterrows():
    sensor_state = "working" # Замените на логику определения состояния датчика

    if sensor_state == "working":
        color = "green"
    else:
        color = "red"

    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"Датчик {row['sensor_id']}: {sensor_state}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохранение карты
m.save("8.html")