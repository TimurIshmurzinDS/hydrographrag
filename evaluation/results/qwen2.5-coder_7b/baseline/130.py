import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных (пример)
bayankol_data = pd.read_csv('bayankol_data.csv')
shilik_data = pd.read_csv('shilik_data.csv')

# Пример структуры данных:
# bayankol_data: {'date': [datetime], 'flow': [float]}
# shilik_data: {'date': [datetime], 'flow': [float]}

# Выравнивание временных рядов
bayankol_data.set_index('date', inplace=True)
shilik_data.set_index('date', inplace=True)

# Убедитесь, что временные ряды имеют одинаковый периодичность
bayankol_data = bayankol_data.resample('D').mean().fillna(method='ffill')
shilik_data = shilik_data.resample('D').mean().fillna(method='ffill')

# Измерение отклонения
flow_difference = bayankol_data['flow'] - shilik_data['flow']

# Создание карты с использованием folium
m = folium.Map(location=[50, 120], zoom_start=6)

# Пример данных для визуализации (замените на реальные данные)
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [120, 50]
            },
            "properties": {
                "time": "2023-04-01T00:00:00Z",
                "flow_difference": flow_difference.loc['2023-04-01']
            }
        }
    ]
}

# Добавление данных на карту
TimestampedGeoJson(geojson_data, period="PT1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("130.html")