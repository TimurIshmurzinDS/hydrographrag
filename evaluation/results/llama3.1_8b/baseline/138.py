import pandas as pd
from folium import Map, CircleMarker
import geopandas as gpd

# Загрузим данные о текущих уровнях воды в реках Лепсы и Бутак.
data = {
    'river': ['Лепса', 'Бутак'],
    'water_level': [10.5, 12.8],
    'latitude': [55.1234, 56.5678],
    'longitude': [35.6789, 37.2345]
}
df = pd.DataFrame(data)

# Создадим географические объекты для рек Лепсы и Бутак.
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# Визуализируем данные на карте.
m = Map(location=[55.5, 36.0], zoom_start=8)
for i, row in gdf.iterrows():
    CircleMarker([row.geometry.y, row.geometry.x], radius=10).add_to(m)

# Сравним уровни воды в двух реках.
max_water_level = df['water_level'].max()
min_water_level = df['water_level'].min()

# Визуализируем результаты сравнения на карте.
m.add_child(folium.Marker([55.5, 36.0], popup=f'Максимальный уровень воды: {max_water_level} м', icon=folium.Icon(color='red')).add_to(m))
m.add_child(folium.Marker([55.5, 36.0], popup=f'Минимальный уровень воды: {min_water_level} м', icon=folium.Icon(color='green')).add_to(m))

# Сохраняем карту в файл.
m.save("138.html")