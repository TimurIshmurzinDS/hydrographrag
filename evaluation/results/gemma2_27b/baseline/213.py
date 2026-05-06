python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
import folium

# Загрузка данных о показаниях датчика реки Dos River
river_data = pd.read_csv("river_data.csv")

# Загрузка данных о ценах Ethereum
eth_prices = pd.read_csv("eth_prices.csv")

# Объединение данных в один DataFrame
df = pd.merge(river_data, eth_prices, on="date")

# Предобработка данных (удаление пропусков, форматирование)

# Разделение данных на обучающий и тестовый набор
X = df[["river_level", "temperature"]].values
y = df["eth_price"].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Обучение модели MLPRegressor
model = MLPRegressor()
model.fit(X_train, y_train)

# Предсказание на тестовом наборе
y_pred = model.predict(X_test)

# Оценка точности модели
r2 = r2_score(y_test, y_pred)
print("R-squared:", r2)

# Прогноз цены Ethereum на основе новых данных о показаниях датчика
new_data = pd.DataFrame({"river_level": [10], "temperature": [25]})
predicted_price = model.predict(new_data)
print("Predicted price:", predicted_price)

# Визуализация данных на карте (folium)
m = folium.Map()
folium.Marker([df["latitude"].mean(), df["longitude"].mean()], popup="Dos River").add_to(m)
m.save("213.html")