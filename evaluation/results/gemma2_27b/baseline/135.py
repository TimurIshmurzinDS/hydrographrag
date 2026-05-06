import pandas as pd
import folium
from scipy import stats

# Загрузка данных о расходах рек (заменить на ваши данные)
shilik_data = pd.read_csv("shilik_river_flow.csv", index_col="date")
sharyn_data = pd.read_csv("sharyn_river_flow.csv", index_col="date")

# Расчет SPI (заменить на вашу функцию)
def calculate_SPI(data):
    return stats.norm.ppf(data.rank() / len(data))

shilik_SPI = calculate_SPI(shilik_data["flow"])
sharyn_SPI = calculate_SPI(sharyn_data["flow"])

# Создание карты
m = folium.Map(location=[43, 80], zoom_start=7)

# Добавление графиков SPI на карту
folium.Chart(pd.DataFrame({"SPI": shilik_SPI}).set_index("date").plot()).add_to(m)
folium.Chart(pd.DataFrame({"SPI": sharyn_SPI}).set_index("date").plot()).add_to(m)

# Сохранение карты
m.save("135.html")