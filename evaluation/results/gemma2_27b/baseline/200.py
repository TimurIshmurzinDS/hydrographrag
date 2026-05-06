import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, FeatureGroup, GeoJson

# 1. Получение данных
data = pd.read_csv("river_data.csv") # Заменить "river_data.csv" на фактическое имя файла

# 2. Подготовка данных
dates = data["date"]
levels = data["level"]

# 3. Расчет статистики
mean_level = levels.mean()
std_level = levels.std()
threshold = mean_level + 2 * std_level

# 4. Определение экстремальных значений
extreme_dates = dates[levels > threshold]

# 5. Визуализация
m = Map(location=[data["latitude"].mean(), data["longitude"].mean()], zoom_start=10)

for date in extreme_dates:
    feature = FeatureGroup()
    feature.add_child(GeoJson(data[data["date"] == date], name="extreme"))
    m.add_child(feature)

# 6. Сохранение карты
m.save("200.html")