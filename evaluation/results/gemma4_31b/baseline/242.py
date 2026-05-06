import osmnx as ox
import geopandas as gpd
import folium
from shapely.geometry import LineString, MultiLineString

def generate_cake_template():
    # 1. Определяем область поиска (Река Тентек)
    # Мы ищем объекты с тегом 'waterway' в районе реки Тентек
    place_name = "Tentek River, Kazakhstan" 
    
    try:
        # Извлекаем все водные пути в указанной области
        # Используем tags={'waterway': True} для получения всех притоков и русел
        gdf = ox.features_from_place(place_name, tags={'waterway': True})
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # 2. Очистка данных
    # Оставляем только линейные объекты (LineString или MultiLineString)
    gdf = gdf[gdf.geometry.type.isin(['LineString', 'MultiLineString'])]
    
    # Переводим координаты в метрическую систему (UTM) для корректного расчета буфера в метрах
    # Для региона Казахстана/Центральной Азии используем подходящую проекцию
    gdf_projected = gdf.to_crs(epsg=32642) # UTM zone 42N

    # 3. Создание формы пирога (Буферизация)
    # Задаем ширину "тела" пирога (например, 500 метров в масштабе карты, 
    # что будет соответствовать ширине заготовки на противне)
    buffer_width = 500 
    cake_shape = gdf_projected.buffer(buffer_width)
    
    # Объединяем все буферы в один общий полигон (dissolve)
    cake_polygon = cake_shape.unary_union
    
    # 4. Упрощение геометрии (чтобы края не были слишком "зубчатыми")
    # tolerance задает степень упрощения
    simplified_cake = cake_polygon.simplify(tolerance=100)
    
    # Возвращаем результат в географические координаты (WGS84) для отображения на карте
    final_gdf = gpd.GeoDataFrame(geometry=[simplified_cake], crs=epsg=32642).to_crs(epsg=4326)
    
    # 5. Визуализация с помощью folium
    # Создаем карту, центрированную на объекте
    centroid = final_gdf.geometry.centroid.iloc[0]
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')
    
    # Добавляем полигон "пирога" на карту
    folium.GeoJson(
        final_gdf,
        style_function=lambda x: {
            'fillColor': '#f4a460', # Цвет выпечки (песочный)
            'color': '#8b4513',     # Цвет корочки (коричневый)
            'weight': 2,
            'fillOpacity': 0.7
        },
        tooltip="Шаблон пирога 'Река Тентек'"
    ).add_to(m)
    
    # Сохранение результата
    m.save("242.html")
    print("Modeling complete. The cake template has been saved to 242.html")

if __name__ == "__main__":
    generate_cake_template()