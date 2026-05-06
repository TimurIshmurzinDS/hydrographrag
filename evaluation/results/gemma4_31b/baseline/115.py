import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import Polygon, Point
import numpy as np

# 1. Симуляция данных (так как реальные shape-файлы рек Temirlik и Byzhy требуют внешних источников)
# Создаем искусственные границы бассейнов
def create_mock_data():
    # Бассейн реки Temirlik (примерный полигон)
    temirlik_coords = [[(45.0, 62.0), (45.2, 62.1), (45.1, 62.3), (44.9, 62.2), (45.0, 62.0)]]
    # Бассейн реки Byzhy (примерный полигон)
    byzhy_coords = [[(45.3, 62.4), (45.5, 62.5), (45.4, 62.7), (45.2, 62.6), (45.3, 62.4)]]
    
    basins = gpd.GeoDataFrame({
        'basin_name': ['Temirlik', 'Byzhy'],
        'geometry': [Polygon(temirlik_coords[0]), Polygon(byzhy_coords[0])]
    }, crs="EPSG:4326")
    
    # Симуляция сельскохозяйственных полей (точки с площадью и типом культуры)
    # Генерируем случайные точки внутри или около бассейнов
    np.random.seed(42)
    fields_data = []
    crops = {
        'Wheat': {'Kc': 1.1, 'color': 'yellow'},
        'Cotton': {'Kc': 1.2, 'color': 'green'},
        'Vegetables': {'Kc': 1.0, 'color': 'orange'}
    }
    
    for basin in basins['basin_name']:
        center_lat = 45.0 if basin == 'Temirlik' else 45.4
        center_lon = 62.1 if basin == 'Temirlik' else 62.5
        for i in range(10): # 10 полей на бассейн
            crop_type = np.random.choice(list(crops.keys()))
            fields_data.append({
                'basin': basin,
                'crop': crop_type,
                'area_ha': np.random.uniform(10, 100),
                'lat': center_lat + np.random.uniform(-0.1, 0.1),
                'lon': center_lon + np.random.uniform(-0.1, 0.1),
                'Kc': crops[crop_type]['Kc'],
                'color': crops[crop_type]['color']
            })
            
    fields_df = pd.DataFrame(fields_data)
    fields_gdf = gpd.GeoDataFrame(
        fields_df, 
        geometry=gpd.points_from_xy(fields_df.lon, fields_df.lat), 
        crs="EPSG:4326"
    )
    return basins, fields_gdf

# 2. Расчет потребления воды
def calculate_water_consumption(basins, fields):
    # Константы
    ET0 = 5.5  # Эталонное испарение (мм/день) в пиковый период
    irrigation_efficiency = 0.6 # Эффективность полива (60%)
    
    # Присоединяем данные о бассейнах к полям через пространственное пересечение
    joined = gpd.sjoin(fields, basins, predicate='within')
    
    # Расчет: Объем (м3) = (Площадь * 10000 м2/га) * (ET0 * Kc / 1000 м/мм) / эффективность
    joined['water_demand_m3_day'] = (
        (joined['area_ha'] * 10000) * (ET0 * joined['Kc'] / 1000) / irrigation_efficiency
    )
    
    return joined

# --- Основной процесс ---

# Подготовка данных
basins, fields = create_mock_data()
analysis_results = calculate_water_consumption(basins, fields)

# Агрегация по бассейнам
summary = analysis_results.groupby('basin_name')['water_demand_m3_day'].sum().reset_index()
print("Общее потребление воды по бассейнам (м3/день):")
print(summary)

# 3. Визуализация с помощью Folium
m = folium.Map(location=[45.2, 62.4], zoom_start=8, tiles='CartoDB positron')

# Отрисовка бассейнов
for _, row in basins.iterrows():
    sim_geo = Polygon(row['geometry'].exterior.coords)
    folium.Polygon(
        locations=[(p[1], p[0]) for p in row['geometry'].exterior.coords],
        color='blue',
        fill=True,
        fill_opacity=0.2,
        popup=f"Basin: {row['basin_name']}"
    ).add_to(m)

# Отрисовка полей с цветовой кодировкой по культурам
for _, row in analysis_results.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=5,
        color=row['color'],
        fill=True,
        fill_color=row['color'],
        popup=f"Crop: {row['crop']}<br>Demand: {row['water_demand_m3_day']:.2f} m3/day"
    ).add_to(m)

# Сохранение карты
m.save("115.html")
print("\nКарта успешно сохранена в файл 115.html")