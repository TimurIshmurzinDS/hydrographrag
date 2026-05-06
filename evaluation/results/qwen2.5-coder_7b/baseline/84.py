import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Загрузка данных о гидропостах
data = pd.read_csv('hydrometers.csv')

# Фильтрация данных по времени (весеннее половодье, пример: с марта по июнь)
start_date = '2023-03-01'
end_date = '2023-06-30'
filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# Создание карты
m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=10)

# Группировка данных по гидропостам и расчет среднего расхода воды
grouped_data = filtered_data.groupby('hydrometer_id').agg({'flow_rate': 'mean'}).reset_index()

# Определение порога для резкого роста (например, увеличение более чем на 50%)
threshold = 1.5

# Фильтрация гидропостов с резким ростом расхода
risky_hydrometers = grouped_data[grouped_data['flow_rate'] > threshold * filtered_data.groupby('hydrometer_id')['flow_rate'].transform('mean')]

# Добавление маркеров на карту
marker_cluster = MarkerCluster().add_to(m)

for index, row in risky_hydrometers.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Гидропост {row['hydrometer_id']}: Резкий рост расхода воды",
        icon=folium.Icon(color='red', icon='warning')
    ).add_to(marker_cluster)

# Сохранение карты
m.save("84.html")