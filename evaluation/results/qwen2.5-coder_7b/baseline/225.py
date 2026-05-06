import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Параметры модели
L = 1000  # Длина реки в метрах
dx = 10   # Шаг сетки в метрах
dt = 0.1  # Временной шаг в секундах
T = 3600  # Общее время моделирования в секундах

# Скорость течения реки (в м/с)
velocity = np.ones(L) * 2  # Простой пример: постоянная скорость

# Инициализация уровня воды
water_level = np.zeros(L)

# Уравнение моделирования уровня воды
def water_level_model(water_level, t):
    dwdt = np.gradient(velocity * water_level, dx)
    return dwdt

# Временные точки для моделирования
time_points = np.arange(0, T, dt)

# Решение дифференциального уравнения
solution = odeint(water_level_model, water_level, time_points)

# Визуализация результатов
plt.figure(figsize=(12, 6))
plt.plot(solution[:, 500], label='Уровень воды в центре реки')
plt.xlabel('Время (с)')
plt.ylabel('Уровень воды (м)')
plt.title('Моделирование уровня воды в реке Киси Алматы')
plt.legend()
plt.grid(True)
plt.show()

# Сохранение карты с результатами
import folium

# Создание базовой карты
m = folium.Map(location=[43.2165, 76.9280], zoom_start=13)

# Добавление слоя тепловых точек (пример)
heat_data = [[43.2165 + i * dx / 1000, 76.9280 + j * dx / 1000, solution[-1, i * L // dx + j]] for i in range(L) for j in range(L)]
folium.plugins.HeatMap(heat_data).add_to(m)

# Сохранение карты
m.save("225.html")