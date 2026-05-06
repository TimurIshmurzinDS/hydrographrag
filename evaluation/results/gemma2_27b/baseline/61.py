import geopandas as gpd
import folium

# Загрузка данных о датчиках
sensors = gpd.read_file("sensors_data.shp")  # Замените на путь к файлу с данными

# Определение статуса датчиков (пример)
status_mapping = {
    "sensor_id1": "работающий",
    "sensor_id2": "неисправный",
    "sensor_id3": "требуется обслуживание",
}

sensors["status"] = sensors["sensor_id"].map(status_mapping)

# Создание карты
m = folium.Map(location=[sensors.geometry.y.mean(), sensors.geometry.x.mean()], zoom_start=10)

# Добавление датчиков на карту
for index, row in sensors.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"ID: {row['sensor_id']}<br>Статус: {row['status']}",
        icon=folium.Icon(color="green" if row["status"] == "работающий" else "red")
    ).add_to(m)

# Сохранение карты
m.save("61.html")