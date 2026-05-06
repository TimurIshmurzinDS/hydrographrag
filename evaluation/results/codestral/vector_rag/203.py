python
   import pandas as pd
   from scipy import stats

   # Load the data (assuming it's in a CSV file)
   data = pd.read_csv('koksu_river_data.csv')

   # Define the 50-year flood threshold (for example, using the 98th percentile of the data)
   flood_threshold = data['Water_level_Value'].quantile(0.98)

   # Calculate the probability of exceeding this threshold in a given time period
   exceedances = data[data['Water_level_Value'] > flood_threshold]
   probability = len(exceedances) / len(data)

   print('The probability of exceeding the 50-year flood threshold is:', probability)