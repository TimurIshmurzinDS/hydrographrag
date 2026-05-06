import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Шаг 1: Сбор данных (пример синтетических данных)
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=365, freq='D')
water_levels = np.sin(np.linspace(0, 10, len(dates))) + np.random.normal(0, 0.1, len(dates))
data = pd.DataFrame({'date': dates, 'water_level': water_levels})
data.set_index('date', inplace=True)

# Шаг 2: Предобработка данных
data.dropna(inplace=True)
data['water_level_diff'] = data['water_level'].diff().fillna(0)

# Шаг 3: Анализ временных рядов (простой пример с использованием линейной регрессии)
X = np.array(data.index.map(lambda x: x.toordinal())).reshape(-1, 1)
y = data['water_level_diff']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Шаг 4: Интеграция с алгоритмом майнинга (простой пример условия для запуска майнинга)
def should_mine(water_level_diff):
    return abs(water_level_diff) > 0.2

mining_dates = data[data['water_level_diff'].apply(should_mine)].index
print(f"Даты, когда следует запустить майнинг: {mining_dates}")

# Шаг 5: Визуализация результатов на карте с использованием folium
m = folium.Map(location=[43.2689, 76.9104], zoom_start=10)  # Координаты Баянкольского озера

# Добавление маркеров для дат майнинга
for date in mining_dates:
    folium.Marker(
        location=[43.2689, 76.9104],  # Координаты Баянкольского озера
        popup=f"Дата: {date.strftime('%Y-%m-%d')}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("215.html")