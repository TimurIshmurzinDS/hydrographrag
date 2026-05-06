python
   import pandas as pd

   # Assuming we have a DataFrame df with columns 'Date' and 'Water_consumption_Valuem³s'

   # Convert the Date column to datetime type
   df['Date'] = pd.to_datetime(df['Date'])

   # Create a new column for Season
   df['Season'] = df['Date'].dt.month % 12 + 3 // 4
   df['Season'] = df['Season'].map({0: 'Winter', 1: 'Spring', 2: 'Summer', 3: 'Autumn'})

   # Calculate the average water consumption for each season
   avg_water_consumption = df.groupby('Season')['Water_consumption_Valuem³s'].mean()

   print(avg_water_consumption)