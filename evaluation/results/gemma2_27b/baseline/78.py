import pandas as pd
from scipy.stats import norm
import folium

# Загрузить данные о расходе воды
data = pd.read_csv("temirlik_river_data.csv")

# Определить порог наводнения
flood_threshold = 100 # Заменить на реальное значение

# Вычислить вероятность наводнения для каждого поста
data["flood_probability"] = norm.cdf(flood_threshold, loc=data["mean_flow"], scale=data["std_flow"])

# Создать карту с folium
m = folium.Map(location=[data["latitude"].mean(), data["longitude"].mean()], zoom_start=10)

# Добавить маркеры на карту
for index, row in data.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"Вероятность наводнения: {row['flood_probability']:.2f}").add_to(m)

# Сохранить карту
m.save("78.html")