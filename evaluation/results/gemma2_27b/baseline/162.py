import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import folium

# Загрузить данные о таянии снега и уровне воды
snowmelt_data = pd.read_csv("snowmelt_data.csv", index_col="Date")
water_level_data = pd.read_csv("water_level_data.csv", index_col="Date")

# Расчет разницы от среднего уровня воды
average_water_level = water_level_data["Water Level"].mean()
water_level_diff = water_level_data["Water Level"] - average_water_level

# Вычислить скользящее среднее для данных о таянии снега и уровне воды
snowmelt_moving_average = snowmelt_data["Snow Melt"].rolling(window=7).mean()
water_level_diff_moving_average = water_level_diff.rolling(window=7).mean()

# Корреляционный анализ
correlation, p_value = pearsonr(snowmelt_moving_average, water_level_diff_moving_average)

print("Коэффициент корреляции:", correlation)

# Визуализация данных
plt.figure(figsize=(12, 6))
plt.plot(snowmelt_data.index, snowmelt_moving_average, label="Таяние снега")
plt.plot(water_level_data.index, water_level_diff_moving_average, label="Разница от среднего уровня воды")

plt.xlabel("Дата")
plt.ylabel("Значение")
plt.legend()
plt.title("Корреляция между таянием снега и уровнем воды")
plt.show()

# Карта с местоположением рек
m = folium.Map(location=[45.0, 85.0], zoom_start=7)
folium.Marker([45.2619, 83.9867], popup="Bayankol River").add_to(m)
folium.Marker([44.8833, 84.5667], popup="Lepsy River").add_to(m)

m.save("162.html")