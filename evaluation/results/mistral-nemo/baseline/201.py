import pandas as pd
import geopandas as gpd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import folium

# 1. Подготовка данных
data = pd.read_csv('historical_data.csv') # Замените на путь к вашим данным
data['year'] = pd.DatetimeIndex(data['date']).year
data = data[data['year'] >= 2000] # Используем данные за последние 20 лет

# 2. Геопространственный анализ
river_gdf = gpd.read_file('rivers.shp') # Замените на путь к вашим данным о реках
basin_gdf = gpd.read_file('basin.shp') # Замените на путь к вашим данным о бассейне

# 3. Анализ данных
X = data[['temperature', 'soil_moisture', 'precipitation']]
y = data['drought_risk']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 4. Моделирование риска
predictions = model.predict(X_test)

# 5. Визуализация результатов
m = folium.Map(location=[river_gdf.geometry.y.mean(), river_gdf.geometry.x.mean()], zoom_start=10)
folium.GeoJson(river_gdf, name='rivers').add_to(m)
folium.GeoJson(basin_gdf, name='basin').add_to(m)

for i in range(len(predictions)):
    if predictions[i] == 1:
        folium.CircleMarker(location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']], color='red', radius=5).add_to(m)

m.save("201.html")