import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import folium

# 1. Получение данных
kurty = pd.read_csv("kurty_data.csv", index_col="date")
sharyn = pd.read_csv("sharyn_data.csv", index_col="date")

# 2. Предварительная обработка (пропуски и выбросы - в зависимости от данных)

# 3. Расчет тренда
X_kurty = kurty.index.values.reshape(-1, 1)
y_kurty = kurty["flow"].values
model_kurty = LinearRegression()
model_kurty.fit(X_kurty, y_kurty)

X_sharyn = sharyn.index.values.reshape(-1, 1)
y_sharyn = sharyn["flow"].values
model_sharyn = LinearRegression()
model_sharyn.fit(X_sharyn, y_sharyn)

# 4. Визуализация
plt.plot(kurty.index, model_kurty.predict(X_kurty), label="Kurty Trend")
plt.plot(sharyn.index, model_sharyn.predict(X_sharyn), label="Sharyn Trend")
plt.xlabel("Time")
plt.ylabel("Flow")
plt.legend()

# 5. Сравнение (коэффициент корреляции)
correlation = np.corrcoef(model_kurty.predict(X_kurty), model_sharyn.predict(X_sharyn))[0,1]
print(f"Correlation coefficient: {correlation}")

# Карта (необязательно)
m = folium.Map()
folium.Marker([kurty.index[0], kurty["flow"][0]]).add_to(m)
folium.Marker([sharyn.index[0], sharyn["flow"][0]]).add_to(m)

m.save("123.html")