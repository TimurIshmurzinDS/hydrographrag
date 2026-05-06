import folium
from folium.plugins import TimestampedGeoJson
import pandas as pd

# Загрузим данные о реке Prokhodnaya River и работе сенсора в формате GeoJSON или Shapefile.
river_data = pd.read_json('prokhodnaya_river.geojson')
sensor_data = pd.read_csv('sensor_data.csv')

# Создадим слой ошибок
def create_error_layer(sensor_data, river_data):
    errors = []
    for index, row in sensor_data.iterrows():
        # Используем функцию FuzzyWuzzy для определения сходства между координатами сенсора и координатами реки.
        similarity = fuzz.ratio(row['lat'], river_data.loc[river_data['lat'] == row['lat'], 'lat'].values[0])
        if similarity > 80:
            errors.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [row['lon'], row['lat']]
                },
                'properties': {'error': True}
            })
    return errors

# Создадим слой с ошибками
error_layer = create_error_layer(sensor_data, river_data)

# Визуализируем результаты на карте
m = folium.Map(location=[river_data['lat'].mean(), river_data['lon'].mean()], zoom_start=10)
folium.GeoJson(river_data).add_to(m)
folium.Marker([sensor_data['lat'].mean(), sensor_data['lon'].mean()], popup='Сенсор').add_to(m)

# Добавляем слой ошибок на карту
TimestampedGeoJson({
    'type': 'FeatureCollection',
    'features': error_layer
}, period='PT1H', add_last_point=True, auto_play=False).add_to(m)

# Сохраняем карту в файл
m.save("12.html")