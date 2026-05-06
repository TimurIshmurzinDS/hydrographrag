import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from folium import Map, Marker

# Загрузка данных о расходе воды для реки Sharyn River
data = pd.read_csv('sharyn_river_data.csv', index_col='date', parse_dates=['date'])

# Обработка данных: преобразование в месяц и среднее значение за каждый месяц
data_monthly = data.resample('ME').mean()

# Разделение данных на обучающую и тестовую выборки (80% для обучения, 20% для проверки)
train_size = int(len(data_monthly) * 0.8)
train, test = data_monthly[0:train_size], data_monthly[train_size:len(data_monthly)]

# Обучение модели ARIMA
model = ARIMA(train, order=(5,1,0))
model_fit = model.fit()

# Прогноз среднемесячного расхода воды для реки Kishi Almaty River
forecast_steps = len(test)
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)

# Визуализация прогнозируемого расхода воды на карте с помощью библиотеки folium
m = Map(location=[43.25, 76.95], zoom_start=10)
Marker(location=[43.25, 76.95], popup='Прогноз среднемесячного расхода воды').add_to(m)

# Добавление прогнозируемого расхода воды на карту
for i in range(forecast_steps):
    marker = Marker(location=[43.25, 76.95], popup=f'Месяц: {i+1}, Прогноз: {forecast[i]:.2f}').add_to(m)

# Сохранение карты в файл
m.save("131.html")