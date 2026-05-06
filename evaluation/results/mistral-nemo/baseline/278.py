import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Подготовка данных
data = pd.read_csv('migration_data.csv')  # Замените 'migration_data.csv' на путь к вашим данным о миграции
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Шаг 2: Анализ трендов
decomposition = seasonal_decompose(data['migration'], model='additive')
trend = decomposition.trend

# Шаг 3: Моделирование тренда
X = pd.DataFrame({'t': range(1, len(trend) + 1)})
model = LinearRegression()
model.fit(X, trend)
predicted_trend = model.predict(X)

# Шаг 4: Прогнозирование будущих волн
future_dates = pd.date_range(start=data.index[-1], periods=365*5)  # Предполагается, что мы хотим сделать прогноз на 5 лет вперед
future_X = pd.DataFrame({'t': range(len(data), len(future_dates))})
predicted_future_trend = model.predict(future_X)

# Шаг 5: Визуализация результатов
m = folium.Map(location=[data['lat'].mean(), data['lon'].mean()], zoom_start=2)
folium.Choropleth(
    geo_data='world_countries.json',  # Замените 'world_countries.json' на путь к вашему файлу GeoJSON
    data=data,
    columns=['lat', 'lon'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.8,
    highlight=True
).add_to(m)

folium.LayerControl().add_to(m)
m.save("278.html")