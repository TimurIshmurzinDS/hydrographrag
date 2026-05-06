import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, GeoJson


# Загрузка данных о расходе воды из CSV файла
data = pd.read_csv("turgen_river_flow.csv", index_col="Date")

# Расчет средних значений расхода для каждого месяца
monthly_averages = data.groupby(lambda x: x.month).mean()

# Определение отклонений от нормы
current_flow = data.iloc[-1]["Flow"]
average_flow = monthly_averages.loc[data.index[-1].month]["Flow"]
deviation = (current_flow - average_flow) / average_flow * 100

# Визуализация данных

# Карта Turgen River (заменить на реальные координаты)
m = Map(location=[43.5, 78], zoom_start=12)

# Добавление слоя с рекой (заменить на реальный GeoJson файл)
GeoJson("river_geojson.geojson").add_to(m)

# Визуализация отклонений от нормы цветом

if deviation > 10:
    color = "red"
else:
    color = "green"

# Добавление маркера на карте с текущим расходом и цветом,
# соответствующим отклонению от нормы.

plt.plot(data["Flow"])
plt.show()

m.save("79.html")