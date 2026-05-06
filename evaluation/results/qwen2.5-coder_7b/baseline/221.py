import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2020', periods=365),
    'water_level': [100 + 10 * i for i in range(365)]  # Пример данных, увеличивающиеся на 10 ед. в день
}

df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Подготовка данных
X = df.index.values.reshape(-1, 1)  # Даты как признаки
y = df['water_level']

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Прогнозирование на будущее
future_dates = pd.date_range(start='1/1/2023', periods=365)
future_predictions = model.predict(future_dates.values.reshape(-1, 1))

# Визуализация результатов
m = folium.Map(location=[df.index[0].year, df.index[0].month], zoom_start=5)

for date, level in zip(df.index, df['water_level']):
    folium.Marker([date.year, date.month], popup=f"Water Level: {level}").add_to(m)

for date, prediction in zip(future_dates, future_predictions):
    folium.Marker([date.year, date.month], popup=f"Predicted Water Level: {prediction}", color='red').add_to(m)

m.save("221.html")