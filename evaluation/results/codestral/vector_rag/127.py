python
   import pandas as pd

   # Предположим, что у нас есть DataFrame df с данными о реке Шарын
   # df = pd.read_csv('sharyn_river_data.csv')

   # Определяем максимальное значение уровня воды
   max_water_level = df['Water_level_Value'].max()

   # Вычисляем среднее значение уровня воды
   avg_water_level = df['Water_level_Value'].mean()

   # Рассчитываем разницу
   difference = max_water_level - avg_water_level

   print(f'Разница между максимальным и средним уровнем воды в реке Шарын: {difference}')