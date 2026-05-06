import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data = pd.read_csv('historical_data.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Пример стратегии: покупка при снижении цены и продажа при увеличении цены
def simple_moving_average_strategy(data, window=50):
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['Signal'] = np.where(data['Close'] > data['SMA'], 1, -1)
    data['Position'] = data['Signal'].diff()
    return data

# Применение стратегии
data = simple_moving_average_strategy(data)

# Вычисление доходов
data['Returns'] = data['Close'].pct_change()
data['Strategy_Returns'] = data['Position'].shift(1) * data['Returns']
data['Cumulative_Returns'] = (1 + data['Strategy_Returns']).cumprod()

# Визуализация результатов на карте
m = folium.Map(location=[data.index[0].year, data.index[0].month], zoom_start=2)

geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in data.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [index.year, index.month]
        },
        "properties": {
            "time": index.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "value": row['Cumulative_Returns']
        }
    }
    geojson_data["features"].append(feature)

TimestampedGeoJson(geojson_data).add_to(m)

# Сохранение карты
m.save("285.html")