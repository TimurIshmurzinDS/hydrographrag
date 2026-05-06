import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import folium
from datetime import timedelta

# Шаг 1: Сбор данных (пример синтетических данных)
np.random.seed(42)
dates = pd.date_range(start='2015-01-01', end='2023-12-31')
data = {
    'date': dates,
    'precipitation': np.random.uniform(low=0, high=50, size=len(dates)),
    'temperature': np.random.uniform(low=-10, high=30, size=len(dates)),
    'water_level': np.random.uniform(low=100, high=200, size=len(dates))
}
df = pd.DataFrame(data)
df.set_index('date', inplace=True)

# Шаг 2: Предварительная обработка данных
df['month'] = df.index.month
df['year'] = df.index.year

# Создание признаков для обучения модели
features = ['precipitation', 'temperature', 'month']
X = df[features]
y = df['water_level']

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Шаг 3: Выбор модели (Random Forest)
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Шаг 4: Обучение модели
model.fit(X_train, y_train)

# Оценка качества модели на тестовой выборке
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Среднеквадратическая ошибка модели: {mse}')

# Шаг 5: Прогнозирование уровня воды на следующий сезон (2024 год)
future_dates = pd.date_range(start='2024-01-01', end='2024-12-31')
future_data = {
    'date': future_dates,
    'precipitation': np.random.uniform(low=0, high=50, size=len(future_dates)),
    'temperature': np.random.uniform(low=-10, high=30, size=len(future_dates))
}
future_df = pd.DataFrame(future_data)
future_df.set_index('date', inplace=True)

# Создание признаков для прогнозирования
future_X = future_df[features]
future_y_pred = model.predict(future_X)

# Добавление прогнозных значений в DataFrame
future_df['predicted_water_level'] = future_y_pred

# Шаг 6: Визуализация результатов на карте (пример координат реки Sarykan)
m = folium.Map(location=[42.85, 79.0], zoom_start=10)

# Добавление маркеров с прогнозными значениями уровня воды
for idx, row in future_df.iterrows():
    folium.Marker(
        location=[42.85 + np.random.uniform(-0.1, 0.1), 79.0 + np.random.uniform(-0.1, 0.1)],
        popup=f"Дата: {idx.date()}, Прогнозируемый уровень воды: {row['predicted_water_level']:.2f} м",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("52.html")