import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data = pd.read_csv('dos_river_nanos_data.csv')

# Предположим, что данные имеют следующие столбцы: 'latitude', 'longitude', 'nanos_count', 'date'
# Пример данных:
# latitude,longitude,nanos_count,date
# 40.7128,-74.0060,50,2023-01-01
# 40.7129,-74.0061,60,2023-01-02

# Преобразование даты в формат datetime
data['date'] = pd.to_datetime(data['date'])

# Фильтрация данных за последние 5 лет
end_date = data['date'].max()
start_date = end_date - pd.DateOffset(years=5)
filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# Создание карты
m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=10)

# Преобразование данных в формат GeoJSON для визуализации на карте
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in filtered_data.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": row['date'].isoformat(),
            "nanos_count": row['nanos_count']
        }
    }
    geojson_data["features"].append(feature)

# Добавление слоя GeoJSON на карту
TimestampedGeoJson(geojson_data, period="PT1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("56.html")