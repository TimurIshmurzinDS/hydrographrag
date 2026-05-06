import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
from shapely.geometry import Point
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Сбор данных о реках
data = {
    'river_name': ['Шинжалы', 'Шизжина'],
    'length': [100, 120],
    'width': [10, 15],
    'speed': [2, 3]
}
df = pd.DataFrame(data)

# Создание геообъектов для каждой реки
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['length'], df['width']))

# Анализ данных о наводнениях в регионе за последние несколько лет
navodnenia_data = {
    'river_name': ['Шинжалы', 'Шизжина'],
    'year': [2020, 2019],
    'probability': [0.5, 0.7]
}
navodnenia_df = pd.DataFrame(navodnenia_data)

# Объединение данных о реках и наводнениях
merged_df = pd.merge(gdf, navodnenia_df, on='river_name')

# Разделение данных на обучающую и тестовую выборки
X = merged_df[['length', 'width', 'speed']]
y = merged_df['probability']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели случайного леса для оценки вероятности наводнений
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Оценка вероятности наводнения на каждой реке
predictions = model.predict_proba(X_test)[:, 1]

# Сравнение результатов моделей для обоих рек и определение реки с более высокой вероятностью наводнения
shinzhaly_prob = predictions[0]
shyzhyn_prob = predictions[1]
if shinzhaly_prob > shyzhyn_prob:
    print('Река Шинжалы имеет более высокую вероятность наводнения.')
else:
    print('Река Шизжина имеет более высокую вероятность наводнения.')

# Визуализация результатов на карте
m = Map(location=[40.0, 50.0], zoom_start=6)
marker1 = Marker(location=[40.0, 50.0], popup='Река Шинжалы')
marker2 = Marker(location=[41.0, 51.0], popup='Река Шизжина')
circle1 = CircleMarker(location=[40.0, 50.0], radius=10000, color='red', fill=True)
circle2 = CircleMarker(location=[41.0, 51.0], radius=15000, color='blue', fill=True)

m.add_child(marker1)
m.add_child(marker2)
m.add_child(circle1)
m.add_child(circle2)

m.save("154.html")