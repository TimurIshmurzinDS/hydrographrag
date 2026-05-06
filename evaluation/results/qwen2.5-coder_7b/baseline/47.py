import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Загрузка данных
data = pd.read_csv('shilik_river_data.csv', parse_dates=['date'], index_col='date')

# Проверка первых нескольких строк данных
print(data.head())

# Визуализация временного ряда
plt.figure(figsize=(10, 6))
plt.plot(data['flow'], label='Исторический расход воды')
plt.title('Исторический расход воды в реке Shilik River')
plt.xlabel('Дата')
plt.ylabel('Расход воды (м3/с)')
plt.legend()
plt.show()

# Разделение данных на обучающую и тестовую выборки
train_data = data.iloc[:-30]  # Последние 30 дней для тестирования
test_data = data.iloc[-30:]

# Обучение модели ARIMA
model = ARIMA(train_data['flow'], order=(5,1,0))
model_fit = model.fit()

# Прогнозирование на следующий месяц
forecast_steps = 30
forecast = model_fit.forecast(steps=forecast_steps)

# Визуализация прогнозов
plt.figure(figsize=(10, 6))
plt.plot(train_data['flow'], label='Обученные данные')
plt.plot(test_data['flow'], label='Тестовые данные', color='orange')
plt.plot(forecast.index, forecast, label='Прогнозы', color='red')
plt.title('Прогноз расхода воды в реке Shilik River на следующий месяц')
plt.xlabel('Дата')
plt.ylabel('Расход воды (м3/с)')
plt.legend()
plt.show()

# Визуализация на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Дата: {index.strftime('%Y-%m-%d')}, Расход воды: {row['flow']} м3/с").add_to(m)

# Сохранение карты
m.save("47.html")