import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных
df1 = pd.read_csv("data1.csv", index_col="date")
df2 = pd.read_csv("data2.csv", index_col="date")

# Выравнивание индекса
df1 = df1.reindex(df2.index)

# Расчет метрик
correlation = df1.corr(df2)
rmse = np.sqrt(((df1 - df2)**2).mean())

print("Correlation:", correlation)
print("RMSE:", rmse)

# Визуализация
plt.plot(df1, label="Series 1")
plt.plot(df2, label="Series 2")
plt.legend()
plt.show()