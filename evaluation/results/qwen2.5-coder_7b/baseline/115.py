import geopandas as gpd
import folium

# Загрузка данных о границах участков земли и информации о сельском хозяйстве
temirlik_river = gpd.read_file("path_to_temirlik_river.shp")
byzhy_river = gpd.read_file("path_to_byzhy_river.shp")
agriculture_data = gpd.read_file("path_to_agriculture_data.shp")

# Фильтрация участков земли, которые находятся в бассейнах рек Temirlik и Byzhy
temirlik_agriculture = agriculture_data[agriculture_data.within(temirlik_river.unary_union)]
byzhy_agriculture = agriculture_data[agriculture_data.within(byzhy_river.unary_union)]

# Оценка потребления воды на каждом участке (примерная оценка)
def calculate_water_consumption(row):
    # Примерные коэффициенты потребления воды для разных типов культур
    crop_type = row['crop_type']
    if crop_type == 'Овес':
        return 100  # примерное значение в литрах на гектар
    elif crop_type == 'Пшеница':
        return 200  # примерное значение в литрах на гектар
    else:
        return 150  # стандартное значение для других культур

temirlik_agriculture['water_consumption'] = temirlik_agriculture.apply(calculate_water_consumption, axis=1)
byzhy_agriculture['water_consumption'] = byzhy_agriculture.apply(calculate_water_consumption, axis=1)

# Суммирование потребления воды по всему бассейну
total_water_consumption_temirlik = temirlik_agriculture['water_consumption'].sum()
total_water_consumption_byzhy = byzhy_agriculture['water_consumption'].sum()

print(f"Общее потребление воды для сельского хозяйства в бассейне Temirlik: {total_water_consumption_temirlik} литров")
print(f"Общее потребление воды для сельского хозяйства в бассейне Byzhy: {total_water_consumption_byzhy} литров")

# Визуализация результатов
m = folium.Map(location=[temirlik_river.geometry.centroid.y.mean(), temirlik_river.geometry.centroid.x.mean()], zoom_start=10)

folium.GeoJson(temirlik_river, name="Temirlik River").add_to(m)
folium.GeoJson(byzhy_river, name="Byzhy River").add_to(m)

folium.Choropleth(
    geo_data=temirlik_agriculture,
    name='Water Consumption',
    data=temirlik_agriculture,
    columns=['water_consumption'],
    key_on='feature.properties.index',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Water Consumption (liters)'
).add_to(m)

folium.LayerControl().add_to(m)

m.save("115.html")