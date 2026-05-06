import folium
import geopandas as gpd

# 1. Подготовка данных
tekeli_agricultural_area = ... # Загрузить данные о площади сельскохозяйственных земель для Tekeli River
temirlik_agricultural_area = ... # Загрузить данные о площади сельскохозяйственных земель для Temirlik River
water_consumption_norm = ... # Загрузить норму водопотребления на 1 га сельскохозяйственных земель
tekeli_waterflow = ... # Загрузить средний годовой сток воды для Tekeli River
temirlik_waterflow = ... # Загрузить средний годовой сток воды для Temirlik River

# 2. Расчет потребления воды
tekeli_consumption = tekeli_agricultural_area * water_consumption_norm * tekeli_waterflow
temirlik_consumption = temirlik_agricultural_area * water_consumption_norm * temirlik_waterflow
total_consumption = tekeli_consumption + temirlik_consumption

# 3. Визуализация результатов
m = folium.Map(location=[...], zoom_start=...) # Задать начальную точку и масштаб карты

tekeli_line = gpd.read_file(...) # Загрузить данные о течении реки Tekeli River в формате GeoDataFrame
folium.GeoJson(tekeli_line, style_function=lambda x: {'fillColor': 'blue'}).add_to(m)

temirlik_line = gpd.read_file(...) # Загрузить данные о течении реки Temirlik River в формате GeoDataFrame
folium.GeoJson(temirlik_line, style_function=lambda x: {'fillColor': 'red'}).add_to(m)

# 4. Сохранение результатов
m.save("107.html")