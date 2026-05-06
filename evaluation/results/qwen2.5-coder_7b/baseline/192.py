import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о колебаниях стока реки Бутак (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2023', periods=365, freq='D'),
    'flow': np.sin(np.linspace(0, 4 * np.pi, 365)) * 100 + 500
}
df_flow = pd.DataFrame(data)

# Пример данных об агроценозах (замените на реальные данные)
data_crops = {
    'lat': [55.755826, 55.755826, 55.755826],
    'lon': [37.617300, 37.617400, 37.617500],
    'crop_type': ['Овес', 'Пшеница', 'Рис']
}
df_crops = pd.DataFrame(data_crops)

# Создание карты
m = folium.Map(location=[55.755826, 37.617300], zoom_start=14)

# Визуализация данных о колебаниях стока реки
folium.PolyLine(
    locations=df_flow[['date', 'flow']].values,
    color='blue',
    weight=5,
    opacity=0.7
).add_to(m)

# Визуализация агроценозов
for index, row in df_crops.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=row['crop_type'],
        icon=folium.Icon(color='green', icon='leaf')
    ).add_to(m)

# Сохранение карты
m.save("192.html")