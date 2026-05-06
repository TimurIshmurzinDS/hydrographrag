python
   import pandas as pd
   import matplotlib.pyplot as plt

   # Загрузка данных о расходе воды для рек Темирлик и Турген
   temirlik_data = pd.read_csv('temirlik_river_discharge.csv')
   turgen_data = pd.read_csv('turgen_river_discharge.csv')

   # Графическое отображение сезонных динамик расхода воды
   plt.figure(figsize=(10, 6))
   plt.plot(temirlik_data['Month'], temirlik_data['Discharge'], label='Temirlik River')
   plt.plot(turgen_data['Month'], turgen_data['Discharge'], label='Turgen River')
   plt.title('Seasonal Dynamics of Water Discharge')
   plt.xlabel('Month')
   plt.ylabel('Water Discharge (m³/s)')
   plt.legend()
   plt.show()