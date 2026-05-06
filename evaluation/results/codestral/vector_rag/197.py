python
   import pandas as pd
   from statsmodels.tsa.arima_model import ARIMA

   # Load the data (assuming it's in a CSV file)
   data = pd.read_csv('aksuroverflow_data.csv', index_col='Date_water_level_Value', parse_dates=True)

   # Fit the ARIMA model
   model = ARIMA(data['Water_level_Value'], order=(5,1,0))
   model_fit = model.fit(disp=0)

   # Make predictions for the next season
   forecast, stderr, conf_int = model_fit.forecast(steps=365)  # Assuming a year has 365 days

   print('Forecasted peak discharge for the next season:', forecast[-1])