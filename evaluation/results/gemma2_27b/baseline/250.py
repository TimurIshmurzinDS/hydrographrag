import numpy as np
from scipy import integrate
import folium

# Загрузка данных о топографической сети (пример)
topo_data = np.loadtxt("tentek_rivers.txt", delimiter=",")

# Определение начальных условий спутника
r0 = np.array([0, 6371e3, 0])  # Начальное положение (радиальные координаты)
v0 = np.array([0, 0, 7e3])   # Начальная скорость

# Модель орбиты (пример - Keplerian)
def orbit_model(t, r):
    mu = 398600e11  # Гравитационный параметр Земли
    r_norm = np.linalg.norm(r)
    a = -mu / r_norm**2 * r / r_norm
    return v

# Расчет орбиты
t_span = (0, 3600*24)  # Время расчета (1 сутки)
sol = integrate.solve_ivp(orbit_model, t_span, [r0, v0])

# Проверка пересечений с топографической сетью
for i in range(len(sol.t)):
    r = sol.y[:,i]
    if np.any(np.linalg.norm(topo_data - r, axis=1) < 1e3):
        print("Пересечение!")

# Визуализация (folium)
m = folium.Map(location=[40, 75], zoom_start=6)
for i in range(len(sol.t)):
    r = sol.y[:,i]
    folium.CircleMarker(location=[r[1]/1e3, r[2]/1e3], radius=1).add_to(m)

# Сохранение карты
m.save("250.html")