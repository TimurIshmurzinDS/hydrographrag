import pandas as pd
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import folium

# Загрузка исторических данных о расходе воды в реке Шилик
data = pd.read_csv('water_data.csv')

# Очистка данных от пропусков и аномалий
data.dropna(inplace=True)
data = data[(data['water_usage'] > 0) & (data['water_usage'] < 100)]

# Подготовка данных
data['month'] = pd.to_datetime(data['date']).dt.month
data['year'] = pd.to_datetime(data['date']).dt.year

# Разделение данных на обучающую и тестовую выборки
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Обучение модели ARIMA
model = ARIMA(train_data, order=(5,1,0))
model_fit = model.fit()

# Оценка точности модели на основе данных из тестовой выборки
forecast_steps = len(test_data)
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)

# Прогнозирование расхода воды в реке Шилик на следующий месяц
next_month_forecast = model_fit.forecast(steps=1)[0]

# Визуализация прогнозируемого расхода воды на картине
m = folium.Map(location=[46.5, 76], zoom_start=10)
folium.Marker([46.5, 76], popup='Прогнозированный расход воды в реке Шилик на следующий месяц: ' + str(next_month_forecast)).add_to(m)
m.save("47.html")

# Вывод прогнозируемого расхода воды
print('Прогнозированный расход воды в реке Шилик на следующий месяц:', next_month_forecast)