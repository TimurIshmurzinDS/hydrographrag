import pandas as pd
import numpy as np
from scipy import stats
import folium

# Загрузка данных о расходе воды из CSV файлов
data_aksu = pd.read_csv("aksu_river_flow.csv", index_col="date")
data_temirlik = pd.read_csv("temirlik_river_flow.csv", index_col="date")

# Расчет SPI (Standardized Precipitation Index) для каждой реки
def calculate_spi(data, window=12):
    return stats.zscore(data.rolling(window).mean())

spi_aksu = calculate_spi(data_aksu["flow"])
spi_temirlik = calculate_spi(data_temirlik["flow"])

# Определение реки с большим риском засухи
if np.min(spi_aksu) < np.min(spi_temirlik):
    risky_river = "Aksu River"
else:
    risky_river = "Temirlik River"

print(f"The river with higher risk of drought is {risky_river}")

# Визуализация на карте (необязательно)
m = folium.Map()
folium.Marker([data_aksu.index[0], data_aksu["flow"][0]], popup="Aksu River").add_to(m)
folium.Marker([data_temirlik.index[0], data_temirlik["flow"][0]], popup="Temirlik River").add_to(m)

m.save("111.html")