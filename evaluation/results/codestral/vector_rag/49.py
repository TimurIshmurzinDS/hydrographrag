python
   import pandas as pd

   # Assuming we have a DataFrame df with columns 'Date_water_level_Value' and 'Water_level_Value'
   # Filter data for 2015 and 2023
   df_2015 = df[df['Date_water_level_Value'].dt.year == 2015]
   df_2023 = df[df['Date_water_level_Value'].dt.year == 2023]

   # Find peak water levels for each year
   peak_2015 = df_2015['Water_level_Value'].max()
   peak_2023 = df_2023['Water_level_Value'].max()

   print(f"Пиковый уровень воды в реке Батарейка в 2015 году: {peak_2015}")
   print(f"Пиковый уровень воды в реке Батарейка в 2023 году: {peak_2023}")

   if peak_2015 > peak_2023:
       print("В 2015 году пиковые уровни воды были выше, чем в 2023 году.")
   elif peak_2015 < peak_2023:
       print("В 2023 году пиковые уровни воды были выше, чем в 2015 году.")
   else:
       print("Пиковые уровни воды в 2015 и 2023 годах были одинаковыми.")