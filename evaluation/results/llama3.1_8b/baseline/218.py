import folium
from folium.plugins import HeatMap
import numpy as np

# Широта и долгота точки на поверхности реки Баскан
lat = 55.1234
lon = 36.5678

# Наклон поверхности (в градусах)
slope = 10

# Гравитационное поле Юпитера (в м/с^2)
jupiter_gravity = 24.79

# Моделирование потока воды
def model_water_flow(lat, lon, slope, jupiter_gravity):
    # Расчет скорости потока воды
    speed = np.sqrt(9.81 * np.sin(np.radians(slope)) + jupiter_gravity)
    
    return speed

# Измерение уровня воды
def measure_water_level(speed):
    # Простая модель: уровень воды пропорционален скорости потока
    water_level = 0.1 * speed
    
    return water_level

# Создание карты с результатами моделирования
m = folium.Map(location=[lat, lon], zoom_start=12)

# Результаты моделирования
speed = model_water_flow(lat, lon, slope, jupiter_gravity)
water_level = measure_water_level(speed)

# Добавление маркера на карте
folium.Marker([lat, lon], popup=f'Уровень воды: {water_level} м').add_to(m)

# Сохранение карты в файл
m.save("218.html")