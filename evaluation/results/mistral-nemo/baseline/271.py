import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# 1. Подготовьте данные
data = pd.read_csv('bayankol_river_bitcoin_data.csv')
X = data['river_level']
y = data['bitcoin_price']

# 2. Преобразование данных
X_norm = (X - X.min()) / (X.max() - X.min())
y_norm = (y - y.min()) / (y.max() - y.min())

# 3. Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X_norm, y_norm, test_size=0.2, random_state=42)

# 4. Построение модели
model = LinearRegression()

# 5. Обучение модели
model.fit(X_train.reshape(-1, 1), y_train)

# 6. Проверка модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Среднеквадратичная ошибка: {mse}')

# 7. Предсказание курса биткоина
new_river_level = [[10]]  # Пример новых данных о уровне реки Bayankol River
predicted_bitcoin_price = model.predict(new_river_level)
print(f'Предсказанный курс биткоина: {predicted_bitcoin_price[0] * (y.max() - y.min()) + y.min()}')

# Визуализация на карте с использованием folium
m = folium.Map(location=[43.25, 76.9], zoom_start=8)  # Пример местоположения реки Bayankol River

# Добавить точки на карту для исторических данных о уровне реки и курсе биткоина
for i in range(len(data)):
    folium.CircleMarker(location=[43.25, 76.9], radius=5, color='blue').add_to(m)

# Сохранить карту как HTML-файл
m.save("271.html")