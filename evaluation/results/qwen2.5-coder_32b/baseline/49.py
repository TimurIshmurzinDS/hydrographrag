import pandas as pd
import numpy as np
import folium

# Предположим, что у нас есть данные о уровне воды в формате CSV с колонками: 'date', 'water_level'
# Для примера создадим фейковые данные
data_2015 = pd.DataFrame({
    'date': pd.date_range(start='2015-01-01', end='2015-12-31'),
    'water_level': np.random.uniform(low=100, high=200, size=(365,))
})

data_2023 = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', end='2023-12-31'),
    'water_level': np.random.uniform(low=100, high=200, size=(365,))
})

# Определение пиковых уровней воды
peak_2015 = data_2015['water_level'].max()
peak_2023 = data_2023['water_level'].max()

print(f"Пиковый уровень воды в 2015 году: {peak_2015}")
print(f"Пиковый уровень воды в 2023 году: {peak_2023}")

# Координаты реки Batareyka River (примерные)
lat, lon = 48.7695, 44.7960

# Создание карты
m = folium.Map(location=[lat, lon], zoom_start=12)

# Добавление маркеров с пиковыми уровнями воды
folium.Marker(
    [lat, lon],
    popup=f"Пиковый уровень воды в 2015 году: {peak_2015}",
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    [lat + 0.01, lon],  # небольшое смещение для демонстрации
    popup=f"Пиковый уровень воды в 2023 году: {peak_2023}",
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты
m.save("49.html")