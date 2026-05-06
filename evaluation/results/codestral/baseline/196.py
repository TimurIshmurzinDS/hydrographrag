python
         import pandas as pd
         import matplotlib.pyplot as plt
         # Load data
         koksu_data = pd.read_csv('koksu_river_data.csv')
         emel_data = pd.read_csv('emel_river_data.csv')
         # Check for missing values or anomalies
         print(koksu_data.isnull().sum())
         print(emel_data.isnull().sum())
         # Convert date column to datetime format
         koksu_data['date'] = pd.to_datetime(koksu_data['date'])
         emel_data['date'] = pd.to_datetime(emel_data['date'])
         # Set date column as index
         koksu_data.set_index('date', inplace=True)
         emel_data.set_index('date', inplace=True)
         # Plot seasonal patterns
         plt.figure(figsize=(12, 6))
         plt.subplot(2, 1, 1)
         koksu_data['water_flow'].resample('M').mean().plot()
         plt.title('Koksu River Water Flow')
         plt.subplot(2, 1, 2)
         emel_data['water_flow'].resample('M').mean().plot()
         plt.title('Emel River Water Flow')
         plt.tight_layout()
         plt.show()
         # Compare seasonal patterns
         correlation = koksu_data['water_flow'].resample('M').mean().corr(emel_data['water_flow'].resample('M').mean())
         print('Correlation coefficient:', correlation)