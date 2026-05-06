import folium
from folium.plugins import TimestampedGeoJson
import pandas as pd

# Пример данных о погоде (исторические данные)
historical_data = {
    "time": ["2021-01-01", "2021-01-02", "2021-01-03"],
    "latitude": [55.7558, 55.7558, 55.7558],
    "longitude": [37.6173, 37.6173, 37.6173],
    "temperature": [0, -2, -4]
}

# Пример данных о погоде (современные данные)
modern_data = {
    "time": ["2023-01-01", "2023-01-02", "2023-01-03"],
    "latitude": [55.7558, 55.7558, 55.7558],
    "longitude": [37.6173, 37.6173, 37.6173],
    "temperature": [-2, -4, -6]
}

# Создание DataFrame для исторических данных
historical_df = pd.DataFrame(historical_data)
historical_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["longitude"], row["latitude"]]
            },
            "properties": {
                "time": row["time"],
                "temperature": row["temperature"]
            }
        } for index, row in historical_df.iterrows()
    ]
}

# Создание DataFrame для современных данных
modern_df = pd.DataFrame(modern_data)
modern_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["longitude"], row["latitude"]]
            },
            "properties": {
                "time": row["time"],
                "temperature": row["temperature"]
            }
        } for index, row in modern_df.iterrows()
    ]
}

# Создание карты
m = folium.Map(location=[55.7558, 37.6173], zoom_start=12)

# Добавление исторических данных на карту
TimestampedGeoJson(historical_geojson, period="PT1D", add_last_point=True).add_to(m)

# Добавление современных данных на карту
TimestampedGeoJson(modern_geojson, period="PT1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("281.html")