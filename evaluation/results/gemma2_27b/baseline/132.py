import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузка данных о уровнях воды из CSV файлов (замените на ваши файлы)
lepsy_data = pd.read_csv("lepsy_river_levels.csv", index_col="Date")
tekes_data = pd.read_csv("tekes_river_levels.csv", index_col="Date")

# Расчет среднегодового стока
lepsy_annual_mean = lepsy_data.groupby(lambda x: x.year).mean()
tekes_annual_mean = tekes_data.groupby(lambda x: x.year).mean()

# Определение года с максимальным стоком в реке Lepsy
max_flow_year = lepsy_annual_mean["Level"].idxmax()

# Вывод информации о максимальном стоке
print(f"Год с максимальным стоком в реке Lepsy: {max_flow_year}")
print(f"Средний уровень воды в этот год: {lepsy_annual_mean.loc[max_flow_year, 'Level']} ")

# Сравнение со средним уровнем воды в тот же год в реке Tekes
print(f"Средний уровень воды в реке Tekes за тот же год: {tekes_annual_mean.loc[max_flow_year, 'Level']}")

# Визуализация (необязательно)
m = folium.Map(location=[50, 50], zoom_start=6) # Замените на координаты рек

folium.Marker([lepsy_data.index[0].latitude, lepsy_data.index[0].longitude], popup="Lepsy River").add_to(m)
folium.Marker([tekes_data.index[0].latitude, tekes_data.index[0].longitude], popup="Tekes River").add_to(m)

m.save("132.html")