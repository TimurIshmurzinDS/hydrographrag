import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных о стоке реки Осек и курсе Ethereum за определенный период времени.
data = pd.read_csv('ethereum_osek_data.csv')

# Шаг 2: Обучение модели регрессии на основе данных о стоке реки Осек и курсе Ethereum.
X = data['Osek_level'].values.reshape(-1, 1)
y = data['Ethereum_price'].values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

# Шаг 3: Предсказание будущего курса Ethereum на основе текущих и будущих уровней стока реки Осек.
future_osek_levels = pd.read_csv('future_osek_levels.csv')
predicted_prices = model.predict(future_osek_levels['Osek_level'].values.reshape(-1, 1))

# Шаг 4: Визуализация данных о стоке реки Осек и предсказанном курсе Ethereum на карте.
m = folium.Map(location=[52.7763, 19.4583], zoom_start=10) # Координаты реки Осек

# Добавляем данные о стоке реки Осек на карту
for index, row in data.iterrows():
    folium.CircleMarker(location=[row['Latitude'], row['Longitude']],
                        radius=5,
                        color='blue',
                        fill=True,
                        fill_color='blue').add_to(m)

# Добавляем предсказанный курс Ethereum на карту
for index, price in enumerate(predicted_prices):
    folium.CircleMarker(location=[future_osek_levels.iloc[index]['Latitude'], future_osek_levels.iloc[index]['Longitude']],
                        radius=5,
                        color='green',
                        fill=True,
                        fill_color='green').add_to(m)

# Сохраняем карту в файл
m.save("230.html")