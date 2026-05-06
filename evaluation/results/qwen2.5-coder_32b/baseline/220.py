import pandas as pd
import numpy as np
import folium
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Предположим, что у нас есть CSV файл с данными датчиков реки Батайка
data = pd.read_csv('batareyka_river_data.csv')

# Просмотр первых строк данных
print(data.head())

# Предварительная обработка данных: удаление пропущенных значений и выбор необходимых столбцов
data.dropna(inplace=True)
features = data[['water_level', 'flow_speed', 'temperature']]
target = data['some_target_variable']  # Замените на реальную целевую переменную

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Создание и обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Средняя квадратическая ошибка модели: {mse}')

# Визуализация данных на карте с помощью folium
# Предположим, что у нас есть координаты датчиков в данных
m = folium.Map(location=[54.8326, 73.1190], zoom_start=10)  # Координаты Батайска

for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Water Level: {row['water_level']}, Flow Speed: {row['flow_speed']}"
    ).add_to(m)

# Сохранение карты в файл
m.save("220.html")