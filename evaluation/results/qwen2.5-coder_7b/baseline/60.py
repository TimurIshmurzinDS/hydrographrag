import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
osadki = pd.read_csv('historical_precipitation.csv')
watevel = pd.read_csv('water_level_data.csv')

# Пример структуры данных:
# osadki: ['date', 'precipitation']
# waterevel: ['date', 'water_level']

# Обработка данных
osadki['date'] = pd.to_datetime(osadki['date'])
watevel['date'] = pd.to_datetime(watevel['date'])

# Объединение данных по дате
merged_data = pd.merge(osadki, waterevel, on='date')

# Удаление пропущенных значений
merged_data.dropna(inplace=True)

# Создание модели линейной регрессии
model = LinearRegression()
X = merged_data[['precipitation']]
y = merged_data['water_level']
model.fit(X, y)

# Предсказание уровня воды на основе осадков
predictions = model.predict(X)

# Добавление предсказаний в данные
merged_data['predicted_water_level'] = predictions

# Визуализация данных и предсказаний на карте
m = folium.Map(location=[40.7128, 35.1696], zoom_start=10)

# Создание слоя для точек с реальными данными
real_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in merged_data.iterrows():
    real_data["features"].append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [35.1696, 40.7128]
        },
        "properties": {
            "time": row['date'].isoformat(),
            "real_water_level": row['water_level'],
            "precipitation": row['precipitation']
        }
    })

# Создание слоя для точек с предсказанными данными
predicted_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in merged_data.iterrows():
    predicted_data["features"].append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [35.1696, 40.7128]
        },
        "properties": {
            "time": row['date'].isoformat(),
            "predicted_water_level": row['predicted_water_level'],
            "precipitation": row['precipitation']
        }
    })

# Добавление слоев на карту
TimestampedGeoJson(real_data, period="PT1H", add_last_point=True).add_to(m)
TimestampedGeoJson(predicted_data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("60.html")