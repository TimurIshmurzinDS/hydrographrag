import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta

# Шаг 1: Сбор данных (используем сгенерированные данные)
np.random.seed(0)
dates = pd.date_range(start='2023-01-01', end=datetime.now(), freq='D')
water_levels = np.random.uniform(low=50, high=200, size=len(dates))

data = pd.DataFrame({
    'date': dates,
    'water_level': water_levels
})

# Шаг 2: Обработка данных (выбираем последнее значение уровня воды)
current_water_level = data['water_level'].iloc[-1]
current_date = data['date'].iloc[-1]

# Шаг 3: Моделирование уровня воды (в данном случае просто используем последнее известное значение)

# Шаг 4: Визуализация результатов
# Координаты реки Или (примерные)
ili_river_coords = [45.2671, 70.8399]

m = folium.Map(location=ili_river_coords, zoom_start=10)

folium.Marker(
    location=ili_river_coords,
    popup=f"Текущий уровень воды: {current_water_level:.2f} м\nДата: {current_date.strftime('%Y-%m-%d')}",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в файл
m.save("1.html")

print(f"Текущий уровень воды в реке Или: {current_water_level:.2f} м на дату {current_date.strftime('%Y-%m-%d')}")