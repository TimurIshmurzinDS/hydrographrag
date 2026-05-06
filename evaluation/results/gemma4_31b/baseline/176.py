import geopandas as gpd
import folium
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points
import pandas as pd

def spatial_proximity_analysis():
    # 1. Создание синтетических данных (имитация русел)
    # Координаты в формате [долгота, широта] (WGS84)
    # Река Талгар (основная артерия)
    talgar_river_coords = [
        [77.4500, 43.1500], [77.4800, 43.1600], 
        [77.5200, 43.1800], [77.5600, 43.2000]
    ]
    # Ручей Терисбутак (приток/близлежащий поток)
    terisbutak_stream_coords = [
        [77.4900, 43.1200], [77.4950, 43.1400], 
        [77.5000, 43.1550]
    ]

    # Создание GeoSeries
    river_line = LineString(talgar_river_coords)
    stream_line = LineString(terisbutak_stream_coords)

    # Создание GeoDataFrame
    gdf_river = gpd.GeoDataFrame([{'name': 'River Talgar', 'geometry': river_line}], crs="EPSG:4326")
    gdf_stream = gpd.GeoDataFrame([{'name': 'Stream Terisbutak', 'geometry': stream_line}], crs="EPSG:4326")

    # 2. Перепроектирование в UTM Zone 43N (EPSG:32643) для расчета расстояний в метрах
    gdf_river_utm = gdf_river.to_crs(epsg=32643)
    gdf_stream_utm = gdf_stream.to_crs(epsg=32643)

    # 3. Расчет кратчайшего расстояния
    river_geom = gdf_river_utm.geometry.iloc[0]
    stream_geom = gdf_stream_utm.geometry.iloc[0]

    # Находим ближайшие точки между двумя линиями
    p1, p2 = nearest_points(river_geom, stream_geom)
    
    # Расстояние в метрах
    min_distance = p1.distance(p2)

    # 4. Подготовка данных для визуализации (обратно в WGS84)
    # Создаем линию кратчайшего расстояния
    proximity_line_utm = LineString([p1, p2])
    
    # Конвертируем все обратно в EPSG:4326 для folium
    gdf_prox_utm = gpd.GeoDataFrame([{'geometry': proximity_line_utm}], crs="EPSG:32643")
    gdf_prox = gdf_prox_utm.to_crs(epsg=4326)
    
    # Точки сближения
    p1_wgs = Point(p1).to_crs(epsg=4326) if hasattr(p1, 'to_crs') else None # p1 is a Point, not GDF
    # Для точек используем ручной перевод или через GDF
    p1_gdf = gpd.GeoDataFrame([{'geometry': p1}], crs="EPSG:32643").to_crs(epsg=4326)
    p2_gdf = gpd.GeoDataFrame([{'geometry': p2}], crs="EPSG:32643").to_crs(epsg=4326)
    
    p1_coords = [p1_gdf.geometry.iloc[0].y, p1_gdf.geometry.iloc[0].x]
    p2_coords = [p2_gdf.geometry.iloc[0].y, p2_gdf.geometry.iloc[0].x]

    # 5. Визуализация с помощью folium
    # Центр карты
    m = folium.Map(location=[43.15, 77.50], zoom_start=12, tiles='OpenStreetMap')

    # Рисуем реку Талгар (Синий)
    folium.PolyLine(
        locations=[(p[1], p[0]) for p in talgar_river_coords],
        color='blue', weight=5, opacity=0.8, tooltip='Река Талгар'
    ).add_to(m)

    # Рисуем ручей Терисбутак (Голубой)
    folium.PolyLine(
        locations=[(p[1], p[0]) for p in terisbutak_stream_coords],
        color='cyan', weight=3, opacity=0.8, tooltip='Ручей Терисбутак'
    ).add_to(m)

    # Рисуем линию кратчайшего расстояния (Красный пунктир)
    prox_coords = [(coords[1], coords[0]) for coords in gdf_prox.geometry.iloc[0].coords]
    folium.PolyLine(
        locations=prox_coords,
        color='red', weight=2, dash_array='5, 5', 
        tooltip=f'Кратчайшее расстояние: {min_distance:.2f} м'
    ).add_to(m)

    # Маркеры точек сближения
    folium.CircleMarker(location=p1_coords, radius=4, color='red', fill=True, popup='Точка на р. Талгар').add_to(m)
    folium.CircleMarker(location=p2_coords, radius=4, color='red', fill=True, popup='Точка на р. Терисбутак').add_to(m)

    # Сохранение карты
    m.save("176.html")
    print(f"Анализ завершен. Минимальное расстояние: {min_distance:.2f} метров. Карта сохранена в 176.html")

if __name__ == "__main__":
    spatial_proximity_analysis()