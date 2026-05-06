import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Загрузка данных о расходе реки и типах агроценозов
river_data = pd.read_csv("river_flow_data.csv")
agro_data = pd.read_csv("agro_data.csv")

# Обработка данных: создание признаков (например, сезонность)
river_data["month"] = pd.to_datetime(river_data["date"]).dt.month
river_data["season"] = pd.cut(river_data["month"], bins=[1, 4, 7, 10, 13], labels=["Spring", "Summer", "Autumn", "Winter"])

# Объединение данных о реке и агроценозах
merged_data = pd.merge(river_data, agro_data, on="location")

# Обучение модели: Linear Regression (пример)
model = LinearRegression()
features = ["season", "flow"] # Выбрать соответствующие признаки
target = "stability" # Целевой признак: устойчивость агроценозов

X = pd.get_dummies(merged_data[features], drop_first=True)
y = merged_data[target]

model.fit(X, y)

# Прогнозирование (пример):
new_data = pd.DataFrame({"season": ["Spring"], "flow": [10]}) # Новые данные для прогноза
new_features = pd.get_dummies(new_data[features], drop_first=True)
prediction = model.predict(new_features)

# Визуализация: folium (пример)
m = folium.Map(location=[45, 60], zoom_start=12) # Заменить на координаты района реки Бутак

folium.GeoJson("agro_data.geojson", name="Agroceonozes").add_to(m)

m.save("192.html")