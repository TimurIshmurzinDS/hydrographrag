import numpy as np
from scipy.integrate import odeint
import folium

# Параметры моделирования
r = 0.5  # Коэффициент репродукции
K = 100   # Максимальная вместимость среды обитания
F = np.linspace(0, 1, 100)  # Количество корма (от 0 до 1)

# Функция для решения дифференциального уравнения
def model(N, t, r, K, F):
    dNdt = r * N * (1 - N/K) * F
    return dNdt

# Решение дифференциального уравнения с помощью метода Runge-Kutta
t = np.linspace(0, 10, 100)
N = odeint(model, 10, t, args=(r, K, F))

# Создание карты с использованием библиотеки Folium
m = folium.Map(location=[55.7558, 37.6173], zoom_start=12)

# Добавление данных на карту
for i in range(len(F)):
    folium.Circle([55.7558 + np.random.uniform(-0.01, 0.01), 37.6173 + np.random.uniform(-0.01, 0.01)], radius=N[i] * 10000, color='blue').add_to(m)

# Сохранение карты в файл
m.save("276.html")