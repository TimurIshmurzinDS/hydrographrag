import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium
from folium.plugins import HeatMap

# Пример данных о расходе воды и урожае
data = {
    'date': ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01'],
    'sarykan_flow': [10, 15, 20, 25, 30],
    'tekeli_flow': [8, 12, 16, 20, 24],
    'crop_yield': [100, 120, 130, 140, 150]
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Пример линейной регрессии для Sarykan River
X_sarykan = df[['sarykan_flow']]
y_sarykan = df['crop_yield']
model_sarykan = LinearRegression()
model_sarykan.fit(X_sarykan, y_sarykan)

# Пример линейной регрессии для Tekeli River
X_tekeli = df[['tekeli_flow']]
y_tekeli = df['crop_yield']
model_tekeli = LinearRegression()
model_tekeli.fit(X_tekeli, y_tekeli)

# Визуализация на карте
m = folium.Map(location=[43.0522, 76.9218], zoom_start=10)  # Координаты примерного центра

# Добавление теплового картографа для Sarykan River
heat_data_sarykan = [[row['latitude'], row['longitude'], row['sarykan_flow']] for index, row in df.iterrows()]
HeatMap(heat_data_sarykan).add_to(m)

# Добавление теплового картографа для Tekeli River
heat_data_tekeli = [[row['latitude'], row['longitude'], row['tekeli_flow']] for index, row in df.iterrows()]
HeatMap(heat_data_tekeli).add_to(m)

m.save("110.html")