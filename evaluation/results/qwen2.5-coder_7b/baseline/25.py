import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data_tekes = {
    'timestamp': ['2023-07-01 00:00', '2023-07-02 00:00', '2023-07-03 00:00'],
    'flow_rate_tekes': [50, 60, 70]
}

data_bayankol = {
    'timestamp': ['2023-07-01 00:00', '2023-07-02 00:00', '2023-07-03 00:00'],
    'flow_rate_bayankol': [40, 50, 60]
}

# Преобразование данных в DataFrame
df_tekes = pd.DataFrame(data_tekes)
df_bayankol = pd.DataFrame(data_bayankol)

# Преобразование времени в datetime
df_tekes['timestamp'] = pd.to_datetime(df_tekes['timestamp'])
df_bayankol['timestamp'] = pd.to_datetime(df_bayankol['timestamp'])

# Создание карты
m = folium.Map(location=[50, 10], zoom_start=4)

# Добавление данных на карту
for index, row in df_tekes.iterrows():
    folium.Marker(
        location=[50, 10],
        popup=f'Tekes River: {row["flow_rate_tekes"]} m³/s',
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

for index, row in df_bayankol.iterrows():
    folium.Marker(
        location=[50, 10],
        popup=f'Bayankol River: {row["flow_rate_bayankol"]} m³/s',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("25.html")