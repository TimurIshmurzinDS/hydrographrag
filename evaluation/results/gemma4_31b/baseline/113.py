import folium
from shapely.geometry import LineString, Polygon
import geopandas as gpd

def solve_ecological_impact():
    # 1. Координаты рек (упрощенные аппроксимации для демонстрации моделирования)
    # Река Лепсы (Lepsy) - примерный путь
    lepsy_coords = [
        (43.5, 78.2), (43.6, 78.4), (43.7, 78.6), (43.8, 78.8), (43.9, 79.0)
    ]
    # Река Сарыкан (Sarykan) - примерный путь
    sarykan_coords = [
        (43.2, 78.5), (43.3, 78.7), (43.4, 78.9), (43.5, 79.1)
    ]

    # Создание объектов LineString
    lepsy_line = LineString(lepsy_coords)
    sarykan_line = LineString(sarykan_coords)

    # Создание GeoDataFrame
    rivers_data = {
        'name': ['Lepsy River', 'Sarykan River'],
        'geometry': [lepsy_line, sarykan_line]
    }
    gdf_rivers = gpd.GeoDataFrame(rivers_data, crs="EPSG:4326")

    # Для точного расчета буферов в метрах нужно перевести координаты в проекционную систему (UTM)
    # Используем UTM зону 43N (подходит для Казахстана/Центральной Азии)
    gdf_rivers_utm = gdf_rivers.to_crs(epsg=32643)

    # 2. Моделирование буферных зон
    # Нормальный уровень (500 метров)
    normal_buffer = gdf_rivers_utm.buffer(500)
    # Сниженный уровень (100 метров)
    low_buffer = gdf_rivers_utm.buffer(100)

    # 3. Анализ утраты территорий (Разница между нормальным и низким уровнем)
    # Это и есть зона экологического риска
    risk_zones_utm = normal_buffer.difference(low_buffer)

    # Возвращаем данные в географические координаты для визуализации
    gdf_risk = gpd.GeoDataFrame(geometry=risk_zones_utm, crs="EPSG:32643").to_crs(epsg=4326)
    gdf_rivers_geo = gdf_rivers # уже в 4326

    # 4. Визуализация с помощью folium
    # Центрируем карту по одной из рек
    m = folium.Map(location=[43.5, 78.5], zoom_start=8, tiles='CartoDB positron')

    # Добавляем реки на карту
    for idx, row in gdf_rivers_geo.iterrows():
        coords = list(row['geometry'].coords)
        folium.PolyLine(coords, color='blue', weight=4, opacity=0.8, 
                       tooltip=f"River: {row['name']}").add_to(m)

    # Добавляем зоны риска на карту
    for geom in gdf_risk.geometry:
        if geom.geom_type == 'Polygon':
            coords = list(geom.exterior.coords)
            folium.Polygon(coords, color='red', fill=True, fill_color='orange', 
                           fill_opacity=0.4, weight=1, tooltip="Ecological Risk Zone").add_to(m)
        elif geom.geom_type == 'MultiPolygon':
            for poly in geom.geoms:
                coords = list(poly.exterior.coords)
                folium.Polygon(coords, color='red', fill=True, fill_color='orange', 
                               fill_opacity=0.4, weight=1, tooltip="Ecological Risk Zone").add_to(m)

    # Добавление легенды через HTML
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 90px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; opacity: 0.8; padding: 10px;">
    <b>Легенда:</b><br>
    <i style="background:blue; width:10px; height:10px; display:inline-block;"></i> Русло реки<br>
    <i style="background:orange; width:10px; height:10px; display:inline-block;"></i> Зона риска (утрата флоры/фауны)
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Сохранение карты
    m.save("113.html")
    print("Modeling complete. Map saved as 113.html")

if __name__ == "__main__":
    solve_ecological_impact()