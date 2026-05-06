import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data = {
    'date': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01'],
    'river': ['Lepsy', 'Lepsy', 'Lepsy', 'Shilik', 'Shilik'],
    'flow_volume': [100, 150, 200, 180, 220]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Группировка данных по рекам и расчет сезонного стока
seasonal_stock = df.groupby(['river', df['date'].dt.month]).sum().reset_index()

# Визуализация на карте
m = folium.Map(location=[50.45, 30.52], zoom_start=10)

for index, row in seasonal_stock.iterrows():
    if row['river'] == 'Lepsy':
        color = 'blue'
    else:
        color = 'red'
    
    folium.CircleMarker(
        location=[50.45, 30.52],  # Пример координат (замените на реальные)
        radius=row['flow_volume'] / 10,
        popup=f"{row['river']} - {row['date'].month} - {row['flow_volume']}",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

m.save("152.html")