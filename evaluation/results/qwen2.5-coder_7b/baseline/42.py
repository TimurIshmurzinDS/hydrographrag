import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Загрузка данных о расположении полей сельского хозяйства и показателях качества воды в реке Лепси
fields_data = pd.read_csv('fields.csv')
water_quality_data = pd.read_csv('water_quality.csv')

# Преобразование данных в формат GeoDataFrame
geometry_fields = [Point(xy) for xy in zip(fields_data['longitude'], fields_data['latitude'])]
gdf_fields = gpd.GeoDataFrame(fields_data, geometry=geometry_fields)

geometry_water_quality = [Point(xy) for xy in zip(water_quality_data['longitude'], water_quality_data['latitude'])]
gdf_water_quality = gpd.GeoDataFrame(water_quality_data, geometry=geometry_water_quality)

# Проецирование данных на одинаковую систему координат
gdf_fields = gdf_fields.to_crs(epsg=3857)
gdf_water_quality = gdf_water_quality.to_crs(epsg=3857)

# Определение уровня влияния агрокультуры на качество воды
gdf_fields['water_quality'] = 0

for index, row in gdf_fields.iterrows():
    for _, water_row in gdf_water_quality.iterrows():
        if row.geometry.within(water_row.geometry.buffer(1000)):  # Проверка на расстояние в 1 километре
            gdf_fields.at[index, 'water_quality'] += water_row['quality_index']

# Визуализация результатов
m = folium.Map(location=[gdf_water_quality.geometry.centroid.y.mean(), gdf_water_quality.geometry.centroid.x.mean()], zoom_start=10)

folium.Choropleth(
    geo_data=gdf_fields,
    name="choropleth",
    data=gdf_fields,
    columns=["field_id", "water_quality"],
    key_on='feature.properties.field_id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Уровень влияния агрокультуры на качество воды"
).add_to(m)

folium.LayerControl().add_to(m)

# Сохранение карты
m.save("42.html")