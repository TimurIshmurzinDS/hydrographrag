python
         import pandas as pd
         from statsmodels.tsa.arima_model import ARIMA
         from sklearn.metrics import mean_squared_error
         import folium
         # Загрузка данных
         data = pd.read_csv('batareyka_river_data.csv', index_col='Date', parse_dates=True)
         # Анализ временных рядов и моделирование (ARIMA в качестве примера)
         model = ARIMA(data['Water Level'], order=(5,1,0))
         model_fit = model.fit(disp=0)
         # Прогнозирование на следующий год
         forecast, stderr, conf_int = model_fit.forecast(steps=365)
         # Визуализация результатов на карте
         m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=10)
         for i in range(len(forecast)):
             folium.CircleMarker([data['Latitude'].iloc[-1], data['Longitude'].iloc[-1]], radius=forecast[i]/10, color='blue', fill=True, fill_color='blue').add_to(m)
         m.save("55.html")