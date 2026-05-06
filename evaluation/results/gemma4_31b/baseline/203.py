import numpy as np
import pandas as pd
from scipy import stats
import folium
import matplotlib.pyplot as plt

# 1. Генерация синтетических исторических данных (Annual Maximum Discharge)
# В реальном сценарии здесь будет загрузка CSV файла: df = pd.read_csv('koksu_discharge.csv')
np.random.seed(42)
years = np.arange(1970, 2024)
# Создаем распределение, похожее на гидрологические данные (смещенное вправо)
historical_discharge = np.random.gamma(shape=2.0, scale=150, size=len(years)) + 200 

data = pd.DataFrame({'Year': years, 'Q_max': historical_discharge})

# 2. Моделирование с использованием GEV (Generalized Extreme Value)
# Подгоняем данные к распределению genextreme из scipy
params = stats.genextreme.fit(data['Q_max'])
shape, loc, scale = params

# 3. Расчет порога 50-летнего паводка (Q50)
# Период повторяемости T = 50 лет => Вероятность превышения P = 1/50 = 0.02
# Нас интересует квантиль 0.98 (1 - 0.02)
return_period = 50
probability_exceedance = 1 / return_period
q_50 = stats.genextreme.ppf(1 - probability_exceedance, shape, loc, scale)

print(f"--- Результаты анализа реки Коксу ---")
print(f"Рассчитанный порог 50-летнего паводка (Q50): {q_50:.2f} м3/с")
print(f"Вероятность превышения этого порога в любом году: {probability_exceedance*100:.1f}%")

# 4. Визуализация распределения (для проверки модели)
plt.figure(figsize=(10, 6))
plt.hist(data['Q_max'], bins=15, density=True, alpha=0.6, color='skyblue', label='Исторические данные')
x = np.linspace(min(data['Q_max']), q_50 * 1.2, 100)
plt.plot(x, stats.genextreme.pdf(x, shape, loc, scale), 'r-', lw=2, label='GEV PDF')
plt.axvline(q_50, color='green', linestyle='--', label=f'Q50 Threshold: {q_50:.2f}')
plt.title("Анализ экстремальных расходов воды реки Коксу")
plt.xlabel("Расход воды (м3/с)")
plt.ylabel("Плотность вероятности")
plt.legend()
plt.grid(True)
plt.savefig("flood_analysis.png")
plt.close()

# 5. Геопространственная визуализация (Folium)
# Координаты реки Коксу (примерный центр бассейна в Казахстане/Китае)
koksu_coords = [43.5, 80.5] 

m = folium.Map(location=koksu_coords, zoom_start=7, tiles='OpenStreetMap')

# Добавляем маркер с информацией о расчетах
info_text = (
    f"<b>Река Коксу</b><br>"
    f"Порог 50-летнего паводка: {q_50:.2f} м3/с<br>"
    f"Вероятность превышения: {probability_exceedance*100:.1f}%"
)

folium.Marker(
    location=koksu_coords,
    popup=folium.Popup(info_text, max_width=300),
    tooltip="Результаты моделирования паводка",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавляем круг, имитирующий зону влияния/бассейн
folium.Circle(
    location=koksu_coords,
    radius=50000, 
    color='red',
    fill=True,
    fill_color='red',
    fill_opacity=0.2,
    popup="Зона анализа паводков"
).add_to(m)

# Сохранение карты строго по требованию
m.save("203.html")

print("\nКарта сохранена в файл 203.html")