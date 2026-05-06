import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# 1. Загрузка данных
data = pd.read_csv("tokuraun_river_flow.csv", index_col="date")

# 2. Обработка данных (очистка, форматирование)
# ...

# 3. Модель ARIMA
model = ARIMA(data["flow"], order=(5,1,0)) # Пример: порядок модели (p, d, q)

# 4. Обучение модели
model_fit = model.fit()

# 5. Прогнозирование
forecast = model_fit.forecast(steps=365) # Предсказание на год вперед

# Визуализация (необязательно)
plt.plot(data["flow"], label="Historical Data")
plt.plot(forecast, label="Forecast")
plt.legend()
plt.show()

# Карта (необязательно)
m = folium.Map(location=[43.15, 76.2], zoom_start=8) # Пример координат

folium.Marker([43.15, 76.2], popup="Tokuraun River Basin").add_to(m)

m.save("193.html")