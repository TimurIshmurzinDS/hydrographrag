import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium
from folium.plugins import TimestampedGeoJson

# Сбор данных (пример: загрузка из CSV файла)
data = pd.read_csv('ili_river_data.csv')

# Предполагаем, что данные содержат колонки 'date' и 'flow'
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Анализ данных
print(data.describe())

# Визуализация сезонных паттернов
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(data.index, data['flow'], label='Seasonal Flow')
plt.xlabel('Date')
plt.ylabel('Flow (m³/s)')
plt.title('Seasonal Flow of Ili River')
plt.legend()
plt.show()

# Моделирование
X = data.index.dayofyear.values.reshape(-1, 1)  # Используем день года как признак
y = data['flow'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Визуализация прогнозов на карте
m = folium.Map(location=[43.1675, 76.9083], zoom_start=10)  # Координаты примера (Илибай)

# Создание геоджсон данных для визуализации
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for i, date in enumerate(data.index):
    flow = data.loc[date, 'flow']
    folium.Marker(
        location=[43.1675, 76.9083],  # Координаты примера (Илибай)
        popup=f"Flow on {date.strftime('%Y-%m-%d')}: {flow} m³/s",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("227.html")