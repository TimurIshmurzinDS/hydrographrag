import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import folium

# Загрузка данных о ценах криптовалют и урожайности
data = pd.read_csv("crypto_prices_yield.csv")

# Определение признаков (features) и целевой переменной (target)
features = ["price", "volatility"]
target = "yield"

# Разделение данных на обучающий и тестовый набор
X_train, X_test, y_train, y_test = train_test_split(data[features], data[target])

# Создание модели линейной регрессии
model = LinearRegression()

# Обучение модели на обучающих данных
model.fit(X_train, y_train)

# Предсказание значений на тестовых данных
predictions = model.predict(X_test)

# Оценка точности модели (например, R-squared)
score = model.score(X_test, y_test)

# Выбор криптовалюты с наилучшим показателем прогнозируемой доходности
best_crypto = data["crypto"][model.predict(data[features]) == max(model.predict(data[features]))]

# Визуализация данных на карте (необязательно)
m = folium.Map()
folium.Marker(location=[48.5, 13], popup="Best Crypto: " + best_crypto).add_to(m)
m.save("268.html")

print("Best Cryptocurrency for Investment in Agriculture:", best_crypto)