import geopandas as gpd
import pandas as pd
import folium

# Шаг 1: Сбор данных о сезонных колебаниях реки Каскелен
data = {
    'date': ['2022-01-01', '2022-02-01', '2022-03-01', ...],
    'water_level': [1.5, 2.8, 1.2, ...]
}
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Шаг 2: Геокодирование данных о реке
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df.longitude, df.latitude)
)

# Шаг 3: Анализ данных о сезонных колебаниях реки
optimal_times = analyze_water_levels(gdf) # Функция анализа данных о сезонных колебаниях реки

# Шаг 4: Визуализация результатов на карте с помощью библиотеки folium
m = folium.Map(location=[51.05, 67.02], zoom_start=8)

for index, row in optimal_times.iterrows():
    popup_text = f"Оптимальное время для выпечки хлеба: {row['optimal_time']}"
    folium.Marker([row['latitude'], row['longitude']], popup=popup_text).add_to(m)

m.save("240.html")