import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, GeoJson


# Загрузить данные о уровнях воды из CSV файла
data = pd.read_csv("river_data.csv")

# Преобразовать дату в формат datetime
data["date"] = pd.to_datetime(data["date"])

# Вычислить средний уровень воды за каждый месяц
monthly_mean = data.groupby(pd.Grouper(key="date", freq="M")).mean()

# Определить стандартное отклонение от среднего значения
std_dev = data.groupby(pd.Grouber(key="date", freq="M")).std()

# Визуализировать данные в виде графика
plt.plot(monthly_mean["water_level"], label="Average Water Level")
plt.xlabel("Month")
plt.ylabel("Water Level (meters)")
plt.legend()
plt.show()

# Создать карту с помощью Folium
m = Map(location=[data["latitude"].mean(), data["longitude"].mean()], zoom_start=8)

# Добавить реки на карту
GeoJson(data[["geometry"]]).add_to(m)

# Сохранить карту в HTML файл
m.save("116.html")