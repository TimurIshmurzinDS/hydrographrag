import geopandas as gpd
import folium

# Загрузка данных о сенсорах
sensors = gpd.read_file("sensors_data.shp")  # Замените на путь к вашему файлу

# Создание карты
m = folium.Map(location=[sensors.geometry.y.mean(), sensors.geometry.x.mean()], zoom_start=12)

# Добавление сенсоров на карту
for index, row in sensors.iterrows():
    status = row['status']  # Замените 'status' на название столбца со статусом

    if status == "Работающий":
        color = "green"
    elif status == "Неисправный":
        color = "red"
    else:
        color = "gray"

    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"Статус: {status}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохранение карты
m.save("6.html")