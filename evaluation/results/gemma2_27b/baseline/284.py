import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Загрузка данных (заменить "data.csv" на актуальный файл)
data = pd.read_csv("data.csv")

# Подготовка данных (очистка, преобразование единиц и т.д.)
# ...

# Выбор модели (в данном случае - линейная регрессия)
model = LinearRegression()

# Обучение модели на исторических данных
X = data["time"]
y = data["temperature"]
model.fit(X.values.reshape(-1, 1), y)

# Прогнозирование (пример)
future_time = pd.DataFrame({"time": [2050]})
predicted_temperature = model.predict(future_time)

# Визуализация на карте
m = folium.Map(location=[-25, 0], zoom_start=3)
folium.Marker([data["latitude"].mean(), data["longitude"].mean()], popup="Predicted Temperature: " + str(predicted_temperature[0])).add_to(m)

# Сохранение карты
m.save("284.html")