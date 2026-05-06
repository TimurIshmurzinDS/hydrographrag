import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import folium

# Загрузить данные о уровнях воды из CSV файлов
lepsy_data = pd.read_csv("lepsy_river_data.csv", index_col="Date")
turgen_data = pd.read_csv("turgen_river_data.csv", index_col="Date")

# Создать модель линейной регрессии для каждого набора данных
lepsy_model = LinearRegression()
turgen_model = LinearRegression()

# Обучить модели на данных
lepsy_model.fit(lepsy_data.index.values.reshape(-1, 1), lepsy_data["Water Level"])
turgen_model.fit(turgen_data.index.values.reshape(-1, 1), turgen_data["Water Level"])

# Создать графики трендов
plt.figure()
plt.plot(lepsy_data.index, lepsy_data["Water Level"], label="Lepsy River")
plt.plot(turgen_data.index, turgen_data["Water Level"], label="Turgen River")

# Создать карту с точками рек
m = folium.Map()
folium.Marker([lepsy_data["Latitude"].iloc[0], lepsy_data["Longitude"].iloc[0]], popup="Lepsy River").add_to(m)
folium.Marker([turgen_data["Latitude"].iloc[0], turgen_data["Longitude"].iloc[0]], popup="Turgen River").add_to(m)

# Сохранить карту
m.save("198.html")

plt.legend()
plt.show()