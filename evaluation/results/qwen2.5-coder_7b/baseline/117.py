import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2020', periods=365, freq='D'),
    'urzhar_flow': np.random.randint(100, 500, size=365),
    'aksu_flow': np.random.randint(100, 500, size=365),
    'pollution_level': np.random.rand(365)
}

df = pd.DataFrame(data)

# Предварительный анализ данных
print(df.describe())

# Анализ временных рядов
plt.figure(figsize=(12, 4))
plt.plot(df['date'], df['urzhar_flow'], label='Urzhar River Flow')
plt.plot(df['date'], df['aksu_flow'], label='Aksu River Flow')
plt.xlabel('Date')
plt.ylabel('Flow (m³/s)')
plt.title('River Flows Over Time')
plt.legend()
plt.show()

# Сравнение с экологическими показателями
plt.figure(figsize=(12, 4))
plt.plot(df['date'], df['pollution_level'], label='Pollution Level', color='orange')
plt.xlabel('Date')
plt.ylabel('Pollution Level')
plt.title('Pollution Level Over Time')
plt.legend()
plt.show()

# Моделирование влияния
from sklearn.linear_model import LinearRegression

X = df[['urzhar_flow', 'aksu_flow']]
y = df['pollution_level']

model = LinearRegression()
model.fit(X, y)

print(f'Coefficients: {model.coef_}')
print(f'Intercept: {model.intercept_}')

# Визуализация результатов
m = folium.Map(location=[42.05, 73.98], zoom_start=6)

# Добавление данных о стоках рек и загрязнении на карту
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [73.98, 42.05]
            },
            "properties": {
                "date": df['date'].iloc[0].strftime('%Y-%m-%d'),
                "urzhar_flow": df['urzhar_flow'].iloc[0],
                "aksu_flow": df['aksu_flow'].iloc[0],
                "pollution_level": df['pollution_level'].iloc[0]
            }
        }
    ]
}

TimestampedGeoJson(geojson_data, period="PT1D", add_last_point=True).add_to(m)

m.save("117.html")