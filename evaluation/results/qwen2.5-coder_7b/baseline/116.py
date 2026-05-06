import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2020', periods=365, freq='D'),
    'tekeli_level': np.random.normal(loc=100, scale=5, size=365),
    'lepsy_level': np.random.normal(loc=80, scale=3, size=365)
}

# Создание DataFrame
df = pd.DataFrame(data)

# Визуализация данных
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['tekeli_level'], label='Tekeli River')
plt.plot(df['date'], df['lepsy_level'], label='Lepsy River')
plt.xlabel('Date')
plt.ylabel('Water Level (m)')
plt.title('Water Level in Tekeli and Lepsy Rivers')
plt.legend()
plt.show()

# Создание карты
m = folium.Map(location=[40.7128, -74.0060], zoom_start=5)

# Пример данных для визуализации на карте (замените на реальные данные)
geo_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [40.7128, -74.0060]
            },
            "properties": {
                "time": df['date'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').values,
                "value": df['tekeli_level'].values
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [40.7128, -74.0060]
            },
            "properties": {
                "time": df['date'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').values,
                "value": df['lepsy_level'].values
            }
        }
    ]
}

# Добавление данных на карту
TimestampedGeoJson(geo_data, period="PT1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("116.html")