import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium
from folium.plugins import HeatMap

# Пример данных (замените на реальные данные)
data = {
    'latitude': [50.1, 50.2, 50.3, 50.4, 50.5],
    'longitude': [30.1, 30.2, 30.3, 30.4, 30.5],
    'pollution_level': [10, 15, 20, 25, 30],  # Уровень загрязнения
    'water_quality': [80, 75, 65, 55, 45]   # Качество воды (например, pH)
}

df = pd.DataFrame(data)

# Разделение данных на признаки и целевую переменную
X = df[['latitude', 'longitude', 'pollution_level']]
y = df['water_quality']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Визуализация результатов на карте
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=10)

# Добавление точек с данными о загрязнении и качестве воды
for idx, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Pollution Level: {row['pollution_level']}, Water Quality: {row['water_quality']}",
        icon=folium.Icon(color='red' if row['water_quality'] < 70 else 'green')
    ).add_to(m)

# Добавление теплового карты
heat_data = [[row['latitude'], row['longitude'], row['pollution_level']] for idx, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

m.save("186.html")