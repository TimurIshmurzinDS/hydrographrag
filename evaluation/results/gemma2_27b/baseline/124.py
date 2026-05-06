import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# 1. Загрузка данных
data = pd.read_csv("dos_river_data.csv", index_col="date")

# 2. Предобработка (проверка на пропуски, интерполяция)
# ...

# 3. Обучение модели ARIMA
model = ARIMA(data["water_level"], order=(5,1,0)) # Подбор порядка модели (p,d,q) - empiric
model_fit = model.fit()

# 4. Прогнозирование на 2025 год
forecast = model_fit.forecast(steps=365*3) # Предполагаем, что 2025 год - это 365 дней

# 5. Визуализация (необязательно)
plt.plot(data["water_level"], label="Historical Data")
plt.plot(forecast, label="Forecast")
plt.legend()
plt.show()

# 6. Карта (необязательно)
m = folium.Map(location=[54.72, 38.9], zoom_start=10) #Пример координат
folium.Marker([54.72, 38.9], popup="Lepsy River").add_to(m)
m.save("124.html")