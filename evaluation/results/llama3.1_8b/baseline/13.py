# Импорт необходимых библиотек
import pandas as pd
from folium import Map, Marker
from folium.plugins import TimestampedGeoJson

# Загрузка данных о уровне воды в реке Кумбель за последнее время (предположим, данные хранятся в файле 'water_level_data.csv')
data = pd.read_csv('water_level_data.csv')

# Подготовка данных к анализу и моделированию
data['timestamp'] = pd.to_datetime(data['timestamp'])
data['latitude'] = data['latitude'].astype(float)
data['longitude'] = data['longitude'].astype(float)

# Создание географической карты с указанием местоположения реки Кумбель и последних показаний уровня воды
m = Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# Добавление маркера на карте для указания местоположения реки Кумбель
Marker([data['latitude'].mean(), data['longitude'].mean()]).add_to(m)

# Создание временного гео-JSON с последними показаниями уровня воды
geojson = {
    'type': 'FeatureCollection',
    'features': [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [data['longitude'].iloc[-1], data['latitude'].iloc[-1]]
            },
            'properties': {
                'timestamp': data['timestamp'].iloc[-1],
                'water_level': data['water_level'].iloc[-1]
            }
        }
    ]
}

# Добавление временного гео-JSON на карту
TimestampedGeoJson(geojson, period='P1D', add_last_point=True).add_to(m)

# Сохранение карты в файл '13.html'
m.save('13.html')