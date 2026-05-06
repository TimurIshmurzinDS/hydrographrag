import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium
from folium.plugins import HeatMap

# Пример данных: уровень воды в реке Шарын и состояние экосистемы
data = {
    'water_level': [100, 105, 110, 115, 120, 125, 130, 135, 140, 145],
    'ecosystem_state': [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0, -0.1]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(df[['water_level']], df['ecosystem_state'], test_size=0.2, random_state=42)

# Создание модели линейной регрессии
model = LinearRegression()

# Обучение модели
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Визуализация результатов на карте
m = folium.Map(location=[50.1364, 8.7099], zoom_start=13)  # Пример координат для Шарына

# Добавление точек с уровнями воды и состоянием экосистемы
for index, row in df.iterrows():
    folium.Marker([50.1364 + np.random.uniform(-0.01, 0.01), 8.7099 + np.random.uniform(-0.01, 0.01)],
                  popup=f"Уровень воды: {row['water_level']}, Состояние экосистемы: {row['ecosystem_state']}",
                  icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("181.html")