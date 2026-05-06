import pandas as pd
from folium import Map, CircleMarker
import numpy as np

# Сбор и подготовка данных о уровне воды в реке Или
data = {
    'date': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'level': [10.5, 11.2, 9.8]
}
df = pd.DataFrame(data)

# Подготовка данных для геообработки
df['date'] = pd.to_datetime(df['date'])
df['level'] = df['level'].astype(float)

# Использование модели геообработки (в данном случае простая линейная регрессия)
from sklearn.linear_model import LinearRegression

X = np.array(df['date']).reshape(-1, 1)
y = np.array(df['level'])

model = LinearRegression()
model.fit(X, y)

# Получение прогноза на текущую дату
current_date = pd.to_datetime('2022-01-04')
current_level = model.predict(np.array([[current_date]]))

print(f'Текущий уровень воды в реке Или: {current_level[0]}')

# Визуализация результатов на карте с помощью библиотеки Folium
m = Map(location=[43.5, 76], zoom_start=10)
marker = CircleMarker(location=[43.5, 76], radius=current_level[0]*100).add_to(m)

m.save("1.html")