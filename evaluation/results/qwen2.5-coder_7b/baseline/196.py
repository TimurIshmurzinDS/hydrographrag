import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data_koksu = {
    'date': pd.date_range(start='2013-01-01', periods=10*365, freq='D'),
    'flow_rate': np.random.randint(100, 1000, size=10*365)
}

data_emel = {
    'date': pd.date_range(start='2013-01-01', periods=10*365, freq='D'),
    'flow_rate': np.random.randint(100, 1000, size=10*365)
}

# Создание DataFrame
df_koksu = pd.DataFrame(data_koksu)
df_emel = pd.DataFrame(data_emel)

# Преобразование дат в формат datetime
df_koksu['date'] = pd.to_datetime(df_koksu['date'])
df_emel['date'] = pd.to_datetime(df_emel['date'])

# Группировка данных по месяцам и вычисление среднего расхода воды
monthly_koksu = df_koksu.groupby(df_koksu['date'].dt.month)['flow_rate'].mean().reset_index()
monthly_emel = df_emel.groupby(df_emel['date'].dt.month)['flow_rate'].mean().reset_index()

# Переименование столбцов для удобства
monthly_koksu.columns = ['month', 'avg_flow_rate_koksu']
monthly_emel.columns = ['month', 'avg_flow_rate_emel']

# Визуализация сезонных закономерностей
plt.figure(figsize=(12, 6))
plt.plot(monthly_koksu['month'], monthly_koksu['avg_flow_rate_koksu'], label='Koksu River')
plt.plot(monthly_emel['month'], monthly_emel['avg_flow_rate_emel'], label='Emel River', linestyle='--')
plt.xlabel('Month')
plt.ylabel('Average Flow Rate (m³/s)')
plt.title('Seasonal Variations in Water Flow Rate for Koksu and Emel Rivers')
plt.legend()
plt.show()

# Создание карты для визуализации
m = folium.Map(location=[43.0, 76.0], zoom_start=5)

# Пример данных для визуализации на карте (замените на реальные данные)
geojson_koksu = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [76.0, 43.0]
            },
            "properties": {
                "name": "Koksu River",
                "flow_rate": monthly_koksu['avg_flow_rate_koksu'].mean()
            }
        }
    ]
}

geojson_emel = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [76.0, 43.0]
            },
            "properties": {
                "name": "Emel River",
                "flow_rate": monthly_emel['avg_flow_rate_emel'].mean()
            }
        }
    ]
}

# Добавление данных на карту
TimestampedGeoJson(geojson_koksu, period="P1D", add_last_point=True).add_to(m)
TimestampedGeoJson(geojson_emel, period="P1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("196.html")