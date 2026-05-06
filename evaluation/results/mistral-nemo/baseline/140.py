import geopandas as gpd
import pandas as pd
import folium

# 1. Подготовка данных
def load_data(file_path):
    data = pd.read_csv(file_path)
    return gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['longitude'], data['latitude']))

def prepare_data(sensors_df, rivers_gdf):
    # 2. Анализ стабильности связи
    sensors_with_rivers = gpd.sjoin(sensors_df, rivers_gdf, how='inner', op='intersects')
    stability_scores = calculate_stability_scores(sensors_with_rivers)
    return sensors_with_rivers.assign(stability_score=stability_scores)

def calculate_stability_scores(df):
    # Пример: вычисление процента времени стабильной связи
    df['stability_score'] = (df['connected_time'] / df['total_time']) * 100
    return df['stability_score']

# 3. Визуализация результатов
def visualize_data(df):
    m = folium.Map(location=[53, 72], zoom_start=8)

    for idx, row in df.iterrows():
        stability_color = 'green' if row['stability_score'] > 70 else 'yellow' if row['stability_score'] > 40 else 'red'
        folium.Marker([row['latitude'], row['longitude']], popup=f"Датчик {idx+1}: стабильность связи - {row['stability_score']:.2f}%", icon=folium.Icon(color=stability_color)).add_to(m)

    m.save("140.html")

# Загрузка данных
sensors_df = load_data('sensors.csv')
rivers_gdf = gpd.read_file('rivers.shp')

# Подготовка данных и вычисление показателей стабильности связи
prepared_data = prepare_data(sensors_df, rivers_gdf)

# Визуализация результатов
visualize_data(prepared_data)