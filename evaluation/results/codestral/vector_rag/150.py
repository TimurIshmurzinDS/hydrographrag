python
   import pandas as pd
   import matplotlib.pyplot as plt
   import seaborn as sns

   # Load the data for Karatal River
   karatal_data = pd.read_csv('karatal_water_level_data.csv')

   # Convert Date_water_level_Value to datetime format
   karatal_data['Date_water_level_Value'] = pd.to_datetime(karatal_data['Date_water_level_Value'])

   # Set Date_water_level_Value as the index of the DataFrame
   karatal_data.set_index('Date_water_level_Value', inplace=True)

   # Analyze time series data for Karatal River
   plt.figure(figsize=(12, 6))
   sns.lineplot(data=karatal_data['Water_level_Valuecm'])
   plt.title('Water Level Time Series - Karatal River')
   plt.xlabel('Date')
   plt.ylabel('Water Level (cm)')
   plt.show()

   # Calculate statistical measures for Karatal River
   karatal_stats = karatal_data['Water_level_Valuecm'].describe()

   # Load the data for Ili River
   ili_data = pd.read_csv('ili_water_level_data.csv')

   # Repeat the analysis steps for Ili River...

   # Compare statistical measures between Karatal and Ili Rivers
   comparison_df = pd.DataFrame({'Karatal': karatal_stats, 'Ili': ili_stats})
   print(comparison_df)

   # Check correlation between water level and water quality class for Karatal River
   correlation = karatal_data['Water_level_Valuecm'].corr(karatal_data['Water_quality_class'])
   print('Correlation between Water Level and Water Quality Class:', correlation)