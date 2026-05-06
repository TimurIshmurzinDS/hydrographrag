import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data = pd.read_csv('prokhodnaya_sensor_data.csv')

# Проверка целостности данных
print(data.info())
print(data.isnull().sum())

# Анализ временных рядов
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

# Визуализация данных на карте
m = folium.Map(location=[56.0472, 37.1897], zoom_start=13)  # Координаты примера для Москвы

# Создание слоя с временной геоданныей
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in data.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": row['timestamp'].isoformat(),
            "value": row['sensor_value']
        }
    }
    geojson_data["features"].append(feature)

# Добавление слоя на карту
TimestampedGeoJson(geojson_data, period="PT1M", add_last_point=True).add_to(m)

# Сохранение карты
m.save("12.html")