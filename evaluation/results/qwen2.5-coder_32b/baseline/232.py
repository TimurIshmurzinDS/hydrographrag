import numpy as np
import folium

# Предположим, что уровень воды в реке Каскелен получен из какого-то источника данных.
# Для примера возьмем случайное значение уровня воды.
water_level_caskelen = np.random.uniform(0.5, 2.5)  # Уровень воды в метрах

# Используем уровень воды для генерации случайного числа
np.random.seed(int(water_level_caskelen * 100))  # Преобразуем уровень воды в целое число для seed

# Определяем параметры полета
initial_velocity = np.random.uniform(1000, 1200)  # Начальная скорость в м/с
launch_angle = np.random.uniform(30, 45)  # Угол запуска в градусах

# Константы
G = 6.67430e-11  # Гравитационная постоянная
M_moon = 7.342e22  # Масса Луны в кг
R_moon = 1737100  # Радиус Луны в метрах

# Переводим угол запуска в радианы
launch_angle_rad = np.radians(launch_angle)

# Функция для расчета траектории полета на Луну
def calculate_trajectory(initial_velocity, launch_angle_rad):
    # Начальные координаты (предположим, что запуск происходит с Земли)
    x0, y0 = 0, 0
    
    # Временные параметры
    t_max = 10000  # Максимальное время полета в секундах
    dt = 1  # Шаг времени в секундах
    
    # Списки для хранения координат траектории
    x_coords, y_coords = [x0], [y0]
    
    # Начальные скорости
    vx = initial_velocity * np.cos(launch_angle_rad)
    vy = initial_velocity * np.sin(launch_angle_rad)
    
    for t in range(1, t_max):
        # Расчет гравитационного ускорения Луны
        r = np.sqrt(x_coords[-1]**2 + y_coords[-1]**2)
        if r > R_moon:
            ax = -G * M_moon / r**3 * x_coords[-1]
            ay = -G * M_moon / r**3 * y_coords[-1]
        else:
            break  # Если мы достигли поверхности Луны, прекращаем расчет
        
        # Обновление скоростей
        vx += ax * dt
        vy += ay * dt
        
        # Обновление координат
        x_new = x_coords[-1] + vx * dt
        y_new = y_coords[-1] + vy * dt
        
        x_coords.append(x_new)
        y_coords.append(y_new)
    
    return x_coords, y_coords

# Расчет траектории полета
x_coords, y_coords = calculate_trajectory(initial_velocity, launch_angle_rad)

# Нормализация координат для визуализации на карте (предположим, что Земля находится в начале координат)
latitudes = [y / 10000 for y in y_coords]  # Преобразуем метры в километры
longitudes = [x / 10000 for x in x_coords]

# Создание карты с помощью folium
m = folium.Map(location=[latitudes[0], longitudes[0]], zoom_start=2)

# Добавление траектории на карту
folium.PolyLine(locations=list(zip(latitudes, longitudes)), color='blue').add_to(m)

# Сохранение карты в файл
m.save("232.html")