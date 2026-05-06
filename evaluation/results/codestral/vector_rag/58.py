python
   import pandas as pd
   import matplotlib.pyplot as plt

   # Assuming that the data is stored in a CSV file named 'river_data.csv'
   # with columns 'Date', 'Water_consumption_Value', and 'Year'
   df = pd.read_csv('river_data.csv')

   # Filter data for 2020 and 2023
   df_2020 = df[df['Year'] == 2020]
   df_2023 = df[df['Year'] == 2023]

   # Group data by month and calculate the average water consumption for each month
   df_2020_monthly = df_2020.groupby(pd.to_datetime(df_2020['Date']).dt.month)['Water_consumption_Value'].mean()
   df_2023_monthly = df_2023.groupby(pd.to_datetime(df_2023['Date']).dt.month)['Water_consumption_Value'].mean()

   # Plot the data
   plt.figure(figsize=(10, 6))
   plt.plot(df_2020_monthly.index, df_2020_monthly.values, label='2020')
   plt.plot(df_2023_monthly.index, df_2023_monthly.values, label='2023')
   plt.xlabel('Month')
   plt.ylabel('Average Water Consumption')
   plt.title('Comparison of Monthly Water Consumption in Sarykan River (2020 vs 2023)')
   plt.legend()
   plt.show()