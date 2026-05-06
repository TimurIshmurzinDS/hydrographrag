import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Загрузка данных
data = pd.read_csv("historical_prices.csv")

# Выбор индикаторов
def calculate_indicators(data):
    data["SMA"] = data["Price"].rolling(window=10).mean()
    data["RSI"] = np.nan # Implement RSI calculation
    data["MACD"] = np.nan # Implement MACD calculation
    return data

# Подготовка данных для моделирования
data = calculate_indicators(data)
features = ["SMA", "RSI", "MACD"]
target = ["Buy/Sell Signal"]

X = data[features]
y = data[target]

# Разделение на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Обучение модели
model = LogisticRegression()
model.fit(X_train, y_train)

# Предсказание на тестовом наборе
y_pred = model.predict(X_test)

# Оценка точности модели
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Визуализация результатов (необходимо установить folium)
import folium

m = folium.Map()
# Implement visualization logic here
m.save("285.html")