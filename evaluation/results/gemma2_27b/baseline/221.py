import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import folium

# 1. Загрузка данных (замените на ваш путь к файлу)
data = pd.read_csv("dos_river_water_level.csv", index_col="Date")

# 2. Обработка данных (проверьте на пропущенные значения, очистите от ошибок)
data.dropna(inplace=True)

# 3. Модель ARIMA
model = ARIMA(data["Water Level"], order=(5,1,0)) # Замените порядок модели при необходимости

# 4. Обучение модели
model_fit = model.fit()

# 5. Прогнозирование (замените на желаемый период времени)
predictions = model_fit.predict(start=len(data), end=len(data)+30)

# 6. Визуализация

m = folium.Map(location=[42.98, -95.17], zoom_start=12) # Замените координаты на Dos River
folium.Marker(location=[42.98, -95.17], popup="Predicted Water Level").add_to(m)

# 7. Сохранение карты
m.save("221.html")