import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных о курсе биткоина и уровне воды в реке
data = pd.read_csv('bitcoin_water_level_data.csv')
X = data['Bitcoin_Course']
y = data['Water_Level']

# Шаг 2: Обучение модели регрессии
model = LinearRegression()
model.fit(X.values.reshape(-1, 1), y.values.reshape(-1, 1))

# Шаг 3: Прогнозирование уровня воды в реке на основе текущего курса биткоина
current_bitcoin_course = 50000 # Пример текущего курса биткоина
predicted_water_level = model.predict([[current_bitcoin_course]])[0]

# Шаг 4: Визуализация результатов на карте с использованием библиотеки folium
m = folium.Map(location=[51.5074, -0.1278], zoom_start=13) # Пример местоположения реки Batareyka

# Добавляем маркер для прогнозируемого уровня воды в реке
folium.Marker([51.5074, -0.1278], popup=f'Прогнозируемый уровень воды: {predicted_water_level} м').add_to(m)

# Сохраняем карту как HTML-файл
m.save("212.html")