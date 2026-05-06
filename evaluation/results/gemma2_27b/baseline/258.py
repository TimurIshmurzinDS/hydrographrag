import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import folium

# Загрузка данных (заменить на ваши реальные данные)
btc_data = pd.read_csv("btc_price.csv", index_col="Date")
water_level = pd.read_csv("water_level_emel.csv", index_col="Date")

# Объединение данных по дате
df = btc_data.merge(water_level, on="Date")

# Расчет коэффициента корреляции
correlation = df["Price"].corr(df["Water Level"])
print("Correlation coefficient:", correlation)

# Модель линейной регрессии
model = LinearRegression()
X = df[["Water Level"]]
y = df["Price"]
model.fit(X, y)

# Предсказание курса биткоина при уровне воды, соответствующем засухе
drought_level = 10 # Заменить на реальный уровень воды, соответствующий засухе
predicted_price = model.predict([[drought_level]])
print("Predicted Bitcoin price during drought:", predicted_price[0])

# Визуализация (необязательно)
m = folium.Map(location=[54.7263, 19.8186], zoom_start=10) # Координаты реки Эмел

folium.Marker(location=[54.7263, 19.8186], popup="River Emel").add_to(m)
m.save("258.html")