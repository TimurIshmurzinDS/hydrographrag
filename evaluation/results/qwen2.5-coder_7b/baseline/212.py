import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Загрузка данных
bitcoin_data = pd.read_csv('bitcoin_price.csv')
water_level_data = pd.read_csv('batareyka_water_levels.csv')

# Предварительная обработка данных
# Пример: удаление пропущенных значений
bitcoin_data.dropna(inplace=True)
water_level_data.dropna(inplace=True)

# Формирование признаков
# Пример: использование курса биткоина как признака
data = pd.merge(bitcoin_data, water_level_data, on='date')

# Разделение данных на обучающую и тестовую выборки
X = data[['price']]
y = data['water_level']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Выбор модели
model = LinearRegression()

# Обучение модели
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f'RMSE: {rmse}')

# Прогнозирование уровня воды на основе текущего курса биткоина
current_bitcoin_price = 50000  # Пример значения
predicted_water_level = model.predict([[current_bitcoin_price]])
print(f'Прогнозируемый уровень воды реки Batareyka: {predicted_water_level[0]}')

# Визуализация результатов на карте
m = folium.Map(location=[56.1347, 84.2976], zoom_start=12)  # Координаты примера

# Добавление точек с реальными данными уровня воды
for index, row in water_level_data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Уровень воды: {row["water_level"]}', icon=folium.Icon(color='blue')).add_to(m)

# Добавление точки с прогнозируемым уровнем воды
folium.Marker([56.1347, 84.2976], popup=f'Прогнозируемый уровень воды: {predicted_water_level[0]}', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("212.html")