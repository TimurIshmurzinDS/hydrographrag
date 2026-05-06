import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import folium

# Загрузить данные о уровне воды и ценах на золото
data = pd.read_csv("bayankol_gold_data.csv")

# Подготовка данных для моделирования
X = data["water_level"].values.reshape(-1, 1)
y = data["gold_price"].values

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X, y)

# Предсказание цен на золото
future_water_levels = pd.DataFrame({"water_level": [10, 15, 20]}) # Примерные будущие уровни воды
predicted_prices = model.predict(future_water_levels)

# Визуализация результатов
m = folium.Map(location=[46.8333, 87.9167], zoom_start=12)
folium.GeoJson("bayankol_river.geojson").add_to(m)

for i in range(len(predicted_prices)):
    folium.Marker(location=[46.8333, 87.9167], popup="Predicted Price: {}".format(predicted_prices[i])).add_to(m)

m.save("223.html")