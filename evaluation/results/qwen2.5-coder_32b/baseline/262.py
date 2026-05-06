import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import folium

# Предположим, что у нас есть данные в формате CSV с двумя колонками: 'oil_price' и 'fish_population'
data = pd.read_csv('butak_fish_oil_data.csv')

# Проверка данных
print(data.head())

# Подготовка данных
X = data[['oil_price']]
y = data['fish_population']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Предсказание популяции рыб на тестовой выборке
y_pred = model.predict(X_test)

# Визуализация результатов
plt.scatter(X_test, y_test, color='blue', label='Фактические данные')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Предсказания модели')
plt.xlabel('Цена на нефть')
plt.ylabel('Популяция рыб')
plt.title('Прогноз популяции рыб в реке Бутак на основе цен на нефть')
plt.legend()
plt.show()

# Предположим, что у нас есть координаты реки Бутак
latitude = 56.129047
longitude = 47.383771

# Создание карты с помощью folium
m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Добавление маркера на карте
folium.Marker([latitude, longitude], popup='Река Бутак').add_to(m)

# Сохранение карты в файл
m.save("262.html")

# Вывод коэффициентов модели для анализа
print(f'Коэффициент наклона: {model.coef_[0]}')
print(f'Смещение: {model.intercept_}')