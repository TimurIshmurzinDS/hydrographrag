import geopandas as gpd
from shapely.geometry import Point
import folium
import datetime

# Загрузка данных о станциях мониторинга (замените на актуальный путь к файлу)
stations = gpd.read_file("koktal_monitoring_stations.shp")

# Текущее время
now = datetime.datetime.now()

# Порог для определения работающей станции (1 час)
threshold = datetime.timedelta(hours=1)

# Создание карты
m = folium.Map(location=[stations.geometry.y.mean(), stations.geometry.x.mean()], zoom_start=12)

# Проверка статуса каждой станции и добавление на карту
for index, row in stations.iterrows():
    last_update = datetime.datetime.strptime(row['last_update'], '%Y-%m-%d %H:%M:%S')  # Замените на формат даты из ваших данных

    if now - last_update < threshold:
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=f"Станция {row['station_name']}: Работает",
            icon=folium.Icon(color='green')
        ).add_to(m)
    else:
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=f"Станция {row['station_name']}: Не работает",
            icon=folium.Icon(color='red')
        ).add_to(m)

# Сохранение карты
m.save("4.html")