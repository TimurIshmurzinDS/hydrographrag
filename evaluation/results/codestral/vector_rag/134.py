python
   import pandas as pd

   # Загрузка данных о уровне воды за последнее десятилетие для каждой реки
   kishi_data = pd.read_csv('kishi_almaty_river_water_levels.csv')
   bayankol_data = pd.read_csv('bayankol_river_water_levels.csv')

   # Вычисление стандартного отклонения уровней воды для каждой реки
   kishi_std = kishi_data['Water_level_Value'].std()
   bayankol_std = bayankol_data['Water_level_Value'].std()

   # Сравнение стандартных отклонений
   if bayankol_std > kishi_std:
       print("Волатильность стока в реке Bayankol River выше, чем в реке Kishi Almaty River.")
   else:
       print("Волатильность стока в реке Kishi Almaty River выше или равна волатильности стока в реке Bayankol River.")