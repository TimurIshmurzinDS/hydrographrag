import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import folium

# 1. Загрузка данных (замените на ваши файлы)
sharyn_data = pd.read_csv("sharyn_river_data.csv", index_col="Date")
kishi_data = pd.read_csv("kishi_river_data.csv", index_col="Date")

# 2. Предобработка (проверьте данные на пропуски и аномалии)

# 3. Анализ трендов
sharyn_monthly_mean = sharyn_data.groupby(by=[pd.Grouper(freq='M')]).mean()

plt.plot(sharyn_monthly_mean["Flow"])
plt.xlabel("Month")
plt.ylabel("Average Flow (m³/s)")
plt.title("Monthly Average Flow for Sharyn River")
plt.show()

# 4. Корреляция
correlation = sharyn_data["Flow"].corr(kishi_data["Flow"])
print(f"Correlation coefficient: {correlation}")

# 5. Прогнозирование (линейная регрессия)
model = LinearRegression()
X = sharyn_data[["Flow"]]
y = kishi_data[["Flow"]]
model.fit(X, y)

# 6. Прогноз
predicted_flow = model.predict(sharyn_data[["Flow"]])

# 7. Визуализация (folium)
m = folium.Map(location=[42.85, 79.0], zoom_start=10)
folium.Marker(location=[42.85, 79.0], popup="Kishi Almaty River").add_to(m)

# ... (добавьте код для визуализации прогноза на карте)

m.save("131.html")