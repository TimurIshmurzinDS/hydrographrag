import pandas as pd
import folium

# Загрузка данных (замените на ваши файлы)
data_bayankol = pd.read_csv("bayankol_river_data.csv")
data_lepsy = pd.read_csv("lepsy_river_data.csv")

# Предобработка данных (при необходимости)

# Расчет средних уровней воды по месяцам
monthly_averages_bayankol = data_bayankol.groupby(pd.Grouper(key="date", freq="M"))["water_level"].mean()
monthly_averages_lepsy = data_lepsy.groupby(pd.Grouper(key="date", freq="M"))["water_level"].mean()

# Создание карты Folium
m = folium.Map(location=[data_bayankol["latitude"].mean(), data_bayankol["longitude"].mean()], zoom_start=8)

# Визуализация данных (пример, можно изменить в зависимости от потребностей)
folium.GeoJson("river_shapefile.geojson", name="Bayankol River").add_to(m)
folium.GeoJson("river_shapefile.geojson", name="Lepsy River").add_to(m)

# Добавление графиков уровней воды на карту (пример, можно изменить)
for i in range(len(monthly_averages_bayankol)):
    folium.Marker(location=[data_bayankol["latitude"].iloc[i], data_bayankol["longitude"].iloc[i]], popup=f"Average: {monthly_averages_bayankol.iloc[i]}").add_to(m)

for i in range(len(monthly_averages_lepsy)):
    folium.Marker(location=[data_lepsy["latitude"].iloc[i], data_lepsy["longitude"].iloc[i]], popup=f"Average: {monthly_averages_lepsy.iloc[i]}").add_to(m)

# Сохранение карты
m.save("155.html")