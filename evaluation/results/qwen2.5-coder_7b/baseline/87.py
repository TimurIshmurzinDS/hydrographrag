import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка текущих данных расхода воды на реке Prokhodnaya River
current_data = pd.read_csv('current_flow_data.csv')

# Загрузка исторических данных весеннего паводка
historical_data = pd.read_csv('historical_flood_data.csv')

# Пример структуры данных:
# current_data: {'date': [datetime], 'flow_rate': [float]}
# historical_data: {'year': [int], 'peak_flow_rate': [float]}

# Обработка данных
current_data['date'] = pd.to_datetime(current_data['date'])
historical_data['year'] = historical_data['year'].astype(int)

# Анализ данных
# Пример анализа: сравнение текущего расхода с историческими пиками
current_peak_flow = current_data['flow_rate'].max()
historical_peaks = historical_data['peak_flow_rate']

# Визуализация данных на карте
m = folium.Map(location=[50.123, 47.456], zoom_start=10)

# Добавление текущего расхода воды на карту
current_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [47.456, 50.123]
            },
            "properties": {
                "time": current_data['date'].max().isoformat(),
                "flow_rate": current_peak_flow,
                "description": f"Текущий расход воды: {current_peak_flow} м³/с"
            }
        }
    ]
}

TimestampedGeoJson(current_geojson, period="PT1H", add_last_point=True).add_to(m)

# Добавление исторических пиков паводка на карту
historical_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [47.456, 50.123]
            },
            "properties": {
                "time": f"{year}-03-01T00:00:00Z",
                "flow_rate": peak_flow,
                "description": f"Исторический пик паводка {year}: {peak_flow} м³/с"
            }
        } for year, peak_flow in zip(historical_data['year'], historical_peaks)
    ]
}

TimestampedGeoJson(historical_geojson, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("87.html")