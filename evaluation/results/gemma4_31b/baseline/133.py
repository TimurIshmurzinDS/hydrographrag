import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from scipy import stats

# 1. Симуляция данных (так как реальные данные по конкретным рекам требуют API доступа)
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=100, freq='D')

# Данные для Dos River (Недавние)
precip_dos = np.random.gamma(2, 2, 100)  # Осадки
# Сток зависит от осадков с небольшим лагом и шумом
discharge_dos = np.roll(precip_dos * 1.5 + np.random.normal(10, 2, 100), 2) 

# Данные для Kurty River (Исторические)
# Предположим, Kurty River больше, поэтому значения стока выше
discharge_kurty_hist = np.random.normal(50, 15, 100) 

df = pd.DataFrame({
    'Date': dates,
    'Precip_Dos': precip_dos,
    'Discharge_Dos': discharge_dos,
    'Discharge_Kurty_Hist': discharge_kurty_hist
})

# 2. Анализ влияния осадков на Dos River
correlation = stats.pearsonr(df['Precip_Dos'], df['Discharge_Dos'])[0]

# 3. Сравнительный анализ через Z-score
# Считаем, насколько текущий сток Dos отклоняется от своего среднего 
# и сравниваем это с вариативностью Kurty
z_dos = (df['Discharge_Dos'] - df['Discharge_Dos'].mean()) / df['Discharge_Dos'].std()
z_kurty = (df['Discharge_Kurty_Hist'] - df['Discharge_Kurty_Hist'].mean()) / df['Discharge_Kurty_Hist'].std()

avg_deviation_dos = np.abs(z_dos).mean()
avg_deviation_kurty = np.abs(z_kurty).mean()

print(f"Корреляция осадков и стока Dos River: {correlation:.2f}")
print(f"Среднее отклонение Dos River (Z-score): {avg_deviation_dos:.2f}")
print(f"Среднее отклонее Kurty River (Z-score): {avg_deviation_kurty:.2f}")

# 4. Визуализация данных (Графики)
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(df['Date'], df['Precip_Dos'], color='blue', label='Осадки Dos')
plt.ylabel('Осадки (мм)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(df['Date'], df['Discharge_Dos'], color='green', label='Сток Dos (Текущий)')
plt.plot(df['Date'], df['Discharge_Kurty_Hist'], color='gray', alpha=0.5, label='Сток Kurty (Исторический)')
plt.ylabel('Сток (м3/с)')
plt.legend()
plt.tight_layout()
plt.savefig("analysis_plot.png")
plt.close()

# 5. Геопространственная визуализация (Folium)
# Координаты для примера (гипотетические)
coords_dos = [[45.0, 35.0], [45.1, 35.2], [45.2, 35.3]]
coords_kurty = [[46.0, 36.0], [46.1, 36.2], [46.2, 36.3]]

m = folium.Map(location=[45.5, 35.5], zoom_start=7)

# Рисуем реку Dos
folium.PolyLine(coords_dos, color="blue", weight=5, opacity=0.8, 
                tooltip="Dos River (Recent Impact)").add_to(m)

# Рисуем реку Kurty
folium.PolyLine(coords_kurty, color="gray", weight=5, opacity=0.5, 
                tooltip="Kurty River (Historical Baseline)").add_to(m)

# Добавляем маркеры
folium.Marker([45.0, 35.0], popup="Dos River Start").add_to(m)
folium.Marker([46.0, 36.0], popup="Kurty River Start").add_to(m)

# Сохранение карты
m.save("133.html")

print("Моделирование завершено. Карта сохранена в 133.html")