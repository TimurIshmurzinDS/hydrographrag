python
   import pandas as pd
   from statsmodels.tsa.arima_model import ARIMA

   # Load the historical water consumption data for Sharyn River and Kishi Almaty River
   sharyn_data = pd.read_csv('sharyn_river_data.csv', index_col='Date', parse_dates=True)
   kishi_almaty_data = pd.read_csv('kishi_almaty_river_data.csv', index_col='Date', parse_dates=True)

   # Fit an ARIMA model to the Sharyn River data
   model = ARIMA(sharyn_data['Water_Consumption'], order=(5,1,0))
   model_fit = model.fit(disp=0)

   # Use the fitted model to forecast water consumption for Kishi Almaty River
   forecast = model_fit.forecast(steps=len(kishi_almaty_data))[0]

   # Print the forecasted values
   print("Forecasted Water Consumption for Kishi Almaty River:")
   print(forecast)