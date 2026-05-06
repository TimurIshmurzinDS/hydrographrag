import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с данными о водном уровне реки Аягоз.
# Файл содержит столбцы 'date' и 'water_level'.
data = pd.read_csv('ayagoz_water_level.csv', parse_dates=['date'], index_col='date')

# Шаг 2: Обработка данных
# Проверка пропущенных значений и заполнение их средними значениями.
data['water_level'].fillna(data['water_level'].mean(), inplace=True)

# Шаг 3: Анализ временных рядов
# Декомпозиция временного ряда на тренд, сезонность и остатки.
decomposition = seasonal_decompose(data['water_level'], model='additive', period=12)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Визуализация результатов декомпозиции
plt.figure(figsize=(14, 7))
plt.subplot(411)
plt.plot(data['water_level'], label='Исходные данные')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Тренд')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Сезонность')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Остатки')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

# Шаг 4: Моделирование
# Простая модель для предсказания водного уровня на основе сезонности.
def predict_water_level(month):
    # Используем среднее значение водного уровня для данного месяца из исторических данных
    return data['water_level'].groupby(data.index.month).mean()[month]

# Пример предсказания водного уровня для января (месяц 1)
predicted_january = predict_water_level(1)

# Шаг 5: Визуализация на карте
# Предположим, что у нас есть координаты реки Аягоз.
ayagoz_coords = [42.874369, 74.590083]  # Примерные координаты

m = folium.Map(location=ayagoz_coords, zoom_start=10)

# Добавление маркера с информацией о предсказанном водном уровне
folium.Marker(
    location=ayagoz_coords,
    popup=f'Предсказанный водный уровень в январе: {predicted_january:.2f} м',
    icon=folium.Icon(color='blue')
).add_to(m)

# Шаг 6: Сохранение карты
m.save("228.html")