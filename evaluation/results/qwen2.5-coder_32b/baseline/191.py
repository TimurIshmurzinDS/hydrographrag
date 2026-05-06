import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла:
# - biota_data.csv с данными о биоразнообразии (год, координаты, индекс биоразнообразия)
# - water_extraction_data.csv с данными об интенсивности забора воды (год, координаты, объем забора)

biota_df = pd.read_csv('biota_data.csv')
water_extraction_df = pd.read_csv('water_extraction_data.csv')

# Шаг 2: Предобработка данных
# Преобразуем данные в формат GeoDataFrame

geometry_biota = [Point(xy) for xy in zip(biota_df['longitude'], biota_df['latitude'])]
gdf_biota = gpd.GeoDataFrame(biota_df, geometry=geometry_biota)

geometry_water_extraction = [Point(xy) for xy in zip(water_extraction_df['longitude'], water_extraction_df['latitude'])]
gdf_water_extraction = gpd.GeoDataFrame(water_extraction_df, geometry=geometry_water_extraction)

# Шаг 3: Создание временных рядов
biota_time_series = gdf_biota.groupby(['year', 'geometry']).mean().reset_index()
water_extraction_time_series = gdf_water_extraction.groupby(['year', 'geometry']).sum().reset_index()

# Шаг 4: Анализ корреляций
# Вычислим средние значения индекса биоразнообразия и объема забора воды для каждого года

biota_annual_avg = biota_time_series.groupby('year')['bio_diversity_index'].mean().reset_index()
water_extraction_annual_sum = water_extraction_time_series.groupby('year')['extraction_volume'].sum().reset_index()

# Объединим данные по годам
merged_data = pd.merge(biota_annual_avg, water_extraction_annual_sum, on='year')

# Вычислим коэффициент корреляции Пирсона
correlation_coefficient, _ = pearsonr(merged_data['bio_diversity_index'], merged_data['extraction_volume'])
print(f"Коэффициент корреляции: {correlation_coefficient}")

# Шаг 5: Моделирование изменений
# Для простоты используем линейную регрессию для моделирования зависимости индекса биоразнообразия от объема забора воды

from sklearn.linear_model import LinearRegression

X = merged_data[['extraction_volume']]
y = merged_data['bio_diversity_index']

model = LinearRegression()
model.fit(X, y)

# Предсказание
merged_data['predicted_bio_diversity'] = model.predict(X)

# Шаг 6: Визуализация результатов
# Создадим интерактивную карту с помощью folium

# Берем средние координаты для центрирования карты
center_lat = gdf_biota['geometry'].y.mean()
center_lon = gdf_biota['geometry'].x.mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# Добавим точки биоразнообразия на карту
for _, row in biota_time_series.iterrows():
    folium.CircleMarker(
        location=(row['geometry'].y, row['geometry'].x),
        radius=row['bio_diversity_index'] / 5,
        color='green',
        fill=True,
        fill_color='green'
    ).add_to(m)

# Добавим точки забора воды на карту
for _, row in water_extraction_time_series.iterrows():
    folium.CircleMarker(
        location=(row['geometry'].y, row['geometry'].x),
        radius=row['extraction_volume'] / 1000,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Сохранение карты
m.save("191.html")

# Визуализация временных рядов и модели
plt.figure(figsize=(12, 6))
plt.plot(merged_data['year'], merged_data['bio_diversity_index'], label='Индекс биоразнообразия', color='green')
plt.plot(merged_data['year'], merged_data['predicted_bio_diversity'], label='Предсказанный индекс биоразнообразия', linestyle='--', color='red')
plt.xlabel('Год')
plt.ylabel('Индекс биоразнообразия')
plt.title('Динамика изменения биоразнообразия и его предсказание')
plt.legend()
plt.grid(True)
plt.show()