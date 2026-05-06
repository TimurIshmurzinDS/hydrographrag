python
   import pandas as pd

   # Загрузка данных из файла (предполагается, что у вас есть доступ к файлу с данными)
   data = pd.read_csv('river_data.csv')

   # Фильтрация данных для каждой реки
   lepsy_data = data[data['River'] == 'Lepsy River']
   tekes_data = data[data['River'] == 'Tekes River']

   # Нахождение года с самым высоким уровнем стока в реке Lepsy River
   lepsy_max_year = lepsy_data.loc[lepsy_data['Water_level_Value'].idxmax()]['Year']
   lepsy_max_value = lepsy_data['Water_level_Value'].max()

   # Нахождение уровня стока в реке Tekes River в тот же год
   tekes_value = tekes_data[tekes_data['Year'] == lepsy_max_year]['Water_level_Value'].values[0]

   print(f"Год с самым высоким уровнем стока в реке Lepsy River: {lepsy_max_year}")
   print(f"Уровень стока в этот год: {lepsy_max_value} м")
   print(f"Уровень стока в реке Tekes River в тот же год: {tekes_value} м")