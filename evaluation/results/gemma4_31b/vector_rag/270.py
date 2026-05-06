import geopandas as gpd
import folium
from shapely import wkt

def calculate_ndvi_from_water_level(water_level):
    """
    Рассчитывает прокси-индекс NDVI на основе уровня воды в реке Талгар.
    Логика: NDVI коррелирует с доступностью воды. 
    Слишком низкий уровень = засуха (низкий NDVI).
    Оптимальный уровень = максимальный рост (высокий NDVI).
    Слишком высокий уровень = затопление (снижение NDVI).
    """
    # Гипотетические пороги для реки Талгар (в см)
    OPTIMAL_LEVEL = 150.0 
    CRITICAL_LOW = 20.0
    CRITICAL_HIGH = 500.0
    
    if water_level < CRITICAL_LOW or water_level > CRITICAL_HIGH:
        return 0.1  # Минимальная растительность
    
    # Расчет прокси-значения NDVI (от 0.1 до 0.9)
    # Используем упрощенную модель зависимости
    diff = abs(water_level - OPTIMAL_LEVEL)
    ndvi = 0.9 - (diff / OPTIMAL_LEVEL) * 0.5
    return max(0.1, min(0.9, ndvi))

# 1. Загрузка данных бассейна
# Используем raw string для пути к файлу
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Конвертация в стандартную систему координат WGS84
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Инициализация карты
# Вычисляем центроид полигона бассейна для центрирования карты
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Добавление бассейна на карту
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# Пример использования функции для данных из контекста
# Предположим, Water_level_Valuecm = 165.0
sample_water_level = 165.0
calculated_ndvi = calculate_ndvi_from_water_level(sample_water_level)

print(f"Для уровня воды {sample_water_level} см, расчетный прокси-NDVI: {calculated_ndvi:.2f}")

# 4. Сохранение итоговой карты
m.save("270.html")