import pandas as pd
from sklearn.linear_model import LinearRegression
from folium import Map

# 1. Загрузка данных
data = pd.read_csv("bayankol_water_level.csv", index_col="date")

# 2. Обработка данных (упрощенная версия)
data["water_level_change"] = data["water_level"].diff()

# 3. Поиск паттернов (линейная регрессия для примера)
X = data.index.values.reshape(-1, 1)
y = data["water_level_change"].values
model = LinearRegression().fit(X, y)

# 4. Создание индикатора (простой пример)
def mining_indicator(data):
    return model.predict(data.index.values.reshape(-1, 1)) > 0

# 5. Майнинг (условный пример)
if mining_indicator(data):
    print("Start mining!")

# Визуализация данных на карте (необязательно)
m = Map(location=[46.7833, 82.1667], zoom_start=10)
m.save("215.html")