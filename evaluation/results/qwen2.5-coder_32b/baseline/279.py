import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Загрузка данных (предположим, что данные находятся в CSV файле)
data = pd.read_csv('real_estate_data.csv')

# Предварительная обработка данных
# Проверка на пропуски
print(data.isnull().sum())

# Удаление строк с пропусками (или заполнение средними значениями)
data.dropna(inplace=True)

# Выделение признаков и целевой переменной
X = data[['latitude', 'longitude', 'area', 'rooms']]  # Пример признаков
y = data['price']

# Разделение данных на тренировочную и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение моделей
lr_model = LinearRegression()
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

lr_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

# Оценка моделей
y_pred_lr = lr_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)

mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Линейная регрессия: MSE={mse_lr}, R²={r2_lr}")
print(f"Случайный лес: MSE={mse_rf}, R²={r2_rf}")

# Выбор лучшей модели (например, по метрике R²)
if r2_rf > r2_lr:
    best_model = rf_model
else:
    best_model = lr_model

# Предсказание на тестовых данных с использованием лучшей модели
y_pred_best = best_model.predict(X_test)

# Визуализация результатов на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

for i in range(len(X_test)):
    folium.CircleMarker(
        location=(X_test.iloc[i]['latitude'], X_test.iloc[i]['longitude']),
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"Actual: {y_test.iloc[i]}, Predicted: {y_pred_best[i]:.2f}"
    ).add_to(m)

m.save("279.html")