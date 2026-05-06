import geopandas as gpd
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import folium

# Загрузка данных
gdf = gpd.read_file('path_to_your_shapefile.shp')  # Замените на путь к вашему shapefile
climate_data = pd.read_csv('path_to_climate_data.csv')  # Замените на путь к вашим данным о климате

# Предварительная обработка данных
gdf['Elevation'] = gdf['elevation_column_name']  # Замените на имя столбца с высотой
gdf['Soil_Type'] = gdf['soil_type_column_name']  # Замените на имя столбца с типом почвы

# Объединение данных
merged_data = pd.merge(gdf, climate_data, on='some_common_column')  # Замените на имя общего столбца

# Разделение данных на признаки и целевую переменную
X = merged_data[['Elevation', 'Soil_Type', 'Temperature', 'Precipitation', 'Humidity']]
y = merged_data['Stability']  # Замените на имя столбца с устойчивостью

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Визуализация на карте
m = folium.Map(location=[gdf['latitude'].mean(), gdf['longitude'].mean()], zoom_start=10)

for idx, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color='blue' if row['Stability'] == 'High' else 'red',
        fill=True,
        fill_color='blue' if row['Stability'] == 'High' else 'red',
        popup=f'Elevation: {row["Elevation"]}, Soil Type: {row["Soil_Type"]}'
    ).add_to(m)

m.save("184.html")