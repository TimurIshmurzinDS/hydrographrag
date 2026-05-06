python
   import pandas as pd
   import matplotlib.pyplot as plt

   # Load the data for both rivers (assuming we have a CSV file with columns 'Date', 'Kishi_Almaty_Flow', and 'Shilik_Flow')
   data = pd.read_csv('river_flow_data.csv', parse_dates=['Date'])

   # Set the date as index
   data.set_index('Date', inplace=True)

   # Plotting the flow for both rivers
   plt.figure(figsize=(12, 6))
   plt.plot(data['Kishi_Almaty_Flow'], label='Kishi Almaty River')
   plt.plot(data['Shilik_Flow'], label='Shilik River')
   plt.title('Seasonal Variation of Flow for Kishi Almaty and Shilik Rivers')
   plt.xlabel('Date')
   plt.ylabel('Flow (m³/s)')
   plt.legend()
   plt.show()