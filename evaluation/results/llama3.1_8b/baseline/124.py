import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from folium import Map, Marker

# Загрузка исторических данных реки Dos River
data = pd.read_csv('dos_river_data.csv', index_col='date', parse_dates=['date'])

# Преобразование данных в формат для обучения модели ARIMA
data_diff = data.diff().dropna()

# Обучение модели ARIMA и получение прогнозов на 2025 год
model = ARIMA(data_diff, order=(1,1,1))
model_fit = model.fit()
forecast_steps = 365 * 3  # 3 года
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)

# Создание картинки с прогнозами
m = Map(location=[55.0, 60.0], zoom_start=6)
for i in range(forecast_steps):
    x = data.index[-1] + pd.DateOffset(days=i+1)
    y = forecast[i]
    Marker(location=[x.latitude, x.longitude], popup=str(y)).add_to(m)

m.save("124.html")