import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data_kurty = {
    'date': ['2018-04-01', '2018-05-01', '2018-06-01', '2019-04-01', '2019-05-01', '2019-06-01', 
             '2020-04-01', '2020-05-01', '2020-06-01', '2021-04-01', '2021-05-01', '2021-06-01'],
    'flow': [10, 15, 20, 12, 18, 25, 13, 17, 22, 14, 19, 26]
}

data_tekes = {
    'date': ['2018-04-01', '2018-05-01', '2018-06-01', '2019-04-01', '2019-05-01', '2019-06-01', 
             '2020-04-01', '2020-05-01', '2020-06-01', '2021-04-01', '2021-05-01', '2021-06-01'],
    'flow': [8, 13, 18, 10, 16, 23, 11, 15, 20, 12, 17, 24]
}

# Преобразование данных в DataFrame
kurty_df = pd.DataFrame(data_kurty)
tekes_df = pd.DataFrame(data_tekes)

# Преобразование даты в формат datetime
kurty_df['date'] = pd.to_datetime(kurty_df['date'])
tekes_df['date'] = pd.to_datetime(tekes_df['date'])

# Создание карты
m = folium.Map(location=[52.0, 19.0], zoom_start=6)

# Добавление данных на карту
kurty_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [19.5, 52.0]  # Координаты примера (замените на реальные)
            },
            "properties": {
                "time": kurty_df['date'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').tolist(),
                "value": kurty_df['flow'].tolist()
            }
        }
    ]
}

tekes_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [19.5, 52.0]  # Координаты примера (замените на реальные)
            },
            "properties": {
                "time": tekes_df['date'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').tolist(),
                "value": tekes_df['flow'].tolist()
            }
        }
    ]
}

TimestampedGeoJson(kurty_geojson, period="PT1D", add_last_point=True).add_to(m)
TimestampedGeoJson(tekes_geojson, period="PT1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("129.html")