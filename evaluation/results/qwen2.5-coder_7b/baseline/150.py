import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data = pd.read_csv('water_level_data.csv')

# Предположим, что данные имеют следующие столбцы: 'date', 'latitude', 'longitude', 'level'
# Пример данных:
# date,latitude,longitude,level
# 2023-01-01,43.123456,76.543210,100
# 2023-01-02,43.123456,76.543210,102
# ...

# Очистка данных (удаление пропущенных значений)
data.dropna(inplace=True)

# Создание карты
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# Формирование GeoJSON для визуализации
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
            "time": row['date'],
            "level": row['level']
        }
    }
    geojson_data["features"].append(feature)

# Добавление слоя с временной геоданныей
TimestampedGeoJson(geojson_data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("150.html")