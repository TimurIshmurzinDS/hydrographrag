import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import folium

# 1. Загрузка данных
df = pd.read_csv("data.csv") # Заменить "data.csv" на имя файла с данными

# 2. Предобработка (если необходимо)
# ...

# 3. Определение переменных
X = df["river_flow"]  # Стоки реки Осек
y = df["ethereum_price"] # Цена Ethereum

# 4. Модель линейной регрессии
model = LinearRegression()

# 5. Обучение модели
model.fit(X.values.reshape(-1, 1), y)

# 6. Предсказание
predictions = model.predict(X.values.reshape(-1, 1))

# 7. Визуализация (необязательно)
plt.scatter(X, y)
plt.plot(X, predictions, color='red')
plt.xlabel("River Flow")
plt.ylabel("Ethereum Price")
plt.show()

# 8. Карта (необязательно)
m = folium.Map(location=[54.72, 36.29], zoom_start=10) # Координаты реки Осек
folium.Marker([54.72, 36.29], popup="River Osek").add_to(m)

# Сохранение карты
m.save("230.html")