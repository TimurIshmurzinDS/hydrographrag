import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import folium

# Подготовка данных
data = pd.read_csv('dos_river_data.csv')
X = data.drop(['level'], axis=1)
y = data['level']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Проверка модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'MSE: {mse}')

# Прогнозирование
current_data = pd.DataFrame({'temperature': [25], 'precipitation': [10]})
future_level = model.predict(current_data)

# Визуализация на карте
m = folium.Map(location=[55.7558, 37.6173], zoom_start=12)
folium.Marker([55.7558, 37.6173], popup=f'Уровень воды: {future_level[0]}').add_to(m)
m.save("221.html")