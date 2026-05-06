import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Пример данных: уровень воды и стоимость токенов
data = {
    'water_level': [10, 20, 30, 40, 50],  # Уровень воды в метрах
    'token_price': [100, 150, 200, 250, 300]  # Стоимость токенов
}

# Создание DataFrame
df = pd.DataFrame(data)

# Подготовка данных
X = df[['water_level']]
y = df['token_price']

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X, y)

# Прогнозирование стоимости токенов на основе текущего уровня воды
current_water_level = 35  # Текущий уровень воды в метрах
predicted_token_price = model.predict([[current_water_level]])

print(f"Прогнозируемая стоимость токенов при уровне воды {current_water_level} м: {predicted_token_price[0]:.2f}")

# Визуализация на карте с использованием folium
m = folium.Map(location=[56.1397, 84.1270], zoom_start=12)  # Координаты примера (Салехард)

# Добавление маркера для текущего уровня воды
folium.Marker(
    location=[56.1397, 84.1270],
    popup=f"Текущий уровень воды: {current_water_level} м<br>Прогнозируемая стоимость токенов: {predicted_token_price[0]:.2f}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("264.html")