python
   import pandas as pd
   from statsmodels.tsa.arima_model import ARIMA
   import matplotlib.pyplot as plt

   # Load the data (assuming it's in a CSV format)
   data = pd.read_csv('dos_river_data.csv', index_col='Date_water_level_Value', parse_dates=True)

   # Use Water_level_Valuecm for modeling
   water_level_series = data['Water_level_Valuecm']

   # Fit the ARIMA model (p, d, q parameters need to be determined using methods like ACF and PACF plots or Grid Search)
   model = ARIMA(water_level_series, order=(1, 1, 1))
   model_fit = model.fit(disp=0)

   # Forecast the next 5 years (assuming data is daily and we want to forecast for each day in the next 5 years)
   forecast, stderr, conf_int = model_fit.forecast(steps=365*5)

   # Plot the results
   plt.figure(figsize=(12,8))
   plt.plot(water_level_series.index, water_level_series, label='Historical Data')
   plt.plot(pd.date_range(start=water_level_series.index[-1], periods=365*5), forecast, color='red', label='Forecast')
   plt.fill_between(pd.date_range(start=water_level_series.index[-1], periods=365*5), conf_int[:, 0], conf_int[:, 1], color='pink', alpha=0.2)
   plt.title('Water Level Forecast for Dos River')
   plt.xlabel('Date')
   plt.ylabel('Water Level (cm)')
   plt.legend()
   plt.show()