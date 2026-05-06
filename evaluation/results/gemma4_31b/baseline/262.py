import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# 1. Генерация синтетических данных
# Предположим, данные за 12 лет (2012-2023)
np.random.seed(42)
years = np.arange(2012, 2024)
# Цены на нефть (условно в USD за баррель)
oil_prices = np.array([80, 95, 105, 50, 45, 60, 65, 40, 55, 70, 85, 80])
# Популяция рыб (зависит от цены на нефть с некоторым шумом)
# Формула: Pop = Constant - (Coefficient * OilPrice) + Noise
fish_population = 10000 - (50 * oil_prices) + np.random.normal(0, 500, len(oil_prices))

# Создание DataFrame
df = pd.DataFrame({
    'Year': years,
    'Oil_Price': oil_prices,
    'Fish_Population': fish_population
})

# 2. Построение модели машинного обучения
X = df[['Oil_Price']] # Независимая переменная
y = df['Fish_Population'] # Зависимая переменная

model = LinearRegression()
model.fit(X, y)

# Предсказание для текущей цены (например, 75 USD)
current_oil_price = np.array([[75]])
predicted_pop = model.predict(current_oil_price)[0]

print(f"При цене на нефть {current_oil_price[0][0]} USD, прогнозируемая популяция рыб: {int(predicted_pop)}")

# 3. Геопространственная визуализация
# Координаты реки Бутак (примерные координаты региона)
# Бутак протекает в Казахстане
lat, lon = 46.5, 68.0 

# Создание карты
m = folium.Map(location=[lat, lon], zoom_start=7, tiles='OpenStreetMap')

# Добавление маркера с информацией о прогнозе
info_text = f"Река Бутак<br>Прогноз популяции рыб: {int(predicted_pop)} особей<br>Основано на цене нефти: 75 USD"
folium.Marker(
    location=[lat, lon],
    popup=info_text,
    tooltip="Прогноз экосистемы",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавление линии, имитирующей русло реки (упрощенно)
river_coords = [[46.2, 67.5], [46.5, 68.0], [46.8, 68.5]]
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Русло реки Бутак").add_to(m)

# Сохранение карты
m.save("262.html")

print("Карта успешно сохранена в файл 262.html")