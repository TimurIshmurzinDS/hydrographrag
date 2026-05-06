import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
lepsy_data = pd.read_csv('lepsy_river_data.csv')
aksu_data = pd.read_csv('aksu_river_data.csv')

# Предположим, что данные имеют столбцы 'date' и 'flow'
# Приведение дат к стандартному формату
lepsy_data['date'] = pd.to_datetime(lepsy_data['date'])
aksu_data['date'] = pd.to_datetime(aksu_data['date'])

# Группировка данных по месяцам и вычисление среднего значения стока
lepsy_monthly_flow = lepsy_data.groupby(lepsy_data['date'].dt.month)['flow'].mean().reset_index()
aksu_monthly_flow = aksu_data.groupby(aksu_data['date'].dt.month)['flow'].mean().reset_index()

# Создание карты
m = folium.Map(location=[50, 40], zoom_start=6)

# Формирование данных для визуализации на карте
lepsy_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [40, 50]},
            "properties": {
                "time": f"{i+1}-01-01T00:00:00Z",
                "value": lepsy_monthly_flow['flow'][i]
            }
        } for i in range(len(lepsy_monthly_flow))
    ]
}

aksu_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [45, 50]},
            "properties": {
                "time": f"{i+1}-01-01T00:00:00Z",
                "value": aksu_monthly_flow['flow'][i]
            }
        } for i in range(len(aksu_monthly_flow))
    ]
}

# Добавление данных на карту
TimestampedGeoJson(lepsy_geojson, period="P1M", add_last_point=True).add_to(m)
TimestampedGeoJson(aksu_geojson, period="P1M", add_last_point=True).add_to(m)

# Сохранение карты
m.save("210.html")