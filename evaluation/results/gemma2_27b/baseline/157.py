import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# 1. Загрузка данных
data = pd.read_csv("river_flow_data.csv", index_col="Date")

# 2. Предобработка (при необходимости)
# ...

# 3. Разделение на обучающий и тестовый набор
train_data = data[:-12]
test_data = data[-12:]

# 4. Обучение модели ARIMA
model = ARIMA(train_data["Flow"], order=(5,1,0))
results = model.fit()

# 5. Прогнозирование
predictions = results.forecast(steps=12)

# 6. Визуализация на карте (при необходимости)
m = folium.Map(location=[43.87, 80.92], zoom_start=8)

folium.Marker(location=[43.87, 80.92], popup="Shilik River").add_to(m)
folium.Marker(location=[43.65, 81.15], popup="Shyzhyn River").add_to(m)

# ... добавить графики прогнозов на карту

m.save("157.html")