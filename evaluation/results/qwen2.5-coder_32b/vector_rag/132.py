import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование в CRS EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты Folium с центром по центроиду бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые данные о уровнях воды для рек Лепсы и Текес
water_level_data = [
    {"river": "Lepsy River", "date": "2018-05-15", "level": 123.4},
    {"river": "Lepsy River", "date": "2019-06-20", "level": 130.5},
    {"river": "Lepsy River", "date": "2020-07-25", "level": 145.6},
    {"river": "Tekes River", "date": "2018-05-15", "level": 150.3},
    {"river": "Tekes River", "date": "2019-06-20", "level": 147.8},
    {"river": "Tekes River", "date": "2020-07-25", "level": 160.2}
]

# Преобразование дат в формат datetime
import pandas as pd
water_level_df = pd.DataFrame(water_level_data)
water_level_df['date'] = pd.to_datetime(water_level_df['date'])

# Нахождение года с самым высоким уровнем воды для реки Лепсы
lepsy_max_year = water_level_df[water_level_df['river'] == 'Lepsy River'].groupby(water_level_df['date'].dt.year)['level'].max().idxmax()
lepsy_max_level = water_level_df[(water_level_df['river'] == 'Lepsy River') & (water_level_df['date'].dt.year == lepsy_max_year)]['level'].max()

# Нахождение года с самым высоким уровнем воды для реки Текес
tekes_max_year = water_level_df[water_level_df['river'] == 'Tekes River'].groupby(water_level_df['date'].dt.year)['level'].max().idxmax()
tekes_max_level = water_level_df[(water_level_df['river'] == 'Tekes River') & (water_level_df['date'].dt.year == tekas_max_year)]['level'].max()

# Вывод результатов
print(f"Год с самым высоким уровнем воды в реке Лепсы: {lepsy_max_year}, уровень: {lepsy_max_level}")
print(f"Год с самым высоким уровнем воды в реке Текес: {tekes_max_year}, уровень: {tekes_max_level}")

# Сохранение карты
m.save("132.html")