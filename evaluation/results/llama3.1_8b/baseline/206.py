import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from folium import Map, Marker

# Загрузка исторических данных
data = pd.read_csv('water_data.csv')

# Предобработка данных
data['date'] = pd.to_datetime(data['date'])
data['month'] = data['date'].dt.month
data['day_of_week'] = data['date'].dt.dayofweek

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(data.drop('water_level', axis=1), data['water_level'], test_size=0.2, random_state=42)

# Выбор модели
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Обучение модели
model.fit(X_train, y_train)

# Предсказание доступности воды на будущую дату
future_date = pd.to_datetime('2023-03-15')
future_data = pd.DataFrame({'month': [future_date.month], 'day_of_week': [future_date.dayofweek]})
future_prediction = model.predict(future_data)

# Визуализация результатов на карте
m = Map(location=[43.5, 77.0], zoom_start=10)
marker = Marker(location=[43.5, 77.0], popup=f'Прогноз доступности воды: {future_prediction[0]}')
m.add_child(marker)
m.save('206.html')