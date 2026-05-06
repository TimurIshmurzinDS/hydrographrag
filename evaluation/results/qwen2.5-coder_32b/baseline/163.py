import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium
from branca.colormap import LinearColormap

# Шаг 1: Сбор данных
# Предположим, что у нас есть геоданные о русле рек и исторические данные о уровнях воды.
# Для примера создадим фейковые данные.

# Создание геоданных для рек
data = {
    'name': ['Sarykan River', 'Shyzhyn River'],
    'geometry': [
        Polygon([(70.2, 45.1), (70.3, 45.2), (70.4, 45.3)]),
        Polygon([(70.6, 45.4), (70.7, 45.5), (70.8, 45.6)])
    ]
}
rivers_gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Создание исторических данных о уровнях воды
water_level_data = {
    'date': pd.date_range(start='1/1/2023', periods=10),
    'Sarykan_River_level': [1.5, 1.7, 2.0, 2.5, 3.0, 2.8, 2.6, 2.4, 2.2, 2.0],
    'Shyzhyn_River_level': [1.2, 1.4, 1.7, 2.1, 2.5, 2.3, 2.1, 1.9, 1.7, 1.5]
}
water_levels_df = pd.DataFrame(water_level_data)

# Шаг 2: Обработка данных
# Предположим, что данные уже очищены и готовы к использованию.

# Шаг 3: Моделирование
# Для простоты предположим, что модель предсказывает максимальный уровень воды на основе исторических данных.
max_levels = water_levels_df[['Sarykan_River_level', 'Shyzhyn_River_level']].max()

# Шаг 4: Оценка рисков
# Предположим, что риск высок, если уровень воды превышает определенный порог (например, 2.5 для Сарыкан и 2.3 для Шыжын).
risk_thresholds = {'Sarykan River': 2.5, 'Shyzhyn River': 2.3}
rivers_gdf['risk_level'] = rivers_gdf['name'].map(lambda x: 'High' if max_levels[x] > risk_thresholds[x] else 'Low')

# Шаг 5: Визуализация
m = folium.Map(location=[45.3, 70.6], zoom_start=10)

# Добавление рек на карту с цветовой кодировкой риска
color_map = LinearColormap(['green', 'red'], vmin=0, vmax=1)
for _, row in rivers_gdf.iterrows():
    color = 'red' if row['risk_level'] == 'High' else 'green'
    folium.GeoJson(row['geometry']).add_to(m)
    folium.Marker(
        location=row['geometry'].centroid.coords[0],
        popup=f"River: {row['name']}<br>Risk Level: {row['risk_level']}",
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# Шаг 6: Сохранение результатов
m.save("163.html")