import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt
import folium

# 1. Подготовка данных
data = pd.read_csv('batareyka_river_water_level.csv')
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# 2. Анализ данных
plt.plot(data['water_level'])
plt.title('Historical Water Level Trends')
plt.xlabel('Date')
plt.ylabel('Water Level (m)')
plt.show()

# 3. Моделирование
model = ARIMA(data['water_level'], order=(5,1,0))
model_fit = model.fit(disp=0)
forecast, se, conf_int = model_fit.forecast(steps=365)

# 4. Валидация
residuals = pd.DataFrame(model_fit.resid)
residuals.plot(kind='kde')
plt.title('Residuals (t-test: %f)' % stats.ttest_1samp(residuals, 0)[1])
plt.show()

# 5. Предсказание
future_dates = pd.date_range(start=data.index[-1], periods=366)
forecast_df = pd.DataFrame({'date': future_dates, 'water_level': forecast})
forecast_df.set_index('date', inplace=True)

# Визуализация на карте с использованием folium
m = folium.Map(location=[55.7821, 37.6219], zoom_start=12)
folium.Choropleth(geo_data='world_countries.json',
                  data=forecast_df,
                  columns=['date', 'water_level'],
                  key_on='feature.properties.name',
                  fill_color='YlGnBu',
                  fill_opacity=0.7,
                  line_opacity=0.8,
                  highlight=True).add_to(m)
m.save("55.html")