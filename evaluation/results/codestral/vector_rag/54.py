python
   import pandas as pd

   # Assuming we have a DataFrame df with columns 'Year' and 'Water_consumption_Valuem³s'
   # We need to ensure that the data is sorted by year
   df = df.sort_values('Year')

   # Calculate average water consumption for each decade
   df['Decade'] = (df['Year'] // 10) * 10
   avg_consumption = df.groupby('Decade')['Water_consumption_Valuem³s'].mean()

   # Calculate the difference between the last and previous decade
   diff = avg_consumption.iloc[-1] - avg_consumption.iloc[-2]

   print(f"The difference in water consumption between the last and previous decade is: {diff} m³s")