import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import folium

# Шаг 1: Сбор данных
data = pd.read_csv('shilik_river_data.csv')

# Шаг 2: Подготовка данных
data = data.drop_duplicates()
data['water_level'].fillna(data['water_level'].mean(), inplace=True)
scaler = StandardScaler()
data[['temperature', 'precipitation']] = scaler.fit_transform(data[['temperature', 'precipitation']])

# Шаг 3: Геостатистическое моделирование
X = data.drop('water_level', axis=1)
y = data['water_level']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Шаг 4: Машинное обучение
predictions = model.predict(X_test)

# Шаг 5: Визуализация
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=8)

for i in range(len(data)):
    folium.CircleMarker(
        location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
        radius=predictions[i]*0.1,
        color='blue',
        fill=True
    ).add_to(m)

m.save("59.html")