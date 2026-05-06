import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data = pd.read_csv('dos_river_data.csv', parse_dates=['date'], index_col='date')

# Анализ временного ряда
print(data.info())
print(data.describe())

# Построение графика уровня воды
data['water_level'].plot(figsize=(10, 6))
plt.title('Уровень воды в реке Dos River')
plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.show()

# Разделение данных на обучающую и тестовую выборки
train_data = data[:'2020-12-31']
test_data = data['2021-01-01':]

# Обучение модели SARIMAX
model = SARIMAX(train_data['water_level'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
results = model.fit()

# Прогнозирование на тестовую выборку
forecast = results.get_forecast(steps=len(test_data))
forecast_ci = forecast.conf_int()

# Прогнозирование на весь временной ряд
full_forecast = results.get_forecast(steps=len(data))
full_forecast_ci = full_forecast.conf_int()

# Визуализация результатов
plt.figure(figsize=(10, 6))
plt.plot(train_data['water_level'], label='Обучение')
plt.plot(test_data['water_level'], label='Тест')
plt.plot(full_forecast.predicted_mean, label='Прогноз', color='red')
plt.fill_between(full_forecast_ci.index, full_forecast_ci.iloc[:, 0], full_forecast_ci.iloc[:, 1], color='pink', alpha=0.5)
plt.title('Прогноз уровня воды в реке Dos River на 2025 год')
plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.legend()
plt.show()

# Создание карты с прогнозами
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# Добавление точек с историческими данными
for idx, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Уровень воды: {row['water_level']}", tooltip=row['date']).add_to(m)

# Добавление прогнозов на карту
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for idx, row in full_forecast.predicted_mean.iteritems():
    geojson_data["features"].append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [data.loc[idx]['longitude'], data.loc[idx]['latitude']]
        },
        "properties": {
            "time": idx.strftime('%Y-%m-%d'),
            "water_level": row
        }
    })

TimestampedGeoJson(geojson_data, period='P1D', add_last_point=True).add_to(m)

# Сохранение карты
m.save("124.html")