import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# 1. Сбор данных (замените на ваши данные)
data = pd.read_csv("aksu_river_flow.csv", index_col="date")

# 2. Предобработка данных (проверьте и заполните пропуски, если есть)
data.fillna(method="ffill", inplace=True)

# 3. Выбор модели (ARIMA в этом примере)
model = ARIMA(data["flow"], order=(5,1,0)) # Подберите порядок модели (p,d,q) на основе анализа данных

# 4. Обучение модели
model_fit = model.fit()

# 5. Прогнозирование
forecast = model_fit.forecast(steps=365)  # Предположим, что следующий сезон - 365 дней

# Визуализация (необязательно)
plt.plot(data["flow"], label="historical")
plt.plot(forecast, label="prediction")
plt.legend()
plt.show()

# Карта (необязательно, если есть координаты реки)
m = folium.Map(location=[40.5, 72.5], zoom_start=10) # Замените на координаты реки Aksu
folium.Marker([40.5, 72.5]).add_to(m)

# Сохранение карты
m.save("197.html")