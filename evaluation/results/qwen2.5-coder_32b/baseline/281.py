import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import folium

# Загрузка данных о погоде (примерный формат)
data = pd.read_csv('weather_data.csv', parse_dates=['date'])
data.set_index('date', inplace=True)

# Пример исторического метода: Бюргеровский анализ атмосферных ячеек
def burger_method(data):
    # Простой пример: предсказание температуры на основе средней температуры за последние 3 дня
    data['burger_pred'] = data['temperature'].rolling(window=3).mean()
    return data

# Применение исторического метода
data = burger_method(data)

# Подготовка данных для современного алгоритма
features = ['humidity', 'pressure', 'wind_speed']
X = data[features].shift(1).dropna()
y = data['temperature'].loc[X.index]

# Разделение на обучающую и тестовую выборки
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Обучение современного алгоритма (Random Forest)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогнозирование с использованием современного алгоритма
data['rf_pred'] = np.nan
data.loc[X.index, 'rf_pred'] = model.predict(X)

# Оценка точности моделей
burger_mae = mean_absolute_error(data['temperature'].dropna(), data['burger_pred'].dropna())
burger_r2 = r2_score(data['temperature'].dropna(), data['burger_pred'].dropna())

rf_mae = mean_absolute_error(y_test, data.loc[X_test.index, 'rf_pred'])
rf_r2 = r2_score(y_test, data.loc[X_test.index, 'rf_pred'])

print(f"Исторический метод (Бюргер): MAE={burger_mae}, R²={burger_r2}")
print(f"Современный алгоритм (Random Forest): MAE={rf_mae}, R²={rf_r2}")

# Визуализация на карте
# Предположим, что у нас есть координаты мест измерений погоды
locations = pd.read_csv('weather_locations.csv')  # Примерный формат: 'city', 'latitude', 'longitude'

# Создание карты с использованием folium
m = folium.Map(location=[55.75, 37.62], zoom_start=10)  # Координаты Москвы

for idx, row in locations.iterrows():
    city = row['city']
    lat = row['latitude']
    lon = row['longitude']
    
    # Получение последних значений прогнозов для города
    last_date = data.index[-1]
    burger_temp = data.loc[last_date, 'burger_pred']
    rf_temp = data.loc[last_date, 'rf_pred']
    
    folium.Marker(
        location=[lat, lon],
        popup=f"Город: {city}<br>Бюргер: {burger_temp}°C<br>Random Forest: {rf_temp}°C",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты
m.save("281.html")