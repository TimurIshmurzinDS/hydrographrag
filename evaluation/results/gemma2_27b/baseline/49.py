import geopandas as gpd
import folium

# Загрузка данных о уровнях воды
data_2015 = gpd.read_file("batareyka_water_levels_2015.csv") 
data_2023 = gpd.read_file("batareyka_water_levels_2023.csv")

# Фильтрация данных по годам
data_2015 = data_2015[data_2015["year"] == 2015]
data_2023 = data_2023[data_2023["year"] == 2023]

# Расчет пиковых значений
peak_level_2015 = data_2015["water_level"].max()
peak_level_2023 = data_2023["water_level"].max()

# Создание карты
m = folium.Map(location=[55.75, 37.62], zoom_start=12) # Замените на координаты реки Batareyka

# Добавление маркеров пиковых уровней
folium.Marker([data_2015["latitude"].iloc[0], data_2015["longitude"].iloc[0]], 
              popup=f"Пиковый уровень в 2015: {peak_level_2015}").add_to(m)

folium.Marker([data_2023["latitude"].iloc[0], data_2023["longitude"].iloc[0]], 
              popup=f"Пиковый уровень в 2023: {peak_level_2023}"]).add_to(m)

# Сохранение карты
m.save("49.html")