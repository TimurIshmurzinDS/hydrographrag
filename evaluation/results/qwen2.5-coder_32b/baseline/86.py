import pandas as pd
import numpy as np
import folium
from scipy.stats import zscore

# Предполагаем, что у нас есть временные ряды уровней воды для каждой из рек в формате CSV.
# Пример данных:
data = {
    'date': pd.date_range(start='2023-01-01', periods=365),
    'Karaoy_River': np.random.normal(loc=1.0, scale=0.1, size=365) + np.linspace(0, 0.5, 365), # Пример данных с трендом
    'Temirlik_River': np.random.normal(loc=1.2, scale=0.1, size=365),
    'Turgen_River': np.random.normal(loc=1.1, scale=0.1, size=365) + np.linspace(0, 0.4, 365), # Пример данных с трендом
}

df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Определение пороговых значений для опасного роста уровня воды (например, среднее значение + 2 стандартных отклонения)
thresholds = df.mean() + 2 * df.std()

# Проверка превышения пороговых значений
dangerous_levels = (df > thresholds).any()

# Координаты рек для визуализации на карте
river_coords = {
    'Karaoy_River': [43.0158, 76.9253],
    'Temirlik_River': [42.8603, 77.1015],
    'Turgen_River': [42.9500, 77.0500]
}

# Создание карты
m = folium.Map(location=[42.9500, 77.0000], zoom_start=10)

for river, coord in river_coords.items():
    if dangerous_levels[river]:
        folium.Marker(
            location=coord,
            popup=f"{river}: Опасный рост уровня воды",
            icon=folium.Icon(color='red')
        ).add_to(m)
    else:
        folium.Marker(
            location=coord,
            popup=f"{river}: Уровень воды в норме",
            icon=folium.Icon(color='green')
        ).add_to(m)

# Сохранение карты
m.save("86.html")