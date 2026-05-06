import geopandas as gpd
import pandas as pd
from osgeo import ogr, osr
import folium

# 1. Получение данных о расходе воды в реке Аксу и потреблении воды сельским хозяйством
water_data = pd.read_csv('аксу_расход_воды.csv')
agriculture_water_use = pd.read_csv('сельхоз_потребление_воды.csv')

# 2. Создание цифровой модели рельефа (DTM) реки Аксу
dtm = gpd.read_file('аксу_dtm.shp')

# 3. Использование методов геостатистики для интерполяции данных расхода воды и создания карты распределения расхода воды в реке
water_gdf = gpd.GeoDataFrame(water_data, geometry=gpd.points_from_xy(water_data['lon'], water_data['lat']))
water_interpolation = interpolate(water_gdf, 'расход_воды', method='IDW')

# 4. Определение площади водосборного бассейна реки Аксу с помощью инструментов анализа водосбора
catchment_area = calculate_catchment_area(dtm, river_outlet)

# 5. Расчет объема воды, забираемой на нужды сельского хозяйства
agriculture_water_volume = agriculture_water_use['потребление_воды'].sum() * catchment_area

# 6. Визуализация результатов на карте с помощью библиотеки `folium`
m = folium.Map(location=[water_gdf['lat'].mean(), water_gdf['lon'].mean()], zoom_start=8)

for idx, row in water_gdf.iterrows():
    folium.CircleMarker(
        location=(row['lat'], row['lon']),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

folium.GeoJson(
    data=catchment_area,
    style_function=lambda x: {'fillColor': 'green', 'color': 'black', 'weight': 2},
    highlight_function=lambda x: folium.GeoJsonHighlight(style_function=lambda x: {'fillColor': 'yellow'})
).add_to(m)

m.save("аксу_водосборный_бассейн.html")