import pandas as pd
from folium import Map, Marker, CircleMarker
import numpy as np

# Подготовка данных
data = {
    'river_length': [100],  # Длина реки Уржар в км
    'river_width': [10],   # Ширина реки Уржар в м
    'flow_speed': [2.5],   # Скорость течения воды в реке Уржар в м/с
    'avg_rainfall': [500]  # Средние осадки за год в мм
}

df = pd.DataFrame(data)

# Создание модели наводнений на основе уравнения Сен-Урена
def saint_venant_equation(flow_speed, river_width, rainfall):
    return (flow_speed ** 2) * (river_width ** 3) / (rainfall ** 2)

# Внедрение данных о климатических условиях
df['risk'] = df.apply(lambda row: saint_venant_equation(row['flow_speed'], row['river_width'], row['avg_rainfall']), axis=1)

# Оценка риска наводнений
max_risk = df['risk'].max()
min_risk = df['risk'].min()

print(f'Максимальный риск наводнений: {max_risk}')
print(f'Минимальный риск наводнений: {min_risk}')

# Визуализация результатов на карте
m = Map(location=[50.0, 70.0], zoom_start=8)
marker = Marker(location=[50.0, 70.0], popup='Река Уржар', icon=None).add_to(m)

circle = CircleMarker(location=[50.0, 70.0], radius=max_risk * 10000, color='red').add_to(m)

m.save("209.html")