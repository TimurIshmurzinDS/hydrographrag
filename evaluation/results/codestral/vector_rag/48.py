python
   import pandas as pd

   # Предположим, что у нас есть DataFrame df с колонками 'Date' и 'Water_consumption_Valuem³s'
   filtered_data = df[(df['Date'] >= '2010-01-01') & (df['Date'] <= '2020-12-31')]

   # Теперь у нас есть данные о расходе воды в реке Каркара за период с 2010 по 2020 годы
   print(filtered_data)