import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных: временные ряды стока рек
kurty_data = {
    'date': pd.date_range(start='1/1/2020', periods=365, freq='D'),
    'flow': np.random.randint(100, 500, size=365)
}

sharyn_data = {
    'date': pd.date_range(start='1/1/2020', periods=365, freq='D'),
    'flow': np.random.randint(100, 500, size=365)
}

kurty_df = pd.DataFrame(kurty_data)
sharyn_df = pd.DataFrame(sharyn_data)

# Предварительный анализ данных
print("Пример данных для Kurty River:")
print(kurty_df.head())
print("\nПример данных для Sharyn River:")
print(sharyn_df.head())

# Анализ тренда с использованием линейной регрессии
kurty_model = LinearRegression()
kurty_model.fit(kurty_df['date'].values.reshape(-1, 1), kurty_df['flow'])
kurty_slope = kurty_model.coef_[0]
kurty_intercept = kurty_model.intercept_

sharyn_model = LinearRegression()
sharyn_model.fit(sharyn_df['date'].values.reshape(-1, 1), sharyn_df['flow'])
sharyn_slope = sharyn_model.coef_[0]
sharyn_intercept = sharyn_model.intercept_

print(f"\nКоэффициенты тренда для Kurty River: Slope = {kurty_slope}, Intercept = {kurty_intercept}")
print(f"Коэффициенты тренда для Sharyn River: Slope = {sharyn_slope}, Intercept = {sharyn_intercept}")

# Визуализация данных на карте
m = folium.Map(location=[50, 30], zoom_start=6)

kurty_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [50 + i * 0.1, 30 + i * 0.1]
            },
            "properties": {
                "time": kurty_df['date'][i].isoformat(),
                "value": kurty_df['flow'][i],
                "label": f"Kurty River: {kurty_df['flow'][i]}"
            }
        } for i in range(len(kurty_df))
    ]
}

sharyn_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [50 + i * 0.1, 30 + i * 0.1]
            },
            "properties": {
                "time": sharyn_df['date'][i].isoformat(),
                "value": sharyn_df['flow'][i],
                "label": f"Sharyn River: {sharyn_df['flow'][i]}"
            }
        } for i in range(len(sharyn_df))
    ]
}

TimestampedGeoJson(kurty_geojson, period="PT1D", add_last_point=True).add_to(m)
TimestampedGeoJson(sharyn_geojson, period="PT1D", add_last_point=True).add_to(m)

m.save("123.html")