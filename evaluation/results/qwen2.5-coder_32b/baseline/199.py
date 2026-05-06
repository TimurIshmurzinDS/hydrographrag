import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import folium

# Предположим, что у нас есть данные в CSV формате
# Данные должны содержать столбцы: 'Date', 'Precipitation_Urzhar', 'Flow_Urzhar', 'Precipitation_Byzhy', 'Flow_Byzhy'
data = pd.read_csv('hydro_data.csv', parse_dates=['Date'])

# Проверка первых строк данных
print(data.head())

# Предварительная обработка данных: удаление пропусков
data.dropna(inplace=True)

# Визуализация временных рядов
plt.figure(figsize=(14, 7))

plt.subplot(2, 1, 1)
plt.plot(data['Date'], data['Precipitation_Urzhar'], label='Осадки Urzhar River')
plt.plot(data['Date'], data['Flow_Urzhar'], label='Сток Urzhar River', color='orange')
plt.title('Исторические данные Urzhar River')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(data['Date'], data['Precipitation_Byzhy'], label='Осадки Byzhy River', color='green')
plt.plot(data['Date'], data['Flow_Byzhy'], label='Сток Byzhy River', color='red')
plt.title('Исторические данные Byzhy River')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.legend()

plt.tight_layout()
plt.show()

# Вычисление коэффициента корреляции Пирсона
corr_urzhar = pearsonr(data['Precipitation_Urzhar'], data['Flow_Urzhar'])
corr_byzhy = pearsonr(data['Precipitation_Byzhy'], data['Flow_Byzhy'])

print(f"Коэффициент корреляции для Urzhar River: {corr_urzhar[0]}, p-value: {corr_urzhar[1]}")
print(f"Коэффициент корреляции для Byzhy River: {corr_byzhy[0]}, p-value: {corr_byzhy[1]}")

# Создание интерактивной карты с отметками мест измерений данных
m = folium.Map(location=[49.5, 67], zoom_start=8)

# Координаты для Urzhar River и Byzhy River (примерные)
urzhar_coords = [49.3210, 67.3275]
byzhy_coords = [49.4500, 67.5500]

folium.Marker(urzhar_coords, popup='Urzhar River').add_to(m)
folium.Marker(byzhy_coords, popup='Byzhy River').add_to(m)

# Сохранение карты
m.save("199.html")