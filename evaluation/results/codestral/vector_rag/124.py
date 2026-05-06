python
   import pandas as pd
   from sklearn.linear_model import LinearRegression

   # Load the historical water level data for Dos River
   dos_data = pd.read_csv('dos_river_water_levels.csv')

   # Load the historical water level data for Lepsy River
   lepsy_data = pd.read_csv('lepsy_river_water_levels.csv')

   # Create a linear regression model using Dos River data to predict Lepsy River data
   model = LinearRegression()
   model.fit(dos_data['Water_level_Valuecm'].values.reshape(-1, 1), lepsy_data['Water_level_Value'])

   # Predict the water levels for Lepsy River in 2025 using Dos River data from 2025
   dos_2025 = pd.read_csv('dos_river_water_levels_2025.csv')
   lepsy_2025_predictions = model.predict(dos_2025['Water_level_Valuecm'].values.reshape(-1, 1))

   # Print the predictions
   print("Predicted water levels for Lepsy River in 2025:")
   print(lepsy_2025_predictions)