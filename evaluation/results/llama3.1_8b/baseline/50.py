import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from folium import Map, Marker

# Загрузка данных
data = pd.read_csv('dos_river_data.csv')

# Подготовка данных
X = data.drop(['level'], axis=1)
y = data['level']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели случайного леса
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка качества обученной модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Среднеквадратическая ошибка: {mse}')

# Прогнозирование уровня воды на основе новых данных
new_data = pd.DataFrame({'date': ['2023-02-20'], 'time': ['12:00'], 'precipitation': [10.5], 'temperature': [15]})
new_level = model.predict(new_data)

# Визуализация результатов на карте
m = Map(location=[40.0, 30.0], zoom_start=6)
Marker(location=[40.0, 30.0], popup=f'Уровень воды: {new_level[0]}').add_to(m)
m.save("50.html")