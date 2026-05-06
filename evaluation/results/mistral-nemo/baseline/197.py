import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import folium

# 1. Подготовка данных
data = pd.read_csv('aksu_river_discharge.csv')
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# 2. Анализ данных
# Здесь можно добавить код для анализа данных и выявления закономерностей

# 3. Выбор модели
model = ARIMA(data, order=(5,1,0))

# 4. Обучение модели
model_fit = model.fit(disp=0)

# 5. Прогнозирование
forecast, stderr, conf_int = model_fit.forecast(steps=365)
forecast_df = pd.DataFrame({'Forecast': forecast}, index=pd.date_range(start='2022-01-01', periods=365))

# 6. Визуализация
m = folium.Map(location=[43.25, 76.9], zoom_start=8) # Координаты и масштаб карты реки Aksu River

for index, row in forecast_df.iterrows():
    folium.CircleMarker(location=[43.25, 76.9], radius=row['Forecast']/1000, fill=True).add_to(m)

m.save("197.html")