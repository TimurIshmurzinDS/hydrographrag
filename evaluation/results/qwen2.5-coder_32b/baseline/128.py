import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# Предположим, что у нас есть два файла с историческими данными: 'lepsy_river_data.csv' и 'dos_river_data.csv'
# Файлы содержат столбцы: 'date', 'water_level'

# Загрузка данных
lepsy_data = pd.read_csv('lepsy_river_data.csv', parse_dates=['date'], index_col='date')
dos_data = pd.read_csv('dos_river_data.csv', parse_dates=['date'], index_col='date')

# Проверка первых строк данных
print(lepsy_data.head())
print(dos_data.head())

# Анализ корреляции между уровнями воды в реках
correlation = lepsy_data['water_level'].corr(dos_data['water_level'])
print(f'Корреляция между уровнями воды: {correlation}')

# Моделирование временных рядов для Lepsy River
lepsy_model = ARIMA(lepsy_data['water_level'], order=(5, 1, 0))
lepsy_results = lepsy_model.fit()

# Прогнозирование уровня воды в реке Lepsy River на следующий сезон (например, 365 дней)
forecast_lepsy = lepsy_results.forecast(steps=365)

# Оценка вероятности паводка в реке Dos River
# Предположим, что уровень воды выше определенного порога считается паводком
threshold_dos = dos_data['water_level'].quantile(0.95)  # Например, 95-й перцентиль

# Прогнозируемый уровень воды в реке Dos River на основе корреляции
forecast_dos = forecast_lepsy * (correlation + 1)

# Оценка вероятности паводка
flood_probability = np.mean(forecast_dos > threshold_dos)
print(f'Вероятность паводка в реке Dos River: {flood_probability:.2%}')

# Визуализация результатов на карте с использованием folium
m = folium.Map(location=[45.0, 37.0], zoom_start=6)  # Координаты примерные

# Добавление маркеров для рек
folium.Marker([45.1, 37.2], popup='Lepsy River').add_to(m)
folium.Marker([45.3, 37.4], popup='Dos River').add_to(m)

# Сохранение карты в файл
m.save("128.html")

# Визуализация временных рядов и прогноза
plt.figure(figsize=(14, 7))
plt.plot(lepsy_data.index, lepsy_data['water_level'], label='Lepsy River')
plt.plot(dos_data.index, dos_data['water_level'], label='Dos River')
plt.plot(pd.date_range(start=lepsy_data.index[-1], periods=365), forecast_lepsy, label='Forecast Lepsy River', linestyle='--')
plt.axhline(y=threshold_dos, color='r', linestyle='-', label=f'Threshold Dos River ({threshold_dos:.2f})')
plt.title('Уровень воды в реках и прогноз для следующего сезона')
plt.xlabel('Дата')
plt.ylabel('Уровень воды')
plt.legend()
plt.show()