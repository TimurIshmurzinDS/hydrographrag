import pandas as pd
import requests
from shapely.geometry import Point
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть API для получения данных о уровне воды реки Shyzhyn River.
# Для примера используем фиктивные данные.

def get_water_level_data():
    # Функция для получения данных о уровне воды (замените на реальный запрос к API)
    data = {
        'date': ['2023-10-01', '2023-10-02', '2023-10-03'],
        'water_level': [1.5, 2.0, 2.5]  # Уровень воды в метрах
    }
    return pd.DataFrame(data)

# Шаг 2: Обработка данных
df = get_water_level_data()
current_water_level = df['water_level'].iloc[-1]

# Шаг 3: Определение порогов оповещений
critical_water_level = 2.0  # Критический уровень воды в метрах

# Шаг 4: Анализ данных
if current_water_level > critical_water_level:
    alert_message = "Внимание! Уровень воды превысил критическое значение."
else:
    alert_message = "Уровень воды в норме."

# Шаг 5: Визуализация результатов
# Координаты реки Shyzhyn River (примерные)
river_location = Point(49.283, 17.650)

m = folium.Map(location=[river_location.y, river_location.x], zoom_start=10)

folium.Marker(
    location=[river_location.y, river_location.x],
    popup=f"Уровень воды: {current_water_level} м\n{alert_message}",
    icon=folium.Icon(color='red' if current_water_level > critical_water_level else 'green')
).add_to(m)

# Шаг 6: Сохранение результата
m.save("28.html")

print(alert_message)