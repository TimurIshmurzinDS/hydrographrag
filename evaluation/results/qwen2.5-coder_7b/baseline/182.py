import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium
from folium.plugins import HeatMap

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2020', periods=365),
    'water_level': np.random.uniform(10, 20, 365),  # Уровень воды в метрах
    'precipitation': np.random.normal(50, 20, 365),  # Осадки в мм
    'agriculture_water_consumption': np.random.uniform(1000, 2000, 365)  # Потребление воды для сельскохозяйственных нужд в кубометрах
}

df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Создание модели линейной регрессии для предсказания уровня воды
X = df[['precipitation', 'agriculture_water_consumption']]
y = df['water_level']
model = LinearRegression()
model.fit(X, y)

# Прогнозирование уровня воды на основе текущих условий
current_conditions = {
    'precipitation': 50,
    'agriculture_water_consumption': 1500
}
predicted_water_level = model.predict([list(current_conditions.values())])[0]

# Оценка рисков дефицита воды
deficit_risk = (predicted_water_level < 12) * 100  # Если уровень воды ниже 12 метров, риск дефицита составляет 100%

# Визуализация результатов на карте
m = folium.Map(location=[54.3678, 49.1667], zoom_start=10)

# Добавление теплового карты осадков
heat_data = [[row['latitude'], row['longitude'], row['precipitation']] for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

# Добавление маркера текущего уровня воды
folium.Marker(
    location=[54.3678, 49.1667],
    popup=f'Predicted Water Level: {predicted_water_level:.2f} m<br>Deficit Risk: {deficit_risk}%',
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("182.html")