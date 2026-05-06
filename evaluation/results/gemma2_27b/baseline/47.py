import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import folium

# 1. Сбор данных
data = pd.read_csv("shilik_river_flow.csv", index_col="Date", parse_dates=True)

# 2. Предобработка данных
data.fillna(method="ffill", inplace=True)  # Заполнение пропусков

# 3. Выбор модели (ARIMA в этом примере)
model = ARIMA(data["Flow"], order=(5,1,0)) # Порядок модели может быть оптимизирован

# 4. Обучение модели
model_fit = model.fit()

# 5. Прогнозирование
forecast = model_fit.predict(start=len(data), end=len(data)+30)  # Прогноз на 30 дней

# 6. Визуализация (необязательно)
m = folium.Map(location=[51.8, 92.7], zoom_start=8) # Координаты реки Shilik

folium.Marker([51.8, 92.7], popup="<b>Прогноз расхода воды</b><br>{}".format(forecast[0])).add_to(m)
m.save("47.html")