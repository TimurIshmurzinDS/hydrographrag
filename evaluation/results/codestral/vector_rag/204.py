python
   import pandas as pd
   import matplotlib.pyplot as plt

   # Load the data for both rivers
   byzhy_data = pd.read_csv('byzhy_river_discharge.csv')
   urzhar_data = pd.read_csv('urzhar_river_discharge.csv')

   # Plotting the discharge data
   plt.figure(figsize=(10, 6))
   plt.plot(byzhy_data['Date'], byzhy_data['Discharge'], label='Byzhy River')
   plt.plot(urzhar_data['Date'], urzhar_data['Discharge'], label='Urzhar River')
   plt.title('Comparison of Discharge Regimes for Byzhy and Urzhar Rivers')
   plt.xlabel('Date')
   plt.ylabel('Discharge (m³/s)')
   plt.legend()
   plt.show()