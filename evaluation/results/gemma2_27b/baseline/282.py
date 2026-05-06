import pandas as pd
from sklearn.model_selection import train_test_split
from prophet import Prophet

# 1. Сбор данных
data = pd.read_csv("crypto_prices.csv", index_col="Date")

# 2. Подготовка данных
data["rolling_mean"] = data["Price"].rolling(window=7).mean()
data["volatility"] = data["Price"].pct_change().rolling(window=14).std()

# 3. Выбор модели (Prophet)
model = Prophet()

# 4. Обучение модели
train_data = data[:-30]
test_data = data[-30:]
model.fit(train_data[["Date", "Price"]])

# 5. Прогнозирование
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# 6. Визуализация
fig1 = model.plot(forecast)
plt.show()