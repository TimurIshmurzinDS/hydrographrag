import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровнях воды (заменить на реальные данные)
water_level_data = [
    {"river": "Aksu River", "date": "2023-10-01", "level": 540.2},
    {"river": "Byzhy River", "date": None, "level": None},  # Пример неисправного датчика
]

# Проверка данных о уровне воды и датах измерений
for data in water_level_data:
    river = data["river"]
    date = data["date"]
    level = data["level"]
    
    if date is None or level is None:
        print(f"Датчик на реке {river} неисправен. Дата: {date}, Уровень воды: {level}")
    else:
        print(f"На реке {river} уровень воды: {level} м, дата измерения: {date}")

# Сохранение карты
m.save("65.html")