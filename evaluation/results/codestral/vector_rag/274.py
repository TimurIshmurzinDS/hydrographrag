python
   import matplotlib.pyplot as plt

   # Гипотетические данные о добыче золота в XIX и XX веках
   gold_production_19th_century = [50, 60, 70, 80, 90]
   gold_production_20th_century = [100, 110, 120, 130, 140]

   # Создание графика
   plt.figure(figsize=(10, 6))
   plt.plot(gold_production_19th_century, label='XIX век')
   plt.plot(gold_production_20th_century, label='XX век')
   plt.title('Динамика добычи золота в XIX и XX веках')
   plt.xlabel('Временной интервал')
   plt.ylabel('Количество добываемого золота')
   plt.legend()
   plt.show()