import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data_2020 = pd.read_csv('sarykan_water_flow_2020.csv')
data_2023 = pd.read_csv('sarykan_water_flow_2023.csv')

# Убедитесь, что данные отсортированы по датам
data_2020['date'] = pd.to_datetime(data_2020['date'])
data_2023['date'] = pd.to_datetime(data_2023['date'])

data_2020.sort_values(by='date', inplace=True)
data_2023.sort_values(by='date', inplace=True)

# Создание словарей для визуализации
geojson_2020 = {
    "type": "FeatureCollection",
    "features": []
}

geojson_2023 = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in data_2020.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": row['date'].isoformat(),
            "value": row['flow']
        }
    }
    geojson_2020["features"].append(feature)

for index, row in data_2023.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": row['date'].isoformat(),
            "value": row['flow']
        }
    }
    geojson_2023["features"].append(feature)

# Создание карты
m = folium.Map(location=[data_2020['latitude'].mean(), data_2020['longitude'].mean()], zoom_start=10)

# Добавление слоев данных на карту
TimestampedGeoJson(geojson_2020, period="PT1M", add_last_point=True).add_to(m)
TimestampedGeoJson(geojson_2023, period="PT1M", add_last_point=True).add_to(m)

# Добавление легенды
folium.LayerControl().add_to(m)

# Сохранение карты
m.save("58.html")