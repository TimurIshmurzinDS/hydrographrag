import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
import folium

# Загрузить данные уровней воды из CSV файла
data = pd.read_csv("koksu_river_levels.csv", index_col="date")

# Вычислить среднее значение и стандартное отклонение
mean = np.mean(data["level"])
std = np.std(data["level"])

# Уровень 50-летнего паводка (получить из гидрологических данных)
threshold = 50

# Расчет вероятности превышения порога
probability = 1 - norm.cdf(threshold, loc=mean, scale=std)

print("Вероятность превышения порога:", probability)

# Визуализация

plt.figure()
x = np.linspace(data["level"].min(), data["level"].max(), 100)
y = norm.pdf(x, loc=mean, scale=std)
plt.plot(x, y)
plt.axvline(threshold, color="red", linestyle="--")

plt.xlabel("Уровень воды")
plt.ylabel("Вероятность")
plt.title("Распределение вероятностей уровней воды")
plt.show()

# Карта (если требуется)

m = folium.Map(location=[43.25, 76.9], zoom_start=10)
folium.Marker(location=[43.25, 76.9], popup="Koksu River").add_to(m)
m.save("203.html")