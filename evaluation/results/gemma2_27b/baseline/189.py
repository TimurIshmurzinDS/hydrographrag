import pandas as pd
from sklearn.linear_model import LogisticRegression
import folium

# 1. Загрузка данных о климате (пример)
data = pd.read_csv("climate_data_turgen.csv")

# 2. Подготовка данных для моделирования (пример)
features = data[["temperature", "precipitation"]]
target = data["drought"]

# 3. Обучение модели (логистическая регрессия - пример)
model = LogisticRegression()
model.fit(features, target)

# 4. Предсказание вероятности засухи (пример)
new_data = pd.DataFrame({"temperature": [25], "precipitation": [10]})
probability = model.predict_proba(new_data)[0][1]

# 5. Картирование (пример)
m = folium.Map(location=[45, 30], zoom_start=8)
folium.Marker([45, 30], popup="Probability of drought: " + str(probability)).add_to(m)
m.save("189.html")