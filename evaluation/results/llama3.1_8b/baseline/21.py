import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from folium import Map, Marker

# Загрузка данных
data = pd.read_csv('water_data.csv')

# Подготовка данных
X = data[['temperature', 'precipitation', 'flow_rate']]
y = data['seasonal_water_usage']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели линейной регрессии
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)

# Создание модели случайного леса
model_rf = RandomForestRegressor(n_estimators=100)
model_rf.fit(X_train, y_train)

# Оценка точности моделей
y_pred_lr = model_lr.predict(X_test)
y_pred_rf = model_rf.predict(X_test)

print('Точность модели линейной регрессии:', model_lr.score(X_test, y_test))
print('Точность модели случайного леса:', model_rf.score(X_test, y_test))

# Визуализация результатов на карте
m = Map(location=[50.0, 30.0], zoom_start=6)
marker = Marker(location=[50.0, 30.0], popup='Река Шижинь')
m.add_child(marker)

# Сохранение карты как HTML-файл
m.save('21.html')