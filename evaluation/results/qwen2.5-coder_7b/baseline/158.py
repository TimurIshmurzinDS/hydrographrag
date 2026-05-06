import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2020', periods=365),
    'river': ['Bayankol'] * 180 + ['Sarykan'] * 185,
    'flow_rate': np.random.normal(loc=100, scale=50, size=365),
    'rainfall': np.random.normal(loc=20, scale=10, size=365),
    'flood_event': [np.random.choice([0, 1], p=[0.9, 0.1]) for _ in range(365)]
}

df = pd.DataFrame(data)
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

# Преобразование даты в формат datetime
df['date'] = pd.to_datetime(df['date'])

# Создание признаков
df['month'] = df['date'].dt.month
df['day_of_year'] = df['date'].dt.dayofyear

# Разделение данных на обучающую и тестовую выборки
X = df[['flow_rate', 'rainfall', 'month', 'day_of_year']]
y = df['flood_event']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
print(classification_report(y_test, y_pred))

# Визуализация на карте
m = folium.Map(location=[43.0721, 85.6924], zoom_start=6)

# Создание GeoJSON для визуализации
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in df.iterrows():
    if row['flood_event'] == 1:
        geojson_data["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [85.6924, 43.0721]  # Пример координат
            },
            "properties": {
                "time": row['date'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                "river": row['river'],
                "flow_rate": row['flow_rate'],
                "rainfall": row['rainfall']
            }
        })

# Добавление GeoJSON на карту
TimestampedGeoJson(geojson_data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("158.html")