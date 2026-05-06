import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Пример данных: исторические данные о солнечных вспышках и других признаках
data = {
    'year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019],
    'solar_flare_count': [10, 12, 15, 18, 20, 22, 24, 26, 28, 30],
    'sunspot_number': [50, 55, 60, 65, 70, 75, 80, 85, 90, 95],
    'solar_wind_speed': [400, 420, 440, 460, 480, 500, 520, 540, 560, 580]
}

df = pd.DataFrame(data)

# Разделение данных на признаки и целевую переменную
X = df[['sunspot_number', 'solar_wind_speed']]
y = df['solar_flare_count']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели линейной регрессии
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred_linear = linear_model.predict(X_test)

# Оценка модели линейной регрессии
mse_linear = mean_squared_error(y_test, y_pred_linear)
r2_linear = r2_score(y_test, y_pred_linear)

print(f"Линейная регрессия: MSE={mse_linear}, R^2={r2_linear}")

# Создание модели случайного леса
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred_rf = rf_model.predict(X_test)

# Оценка модели случайного леса
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Случайный лес: MSE={mse_rf}, R^2={r2_rf}")

# Прогнозирование на будущие периоды
future_years = np.array([[100, 600], [105, 620], [110, 640]])
future_predictions_linear = linear_model.predict(future_years)
future_predictions_rf = rf_model.predict(future_years)

print("Прогнозы линейной регрессии на будущие периоды:")
for year, pred in zip(future_years[:, 0], future_predictions_linear):
    print(f"Год {year}: Вероятность солнечных вспышек = {pred:.2f}")

print("Прогнозы случайного леса на будущие периоды:")
for year, pred in zip(future_years[:, 0], future_predictions_rf):
    print(f"Год {year}: Вероятность солнечных вспышек = {pred:.2f}")

# Визуализация результатов
m = folium.Map(location=[50, 10], zoom_start=3)

for year, pred in zip(df['year'], df['solar_flare_count']):
    folium.Marker([50, 10], popup=f"Год {year}: Вероятность солнечных вспышек = {pred:.2f}").add_to(m)

m.save("275.html")