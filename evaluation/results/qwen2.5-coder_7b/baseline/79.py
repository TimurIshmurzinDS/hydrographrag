import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных о расходе воды реки Turgen River
data = pd.read_csv('turgen_river_water_flow.csv')

# Предположим, что данные имеют следующие столбцы: 'date', 'flow_rate'
# Приведение даты к формату datetime
data['date'] = pd.to_datetime(data['date'])

# Группировка данных по месяцам и вычисление среднего расхода воды
monthly_data = data.groupby(data['date'].dt.month)['flow_rate'].mean().reset_index()
monthly_data.columns = ['month', 'average_flow']

# Создание карты с использованием folium
m = folium.Map(location=[54.167, 83.200], zoom_start=10)

# Добавление слоя данных о расходе воды на карте
TimestampedGeoJson({
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [83.200, 54.167]
            },
            "properties": {
                "time": monthly_data['month'].apply(lambda x: f'{x}-01T00:00:00Z'),
                "value": monthly_data['average_flow']
            }
        }
    ]
}).add_to(m)

# Сохранение карты
m.save("79.html")