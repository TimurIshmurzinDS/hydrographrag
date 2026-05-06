python
   import pandas as pd
   import matplotlib.pyplot as plt

   # Assuming we have data in a CSV file with columns 'Year', 'Month', 'Prokhodnaya_River', 'Baskan_River'
   data = pd.read_csv('river_data.csv')

   # Calculate average seasonal water consumption for each river
   avg_prokhodnaya = data['Prokhodnaya_River'].mean()
   avg_baskan = data['Baskan_River'].mean()

   print(f'Average seasonal water consumption for Prokhodnaya River: {avg_prokhodnaya}')
   print(f'Average seasonal water consumption for Baskan River: {avg_baskan}')

   # Visualize data using a line plot
   plt.figure(figsize=(10, 6))
   plt.plot(data['Year'], data['Prokhodnaya_River'], label='Prokhodnaya River')
   plt.plot(data['Year'], data['Baskan_River'], label='Baskan River')
   plt.xlabel('Year')
   plt.ylabel('Seasonal Water Consumption')
   plt.title('Comparison of Seasonal Water Consumption on Prokhodnaya and Baskan Rivers')
   plt.legend()
   plt.show()