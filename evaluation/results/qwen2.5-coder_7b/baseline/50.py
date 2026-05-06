import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Загрузка данных
data = pd.read_csv('dos_river_data.csv')

# Предположим, что данные имеют следующие столбцы:
# 'date', 'water_level', 'precipitation', 'temperature', 'humidity'

# Преобразование даты в формат datetime
data['date'] = pd.to_datetime(data['date'])

# Установка даты как индекса
data.set_index('date', inplace=True)

# Разделение данных на признаки и целевую переменную
X = data[['precipitation', 'temperature', 'humidity']]
y = data['water_level']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели случайного леса
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Обучение модели
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Визуализация прогноза на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Water Level: {row['water_level']}, Predicted: {y_pred[index]}").add_to(m)

m.save("50.html")