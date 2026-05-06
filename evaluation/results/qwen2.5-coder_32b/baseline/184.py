import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import Point

# Шаг 1: Сбор данных
# Предположим, что у нас есть геоданные о пойменных землях и данные о климатических изменениях.
# Для примера создадим фейковые данные.

# Создание геоданных о пойменных землях (пример)
data = {
    'id': [1, 2, 3],
    'geometry': [Point(45.0, 60.0), Point(45.1, 60.1), Point(45.2, 60.2)],
    'soil_quality': [8, 7, 9],  # Качество почвы (шкала от 1 до 10)
    'water_balance': [6, 5, 7]   # Водный баланс (шкала от 1 до 10)
}
gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Предположим, что у нас есть данные о климатических изменениях
climate_data = {
    'id': [1, 2, 3],
    'temperature_change': [0.5, 0.7, 0.6],  # Изменение температуры (градусы Цельсия)
    'precipitation_change': [-10, -8, -9]   # Изменение осадков (мм в год)
}
climate_df = pd.DataFrame(climate_data)

# Шаг 2: Подготовка данных
# Объединим данные о пойменных землях и климатических изменениях по id
gdf = gdf.merge(climate_df, on='id')

# Шаг 3: Анализ экологических показателей
# Вычислим индекс экологической устойчивости (простая сумма нормированных показателей)
gdf['ecological_index'] = (gdf['soil_quality'] / 10 + 
                            gdf['water_balance'] / 10 +
                            (1 - gdf['temperature_change']) + 
                            (1 - gdf['precipitation_change'] / 100)) / 4

# Шаг 4: Моделирование изменений климата
# Предположим, что мы уже оценили изменения и они включены в данные.

# Шаг 5: Визуализация результатов
# Создадим интерактивную карту с использованием folium
m = folium.Map(location=[60.1, 45.1], zoom_start=12)

# Добавление точек на карту с цветовой градацией в зависимости от индекса экологической устойчивости
for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=10,
        color='blue' if row['ecological_index'] >= 0.7 else 'red',
        fill=True,
        fill_color='blue' if row['ecological_index'] >= 0.7 else 'red',
        popup=f"ID: {row['id']}<br>Экологический индекс: {row['ecological_index']:.2f}"
    ).add_to(m)

# Сохранение карты в файл
m.save("184.html")