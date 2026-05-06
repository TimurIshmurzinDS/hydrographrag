import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных: Дата, Уровень воды (м), Широта, Долгота
data = {
    'Date': ['2023-04-01', '2023-04-02', '2023-04-03', '2023-04-04'],
    'WaterLevel': [1.5, 1.6, 1.7, 1.8],
    'Latitude': [55.123, 55.124, 55.125, 55.126],
    'Longitude': [80.123, 80.124, 80.125, 80.126]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование даты в формат datetime
df['Date'] = pd.to_datetime(df['Date'])

# Определение временного периода весеннего таяния (например, с апреля по июнь)
winter_melt_period = df[(df['Date'].dt.month >= 4) & (df['Date'].dt.month <= 6)]

# Создание карты
m = folium.Map(location=[55.123, 80.123], zoom_start=12)

# Добавление точек с уровнями воды на карте
for index, row in winter_melt_period.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Уровень воды: {row['WaterLevel']} м",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("27.html")