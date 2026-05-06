import pandas as pd
import geopandas as gpd
import folium

# Загрузка данных о расходе воды (замените на ваши файлы)
data_2020 = pd.read_csv("sarykan_2020.csv") 
data_2023 = pd.read_csv("sarykan_2023.csv")

# Преобразование данных в удобный формат
data_2020['Date'] = pd.to_datetime(data_2020['Date'])
data_2020['Month'] = data_2020['Date'].dt.month
data_2023['Date'] = pd.to_datetime(data_2023['Date'])
data_2023['Month'] = data_2023['Date'].dt.month

# Расчет средних значений расхода воды по месяцам
monthly_avg_2020 = data_2020.groupby('Month')['Discharge'].mean()
monthly_avg_2023 = data_2023.groupby('Month')['Discharge'].mean()

# Загрузка геоданных реки Sarykan (замените на ваш файл)
river = gpd.read_file("sarykan_river.shp")

# Создание карты с folium
m = folium.Map(location=[42.5, 70], zoom_start=10)

# Добавление геоданных реки на карту
folium.GeoJson(river).add_to(m)

# Добавление графиков изменения расхода воды
for year, data in zip([2020, 2023], [monthly_avg_2020, monthly_avg_2023]):
    folium.plugins.Chart(data=data.values.tolist(),
                         name=f"Средний расход {year}",
                         x_axis="Месяц", y_axis="Расход воды (м³/с)").add_to(m)

# Сохранение карты
m.save("58.html")