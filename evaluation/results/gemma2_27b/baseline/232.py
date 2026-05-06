import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import folium

# Константы
G = 6.67430e-11  # Гравитационная постоянная
M_earth = 5.972e24  # Масса Земли
M_moon = 7.342e22   # Масса Луны
R_earth = 6371e3    # Радиус Земли

# Расчет силы тяжести
def gravity(r):
    return -G * M_earth / np.linalg.norm(r)**3 * r

# Уравнение движения ракеты
def motion(y, t):
    r = y[:3]
    v = y[3:]
    a = gravity(r)
    return np.concatenate((v, a))

# Начальные условия (пример)
y0 = np.array([R_earth, 0, 0, 0, 1e4, 0])  # Положение и скорость

# Решение уравнения движения
t = np.linspace(0, 3600 * 24, 1000)
sol = odeint(motion, y0, t)

# Визуализация на карте (folium)
m = folium.Map(location=[0, 0], zoom_start=2)
folium.PolyLine(list(zip(sol[:, 0], sol[:, 1])), color='red').add_to(m)
m.save("232.html")