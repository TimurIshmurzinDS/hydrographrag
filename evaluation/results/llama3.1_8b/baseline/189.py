import pandas as pd
from folium import Map, Marker, CircleMarker
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Сбор и преобразование данных
data = pd.read_csv('turgan_river_data.csv')
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Создание географических объектов
import geopandas as gpd
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.longitude, data.latitude))

# Моделирование
X = data.drop(['zasukha'], axis=1)
y = data['zasukha']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print('Точность модели:', accuracy_score(y_test, y_pred))

# Визуализация
m = Map(location=[data.latitude.mean(), data.longitude.mean()], zoom_start=10)
for i in range(len(data)):
    if data['zasukha'][i] == 1:
        Marker([data.latitude[i], data.longitude[i]]).add_to(m)

# Вероятность возникновения засухи
prob = model.predict_proba(X_test)[:, 1]
m.add_child(CircleMarker(location=[data.latitude.mean(), data.longitude.mean()], radius=100, color='red', fill=True, fill_color='red').add_data({'probability': prob.mean()}))

# Сохранение карты
m.save('189.html')