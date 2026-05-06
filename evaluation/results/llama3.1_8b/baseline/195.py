import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium

# Шаг 1. Подготовка данных
river_path = 'path_to_river.shp' # путь к файлу с расположением реки Уржар и ее притоков
soil_types_path = 'path_to_soil_types.shp' # путь к файлу с типами почв в районе реки Уржар
irrigation_data_path = 'path_to_irrigation_data.csv' # путь к файлу с данными о поливной воде

# Шаг 2. Геопrocessing
river_gdf = gpd.read_file(river_path)
soil_types_gdf = gpd.read_file(soil_types_path)

# Рассчитываем индекс солености почвы на основе данных о поливной воде и типах почв.
irrigation_data = pd.read_csv(irrigation_data_path)
irrigation_data['solinity_index'] = irrigation_data['water_salt_content'] * soil_types_gdf['soil_salinity']

# Шаг 3. Визуализация результатов
m = folium.Map(location=[river_gdf.geometry.centroid.y.mean(), river_gdf.geometry.centroid.x.mean()], zoom_start=10)

# Добавляем слой с зонами высокого риска засоления почв.
high_risk_zones = irrigation_data.groupby('zone_id')['solinity_index'].mean().reset_index()
folium.Choropleth(
    geo_data=river_gdf,
    name='High Risk Zones',
    data=high_risk_zones,
    columns=['zone_id', 'solinity_index'],
    key_on='feature.properties.zone_id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)

# Сохраняем карту в файл.
m.save("195.html")