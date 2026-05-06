import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import folium

# Шаг 1: Сбор данных о расходе воды реки Или
# Предположим, что у нас есть CSV файл с историческими данными о расходе воды
data = pd.read_csv('ili_river_discharge.csv', parse_dates=['date'], index_col='date')

# Шаг 2: Анализ временных рядов
# Декомпозиция временного ряда на тренд, сезонность и остаток
decomposition = seasonal_decompose(data['discharge'], model='additive')
fig = decomposition.plot()
plt.show()

# Прогнозирование будущих значений (простой пример с использованием последних данных)
future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=30, freq='D')
forecast_values = [data['discharge'].iloc[-1]] * 30  # Простая модель: предполагаем постоянный расход
forecast_df = pd.DataFrame(forecast_values, index=future_dates, columns=['discharge'])

# Шаг 3: Визуализация на карте
# Координаты реки Или (примерные)
ili_river_coords = [46.0519, 20.7820]

m = folium.Map(location=ili_river_coords, zoom_start=10)

# Добавление маркера для реки Или
folium.Marker(
    location=ili_river_coords,
    popup='Река Или',
    icon=folium.Icon(icon="info-sign")
).add_to(m)

# Сохранение карты в HTML файл
m.save("235.html")

print("Карта сохранена как 235.html")