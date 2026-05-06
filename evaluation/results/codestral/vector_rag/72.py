python
   import pandas as pd
   import matplotlib.pyplot as plt

   # Assuming df is a DataFrame with the data
   # Here we are plotting water levels over time for both rivers

   plt.figure(figsize=(10,6))

   # Filter data for Tentek River and plot
   tentek_data = df[df['River'] == 'Tentek River']
   plt.plot(tentek_data['Date_water_level_Value'], tentek_data['Water_level_Valuecm'], label='Tentek River')

   # Filter data for Temirlik River and plot
   temirlik_data = df[df['River'] == 'Temirlik River']
   plt.plot(temirlik_data['Date_water_level_Value'], temirlik_data['Water_level_Valuecm'], label='Temirlik River')

   # Add labels and title
   plt.xlabel('Date')
   plt.ylabel('Water Level (cm)')
   plt.title('Water Levels Over Time for Tentek River and Temirlik River')
   plt.legend()
   plt.show()