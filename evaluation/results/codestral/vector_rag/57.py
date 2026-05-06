python
   import pandas as pd
   from statsmodels.tsa.arima_model import ARIMA
   import matplotlib.pyplot as plt

   # Load the water level data for Kurty River
   data = pd.read_csv('kurty_river_water_level_data.csv', index_col='Date_water_level_Value', parse_dates=True)

   # Fit ARIMA model to the data
   model = ARIMA(data['Water_level_Valuecm'], order=(5,1,0))
   model_fit = model.fit(disp=0)

   # Make water level predictions for the next 30 days
   forecast, stderr, conf_int = model_fit.forecast(steps=30)

   # Plot the results
   plt.figure(figsize=(12,8))
   plt.plot(data['Water_level_Valuecm'], label='Historical')
   plt.plot(pd.date_range(start=data.index[-1], periods=31)[1:], forecast, color='red', label='Forecast')
   plt.fill_between(pd.date_range(start=data.index[-1], periods=31)[1:], conf_int[:,0], conf_int[:,1], color='pink')
   plt.legend()
   plt.title('Water Level Forecast for Kurty River')
   plt.xlabel('Date')
   plt.ylabel('Water Level (cm)')
   plt.show()