import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import folium

# 1. Сбор и предобработка данных (замените на ваши данные)
data = pd.read_csv("kurty_river_data.csv", index_col="Date", parse_dates=True)

# 2. Выбор модели (ARIMA в этом примере)
model = ARIMA(data["WaterLevel"], order=(5,1,0))  
model_fit = model.fit()

# 3. Прогнозирование
forecast = model_fit.predict(start=len(data), end=len(data)+30) # прогноз на 30 дней

# 4. Визуализация (простой пример, можно улучшить)
m = folium.Map(location=[54.8, 61.2], zoom_start=10)  # координаты реки Kurty River
folium.Marker([54.8, 61.2], popup="Прогноз уровня воды").add_to(m)

m.save("57.html")