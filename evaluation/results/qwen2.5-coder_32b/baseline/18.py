import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import folium
from folium.plugins import HeatMap

# Предположим, что у нас есть данные о реке Bayankol River в CSV файле
# Структура данных: дата, уровень воды (в метрах), признаки паводка (0 - нет, 1 - да)
data = pd.read_csv('bayankol_river_data.csv', parse_dates=['date'])

# Анализ временных рядов для выявления сезонных паттернов
data['month'] = data['date'].dt.month
monthly_avg_water_level = data.groupby('month')['water_level'].mean()

# Формирование признаков и целевой переменной
features = data[['month', 'water_level']]
target = data['flood_warning']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Обучение модели случайного леса для предсказания паводков
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Предположим, что у нас есть географические координаты точек наблюдения реки
coordinates = [
    [45.0321, 86.9756],  # Примерные координаты для иллюстрации
    [45.0421, 86.9856],
    [45.0521, 86.9956]
]

# Предположим, что у нас есть данные о вероятности паводка для каждой точки
flood_probabilities = [
    model.predict_proba([[7, monthly_avg_water_level[7]]])[0][1],  # Примерные значения для иллюстрации
    model.predict_proba([[8, monthly_avg_water_level[8]]])[0][1],
    model.predict_proba([[9, monthly_avg_water_level[9]]])[0][1]
]

# Создание интерактивной карты с тепловым картографированием зон риска паводков
m = folium.Map(location=[45.0421, 86.9856], zoom_start=10)

# Добавление тепловой карты на основе вероятности паводка
heat_data = [[coordinates[i][0], coordinates[i][1], flood_probabilities[i]] for i in range(len(coordinates))]
HeatMap(heat_data).add_to(m)

# Сохранение карты в HTML файл
m.save("18.html")