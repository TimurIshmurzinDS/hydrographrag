import geopandas as gpd
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Подготовка данных
water_data = pd.read_csv('water_consumption.csv')
crop_yield_data = pd.read_csv('crop_yield.csv')

# Шаг 2: Преобразование данных в формат GeoDataFrame
gdf_water = gpd.GeoDataFrame(water_data, geometry=gpd.points_from_xy(water_data['longitude'], water_data['latitude']))
gdf_crop = gpd.GeoDataFrame(crop_yield_data, geometry=gpd.points_from_xy(crop_yield_data['longitude'], crop_yield_data['latitude']))

# Шаг 3: Вычисление средних значений
mean_water_consumption = gdf_water.groupby('region')['water_consumption'].mean()
mean_crop_yield = gdf_crop.groupby('region')['crop_yield'].mean()

# Шаг 4: Регрессионный анализ
X = mean_water_consumption.values.reshape(-1, 1)
y = mean_crop_yield.values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

# Шаг 5: Визуализация результатов
m = folium.Map(location=[gdf_water['latitude'].mean(), gdf_water['longitude'].mean()], zoom_start=6)

for idx, row in gdf_water.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

for idx, row in gdf_crop.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='green',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

m.save("185.html")