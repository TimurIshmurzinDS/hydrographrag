import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о расходе воды (заменить на реальные данные)
data = [
    {"Date_water_level_Value": "2021-06-15", "Water_consumption_Valuem³s": 15.2},
    {"Date_water_level_Value": "2021-07-20", "Water_consumption_Valuem³s": 14.8},
    {"Date_water_level_Value": "2021-08-10", "Water_consumption_Valuem³s": 16.5},
    {"Date_water_level_Value": "2021-12-05", "Water_consumption_Valuem³s": 8.3},
    {"Date_water_level_Value": "2022-01-15", "Water_consumption_Valuem³s": 7.9},
    {"Date_water_level_Value": "2022-02-25", "Water_consumption_Valuem³s": 8.6},
]

# Преобразование даты в формат datetime
import pandas as pd
df = pd.DataFrame(data)
df['Date_water_level_Value'] = pd.to_datetime(df['Date_water_level_Value'])

# Разделение данных на летние и зимние периоды
summer_data = df[(df['Date_water_level_Value'].dt.month >= 6) & (df['Date_water_level_Value'].dt.month <= 8)]
winter_data = df[(df['Date_water_level_Value'].dt.month >= 12) | (df['Date_water_level_Value'].dt.month <= 2)]

# Вычисление среднего расхода воды
summer_avg_consumption = summer_data['Water_consumption_Valuem³s'].mean()
winter_avg_consumption = winter_data['Water_consumption_Valuem³s'].mean()

print(f"Средний расход воды в летний период: {summer_avg_consumption} м³/с")
print(f"Средний расход воды в зимний период: {winter_avg_consumption} м³/с")

# Сохранение карты
m.save("51.html")