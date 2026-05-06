import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Пример данных (замените на реальные данные)
data = {
    'year': [2015, 2016, 2017, 2018, 2019, 2020],
    'population_origin_country': [1000, 1200, 1300, 1400, 1500, 1600],
    'population_destination_country': [500, 600, 700, 800, 900, 1000],
    'economic_factors': [2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
}

df = pd.DataFrame(data)

# Подготовка данных
X = df[['population_origin_country', 'population_destination_country', 'economic_factors']]
y = df['year']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Прогнозирование следующей волны миграции
next_year_prediction = model.predict([[1700, 800, 5.5]])
print(f"Predicted next year of migration: {int(next_year_prediction[0])}")

# Визуализация на карте (пример)
m = folium.Map(location=[39.9042, 116.4074], zoom_start=5)

folium.Marker([39.9042, 116.4074], popup='Beijing').add_to(m)

# Сохранение карты
m.save("278.html")