import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from folium import Map, GeoJson


# Загрузить данные о расходе воды для рек Emel и Turgen
emel_data = pd.read_csv("emel_discharge.csv", index_col="Year")
turgen_data = pd.read_csv("turgen_discharge.csv", index_col="Year")

# Вычислить годовой расход воды
emel_annual_flow = emel_data["Discharge"].sum()
turgen_annual_flow = turgen_data["Discharge"].sum()

# Расчет процентного изменения расхода по сравнению с предыдущим годом
emel_percentage_change = (emel_annual_flow - emel_annual_flow.shift(1)) / emel_annual_flow.shift(1) * 100
turgen_percentage_change = (turgen_annual_flow - turgen_annual_flow.shift(1)) / turgen_annual_flow.shift(1) * 100

# Вычислить коэффициент вариации
emel_cv = np.std(emel_annual_flow) / np.mean(emel_annual_flow)
turgen_cv = np.std(turgen_annual_flow) / np.mean(turgen_annual_flow)

# Сравнить коэффициенты вариации
if emel_cv > turgen_cv:
    print("Река Emel демонстрирует более значительную межгодовую изменчивость стока.")
else:
    print("Река Turgen демонстрирует более значительную межгодовую изменчивость стока.")

# Визуализация данных (необязательно)
m = Map(location=[43.25, 76.9], zoom_start=8)
GeoJson("rivers.geojson").add_to(m)
m.save("202.html")