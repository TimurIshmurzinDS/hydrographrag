import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import folium

# 1. Генерация синтетических исторических данных (имитация данных бассейна р. Токыраун)
# В реальном сценарии здесь будет загрузка CSV файла: df = pd.read_csv('tokyraun_data.csv')
np.random.seed(42)
dates = pd.date_range(start="2018-01-01", end="2023-12-01", freq='MS')
n_months = len(dates)

# Имитируем сток реки (сезонный характер: пик весной/летом)
discharge = 10 + 15 * np.sin(np.linspace(0, 2 * np.pi * (n_months/12), n_months)) + np.random.normal(0, 2, n_months)
# Имитируем потребность в воде (коррелирует со стоком, но с задержкой и сезонным пиком)
irrigation_demand = 0.6 * discharge + 5 * np.sin(np.linspace(0, 2 * np.pi * (n_months/12), n_months)) + np.random.normal(0, 1, n_months)

df = pd.DataFrame({'date': dates, 'discharge': discharge, 'demand': irrigation_demand})

# 2. Подготовка признаков (Feature Engineering)
df['month'] = df['date'].dt.month
df['discharge_lag1'] = df['discharge'].shift(1)
df['discharge_lag2'] = df['discharge'].shift(2)
df = df.dropna()

# Признаки (X) и целевая переменная (y)
X = df[['discharge', 'month', 'discharge_lag1', 'discharge_lag2']]
y = df['demand']

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 3. Обучение модели
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Проверка точности
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Model Mean Absolute Error: {mae:.2f}")

# 4. Прогноз на следующий год (2024)
future_dates = pd.date_range(start="2024-01-01", end="2024-12-01", freq='MS')
# Предположим, что сток в 2024 будет повторять средний цикл с небольшим отклонением
future_discharge = 10 + 15 * np.sin(np.linspace(0, 2 * np.pi, 12)) + np.random.normal(0, 1, 12)
future_months = future_dates.month
# Упрощенно берем последние лаги из имеющихся данных
last_lag1 = df['discharge'].iloc[-1]
last_lag2 = df['discharge'].iloc[-2]

future_X = pd.DataFrame({
    'discharge': future_discharge,
    'month': future_months,
    'discharge_lag1': [last_lag1] * 12, 
    'discharge_lag2': [last_lag2] * 12
})

future_demand = model.predict(future_X)
avg_future_demand = np.mean(future_demand)
print(f"Predicted average irrigation demand for 2024: {avg_future_demand:.2f} units")

# 5. Геопространственная визуализация
# Координаты бассейна реки Токыраун (примерные координаты региона)
center_lat, center_lon = 43.5, 78.0 

m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles='OpenStreetMap')

# Имитация точек водозабора в бассейне
water_points = [
    {"name": "Водозабор Северный", "coords": [43.7, 78.1], "demand": future_demand[5]}, # Июнь
    {"name": "Водозабор Центральный", "coords": [43.5, 77.8], "demand": future_demand[6]}, # Июль
    {"name": "Водозабор Южный", "coords": [43.2, 77.9], "demand": future_demand[7]}, # Август
]

for point in water_points:
    folium.CircleMarker(
        location=point["coords"],
        radius=10,
        popup=f"{point['name']}: Прогноз потребности {point['demand']:.2f} м³/с",
        color="blue",
        fill=True,
        fill_color="cyan"
    ).add_to(m)

# Добавление полигона, имитирующего бассейн реки
basin_coords = [
    [43.8, 77.7], [43.8, 78.3], [43.1, 78.3], [43.1, 77.7], [43.8, 77.7]
]
folium.Polygon(
    locations=basin_coords,
    color="green",
    weight=2,
    fill=True,
    fill_opacity=0.2,
    popup="Бассейн реки Токыраун"
).add_to(m)

# Сохранение карты
m.save("193.html")
print("Map has been saved as 193.html")