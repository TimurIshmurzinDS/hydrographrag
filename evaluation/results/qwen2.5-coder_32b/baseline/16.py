import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import folium

# Шаг 1: Сбор данных (примерные данные)
data = {
    'date': pd.date_range(start='2023-01-01', periods=365),
    'water_level': np.random.uniform(1.0, 5.0, size=365),  # Уровень воды
    'precipitation': np.random.uniform(0.0, 20.0, size=365),  # Осадки
    'temperature': np.random.uniform(-10.0, 30.0, size=365),  # Температура
    'flood_risk': np.random.choice([0, 1], size=365)  # Признак паводка (0 - нет, 1 - есть)
}

df = pd.DataFrame(data)

# Шаг 2: Обработка данных
df.dropna(inplace=True)

# Шаг 3: Моделирование риска паводка
X = df[['water_level', 'precipitation', 'temperature']]
y = df['flood_risk']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Точность модели: {accuracy:.2f}')

# Предсказание риска паводка на основе текущих данных
current_data = np.array([[3.5, 15.0, 18.0]])  # Примерные текущие данные
current_risk = model.predict(current_data)
print(f'Текущий риск паводка: {"Высок" if current_risk[0] == 1 else "Низк"}')

# Шаг 4: Визуализация результатов
# Предположим, что у нас есть координаты реки Ulken Almaty River
river_coordinates = [42.8746, 75.0938]  # Примерные координаты

m = folium.Map(location=river_coordinates, zoom_start=12)

# Добавление маркера с уровнем риска паводка
folium.Marker(
    location=river_coordinates,
    popup=f'Риск паводка: {"Высок" if current_risk[0] == 1 else "Низк"}',
    icon=folium.Icon(color='red' if current_risk[0] == 1 else 'green')
).add_to(m)

# Сохранение карты
m.save("16.html")