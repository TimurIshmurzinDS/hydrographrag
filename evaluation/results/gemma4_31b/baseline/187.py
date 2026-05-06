import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import folium
from folium.plugins import MarkerCluster

# 1. Генерация синтетических данных (так как реальные данные по р. Токыраун ограничены)
# Координаты примерно в регионе Центральной Азии
river_coords = [
    (44.12, 68.50), (44.15, 68.55), (44.18, 68.60), 
    (44.22, 68.62), (44.25, 68.68), (44.30, 68.75)
]
river_line = LineString(river_coords)

# Создаем список животноводческих хозяйств (названия и координаты)
farms_data = {
    'farm_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'lat': [44.13, 44.16, 44.20, 44.26, 44.28, 44.14, 44.21, 44.29],
    'lon': [68.51, 68.58, 68.61, 68.65, 68.72, 68.65, 68.68, 68.80]
}
df_farms = pd.DataFrame(farms_data)

# 2. Геопространственная обработка
# Создаем GeoDataFrame для реки
gdf_river = gpd.GeoDataFrame([{'geometry': river_line}], crs="EPSG:4326")

# Создаем GeoDataFrame для хозяйств
geometry = [Point(xy) for xy in zip(df_farms['lon'], df_farms['lat'])]
gdf_farms = gpd.GeoDataFrame(df_farms, geometry=geometry, crs="EPSG:4326")

# Для точного расчета расстояний переводим координаты в метрическую систему (UTM)
# Используем зону 43N (подходит для многих регионов ЦА)
gdf_river_utm = gdf_river.to_crs(epsg=32643)
gdf_farms_utm = gdf_farms.to_crs(epsg=32643)

# Вычисляем расстояние от каждого хозяйства до реки (в метрах)
river_geom = gdf_river_utm.geometry.iloc[0]
gdf_farms['dist_to_river'] = gdf_farms_utm.geometry.apply(lambda x: x.distance(river_geom))

# 3. Оценка влияния снижения уровня воды
def assess_risk(dist):
    # Моделируем ситуацию: при снижении уровня воды 
    # доступность падает, и критический порог смещается
    if dist < 1000:
        return 'Low Risk', 'green'
    elif dist < 3000:
        return 'Medium Risk', 'orange'
    else:
        return 'High Risk', 'red'

gdf_farms[['risk_level', 'color']] = gdf_farms['dist_to_river'].apply(
    lambda x: pd.Series(assess_risk(x))
)

# 4. Визуализация на карте
m = folium.Map(location=[44.2, 68.6], zoom_start=11, tiles='CartoDB positron')

# Отрисовка реки
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Река Токыраун").add_to(m)

# Отрисовка хозяйств
for idx, row in gdf_farms.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=7,
        color=row['color'],
        fill=True,
        fill_color=row['color'],
        fill_opacity=0.7,
        popup=f"Хозяйство {row['farm_id']}<br>Дистанция: {row['dist_to_river']:.0f}м<br>Риск: {row['risk_level']}"
    ).add_to(m)

# Добавление легенды
legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 180px; height: 110px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.8; padding: 10px;">
     <b>Уровень риска:</b><br>
     <i style="background:green; width:10px; height:10px; display:inline-block"></i> Низкий<br>
     <i style="background:orange; width:10px; height:10px; display:inline-block"></i> Средний<br>
     <i style="background:red; width:10px; height:10px; display:inline-block"></i> Высокий
     </div>
     '''
m.get_root().html.add_child(folium.Element(legend_html))

# Сохранение карты
m.save("187.html")

print("Моделирование завершено. Результаты сохранены в файл 187.html")
print(gdf_farms[['farm_id', 'dist_to_river', 'risk_level']])