import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from datetime import datetime

# 1. Симуляция исторических данных стока (так как реальные файлы отсутствуют)
# Создаем временной ряд за 5 лет (60 месяцев)
np.random.seed(42)
dates = pd.date_range(start="2018-01-01", periods=60, freq='M')

def generate_river_flow(base_flow, peak_flow, phase_shift=0):
    """Генерация синтетического стока с учетом сезонности (синусоида + шум)"""
    x = np.linspace(0, 5 * 2 * np.pi, 60)
    # Моделируем весенний пик (синусоида)
    seasonal = (peak_flow - base_flow) * (1 + np.sin(x + phase_shift)) / 2
    noise = np.random.normal(0, base_flow * 0.1, 60)
    return base_flow + seasonal + noise

# Byzhy River: более стабильная, средний сток ниже
byzhy_flow = generate_river_flow(base_flow=2.0, peak_flow=12.0, phase_shift=0)
# Urzhar River: более выраженные паводки, сток выше
urzhar_flow = generate_river_flow(base_flow=1.5, peak_flow=25.0, phase_shift=0.5)

df = pd.DataFrame({
    'Date': dates,
    'Byzhy': byzhy_flow,
    'Urzhar': urzhar_flow
})
df.set_index('Date', inplace=True)

# 2. Статистический анализ
stats = pd.DataFrame({
    'Mean': df.mean(),
    'Max': df.max(),
    'Min': df.min(),
    'Std': df.std(),
    'CV': df.std() / df.mean() # Коэффициент вариации
})

print("--- Сравнительная статистика стока ---")
print(stats)

# 3. Анализ сезонности (Среднемесячный гидрограф)
df['Month'] = df.index.month
monthly_avg = df.groupby('Month')[['Byzhy', 'Urzhar']].mean()

# Визуализация графиков
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(df.index, df['Byzhy'], label='Byzhy River', color='blue')
plt.plot(df.index, df['Urzhar'], label='Urzhar River', color='green')
plt.title('Временные ряды стока (5 лет)')
plt.xlabel('Год')
plt.ylabel('Расход воды (м3/с)')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(monthly_avg.index, monthly_avg['Byzhy'], marker='o', label='Byzhy', color='blue')
plt.plot(monthly_avg.index, monthly_avg['Urzhar'], marker='s', label='Urzhar', color='green')
plt.title('Среднегодовой гидрограф')
plt.xlabel('Месяц')
plt.ylabel('Средний расход (м3/с)')
plt.xticks(range(1, 13))
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# 4. Геопространственная визуализация
# Координаты (примерные для демонстрации расположения в регионе)
locations = {
    "Byzhy River": [45.123, 68.456],
    "Urzhar River": [45.567, 69.123]
}

# Создание карты
m = folium.Map(location=[45.3, 68.8], zoom_start=8, tiles='OpenStreetMap')

for river, coords in locations.items():
    folium.Marker(
        location=coords,
        popup=f"{river}: Ср. сток {stats.loc['Mean', river]:.2f} м3/с",
        icon=folium.Icon(color='blue' if 'Byzhy' in river else 'green', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("204.html")
print("\nКарта сохранена в файл 204.html")