import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import folium

# Шаг 1: Сбор данных о курсе биткоина и уровне воды в реке Эмел.
# Предполагается, что у вас есть два CSV-файла с данными о курсе биткоина ('bitcoin.csv') и уровне воды в реке Эмел ('emel_water_level.csv')
bitcoin_data = pd.read_csv('bitcoin.csv', parse_dates=['Date'], index_col='Date')
water_level_data = pd.read_csv('emel_water_level.csv', parse_dates=['Date'], index_col='Date')

# Шаг 2: Анализ данных для выявления корреляции между курсом биткоина и уровнем воды в реке Эмел.
correlation = bitcoin_data['Price'].corr(water_level_data['WaterLevel'])
print(f'Корреляция между курсом биткоина и уровнем воды в реке Эмел: {correlation}')

# Шаг 3: Прогнозирование будущего уровня воды в реке Эмел с использованием метода ARIMA.
model = ARIMA(water_level_data['WaterLevel'], order=(5,1,0))
model_fit = model.fit(disp=0)
forecast = model_fit.forecast(steps=365)  # Прогноз на ближайший год

# Шаг 4: Использование результатов моделирования уровня воды для прогноза изменения курса биткоина.
# Для этого мы можем использовать коэффициент корреляции, найденный в шаге 2.
# Предполагается, что изменение курса биткоина будет пропорционально изменению уровня воды в реке Эмел.
bitcoin_forecast = bitcoin_data['Price'].iloc[-1] * (1 + correlation * (forecast / water_level_data['WaterLevel'].iloc[-1] - 1))

# Шаг 5: Визуализация результатов на карте с использованием библиотеки `folium`.
m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)  # Координаты реки Эмел и начальный масштаб карты

# Добавляем маркеры для прогнозируемых значений уровня воды в реке Эмел.
for idx, level in enumerate(forecast):
    folium.Marker([40.7128, -74.0060], popup=f'Уровень воды: {level:.2f} м\nПрогноз на {idx+1} день').add_to(m)

# Добавляем маркер для текущего курса биткоина.
folium.Marker([40.7128, -74.0060], popup=f'Текущий курс биткоина: ${bitcoin_data["Price"].iloc[-1]:.2f}\nПрогнозируемый курс биткоина: ${bitcoin_forecast:.2f}').add_to(m)

# Сохраняем карту в файл.
m.save("258.html")