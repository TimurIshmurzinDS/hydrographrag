python
   import pandas as pd
   import matplotlib.pyplot as plt

   # Загрузка данных о расходе воды для каждой реки из базы данных или файлов CSV
   kurty_data = pd.read_csv('kurty_river_water_consumption.csv')
   tekes_data = pd.read_csv('tekes_river_water_consumption.csv')

   # Фильтрация данных для периода весеннего половодья за последние 5 лет
   kurty_spring_data = kurty_data[(kurty_data['date'].dt.month >= 3) & (kurty_data['date'].dt.month <= 5) & (kurty_data['date'].dt.year > pd.Timestamp.now().year - 5)]
   tekes_spring_data = tekes_data[(tekes_data['date'].dt.month >= 3) & (tekes_data['date'].dt.month <= 5) & (tekes_data['date'].dt.year > pd.Timestamp.now().year - 5)]

   # Вычисление статистических показателей для каждой реки
   kurty_stats = kurty_spring_data['Water_consumption_Value'].describe()
   tekes_stats = tekes_spring_data['Water_consumption_Value'].describe()

   # Сравнение статистических показателей между двумя реками
   print("Статистические показатели для реки Курты:")
   print(kurty_stats)
   print("\nСтатистические показатели для реки Текес:")
   print(tekes_stats)

   # Визуализация сравнения расхода воды между двумя реками
   plt.figure(figsize=(10, 6))
   plt.boxplot([kurty_spring_data['Water_consumption_Value'], tekes_spring_data['Water_consumption_Value']], labels=['Курты', 'Текес'])
   plt.title('Сравнение расхода воды в реках Курты и Текес')
   plt.ylabel('Расход воды (м³/с)')
   plt.show()