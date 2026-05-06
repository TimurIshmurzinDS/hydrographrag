import geopandas as gpd
import folium
from shapely import wkt

def crypto_trading_logic(water_level_cm):
    """
    Теоретический алгоритм торговли на основе уровня реки.
    Если уровень воды выше 500 см -> Сигнал SELL
    Если уровень воды ниже 200 см -> Сигнал BUY
    В остальных случаях -> HOLD
    """
    if water_level_cm > 500:
        return "SELL"
    elif water_level_cm < 200:
        return "BUY"
    else:
        return "HOLD"

# 1. Загрузка данных бассейна (строго raw string)
# Файл содержит только внешние границы полигона бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Конвертация в стандартную систему координат WGS84
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Инициализация карты Folium
# Используем центроид полигона бассейна для центрирования карты
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Добавление бассейна на карту
folium.GeoJson(
    basin_gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# 4. Пример работы алгоритма с данными из контекста
# Имитация данных: уровень воды в г. Аягоз
current_water_level = 450  # Значение Water_level_Valuecm
signal = crypto_trading_logic(current_water_level)

print(f"Текущий уровень реки Аягоз: {current_water_level} см")
print(f"Сгенерированный торговый сигнал: {signal}")

# 5. Сохранение итоговой карты (строго по имени файла)
m.save("236.html")