import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор и подготовка данных
# Предположим, что у нас есть CSV файл с историческими данными о расходе воды реки Шарын
data = pd.read_csv('sharyn_water_flow.csv', parse_dates=['date'], index_col='date')

# Проверяем данные
print(data.head())

# Шаг 2: Анализ временных рядов
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['flow'])
plt.title('Исторический расход воды реки Шарын')
plt.xlabel('Дата')
plt.ylabel('Расход воды (куб. м/с)')
plt.show()

# Шаг 3: Моделирование
model = ARIMA(data['flow'], order=(5,1,0))
model_fit = model.fit()
print(model_fit.summary())

# Прогнозирование на следующие 12 месяцев
forecast = model_fit.forecast(steps=12)
forecast_dates = pd.date_range(start=data.index[-1] + pd.DateOffset(months=1), periods=12, freq='M')

# Шаг 4: Перенос модели
# Предположим, что сезонные тренды для реки Кыши Алматы схожи с рекой Шарын
kishi_forecast = forecast

# Создаем DataFrame для прогноза реки Кыши Алматы
kishi_df = pd.DataFrame({'date': forecast_dates, 'forecast_flow': kishi_forecast})
kishi_df.set_index('date', inplace=True)

# Выводим прогнозируемые значения
print(kishi_df)

# Шаг 5: Визуализация результатов
# Предположим, что у нас есть координаты реки Кыши Алматы
lat = 42.874369
lon = 76.910541

m = folium.Map(location=[lat, lon], zoom_start=12)

# Добавляем маркер с информацией о прогнозе
folium.Marker(
    [lat, lon],
    popup=f"Прогнозируемый среднемесячный расход воды: {kishi_forecast.mean():.2f} куб. м/с"
).add_to(m)

# Сохраняем карту в HTML файл
m.save("131.html")