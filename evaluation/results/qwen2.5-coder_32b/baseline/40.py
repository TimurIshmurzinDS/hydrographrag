import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
import folium

# Шаг 1: Сбор данных (примерные данные)
data = {
    'latitude': [42.85, 42.90, 43.00],
    'longitude': [76.90, 77.00, 77.10],
    'pollution_level': [20, 30, 40]  # Уровень загрязнения в мг/л
}

df = pd.DataFrame(data)

# Шаг 2: Подготовка данных (примерная очистка)
df.dropna(inplace=True)  # Удаление пропусков

# Функция для пространственного интерполирования IDW
def idw_interpolation(df, query_point, power=2):
    distances = distance_matrix([(query_point[0], query_point[1])], df[['latitude', 'longitude']])[0]
    weights = 1 / (distances ** power)
    weighted_values = df['pollution_level'].values * weights
    return np.sum(weighted_values) / np.sum(weights)

# Шаг 3: Создание модели и интерполирование данных на сетке
latitudes = np.linspace(df['latitude'].min(), df['latitude'].max(), num=100)
longitudes = np.linspace(df['longitude'].min(), df['longitude'].max(), num=100)
grid_points = [(lat, lon) for lat in latitudes for lon in longitudes]

interpolated_values = [idw_interpolation(df, point) for point in grid_points]
grid_df = pd.DataFrame(grid_points, columns=['latitude', 'longitude'])
grid_df['pollution_level'] = interpolated_values

# Шаг 4: Визуализация данных на карте
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=10)

# Добавление точек измерений
for _, row in df.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        popup=f"Уровень загрязнения: {row['pollution_level']} мг/л"
    ).add_to(m)

# Добавление интерполированных значений
for _, row in grid_df.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=2,
        color='blue',
        fill=True,
        fill_color='blue',
        opacity=0.5,
        popup=f"Уровень загрязнения: {row['pollution_level']:.2f} мг/л"
    ).add_to(m)

# Сохранение карты
m.save("40.html")