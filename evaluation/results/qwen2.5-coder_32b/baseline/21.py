import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import folium
from folium.plugins import HeatMap

# Предположим, что у нас есть данные в CSV формате
# Данные должны содержать столбцы: 'date', 'flow_rate', 'temperature', 'precipitation'
data = pd.read_csv('shyzhyn_river_data.csv', parse_dates=['date'])

# Предварительная обработка данных
data.dropna(inplace=True)
data['month'] = data['date'].dt.month

# Выбор признаков и целевой переменной
features = ['temperature', 'precipitation', 'month']
X = data[features]
y = data['flow_rate']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели случайного леса
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
print(f'Средняя квадратическая ошибка: {mse}')

# Создание новых данных для прогнозирования сезонного расхода воды
forecast_data = pd.DataFrame({
    'temperature': np.random.normal(data['temperature'].mean(), data['temperature'].std(), 12),
    'precipitation': np.random.normal(data['precipitation'].mean(), data['precipitation'].std(), 12),
    'month': range(1, 13)
})

# Прогнозирование сезонного расхода воды
forecasted_flow = model.predict(forecast_data)

# Визуализация результатов на карте с использованием folium
m = folium.Map(location=[49.5880, 76.6413], zoom_start=12)  # Координаты Шыжын

# Предположим, что у нас есть координаты точек измерения на реке
locations = [
    [49.5880, 76.6413],
    [49.5900, 76.6500],
    [49.5750, 76.6300]
]

# Добавление точек измерения на карту
for loc in locations:
    folium.Marker(loc).add_to(m)

# Предположим, что у нас есть данные о фактическом расходе воды для этих точек
actual_flow = [150, 200, 180]  # Примерные значения

# Создание тепловой карты для прогнозируемого и фактического расхода воды
heat_data_actual = [[loc[0], loc[1], flow] for loc, flow in zip(locations, actual_flow)]
heat_data_forecasted = [[loc[0], loc[1], forecast] for loc, forecast in zip(locations, forecasted_flow)]

# Добавление тепловой карты для фактического расхода воды
HeatMap(heat_data_actual, name='Фактический расход').add_to(m)

# Добавление тепловой карты для прогнозируемого расхода воды
HeatMap(heat_data_forecasted, name='Прогнозируемый расход').add_to(m)

folium.LayerControl().add_to(m)
m.save("21.html")