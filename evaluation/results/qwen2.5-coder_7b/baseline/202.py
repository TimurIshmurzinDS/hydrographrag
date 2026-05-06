import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# Пример данных (замените на реальные данные)
data_emel = {
    'Year': [2018, 2019, 2020, 2021, 2022],
    'Flow': [100, 150, 120, 130, 140]
}

data_turgen = {
    'Year': [2018, 2019, 2020, 2021, 2022],
    'Flow': [200, 250, 220, 230, 240]
}

# Создание DataFrame
df_emel = pd.DataFrame(data_emel)
df_turgen = pd.DataFrame(data_turgen)

# Вычисление стандартного отклонения для каждой реки
std_emel = df_emel['Flow'].std()
std_turgen = df_turgen['Flow'].std()

print(f"Стандартное отклонение стока Emel River: {std_emel}")
print(f"Стандартное отклонение стока Turgen River: {std_turgen}")

# Визуализация данных на карте
m = folium.Map(location=[50, 40], zoom_start=6)

folium.Marker([50, 40], popup='Emel River', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([51, 41], popup='Turgen River', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("202.html")