import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Получение данных
data = pd.read_csv('bayankol_river_data.csv')

# Шаг 2: Обработка данных
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)
data.resample('M').mean()

# Шаг 3: Анализ данных
X = np.array(range(1, len(data) + 1)).reshape(-1, 1)
y = data['water_level'].values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

# Шаг 4: Моделирование паводков
def predict_flood(water_level):
    return model.predict([[water_level]])[0]

# Шаг 5: Визуализация результатов
m = folium.Map(location=[49.8397, 106.6422], zoom_start=8)

for index, row in data.iterrows():
    if predict_flood(row['water_level']) > 5:
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(m)

m.save("18.html")