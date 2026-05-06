python
   import pandas as pd
   import matplotlib.pyplot as plt

   # Load the historical data for Lepsy River and Aksu River
   lepsy_data = pd.read_csv('lepsy_river_data.csv')
   aksu_data = pd.read_csv('aksu_river_data.csv')

   # Assuming the data has columns 'Season' and 'Flow'
   # Group by season and calculate average flow for each river
   lepsy_seasonal_flow = lepsy_data.groupby('Season')['Flow'].mean()
   aksu_seasonal_flow = aksu_data.groupby('Season')['Flow'].mean()

   # Plot the data
   plt.figure(figsize=(10, 6))
   plt.plot(lepsy_seasonal_flow.index, lepsy_seasonal_flow.values, label='Lepsy River')
   plt.plot(aksu_seasonal_flow.index, aksu_seasonal_flow.values, label='Aksu River')
   plt.title('Seasonal Flow Comparison: Lepsy River vs Aksu River')
   plt.xlabel('Season')
   plt.ylabel('Flow (m³/s)')
   plt.legend()
   plt.show()