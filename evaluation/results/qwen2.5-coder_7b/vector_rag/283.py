import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на границе бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных временных рядов (замените на реальные данные)
data1 = {
    'resultTime': ['2023-04-01', '2023-04-02', '2023-04-03'],
    'Date_water_level_Value': [1.5, 1.6, 1.7]
}

data2 = {
    'resultTime': ['2023-04-01', '2023-04-02', '2023-04-03'],
    'Date_water_level_Value': [1.4, 1.5, 1.6]
}

# Преобразование данных в DataFrame
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Функция для сравнения двух временных рядов
def compare_time_series(df1, df2):
    # Проверка на соответствие индексов
    if not df1.index.equals(df2.index):
        raise ValueError("Индексы временных рядов не совпадают")
    
    # Вычисление разницы между значениями
    df_diff = pd.DataFrame({
        'resultTime': df1['resultTime'],
        'Difference': df1['Date_water_level_Value'] - df2['Date_water_level_Value']
    })
    
    return df_diff

# Сравнение временных рядов
comparison_result = compare_time_series(df1, df2)

# Вывод результата сравнения
print(comparison_result)

# Сохранение карты
m.save("283.html")