import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2020', periods=365, freq='D'),
    'temirlik_flow': np.random.randint(100, 500, size=365),
    'turgen_flow': np.random.randint(100, 500, size=365)
}
df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Анализ сезонных динамик
decomposition_temirlik = seasonal_decompose(df['temirlik_flow'], model='additive')
decomposition_turgen = seasonal_decompose(df['turgen_flow'], model='additive')

# Предсказание уровня воды (пример простой линейной регрессии)
X = df.index.dayofyear.values.reshape(-1, 1)
y_temirlik = df['temirlik_flow']
y_turgen = df['turgen_flow']

model_temirlik = LinearRegression()
model_turgen = LinearRegression()

model_temirlik.fit(X, y_temirlik)
model_turgen.fit(X, y_turgen)

# Оценка угрозы наводнений
threshold_temirlik = 400
threshold_turgen = 400

df['temirlik_risk'] = np.where(df['temirlik_flow'] > threshold_temirlik, 'High', 'Low')
df['turgen_risk'] = np.where(df['turgen_flow'] > threshold_turgen, 'High', 'Low')

# Визуализация результатов
m = folium.Map(location=[40.7128, 30.2576], zoom_start=6)

temirlik_geojson = {
    "type": "FeatureCollection",
    "features": []
}

turgen_geojson = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in df.iterrows():
    folium.Marker(
        location=[40.7128, 30.2576],
        popup=f"Temirlik River: {row['temirlik_flow']} m³/s, Risk: {row['temirlik_risk']}",
        icon=folium.Icon(color='red' if row['temirlik_risk'] == 'High' else 'green')
    ).add_to(m)

    folium.Marker(
        location=[40.7128, 30.2576],
        popup=f"Turgen River: {row['turgen_flow']} m³/s, Risk: {row['turgen_risk']}",
        icon=folium.Icon(color='blue' if row['turgen_risk'] == 'High' else 'green')
    ).add_to(m)

m.save("83.html")