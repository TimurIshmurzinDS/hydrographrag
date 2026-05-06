import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import folium

# Предполагаем, что у нас есть временные ряды данных о расходе воды для рек Баскан и Прокходная.
# Для примера создадим синтетические данные.

# Создание синтетических данных
np.random.seed(0)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
baskan_flow = np.sin(np.linspace(0, 10, len(dates))) * 50 + 100
prokhodnaya_flow = np.sin(np.linspace(0, 10, len(dates)) * 1.2) * 40 + 80

# Добавление случайного шума
baskan_flow += np.random.normal(0, 5, size=len(baskan_flow))
prokhodnaya_flow += np.random.normal(0, 5, size=len(prokhodnaya_flow))

# Создание DataFrame
data = pd.DataFrame({
    'date': dates,
    'baskan_flow': baskan_flow,
    'prokhodnaya_flow': prokhodnaya_flow
})

# Определение периода пика половодья (например, июнь-июль)
peak_period_start = '2023-06-01'
peak_period_end = '2023-07-31'

# Фильтрация данных за период пика половодья
peak_data = data[(data['date'] >= peak_period_start) & (data['date'] <= peak_period_end)]

# Сравнение средних значений расхода воды в период пика половодья
mean_baskan_peak = peak_data['baskan_flow'].mean()
mean_prokhodnaya_peak = peak_data['prokhodnaya_flow'].mean()

print(f"Средний расход на реке Баскан в период пика: {mean_baskan_peak:.2f} м³/с")
print(f"Средний расход на реке Прокходная в период пика: {mean_prokhodnaya_peak:.2f} м³/с")

# Статистический тест для сравнения средних значений
t_stat, p_value = ttest_ind(peak_data['baskan_flow'], peak_data['prokhodnaya_flow'])
print(f"t-статистика: {t_stat}, p-value: {p_value}")

# Визуализация данных на карте с помощью folium
m = folium.Map(location=[56.0, 103.0], zoom_start=4)

# Координаты рек (примерные)
baskan_coords = [57.2892, 94.6361]  # примерные координаты Баскан
prokhodnaya_coords = [56.8500, 103.2000]  # примерные координаты Прокходная

# Добавление маркеров на карту
folium.Marker(
    location=baskan_coords,
    popup=f"Баскан: {mean_baskan_peak:.2f} м³/с",
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=prokhodnaya_coords,
    popup=f"Прокходная: {mean_prokhodnaya_peak:.2f} м³/с",
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты
m.save("89.html")

# Построение графика временных рядов для визуального анализа
plt.figure(figsize=(14, 7))
plt.plot(data['date'], data['baskan_flow'], label='Река Баскан', color='blue')
plt.plot(data['date'], data['prokhodnaya_flow'], label='Река Прокходная', color='red')
plt.axvspan(pd.Timestamp(peak_period_start), pd.Timestamp(peak_period_end), color='gray', alpha=0.2, label='Период пика половодья')
plt.xlabel('Дата')
plt.ylabel('Расход воды (м³/с)')
plt.title('Расход воды на реках Баскан и Прокходная')
plt.legend()
plt.grid(True)
plt.show()