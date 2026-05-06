import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Шаг 1: Подготовка данных
data = pd.read_csv('river_data.csv') # Предполагается, что у вас есть файл с историческими данными о уровне воды и других факторах

# Шаг 2: Преобразование данных
X = data[['rainfall', 'temperature']] # Выберите факторы, которые могут повлиять на уровень воды
y = data['water_level']

# Шаг 3: Обучение модели
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

# Шаг 4: Проверка модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Шаг 5: Предсказание будущего уровня воды
future_data = pd.DataFrame([[10, 25]], columns=['rainfall', 'temperature']) # Пример данных на определенную дату в будущем
predicted_level = model.predict(future_data)
print(f'Predicted water level: {predicted_level[0]}')

# Визуализация на карте (для примера, мы просто отметим местоположение реки Dos River)
m = folium.Map(location=[37.7649, -122.4513], zoom_start=13) # Координаты реки Dos River
folium.Marker([37.7649, -122.4513], popup='Dos River').add_to(m)
m.save("221.html")