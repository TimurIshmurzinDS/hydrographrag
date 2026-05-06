import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import folium

# Загрузка исторических данных
data = pd.read_csv('batareyka_river_data.csv', index_col='date', parse_dates=['date'])

# Первичная обработка данных
data['water_level'] = data['water_level'].astype(float)
data = data.dropna()

# Разделение данных на обучающую и тестовую выборки
train_size = int(len(data) * 0.8)
train, test = data[0:train_size], data[train_size:len(data)]

# Создание модели ARIMA
model = ARIMA(train['water_level'], order=(5,1,0))
model_fit = model.fit()

# Предсказание уровня воды на основе исторических трендов
forecast_steps = len(test)
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)

# Оценка точности модели
mse = mean_squared_error(test['water_level'], forecast)
print('Mean Squared Error:', mse)

# Визуализация результатов на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
folium.PolyLine([[data['latitude'].iloc[i], data['longitude'].iloc[i]] for i in range(len(data))], color='blue').add_to(m)
folium.PolyLine([[test['latitude'].iloc[i], test['longitude'].iloc[i]] for i in range(len(test))], color='red').add_to(m)
folium.Marker([data['latitude'].mean(), data['longitude'].mean()], tooltip='Предсказанный уровень воды').add_to(m)

# Сохранение карты
m.save("55.html")