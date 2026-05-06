import geopandas as gpd
import folium
from shapely import wkt

# Предполагаемое критическое значение расхода воды для паводка (в м^3/с)
critical_consumption_value = 10.0  # Примерное значение, должно быть заменено на реальное

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Karaoy River
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о реке Karaoy River (в реальности данные должны быть загружены из источника)
data = [
    {"Date_water_level_Value": "2023-10-01", "Water_consumption_Value": 8.5, "Water_level_Valuecm": 150},
    {"Date_water_level_Value": "2023-10-02", "Water_consumption_Value": 9.0, "Water_level_Valuecm": 160},
    {"Date_water_level_Value": "2023-10-03", "Water_consumption_Value": 10.5, "Water_level_Valuecm": 170},  # Превышение критического значения
    {"Date_water_level_Value": "2023-10-04", "Water_consumption_Value": 9.8, "Water_level_Valuecm": 165},
]

# Проверка данных на превышение критического расхода воды
for entry in data:
    if entry["Water_consumption_Value"] > critical_consumption_value:
        print(f"Превышение критического значения расхода воды: {entry['Date_water_level_Value']} - Расход: {entry['Water_consumption_Value']} м^3/с")

# Сохранение карты
m.save("82.html")