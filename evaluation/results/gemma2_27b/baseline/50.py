import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Загрузка данных о уровнях воды и осадках
water_levels = pd.read_csv("water_levels.csv")
rainfall = pd.read_csv("rainfall.csv")

# Объединение данных по дате
data = pd.merge(water_levels, rainfall, on="date")

# Создание модели линейной регрессии
model = LinearRegression()
model.fit(data[["rainfall"]], data["water_level"])

# Прогнозирование уровня воды на основе прогноза осадков
future_rainfall = 100  # Пример прогноза осадков
predicted_water_level = model.predict([[future_rainfall]])

# Создание карты с folium
m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Добавление маркера на местоположение реки Dos River
folium.Marker([latitude, longitude], popup="Прогнозируемый уровень воды: {}".format(predicted_water_level[0])).add_to(m)

# Сохранение карты
m.save("50.html")