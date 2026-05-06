python
   import pandas as pd
   import matplotlib.pyplot as plt
   from scipy import stats

   # Load the data (assuming it's in a CSV format)
   data = pd.read_csv('water_consumption_data.csv')

   # Filter data for Koksu River and Emel River
   koksu_data = data[data['River'] == 'Koksu River']
   emel_data = data[data['River'] == 'Emel River']

   # Plotting the water consumption over time
   plt.figure(figsize=(10,6))
   plt.plot(koksu_data['Year'], koksu_data['Water_consumption_Valuem³s'], label='Koksu River')
   plt.plot(emel_data['Year'], emel_data['Water_consumption_Valuem³s'], label='Emel River')
   plt.title('Water Consumption in Koksu and Emel Rivers (2011-2021)')
   plt.xlabel('Year')
   plt.ylabel('Water Consumption (m³/s)')
   plt.legend()
   plt.show()

   # Perform a statistical test to check if the differences are significant
   t_stat, p_value = stats.ttest_ind(koksu_data['Water_consumption_Valuem³s'], emel_data['Water_consumption_Valuem³s'])
   print(f'T-Statistic: {t_stat}, P-Value: {p_value}')