import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных из CSV файла
data = pd.read_csv('ulken_almaty_river_floods.csv')

# Предположим, что данные имеют следующие столбцы: 'date', 'latitude', 'longitude', 'flood_level'
# Пример данных:
# date,latitude,longitude,flood_level
# 2019-03-15,43.21,76.54,1.2
# 2020-03-18,43.22,76.55,1.5

# Фильтрация данных для весеннего периода (например, марта)
spring_data = data[(data['date'].dt.month == 3)]

# Создание карты
m = folium.Map(location=[43.21, 76.54], zoom_start=10)

# Формирование GeoJSON данных для визуализации на карте
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in spring_data.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": row['date'].isoformat(),
            "flood_level": row['flood_level'],
            "popup": f"Дата: {row['date']}, Уровень паводка: {row['flood_level']} м"
        }
    }
    geojson_data["features"].append(feature)

# Добавление данных на карту
TimestampedGeoJson(geojson_data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты в файл
m.save("24.html")