import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# 1. Подготовьте данные
data = pd.read_csv('dos_river_data.csv')
X = data[['precipitation', 'temperature', 'river_level_nearby']]
y = data['water_level']

# 2. Выберите метод моделирования (в данном случае - линейная регрессия)
model = LinearRegression()

# 3. Подготовьте данные для обучения модели
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Обучите модель
model.fit(X_train, y_train)

# 5. Проведите оценку модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# 6. Создайте прогнозы
predictions = model.predict(X)  # Предполагается, что X содержит данные для прогноза

# 7. Визуализируйте результаты с помощью folium
m = folium.Map(location=[38.9072, -77.0369], zoom_start=12)  # Координаты реки Dos River
for i in range(len(data)):
    level = data.iloc[i]['water_level']
    color = 'green' if level < 5 else 'yellow' if level < 10 else 'orange' if level < 15 else 'red'
    folium.CircleMarker(location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']], radius=level/2, fill_color=color).add_to(m)

# Сохраните карту как "50.html"
m.save("50.html")