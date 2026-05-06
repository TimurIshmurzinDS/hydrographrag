import pandas as pd
from folium import Map, Marker
import numpy as np

# Сбор данных о водном режиме реки Или (предположим, что данные хранятся в DataFrame)
data = {
    'location': ['Или-1', 'Или-2', 'Или-3'],
    'water_level': [10.5, 12.8, 9.2],
    'consumption': [5000, 6000, 7000]
}
df = pd.DataFrame(data)

# Анализ данных для определения закономерностей и тенденций в изменении уровня потребления воды
mean_consumption = df['consumption'].mean()
print(f"Средний уровень потребления воды: {mean_consumption}")

# Создание гео-модели (предположим, что модель представляет собой простую линейную регрессию)
X = np.array(df[['water_level']]).T
y = np.array(df['consumption'])
coefficients = np.polyfit(X, y, 1)

# Использование модели для прогнозирования текущего уровня потребления воды в реке Или
current_water_level = 11.5
predicted_consumption = coefficients[0] * current_water_level + coefficients[1]
print(f"Прогнозируемый уровень потребления воды: {predicted_consumption}")

# Визуализация результатов на карте с помощью библиотеки Folium
m = Map(location=[50.0, 70.0], zoom_start=6)
Marker(location=[50.0, 70.0], popup=f"Прогнозируемый уровень потребления воды: {predicted_consumption}").add_to(m)
m.save("31.html")