import pandas as pd
from folium import Map, Marker, CircleMarker, Polygon, PolyLine
from folium.plugins import HeatMap

# Сбор данных о расходе воды на реках Tokyraun и Koktal
tokyraun_data = {
    'Latitude': [55.1234, 55.2345, 55.3456],
    'Longitude': [36.4567, 36.5678, 36.6789],
    'Flow Rate (m3/s)': [10, 20, 30]
}

koktal_data = {
    'Latitude': [54.9012, 54.9123, 54.9234],
    'Longitude': [37.0123, 37.0234, 37.0345],
    'Flow Rate (m3/s)': [15, 25, 35]
}

# Создание данных для анализа
tokyraun_df = pd.DataFrame(tokyraun_data)
koktal_df = pd.DataFrame(koktal_data)

# Анализ данных для определения показателей расхода на каждой реке
tokyraun_avg_flow_rate = tokyraun_df['Flow Rate (m3/s)'].mean()
koktal_avg_flow_rate = koktal_df['Flow Rate (m3/s)'].mean()

print(f'Средний расход воды на реке Tokyraun: {tokyraun_avg_flow_rate} м3/с')
print(f'Средний расход воды на реке Koktal: {koktal_avg_flow_rate} м3/с')

# Сравнение показателей расхода на обоих реках для оценки риска затопления
risk_level = tokyraun_avg_flow_rate / koktal_avg_flow_rate

print(f'Уровень риска затопления: {risk_level:.2f}')

# Визуализация результатов на карте с помощью библиотеки Folium
m = Map(location=[55.0, 36.5], zoom_start=10)

Marker([55.1234, 36.4567], popup='Река Tokyraun').add_to(m)
CircleMarker([54.9012, 37.0123], radius=10000).add_to(m)

HeatMap(tokyraun_data['Latitude'], tokyraun_data['Longitude'], data=tokyraun_data['Flow Rate (m3/s)']).add_to(m)

m.save("80.html")