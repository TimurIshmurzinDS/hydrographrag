import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# 1. Подготовка данных
bio_diversity_data = pd.read_csv('bio_diversity_data.csv')
water_withdrawal_data = pd.read_csv('water_withdrawal_data.csv')

# 2. Пространственный анализ
gdf_bio_diversity = gpd.GeoDataFrame(bio_diversity_data, geometry=gpd.points_from_xy(bio_diversity_data['lon'], bio_diversity_data['lat']))
gdf_water_withdrawal = gpd.GeoDataFrame(water_withdrawal_data, geometry=gpd.points_from_xy(water_withdrawal_data['lon'], water_withdrawal_data['lat']))

# 3. Анализ динамики биоразнообразия
X = np.array(gdf_water_withdrawal['intensity']).reshape(-1, 1)
y = np.array(gdf_bio_diversity['bio_diversity']).reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

# 4. Визуализация результатов
m = folium.Map(location=[gdf_bio_diversity['lat'].mean(), gdf_bio_diversity['lon'].mean()], zoom_start=10)

for idx, row in gdf_bio_diversity.iterrows():
    folium.CircleMarker(
        location=(row['lat'], row['lon']),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

for idx, row in gdf_water_withdrawal.iterrows():
    folium.CircleMarker(
        location=(row['lat'], row['lon']),
        radius=5,
        color='red',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

# 5. Интерпретация результатов (не реализовано в коде)