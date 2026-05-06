import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Загрузка данных о снеготаянии и уровнях воды в реках Байкал и Лепсы
bayankol_data = pd.read_csv('bayankol_data.csv')
lepsy_data = pd.read_csv('lepsy_data.csv')

# Объединение данных о снеготаянии и уровнях воды в реках Байкал и Лепсы
data = pd.concat([bayankol_data, lepsy_data])

# Очистка данных и преобразование типов данных
data['snow'] = data['snow'].astype(float)
data['water_level'] = data['water_level'].astype(float)

# Создание необходимых переменных
data['date'] = pd.to_datetime(data['date'])
data['month'] = data['date'].dt.month

# Разделение данных на обучающую и тестовую выборки
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Создание линейной регрессии для определения корреляции между снеготаянием и паводками
X_train = train_data[['snow']]
y_train = train_data['water_level']
X_test = test_data[['snow']]
y_test = test_data['water_level']

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Оценка качества модели
mse = mean_squared_error(y_test, y_pred)
print(f'Коэффициент корреляции: {model.coef_[0]}')

# Визуализация результатов на карте с помощью библиотеки Folium
m = folium.Map(location=[55.5, 95], zoom_start=6)

folium.Marker([55.5, 95], popup='Река Байкал').add_to(m)
folium.Marker([54.2, 93], popup='Река Лепсы').add_to(m)

folium.PolyLine([[55.5, 95], [54.2, 93]], color='red', weight=2).add_to(m)

m.save("162.html")