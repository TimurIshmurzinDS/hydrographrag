import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Пример данных: дата, количество осадков (мм), температура (°C)
data = {
    'date': ['2021-03-01', '2021-03-02', '2021-03-03', '2021-03-04', '2021-03-05'],
    'precipitation': [10, 20, 30, 40, 50],
    'temperature': [5, 10, 15, 20, 25]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Прогнозирование количества воды на основе осадков и температуры
X = df[['precipitation', 'temperature']]
y = df['precipitation']

model = LinearRegression()
model.fit(X, y)

# Пример прогнозирования для следующих 5 дней
future_precipitation = [60, 70, 80, 90, 100]
future_temperature = [30, 35, 40, 45, 50]

future_data = pd.DataFrame({'precipitation': future_precipitation, 'temperature': future_temperature})
predicted_water_flow = model.predict(future_data)

# Визуализация результатов на карте
m = folium.Map(location=[42.1697, 73.5087], zoom_start=10)  # Координаты примерного местоположения реки

for i in range(len(predicted_water_flow)):
    folium.Marker(
        location=[42.1697 + np.random.uniform(-0.1, 0.1), 73.5087 + np.random.uniform(-0.1, 0.1)],
        popup=f'Прогнозируемый расход воды: {predicted_water_flow[i]:.2f} м³',
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

m.save("29.html")