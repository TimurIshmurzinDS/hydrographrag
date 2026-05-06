import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import folium

# Загрузка исторических данных
data = pd.read_csv('historical_data.csv')

# Предобработка данных
data['temperature'] = data['temperature'].fillna(data['temperature'].mean())
data['precipitation'] = data['precipitation'].fillna(data['precipitation'].mean())

# Разделение данных на обучающую и проверочную выборки
X_train, X_test, y_train, y_test = train_test_split(data.drop('drought_risk', axis=1), data['drought_risk'], test_size=0.2, random_state=42)

# Выбор алгоритма
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Тренировка модели
model.fit(X_train, y_train)

# Оценка точности модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Среднеквадратическая ошибка: {mse}')

# Прогнозирование риска летней засухи
current_data = pd.DataFrame({'temperature': [30], 'precipitation': [20]})
predicted_risk = model.predict(current_data)

# Визуализация результатов на карте
m = folium.Map(location=[45.0, 80.0], zoom_start=6)
folium.Marker([45.0, 80.0], popup=f'Прогнозируемый риск летней засухи: {predicted_risk[0]}%').add_to(m)
m.save('201.html')