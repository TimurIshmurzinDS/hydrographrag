import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium

# Сбор и очистка данных
data = {
    'name': ['Приток 1', 'Приток 2', 'Приток 3'],
    'geometry': [
        Polygon([(48.0, 76.0), (47.5, 77.0), (48.5, 78.0)]),
        Polygon([(49.0, 75.0), (50.0, 74.0), (51.0, 73.0)]),
        Polygon([(52.0, 72.0), (53.0, 71.0), (54.0, 70.0)])
    ]
}

gdf = gpd.GeoDataFrame(data, geometry='geometry')

# Геопространственное моделирование
gdf.to_crs(epsg=4326, inplace=True)

# Анализ данных и создание модели
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
gdf['cluster'] = kmeans.fit_predict(gdf.geometry)

# Визуализация результатов
m = folium.Map(location=[48.5, 76.5], zoom_start=10)

for i, row in gdf.iterrows():
    folium.Marker(
        location=row.geometry.centroid.coords[0],
        popup=row.name,
        icon=folium.Icon(color='red' if row.cluster == 0 else 'green' if row.cluster == 1 else 'blue')
    ).add_to(m)

m.save("247.html")