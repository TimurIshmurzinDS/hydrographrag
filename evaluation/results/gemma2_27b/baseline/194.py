import pandas as pd
import geopandas as gpd
from folium import Map, GeoJson


# Загрузка данных о гидрологическом режиме (из CSV или базы данных)
hydro_data = pd.read_csv("hydro_data.csv")

# Загрузка данных о местах для экологического туризма (GeoJSON)
tourism_data = gpd.read_file("tourism_sites.geojson")

# Определение сценария изменения режима реки (например, увеличение расхода на 10%)
scenario = "increased_flow"

# Моделирование изменения режима реки (упрощенная версия)
if scenario == "increased_flow":
    hydro_data["flow"] *= 1.1

# Создание карты с Folium
m = Map(location=[43.25, 78.0], zoom_start=9)

# Добавление данных о гидрологическом режиме на карту (GeoJSON)
GeoJson(hydro_data).add_to(m)

# Добавление данных о местах для экологического туризма на карту
GeoJson(tourism_data).add_to(m)

# Сохранение карты
m.save("194.html")