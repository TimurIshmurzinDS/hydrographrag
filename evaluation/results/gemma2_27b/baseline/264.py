import pandas as pd
from sklearn.model_selection import train_test_split
from prophet import Prophet
import folium

# 1. Загрузка данных
data = pd.read_csv("river_data.csv", index_col="date")

# 2. Обработка данных
data["water_level"] = data["water_level"].fillna(method="ffill")
data["price"] = data["price"].fillna(method="ffill")

# 3. Подготовка данных для Prophet
data = data[["date", "water_level", "price"]]
data = data.rename(columns={"date": "ds", "price": "y"})

# 4. Обучение модели
train, test = train_test_split(data, test_size=0.2)
model = Prophet()
model.fit(train)

# 5. Прогнозирование
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# 6. Визуализация на карте
m = folium.Map(location=[42.87, 79.1], zoom_start=10)

for index, row in forecast.iterrows():
    folium.CircleMarker(
        location=[row["ds"].year, row["y"]], radius=5, color="red"
    ).add_to(m)

# 7. Сохранение карты
m.save("264.html")