import geopandas as gpd
from shapely.geometry import shape
import folium

# Сбор и обработка данных
ili_basin = gpd.read_file('path/to/ili_basin.shp')
sarykan_river = gpd.read_file('path/to/sarykan_river.shp')
shynzhaly_river = gpd.read_file('path/to/shynzhaly_river.shp')

# Объединение данных о бассейне и притоках
merged_data = gpd.GeoDataFrame(
    pd.concat([ili_basin, sarykan_river, shynzhaly_river]),
    geometry='geometry'
)

# Моделирование риска паводков
def calculate_flood_risk(row):
    # Примерная функция для расчета риска паводков
    # В реальности эта функция должна быть более сложной и учитывать множество факторов
    return row['intensity_of_rainfall'] * row['soil_characteristics']

merged_data['flood_risk'] = merged_data.apply(calculate_flood_risk, axis=1)

# Визуализация результатов моделирования
m = folium.Map(location=[46.5, 76.0], zoom_start=10)
folium.Choropleth(
    geo_data=merged_data,
    data=merged_data,
    columns=['flood_risk'],
    key_on='properties.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)
m.save("156.html")