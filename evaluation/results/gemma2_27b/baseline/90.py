import geopandas as gpd
import folium

# Загрузить данные о реках
rivers = gpd.read_file("rivers.shp")  # Заменить "rivers.shp" на путь к файлу с данными о реках

# Загрузить данные о рисках затопления
flood_risk = gpd.read_file("flood_risk.shp") # Заменить "flood_risk.shp" на путь к файлу с данными о рисках

# Фильтр по интересующим рекам
target_rivers = rivers[rivers["name"].isin(["Karaoy River", "Baskan River", "Temirlik River"])]

# Провести пространственный анализ (пересечение)
intersection = gpd.overlay(target_rivers, flood_risk, how="intersection")

# Определить уровень риска для каждой реки
for index, row in intersection.iterrows():
    river_name = row["name"]
    flood_probability = row["flood_probability"]  # Предполагаем, что в данных о рисках есть столбец "flood_probability"
    print(f"{river_name}: риск затопления - {flood_probability}")

# Визуализация результатов на карте
m = folium.Map(location=[42.87, 74.56], zoom_start=10) # Установить центр карты

# Добавить реки на карту
folium.GeoJson(target_rivers).add_to(m)

# Добавить зоны риска затопления на карту
folium.GeoJson(flood_risk).add_to(m)

# Сохранить карту
m.save("90.html")