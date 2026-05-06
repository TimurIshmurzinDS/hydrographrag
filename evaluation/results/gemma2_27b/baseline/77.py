import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузка данных о расходе воды из CSV файлов
baskan_data = pd.read_csv("baskan_river_data.csv", index_col="Date")
prokhodnaya_data = pd.read_csv("prokhodnaya_river_data.csv", index_col="Date")

# Расчет средних значений расхода для каждого сезона
def calculate_seasonal_mean(data):
    spring_mean = data["Flow"].loc[(pd.to_datetime(data.index).month >= 3) & (pd.to_datetime(data.index).month <= 5)].mean()
    summer_mean = data["Flow"].loc[(pd.to_datetime(data.index).month >= 6) & (pd.to_datetime(data.index).month <= 8)].mean()
    autumn_mean = data["Flow"].loc[(pd.to_datetime(data.index).month >= 9) & (pd.to_datetime(data.index).month <= 11)].mean()
    winter_mean = data["Flow"].loc[(pd.to_datetime(data.index).month == 12) | (pd.to_datetime(data.index).month >= 1) & (pd.to_datetime(data.index).month <= 2)].mean()

    return [spring_mean, summer_mean, autumn_mean, winter_mean]

baskan_means = calculate_seasonal_mean(baskan_data)
prokhodnaya_means = calculate_seasonal_mean(prokhodnaya_data)

# Вывод результатов сравнения
print("Средний расход воды весной:")
print("Baskan River:", baskan_means[0])
print("Prokhodnaya River:", prokhodnaya_means[0])

# Прогноз весеннего половодья (на основе сравнения средних значений расхода)
if baskan_means[0] > prokhodnaya_means[0]:
    print("Прогнозируется более высокое весеннее половодье на реке Baskan River.")
else:
    print("Прогнозируется более высокое весеннее половодье на реке Prokhodnaya River.")

# Визуализация данных (необязательно)
m = folium.Map(location=[50, 50], zoom_start=8)
folium.Marker(location=[50, 50], popup="Baskan River").add_to(m)
folium.Marker(location=[51, 51], popup="Prokhodnaya River").add_to(m)

m.save("77.html")