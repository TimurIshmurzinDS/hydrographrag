import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import folium

# Предположим, что у нас есть данные о уровне воды в реке Баскан за несколько лет.
# Для примера создадим синтетические данные.

# Создание синтетических данных
np.random.seed(0)
dates = pd.date_range(start='2010-01-01', end='2023-12-31')
water_levels = 5 + np.sin(np.linspace(0, 10 * np.pi, len(dates))) + np.random.normal(0, 0.5, len(dates))
data = pd.DataFrame({'date': dates, 'water_level': water_levels})
data.set_index('date', inplace=True)

# Анализ сезонности
peaks, _ = find_peaks(data['water_level'], height=0)
peak_dates = data.index[peaks]

# Создание модели временных рядов (упрощенная модель)
model_data = data.copy()
model_data['predicted_water_level'] = model_data['water_level'].rolling(window=365, center=True).mean()

# Визуализация на карте
m = folium.Map(location=[42.8740, 79.1775], zoom_start=10)  # Координаты Башкортостана

# Добавление маркеров для дат пиков уровня воды
for date in peak_dates:
    folium.Marker(
        location=[42.8740, 79.1775],
        popup=f"Пик уровня воды: {date.strftime('%Y-%m-%d')}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты
m.save("218.html")

# Вывод данных для проверки
print(data.head())
print(model_data.head())