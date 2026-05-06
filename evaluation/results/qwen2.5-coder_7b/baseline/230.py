import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Пример данных (замените на реальные данные)
data = {
    'Ethereum_Price': [2000, 2100, 2200, 2300, 2400],
    'Osaka_Stock': [100, 150, 200, 250, 300]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Разделение данных на признаки и целевую переменную
X = df[['Osaka_Stock']]
y = df['Ethereum_Price']

# Создание и обучение модели линейной регрессии
model = LinearRegression()
model.fit(X, y)

# Предсказание курса Ethereum на основе текущего стока реки Осек
current_osaka_stock = 275
predicted_ethereum_price = model.predict([[current_osaka_stock]])

print(f"Предсказанный курс Ethereum: {predicted_ethereum_price[0]:.2f}")

# Визуализация на карте с использованием folium
m = folium.Map(location=[34.6937, 135.1922], zoom_start=10)

folium.Marker(
    [34.6937, 135.1922],
    popup=f"Текущий курс Ethereum: {predicted_ethereum_price[0]:.2f}<br>Сток реки Осек: {current_osaka_stock}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

m.save("230.html")