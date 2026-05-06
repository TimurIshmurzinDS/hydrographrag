import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import folium

# Шаг 1: Сбор данных (пример загрузки из CSV файла)
data = pd.read_csv('water_data.csv')  # Предположим, что данные находятся в файле water_data.csv

# Шаг 2: Предварительная обработка данных
data.dropna(inplace=True)  # Удаление пропусков
features = data[['precipitation', 'temperature', 'humidity']]  # Пример признаков
target = data['water_flow']  # Целевая переменная - водной поток

# Шаг 3: Выбор модели и разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Шаг 4: Обучение модели
model.fit(X_train, y_train)

# Шаг 5: Оценка модели
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
print(f'RMSE: {rmse}')
print(f'MAE: {mae}')

# Шаг 6: Прогнозирование (пример прогноза на следующий год)
future_data = pd.DataFrame({
    'precipitation': [500, 450, 600],  # Пример значений осадков
    'temperature': [20, 18, 22],       # Пример значений температуры
    'humidity': [70, 65, 80]           # Пример значений влажности
})
future_predictions = model.predict(future_data)
print('Прогнозы водного потока:', future_predictions)

# Шаг 7: Визуализация результатов на карте с использованием folium
# Предположим, что у нас есть координаты бассейна рек Aksu River и Kishi Osek River
m = folium.Map(location=[42.8609, 75.1312], zoom_start=10)  # Координаты примерно по центру региона

# Добавление маркеров для точек измерений (пример)
for _, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Water Flow: {row['water_flow']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Добавление маркеров для прогнозных точек (пример)
for i, pred in enumerate(future_predictions):
    folium.Marker(
        location=[42.8609 + 0.1 * i, 75.1312 + 0.1 * i],  # Пример координат
        popup=f"Predicted Water Flow: {pred}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("206.html")