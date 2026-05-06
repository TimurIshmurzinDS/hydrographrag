python
   import pandas as pd
   import matplotlib.pyplot as plt

   # Load the data (assuming it's in a CSV file)
   data = pd.read_csv('hydro_data.csv')

   # Filter the data for Koksu and Byzhy rivers
   koksu_data = data[data['river'] == 'Koksu River']
   byzhy_data = data[data['river'] == 'Byzhy River']

   # Calculate statistics
   koksu_min_trend = koksu_data['min_level'].mean()
   byzhy_min_trend = byzhy_data['min_level'].mean()

   # Visualize the data
   plt.figure(figsize=(10, 6))
   plt.plot(koksu_data['year'], koksu_data['min_level'], label='Koksu River')
   plt.plot(byzhy_data['year'], byzhy_data['min_level'], label='Byzhy River')
   plt.title('Decadal Trend of Minimum Water Levels in Koksu and Byzhy Rivers')
   plt.xlabel('Year')
   plt.ylabel('Minimum Water Level')
   plt.legend()
   plt.show()

   print(f'Average minimum water level in Koksu River: {koksu_min_trend}')
   print(f'Average minimum water level in Byzhy River: {byzhy_min_trend}')